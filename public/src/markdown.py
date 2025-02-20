from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from text_processing import text_to_textnodes, markdown_to_blocks
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
            children.append(ParentNode("strong", [LeafNode(None, node.text)]))
        elif node.text_type == TextType.ITALIC:
            children.append(ParentNode("em", [LeafNode(None, node.text)]))
        elif node.text_type == TextType.CODE:
            children.append(ParentNode("code", [LeafNode(None, node.text)]))
        elif node.text_type == TextType.LINK:
            children.append(ParentNode("a", [LeafNode(None, node.text)], {"href": node.url}))
        elif node.text_type == TextType.IMAGE:
            children.append(LeafNode("img", " ", {"src": node.url, "alt": node.text}))
            children.append(LeafNode(None, " "))  # Add space after image
    
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
    """Convert a code block to an HTMLNode"""
    if "\n" in block:
        # Multi-line code block
        lines = block.split("\n")
        if len(lines) > 2:
            # Extract language if specified
            language = lines[0].replace("```", "").strip()
            code = "\n".join(lines[1:-1])
            code_node = ParentNode("code", [LeafNode(None, code)], {})
            if language:
                code_node.props["class"] = f"language-{language}"
            return ParentNode("pre", [code_node])
    # Inline code
    code = block.replace("```", "").strip()
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, code)])])

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

def markdown_to_html_node(markdown):
    """Convert a markdown string to an HTMLNode object.
    The returned HTMLNode will be a div containing the converted HTML.

    Args:
        markdown: A string containing markdown formatted text

    Returns:
        HTMLNode: A div element containing the converted HTML
    """
    if not markdown:
        return HTMLNode(tag="div", children=[])  # Initialize empty div with empty children list
        
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
    return ParentNode("div", children)
