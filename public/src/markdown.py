from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from text_processing import text_to_textnodes
from block import block_to_block_type, BlockType

def text_to_children(text):
    """Convert text with inline markdown to a list of HTMLNode objects"""
    nodes = text_to_textnodes(text)
    children = []
    
    for node in nodes:
        if node.text_type == TextType.TEXT:
            if node.text:
                children.append(LeafNode(None, node.text))
        elif node.text_type == TextType.BOLD:
            children.append(ParentNode("b", [LeafNode(None, node.text)]))
        elif node.text_type == TextType.ITALIC:
            children.append(ParentNode("i", [LeafNode(None, node.text)]))
        elif node.text_type == TextType.CODE:
            # For inline code, use just code tag
            text_value = node.text.strip() if node.text else " "
            children.append(ParentNode("code", [LeafNode(None, text_value)]))
        elif node.text_type == TextType.LINK:
            children.append(ParentNode("a", [LeafNode(None, node.text)], {"href": node.url}))
        elif node.text_type == TextType.IMAGE:
            children.append(LeafNode("img", " ", {"src": node.url, "alt": node.text}))
    
    return children

def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode"""
    children = text_to_children(block)
    if not children:
        children = [LeafNode(None, block)]
    return ParentNode("p", children)

def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode"""
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level:].strip()
    children = text_to_children(text)
    if not children:
        children = [LeafNode(None, text)]
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    """Convert a code block to an HTML node"""
    # Remove the ``` markers and any language identifier
    lines = block.split('\n')
    if len(lines) == 1:  # Inline code
        code = lines[0].strip('`').strip()
        return ParentNode("pre", [ParentNode("code", [LeafNode(None, code)])])
    
    # Get language if specified
    lang = lines[0].strip().replace('```', '').strip()
    props = {"class": f"language-{lang}"} if lang else None
    
    # Remove opening and closing ``` lines
    code_lines = lines[1:-1]
    code_content = '\n'.join(code_lines)
    
    # Create the HTML structure
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, code_content)], props)])

def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode"""
    lines = block.split("\n")
    text = "\n".join(line[2:] for line in lines)  # Remove "> " from each line
    children = text_to_children(text)
    if not children:
        children = [LeafNode(None, text)]
    return ParentNode("blockquote", children)

def list_item_to_html_node(text):
    """Convert a list item text to an HTMLNode"""
    # Remove the list marker (* or - or number)
    content = text.strip()
    if content.startswith(("* ", "- ")):
        content = content[2:]
    else:
        content = content.split(". ", 1)[1]
    children = text_to_children(content)
    if not children:
        children = [LeafNode(None, content)]
    return ParentNode("li", children)

def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode"""
    items = block.split("\n")
    children = [list_item_to_html_node(item) for item in items]
    return ParentNode("ul", children)

def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode"""
    items = block.split("\n")
    children = [list_item_to_html_node(item) for item in items]
    return ParentNode("ol", children)

def markdown_to_blocks(markdown):
    """Split a markdown string into a list of block strings."""
    blocks = []
    current_block = []
    in_code_block = False
    
    for line in markdown.split("\n"):
        if line.startswith("```"):
            if in_code_block:
                # End of code block
                current_block.append(line)
                blocks.append("\n".join(current_block))
                current_block = []
                in_code_block = False
            else:
                # Start of code block
                if current_block:
                    blocks.append("\n".join(current_block))
                current_block = [line]
                in_code_block = True
        elif in_code_block:
            current_block.append(line)
        elif line == "":
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line)
    
    if current_block:
        blocks.append("\n".join(current_block))
    
    return [block for block in blocks if block.strip()]

def markdown_to_html_node(markdown):
    """Convert a markdown string to an HTML node."""
    if not markdown.strip():
        return HTMLNode(tag="div", value=None, children=[], props=None)
        
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        if block.startswith("#"):
            children.append(heading_to_html_node(block))
        elif block.startswith("```"):
            children.append(code_to_html_node(block))
        elif block.startswith(">"):
            children.append(quote_to_html_node(block))
        elif block.startswith("* "):
            children.append(unordered_list_to_html_node(block))
        elif block.startswith("1. "):
            children.append(ordered_list_to_html_node(block))
        else:
            children.append(paragraph_to_html_node(block))
    return ParentNode("div", children)

def extract_title(markdown):
    """
    Extract the title (h1) from a markdown string.
    Args:
        markdown: A string containing markdown formatted text
    Returns:
        str: The text from the first h1 header
    Raises:
        ValueError: If no h1 header is found
    """
    lines = markdown.split('\n')
    for line in lines:
        if line.strip().startswith('# '):
            return line.strip().removeprefix('# ').strip()
    raise ValueError("No h1 header found in markdown file")
