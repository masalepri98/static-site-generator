import unittest
from text_processing import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        # Test basic code block splitting
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_multiple(self):
        # Test multiple delimited sections
        node = TextNode("Hello `code` world `more code`!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(
            [(node.text, node.text_type) for node in new_nodes],
            [
                ("Hello ", TextType.TEXT),
                ("code", TextType.CODE),
                (" world ", TextType.TEXT),
                ("more code", TextType.CODE),
                ("!", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_no_delimiter(self):
        # Test text without delimiters
        node = TextNode("Plain text without delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Plain text without delimiters")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_empty_text(self):
        # Test empty text between delimiters
        node = TextNode("Text with ``empty`` delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [(node.text, node.text_type) for node in new_nodes],
            [
                ("Text with ", TextType.TEXT),
                ("", TextType.CODE),
                ("empty", TextType.TEXT),
                ("", TextType.CODE),
                (" delimiters", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_multiple_nodes(self):
        # Test list with multiple input nodes
        nodes = [
            TextNode("Normal text", TextType.TEXT),
            TextNode("Text with `code`", TextType.TEXT),
            TextNode("More `code` here", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),  # Should be unchanged
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(
            [(node.text, node.text_type) for node in new_nodes],
            [
                ("Normal text", TextType.TEXT),
                ("Text with ", TextType.TEXT),
                ("code", TextType.CODE),
                ("More ", TextType.TEXT),
                ("code", TextType.CODE),
                (" here", TextType.TEXT),
                ("Bold text", TextType.BOLD),
            ]
        )

    def test_split_nodes_delimiter_different_delimiters(self):
        # Test different types of delimiters
        test_cases = [
            ("Text with *bold* words", "*", TextType.BOLD),
            ("Text with _italic_ words", "_", TextType.ITALIC),
            ("Text with `code` words", "`", TextType.CODE),
        ]
        for text, delimiter, text_type in test_cases:
            with self.subTest(delimiter=delimiter):
                node = TextNode(text, TextType.TEXT)
                new_nodes = split_nodes_delimiter([node], delimiter, text_type)
                self.assertTrue(len(new_nodes) >= 3)
                self.assertEqual(new_nodes[1].text_type, text_type)

    def test_split_nodes_delimiter_empty_delimiter(self):
        # Test empty delimiter
        node = TextNode("Text that should not change", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Text that should not change")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

if __name__ == "__main__":
    unittest.main()
