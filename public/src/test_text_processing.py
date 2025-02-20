import unittest
from textnode import TextNode, TextType
from text_processing import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

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

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_basic(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/image.png) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/image.png")
        self.assertEqual(new_nodes[2].text, " in it")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "![first](first.png) text ![second](second.png) more text ![third](third.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in new_nodes],
            [
                ("first", TextType.IMAGE, "first.png"),
                (" text ", TextType.TEXT, None),
                ("second", TextType.IMAGE, "second.png"),
                (" more text ", TextType.TEXT, None),
                ("third", TextType.IMAGE, "third.png"),
            ]
        )

    def test_split_nodes_image_no_images(self):
        node = TextNode("Just plain text here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Just plain text here")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_image_empty_alt(self):
        node = TextNode("An image with ![](empty.png) empty alt text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "empty.png")

    def test_split_nodes_image_with_special_chars(self):
        node = TextNode(
            "Image with ![sp(e)cial ch@rs!](http://example.com/image!@#.png) special chars",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "sp(e)cial ch@rs!")
        self.assertEqual(new_nodes[1].url, "http://example.com/image!@#.png")

    def test_split_nodes_image_multiple_nodes(self):
        nodes = [
            TextNode("Text before", TextType.TEXT),
            TextNode("![image](test.png)", TextType.TEXT),
            TextNode("Text after", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in new_nodes],
            [
                ("Text before", TextType.TEXT, None),
                ("image", TextType.IMAGE, "test.png"),
                ("Text after", TextType.TEXT, None),
                ("Bold text", TextType.BOLD, None),
            ]
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_basic(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text, " in it")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_link_multiple(self):
        node = TextNode(
            "This is text with a [first link](https://example.com) and [second link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in new_nodes],
            [
                ("This is text with a ", TextType.TEXT, None),
                ("first link", TextType.LINK, "https://example.com"),
                (" and ", TextType.TEXT, None),
                ("second link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_split_nodes_link_no_links(self):
        node = TextNode("Just plain text here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Just plain text here")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_link_empty_text(self):
        node = TextNode("A link with [](empty.com) empty text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "empty.com")

    def test_split_nodes_link_with_special_chars(self):
        node = TextNode(
            "Link with [sp(e)cial ch@rs!](http://example.com/page!@#) special chars",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "sp(e)cial ch@rs!")
        self.assertEqual(new_nodes[1].url, "http://example.com/page!@#")

    def test_split_nodes_link_multiple_nodes(self):
        nodes = [
            TextNode("Text before", TextType.TEXT),
            TextNode("[link](test.com)", TextType.TEXT),
            TextNode("Text after", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Text before")
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "test.com")
        self.assertEqual(new_nodes[2].text, "Text after")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

    def test_split_nodes_link_with_image(self):
        node = TextNode(
            "This has ![an image](image.jpg) and [a link](link.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [(n.text, n.text_type, n.url) for n in new_nodes],
            [
                ("This has ![an image](image.jpg) and ", TextType.TEXT, None),
                ("a link", TextType.LINK, "link.com"),
            ]
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_empty(self):
        nodes = text_to_textnodes("")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_textnodes_plain(self):
        nodes = text_to_textnodes("Plain text")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_textnodes_example(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            ("This is ", TextType.TEXT, None),
            ("text", TextType.BOLD, None),
            (" with an ", TextType.TEXT, None),
            ("italic", TextType.ITALIC, None),
            (" word and a ", TextType.TEXT, None),
            ("code block", TextType.CODE, None),
            (" and an ", TextType.TEXT, None),
            ("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            (" and a ", TextType.TEXT, None),
            ("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual([(n.text, n.text_type, n.url) for n in nodes], expected)

    def test_text_to_textnodes_nested(self):
        text = "**Bold *italic* text**"
        nodes = text_to_textnodes(text)
        expected = [
            ("Bold *italic* text", TextType.BOLD, None),
        ]
        self.assertEqual([(n.text, n.text_type, n.url) for n in nodes], expected)

    def test_text_to_textnodes_multiple(self):
        text = "`code` and more `code`"
        nodes = text_to_textnodes(text)
        expected = [
            ("code", TextType.CODE, None),
            (" and more ", TextType.TEXT, None),
            ("code", TextType.CODE, None),
        ]
        self.assertEqual([(n.text, n.text_type, n.url) for n in nodes], expected)

    def test_text_to_textnodes_mixed(self):
        text = "This is a ![image](test.png) with a [link](https://example.com) and *italic* text"
        nodes = text_to_textnodes(text)
        expected = [
            ("This is a ", TextType.TEXT, None),
            ("image", TextType.IMAGE, "test.png"),
            (" with a ", TextType.TEXT, None),
            ("link", TextType.LINK, "https://example.com"),
            (" and ", TextType.TEXT, None),
            ("italic", TextType.ITALIC, None),
            (" text", TextType.TEXT, None),
        ]
        self.assertEqual([(n.text, n.text_type, n.url) for n in nodes], expected)

    def test_text_to_textnodes_complex_nested(self):
        text = "**Bold text with a [link](https://example.com) and an ![image](test.png)**"
        nodes = text_to_textnodes(text)
        expected = [
            ("Bold text with a [link](https://example.com) and an ![image](test.png)", TextType.BOLD, None),
        ]
        self.assertEqual([(n.text, n.text_type, n.url) for n in nodes], expected)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_empty(self):
        text = ""
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single(self):
        text = "This is a single block"
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, ["This is a single block"])

    def test_markdown_to_blocks_multiple(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ])

    def test_markdown_to_blocks_excessive_newlines(self):
        text = """
        
        # Heading

        

        Paragraph 1


        Paragraph 2
        
        """
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, [
            "# Heading",
            "Paragraph 1",
            "Paragraph 2"
        ])

    def test_markdown_to_blocks_with_code(self):
        text = """Here's some code:

```python
def hello_world():
    print("Hello, world!")
```

And here's some more text."""
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, [
            "Here's some code:",
            "```python\ndef hello_world():\n    print(\"Hello, world!\")\n```",
            "And here's some more text."
        ])

    def test_markdown_to_blocks_with_lists(self):
        text = """# Shopping List

* Milk
* Eggs
* Bread

# Todo List

1. Write code
2. Write tests
3. Debug"""
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, [
            "# Shopping List",
            "* Milk\n* Eggs\n* Bread",
            "# Todo List",
            "1. Write code\n2. Write tests\n3. Debug"
        ])

    def test_markdown_to_blocks_with_blockquotes(self):
        text = """Here's a quote:

> This is a blockquote
> It can span multiple lines
> Like this

And here's some text after."""
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, [
            "Here's a quote:",
            "> This is a blockquote\n> It can span multiple lines\n> Like this",
            "And here's some text after."
        ])

if __name__ == "__main__":
    unittest.main()
