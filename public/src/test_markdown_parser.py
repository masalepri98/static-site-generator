import unittest
from markdown_parser import extract_markdown_images, extract_markdown_links

class TestMarkdownParser(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_images_with_empty_alt(self):
        text = "This is text with an empty alt ![](https://example.com/image.jpg)"
        expected = [("", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_with_special_chars(self):
        text = "Image with special chars ![my (awesome) image!](https://example.com/image!@#.jpg)"
        expected = [("my (awesome) image!", "https://example.com/image!@#.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_markdown_links_with_empty_text(self):
        text = "This is text with an empty link [](https://example.com)"
        expected = [("", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_with_special_chars(self):
        text = "Link with special chars [(awesome) link!](https://example.com/page!@#)"
        expected = [("(awesome) link!", "https://example.com/page!@#")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_mixed_links_and_images(self):
        text = "This has ![an image](image.jpg) and [a link](link.com)"
        self.assertEqual(extract_markdown_images(text), [("an image", "image.jpg")])
        self.assertEqual(extract_markdown_links(text), [("a link", "link.com")])

if __name__ == "__main__":
    unittest.main()
