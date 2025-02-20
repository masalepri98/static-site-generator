# Static Site Generator

A Python-based static site generator that converts markdown-like text into HTML. This project is built as part of the Boot.dev curriculum.

## Features

- Custom text node handling with support for:
  - Plain text
  - Bold text
  - Italic text
  - Code blocks
  - Links
  - Images
- HTML node generation with proper nesting
- Support for self-closing tags
- Comprehensive test coverage

## Project Structure

- `src/textnode.py`: Defines text node types and conversion logic
- `src/htmlnode.py`: Handles HTML node generation and rendering
- `src/text_processing.py`: Processes text with delimiters for special formatting
- `src/main.py`: Main entry point and example usage
- Tests for each component in corresponding test files

## Running Tests

```bash
cd src
python3 -m unittest discover -v
```

## License

MIT
