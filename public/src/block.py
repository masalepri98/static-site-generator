from enum import Enum, auto

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

def block_to_block_type(block):
    """Convert a block of text to its corresponding BlockType.
    The block should have its leading and trailing whitespace stripped.

    Args:
        block: A string representing a block of text

    Returns:
        BlockType: The type of the markdown block
    """
    if not block:
        return BlockType.PARAGRAPH

    # Split into lines for line-by-line checks
    lines = block.split("\n")
    first_line = lines[0]

    # Check for code block (must start and end with ```)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Check for heading (1-6 # characters followed by a space)
    if first_line.startswith("#"):
        header_parts = first_line.split(" ", 1)
        if len(header_parts) > 1 and 1 <= len(header_parts[0]) <= 6 and all(c == "#" for c in header_parts[0]):
            if len(lines) == 1:
                return BlockType.HEADING
            return BlockType.PARAGRAPH

    # Check if all lines start with > followed by a space
    if all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE

    # Check if all lines start with * or - followed by a space
    if all(line.strip().startswith(("* ", "- ")) for line in lines):
        return BlockType.UNORDERED_LIST

    # Check if all lines start with a number followed by . and a space
    try:
        expected_number = 1
        for line in lines:
            line = line.strip()
            if not line.startswith(f"{expected_number}. "):
                return BlockType.PARAGRAPH
            expected_number += 1
        return BlockType.ORDERED_LIST
    except:
        pass

    return BlockType.PARAGRAPH
