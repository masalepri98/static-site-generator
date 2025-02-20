import re

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Extract all markdown images from text and return their alt text and URLs.
    
    Args:
        text: String containing markdown text
        
    Returns:
        List of tuples containing (alt_text, url) for each image
    """
    pattern = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Extract all markdown links from text and return their anchor text and URLs.
    
    Args:
        text: String containing markdown text
        
    Returns:
        List of tuples containing (anchor_text, url) for each link
    """
    # Replace image markdown with a placeholder to preserve text length
    text = re.sub(r'!\[.*?\]\(.*?\)', lambda m: ' ' * len(m.group(0)), text)
    pattern = r'\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches
