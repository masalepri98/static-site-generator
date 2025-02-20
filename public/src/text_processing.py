from textnode import TextNode, TextType
from markdown_parser import extract_markdown_images, extract_markdown_links
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Split text nodes based on a delimiter and convert the delimited text to a specified type.
    
    Args:
        old_nodes: List of text nodes to process
        delimiter: String that marks the start and end of special text
        text_type: Type to apply to the text between delimiters
        
    Returns:
        List of text nodes with delimited text converted to the specified type
    """
    if not delimiter:
        return old_nodes

    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Split text by delimiter
        parts = old_node.text.split(delimiter)
        
        # If no delimiter found, keep node as is
        if len(parts) == 1:
            new_nodes.append(old_node)
            continue
            
        # Process parts and add nodes
        for i, part in enumerate(parts):
            if i % 2 == 0:  # Regular text
                if part:  # Only add non-empty text
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:  # Delimited text
                new_nodes.append(TextNode(part, text_type))
                    
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split text nodes by markdown image syntax and convert to image nodes.
    
    Args:
        old_nodes: List of text nodes to process
        
    Returns:
        List of text nodes with image markdown converted to image nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Find all images in the text
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
            
        # Split text and create nodes
        current_text = old_node.text
        for alt_text, url in images:
            # Find the image markdown
            image_markdown = f"![{alt_text}]({url})"
            parts = current_text.split(image_markdown, 1)
            
            # Add text before image if it exists
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            # Add image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Update remaining text
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
            
        # Add any remaining text
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
                    
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split text nodes by markdown link syntax and convert to link nodes.
    
    Args:
        old_nodes: List of text nodes to process
        
    Returns:
        List of text nodes with link markdown converted to link nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Find all links in the text
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
            
        # Split text and create nodes
        current_text = old_node.text
        for anchor_text, url in links:
            # Find the link markdown
            link_markdown = f"[{anchor_text}]({url})"
            parts = current_text.split(link_markdown, 1)
            
            # Add text before link if it exists
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            # Add link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            # Update remaining text
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
            
        # Add any remaining text
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
                    
    return new_nodes

def text_to_textnodes(text):
    """Convert text with inline markdown elements to a list of TextNode objects.
    The function processes the following markdown elements in sequence:
    1. Bold: **text**
    2. Italic: *text*
    3. Code: `text`
    4. Images: ![alt](url)
    5. Links: [text](url)

    Args:
        text: A string containing markdown formatted text

    Returns:
        list[TextNode]: A list of TextNode objects representing the formatted text
    """
    if not text:
        return [TextNode("", TextType.TEXT)]
        
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Process both images and links in a single pass to maintain correct order
    final_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            final_nodes.append(node)
            continue
            
        current_text = node.text
        while current_text:
            # Find both images and links
            image_match = re.search(r'!\[(.*?)\]\((.*?)\)', current_text)
            link_match = re.search(r'(?<!!)\[(.*?)\]\((.*?)\)', current_text)
            
            # No more special elements
            if not image_match and not link_match:
                if current_text:
                    final_nodes.append(TextNode(current_text, TextType.TEXT))
                break
                
            # Find which comes first
            image_pos = image_match.start() if image_match else float('inf')
            link_pos = link_match.start() if link_match else float('inf')
            
            if image_pos < link_pos:
                # Process image
                if image_pos > 0:
                    final_nodes.append(TextNode(current_text[:image_pos], TextType.TEXT))
                alt_text = image_match.group(1)
                url = image_match.group(2)
                final_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                current_text = current_text[image_match.end():]
            else:
                # Process link
                if link_pos > 0:
                    final_nodes.append(TextNode(current_text[:link_pos], TextType.TEXT))
                text = link_match.group(1)
                url = link_match.group(2)
                final_nodes.append(TextNode(text, TextType.LINK, url))
                current_text = current_text[link_match.end():]
    
    return final_nodes

def markdown_to_blocks(markdown):
    """Split a markdown string into a list of block strings.
    Each block is separated by one or more empty lines.
    Leading and trailing whitespace is stripped from each block.
    Empty blocks are removed from the output.

    Args:
        markdown: A string containing markdown formatted text

    Returns:
        list[str]: A list of block strings
    """
    # Split on empty lines (one or more newlines)
    blocks = [block.strip() for block in markdown.split("\n\n")]
    # Remove empty blocks
    return [block for block in blocks if block]
