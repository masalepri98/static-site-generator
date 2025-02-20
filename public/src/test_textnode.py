import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq_equal_nodes(self):
        # Test that two nodes with the same properties are equal
        node1 = TextNode("Hello", TextType.TEXT, None)
        node2 = TextNode("Hello", TextType.TEXT, None)
        self.assertEqual(node1, node2)

    def test_eq_different_text(self):
        # Test that nodes with different text are not equal
        node1 = TextNode("Hello", TextType.TEXT, None)
        node2 = TextNode("World", TextType.TEXT, None)
        self.assertNotEqual(node1, node2)

    def test_eq_different_type(self):
        # Test that nodes with different types are not equal
        node1 = TextNode("Hello", TextType.TEXT, None)
        node2 = TextNode("Hello", TextType.BOLD, None)
        self.assertNotEqual(node1, node2)

    def test_eq_different_url(self):
        # Test that nodes with different URLs are not equal
        node1 = TextNode("Click me", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click me", TextType.LINK, "https://blog.boot.dev")
        self.assertNotEqual(node1, node2)

    def test_eq_none_url(self):
        # Test that nodes with None and string URLs are not equal
        node1 = TextNode("Click me", TextType.LINK, None)
        node2 = TextNode("Click me", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node1, node2)

    def test_eq_different_type_same_url(self):
        # Test that nodes with same URL but different types are not equal
        node1 = TextNode("Click me", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click me", TextType.IMAGE, "https://boot.dev")
        self.assertNotEqual(node1, node2)

    def test_eq_empty_text(self):
        # Test that nodes with empty text are handled correctly
        node1 = TextNode("", TextType.TEXT, None)
        node2 = TextNode("", TextType.TEXT, None)
        self.assertEqual(node1, node2)
        
        # Different type but same empty text should not be equal
        node3 = TextNode("", TextType.BOLD, None)
        self.assertNotEqual(node1, node3)

    def test_eq_none_vs_empty_url(self):
        # Test that None URL is not equal to empty string URL
        node1 = TextNode("Click me", TextType.LINK, None)
        node2 = TextNode("Click me", TextType.LINK, "")
        self.assertNotEqual(node1, node2)

    def test_eq_with_non_textnode(self):
        # Test equality with non-TextNode objects
        node = TextNode("Hello", TextType.TEXT, None)
        self.assertNotEqual(node, "Hello")
        self.assertNotEqual(node, None)
        self.assertNotEqual(node, {"text": "Hello", "text_type": TextType.TEXT, "url": None})

    def test_repr(self):
        # Test string representation of nodes
        node = TextNode("Hello", TextType.TEXT, None)
        expected = "TextNode(Hello, TextType.TEXT, None)"
        self.assertEqual(repr(node), expected)

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        # Test conversion of TEXT type
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "Hello, world!")

    def test_text_node_to_html_node_bold(self):
        # Test conversion of BOLD type
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_node_to_html_node_italic(self):
        # Test conversion of ITALIC type
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_node_to_html_node_code(self):
        # Test conversion of CODE type
        text_node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>print('Hello')</code>")

    def test_text_node_to_html_node_link(self):
        # Test conversion of LINK type
        text_node = TextNode("Click me", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://www.boot.dev">Click me</a>'
        )

    def test_text_node_to_html_node_link_no_url(self):
        # Test LINK type without URL raises error
        text_node = TextNode("Click me", TextType.LINK)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Link text node must have a URL")

    def test_text_node_to_html_node_image(self):
        # Test conversion of IMAGE type
        text_node = TextNode("Boot.dev logo", TextType.IMAGE, "https://boot.dev/logo.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://boot.dev/logo.png" alt="Boot.dev logo">'
        )

    def test_text_node_to_html_node_image_no_url(self):
        # Test IMAGE type without URL raises error
        text_node = TextNode("Boot.dev logo", TextType.IMAGE)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Image text node must have a URL")

if __name__ == "__main__":
    unittest.main()