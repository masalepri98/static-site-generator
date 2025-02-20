import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        # Test node with no properties
        node = HTMLNode(tag="p", value="Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        # Test node with one property
        node = HTMLNode(
            tag="a",
            value="Click me!",
            props={"href": "https://www.boot.dev"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.boot.dev"'
        )

    def test_props_to_html_multiple_props(self):
        # Test node with multiple properties
        node = HTMLNode(
            tag="a",
            value="Click me!",
            props={
                "href": "https://www.boot.dev",
                "target": "_blank",
                "class": "link"
            }
        )
        # Convert to set because order of attributes doesn't matter
        actual_props = set(node.props_to_html().split())
        expected_props = {
            'href="https://www.boot.dev"',
            'target="_blank"',
            'class="link"'
        }
        self.assertEqual(actual_props, expected_props)

    def test_repr(self):
        # Test string representation of node
        node = HTMLNode(
            tag="p",
            value="Hello",
            props={"class": "text"},
            children=[HTMLNode(tag="span", value="world")]
        )
        expected = 'HTMLNode(tag=p, value=Hello, children=[HTMLNode(tag=span, value=world, children=None, props=None)], props={\'class\': \'text\'})'
        self.assertEqual(repr(node), expected)

class TestLeafNode(unittest.TestCase):
    def test_leaf_node_no_tag(self):
        # Test leaf node with no tag (raw text)
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_node_with_tag(self):
        # Test leaf node with tag
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_node_with_tag_and_props(self):
        # Test leaf node with tag and properties
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click me!</a>'
        )

    def test_leaf_node_empty_value(self):
        # Test that empty value raises ValueError
        with self.assertRaises(ValueError):
            LeafNode("p", "")

    def test_leaf_node_none_value(self):
        # Test that None value raises TypeError
        with self.assertRaises(TypeError):
            LeafNode("p", None)

    def test_leaf_node_with_children_error(self):
        # Test that adding children raises error
        node = LeafNode("p", "Test")
        with self.assertRaises(AttributeError):
            node.children = [LeafNode("span", "child")]

class TestParentNode(unittest.TestCase):
    def test_parent_node_with_children(self):
        # Test node with multiple children
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_parent_node_with_props(self):
        # Test node with props and children
        node = ParentNode(
            "div",
            [LeafNode("p", "Hello, world!")],
            {"class": "greeting", "id": "hello"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="greeting" id="hello"><p>Hello, world!</p></div>'
        )

    def test_nested_parent_nodes(self):
        # Test nested parent nodes
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold"),
                        LeafNode(None, " and "),
                        LeafNode("i", "italic"),
                    ]
                )
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold</b> and <i>italic</i></p></div>"
        )

    def test_parent_node_no_tag(self):
        # Test that missing tag raises ValueError
        with self.assertRaises(ValueError) as context:
            ParentNode("", [LeafNode(None, "text")])
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

    def test_parent_node_no_children(self):
        # Test that missing children raises ValueError
        with self.assertRaises(ValueError) as context:
            ParentNode("div", [])
        self.assertEqual(str(context.exception), "ParentNode must have children")

    def test_parent_node_none_children(self):
        # Test that None children raises ValueError
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None)
        self.assertEqual(str(context.exception), "ParentNode must have children")

if __name__ == "__main__":
    unittest.main()
