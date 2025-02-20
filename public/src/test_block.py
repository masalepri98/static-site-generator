import unittest
from block import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        text = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_empty(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_heading(self):
        # Valid headings
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

        # Invalid headings
        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#Not a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# "), BlockType.HEADING)

    def test_code(self):
        # Simple code block
        text = """```
print("Hello, world!")
```"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

        # Code block with language
        text = """```python
def hello():
    print("Hello, world!")
```"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

        # Invalid code blocks
        self.assertEqual(block_to_block_type("```python"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```\nprint()"), BlockType.PARAGRAPH)

    def test_quote(self):
        # Single line quote
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

        # Multi-line quote
        text = """> This is a quote
> It spans multiple lines
> Like this"""
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

        # Invalid quotes
        self.assertEqual(block_to_block_type(">Not a quote"), BlockType.PARAGRAPH)
        text = """> This is a quote
But this line isn't
> This is a quote again"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        # Single item lists
        self.assertEqual(block_to_block_type("* Item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item"), BlockType.UNORDERED_LIST)

        # Multi-item lists with *
        text = """* Item 1
* Item 2
* Item 3"""
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

        # Multi-item lists with -
        text = """- Item 1
- Item 2
- Item 3"""
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

        # Invalid lists
        self.assertEqual(block_to_block_type("*Not a list"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-Not a list"), BlockType.PARAGRAPH)
        text = """* Item 1
- Item 2
* Item 3"""
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)  # Mixed markers are OK

    def test_ordered_list(self):
        # Single item
        self.assertEqual(block_to_block_type("1. Item"), BlockType.ORDERED_LIST)

        # Multi-item
        text = """1. Item 1
2. Item 2
3. Item 3"""
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

        # Invalid lists
        self.assertEqual(block_to_block_type("1.Not a list"), BlockType.PARAGRAPH)
        text = """1. Item 1
3. Item 2
4. Item 3"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)  # Numbers must start at 1 and increment
        text = """2. Item 1
3. Item 2
4. Item 3"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)  # Must start at 1

    def test_mixed_content(self):
        # These should all be paragraphs since they mix different block types
        text = """# Heading
This is a paragraph."""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

        text = """1. Item 1
* Item 2"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

        text = """> Quote
Not a quote"""
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
