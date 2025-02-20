class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return "".join(f" {key}=\"{value}\"" for key, value in self.props.items())

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")

    def __repr__(self) -> str:
        return (
            f"HTMLNode(tag={self.tag}, value={self.value}, "
            f"children={self.children}, props={self.props})"
        )


class LeafNode(HTMLNode):
    # Special tags that should be self-closing
    SELF_CLOSING_TAGS = {"img", "br", "hr", "input", "meta", "link"}

    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        if not isinstance(value, str):
            raise TypeError("LeafNode value must be a string")
        if not value and tag not in self.SELF_CLOSING_TAGS:
            raise ValueError("LeafNode value must not be empty")
            
        # Initialize the parent without using setattr
        self.tag = tag
        self.value = value
        self.props = props
        # Set children directly on the instance dictionary
        self.__dict__['children'] = None
        
    def __setattr__(self, name: str, value: any) -> None:
        if name == 'children' and value is not None:
            raise AttributeError("LeafNode cannot have children")
        super().__setattr__(name, value)

    def to_html(self) -> str:
        if self.tag is None:
            return self.value
            
        if self.tag in self.SELF_CLOSING_TAGS:
            return f"<{self.tag}{self.props_to_html()}>"
            
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ):
        if not tag:
            raise ValueError("ParentNode must have a tag")
        if not children:
            raise ValueError("ParentNode must have children")
            
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
