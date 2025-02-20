from textnode import TextNode, TextType

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
