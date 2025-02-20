import unittest
from markdown import (
    text_to_children,
    paragraph_to_html_node,
    heading_to_html_node,
    code_to_html_node,
    quote_to_html_node,
    unordered_list_to_html_node,
    ordered_list_to_html_node,
    markdown_to_html_node,
    extract_title,
)

class TestMarkdownToHTML(unittest.TestCase):
    def test_text_to_children_basic(self):
        node = text_to_children("This is **bold** and *italic* text with `code`")[0]
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "This is ")

    def test_text_to_children_link_and_image(self):
        nodes = text_to_children("This is a [link](https://example.com) and an ![image](test.png)")
        print("\nNodes generated:")
        for i, node in enumerate(nodes):
            print(f"{i}: {node}")
        link_node = nodes[1]
        image_node = nodes[3]
        self.assertEqual(link_node.tag, "a")
        self.assertEqual(link_node.props["href"], "https://example.com")
        self.assertEqual(image_node.tag, "img")
        self.assertEqual(image_node.props["src"], "test.png")
        self.assertEqual(image_node.props["alt"], "image")

    def test_paragraph_to_html_node(self):
        node = paragraph_to_html_node("This is a paragraph with **bold** text.")
        self.assertEqual(node.tag, "p")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[1].tag, "strong")

    def test_heading_to_html_node(self):
        node = heading_to_html_node("## This is a heading")
        self.assertEqual(node.tag, "h2")
        self.assertEqual(node.children[0].value, "This is a heading")

    def test_code_to_html_node_inline(self):
        node = code_to_html_node("```print('Hello')```")
        self.assertEqual(node.tag, "pre")
        self.assertEqual(node.children[0].tag, "code")
        self.assertEqual(node.children[0].children[0].value, "print('Hello')")

    def test_code_to_html_node_multiline(self):
        text = """```python
def hello():
    print('Hello')
```"""
        node = code_to_html_node(text)
        self.assertEqual(node.tag, "pre")
        code_node = node.children[0]
        self.assertEqual(code_node.tag, "code")
        self.assertEqual(code_node.props["class"], "language-python")
        self.assertEqual(code_node.children[0].value, "def hello():\n    print('Hello')")

    def test_quote_to_html_node(self):
        text = """> This is a quote
> It spans multiple lines"""
        node = quote_to_html_node(text)
        self.assertEqual(node.tag, "blockquote")
        self.assertEqual(node.children[0].value, "This is a quote\nIt spans multiple lines")

    def test_unordered_list_to_html_node(self):
        text = """* Item 1
* Item 2
* Item 3"""
        node = unordered_list_to_html_node(text)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "li")
        self.assertEqual(node.children[0].children[0].value, "Item 1")

    def test_ordered_list_to_html_node(self):
        text = """1. First
2. Second
3. Third"""
        node = ordered_list_to_html_node(text)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[1].tag, "li")
        self.assertEqual(node.children[1].children[0].value, "Second")

    def test_markdown_to_html_node_empty(self):
        node = markdown_to_html_node("")
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 0)

    def test_markdown_to_html_node_complex(self):
        text = """# Main Title

This is a paragraph with **bold** and *italic* text.

## Subtitle

* List item 1
* List item 2

```python
def hello():
    print('Hello')
```

> This is a quote
> With multiple lines"""
        
        node = markdown_to_html_node(text)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 6)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(node.children[2].tag, "h2")
        self.assertEqual(node.children[3].tag, "ul")
        self.assertEqual(node.children[4].tag, "pre")
        self.assertEqual(node.children[5].tag, "blockquote")

    def test_extract_title_basic(self):
        markdown = "# Hello, World!\nThis is a test"
        self.assertEqual(extract_title(markdown), "Hello, World!")

    def test_extract_title_with_spaces(self):
        markdown = "   #    Spaced Title    \nThis is a test"
        self.assertEqual(extract_title(markdown), "Spaced Title")

    def test_extract_title_no_header(self):
        markdown = "This is a test\nNo header here"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_extract_title_multiple_headers(self):
        markdown = "# First Header\n## Second Header\n# Another First"
        self.assertEqual(extract_title(markdown), "First Header")

if __name__ == "__main__":
    unittest.main()
