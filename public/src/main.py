from textnode import TextNode, TextType

def main():
    # Create a text node with a link type
    node = TextNode("Click me!", TextType.LINK, "https://www.boot.dev")
    print(node)

    # Create a text node with regular text
    text_node = TextNode("Hello, world!", TextType.TEXT)
    print(text_node)

if __name__ == "__main__":
    main()