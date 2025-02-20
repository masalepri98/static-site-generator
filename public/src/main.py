from textnode import TextNode, TextType
import os
import shutil
import logging
from markdown import markdown_to_html_node, extract_title

def copy_directory(src_dir, dest_dir):
    """
    Recursively copy all contents from src_dir to dest_dir.
    First deletes all contents in dest_dir if it exists.
    
    Args:
        src_dir (str): Source directory path
        dest_dir (str): Destination directory path
    """
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        logging.info(f"Deleting existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create destination directory
    logging.info(f"Creating directory: {dest_dir}")
    os.makedirs(dest_dir)
    
    # Walk through source directory
    for root, dirs, files in os.walk(src_dir):
        # Calculate the corresponding destination directory
        rel_path = os.path.relpath(root, src_dir)
        dest_path = os.path.join(dest_dir, rel_path)
        
        # Create directories in destination
        for dir_name in dirs:
            dir_path = os.path.join(dest_path, dir_name)
            logging.info(f"Creating directory: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
        
        # Copy files
        for file_name in files:
            src_file = os.path.join(root, file_name)
            dest_file = os.path.join(dest_path, file_name)
            logging.info(f"Copying file: {src_file} -> {dest_file}")
            shutil.copy2(src_file, dest_file)

def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path (str): Path to the source markdown file
        template_path (str): Path to the template HTML file
        dest_path (str): Path where the generated HTML file should be written
    """
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown content
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read template
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write output file
    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursive(content_dir, template_path, dest_dir):
    """Generate HTML pages for all markdown files in content directory"""
    # Walk through the content directory
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                # Get the source file path
                source_file = os.path.join(root, file)
                
                # Calculate the destination path
                rel_path = os.path.relpath(root, content_dir)
                dest_path = os.path.join(dest_dir, rel_path)
                
                # Convert index.md to index.html, other.md to other/index.html
                if file == 'index.md':
                    dest_file = os.path.join(dest_path, 'index.html')
                else:
                    # Remove .md extension and create directory
                    file_base = os.path.splitext(file)[0]
                    dest_file = os.path.join(dest_path, file_base, 'index.html')
                
                # Generate the page
                generate_page(source_file, template_path, dest_file)

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Define directories and files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    content_dir = os.path.join(parent_dir, "content")
    template_path = os.path.join(parent_dir, "template.html")
    static_dir = os.path.join(parent_dir, "static")
    public_dir = os.path.join(parent_dir, "public")
    
    # Delete and recreate public directory
    if os.path.exists(public_dir):
        logging.info(f"Deleting existing directory: {public_dir}")
        shutil.rmtree(public_dir)
    
    # Copy static files
    if os.path.exists(static_dir):
        logging.info("Copying static files...")
        copy_directory(static_dir, os.path.join(public_dir, "static"))
    
    # Generate all pages recursively
    logging.info("Generating pages...")
    generate_pages_recursive(content_dir, template_path, public_dir)

    # Create a text node with a link type
    node = TextNode("Click me!", TextType.LINK, "https://www.boot.dev")
    print(node)

    # Create a text node with regular text
    text_node = TextNode("Hello, world!", TextType.TEXT)
    print(text_node)

if __name__ == "__main__":
    main()