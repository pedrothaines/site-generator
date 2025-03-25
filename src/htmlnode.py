class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self, visited=None):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""

        props_string = ""
        for prop in self.props:
            props_string = f'{props_string} {prop}="{self.props[prop]}"'
        return props_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self, visited=None):
        if self.value is None:
            raise ValueError("missing value")

        if self.tag is None:
            return str(self.value)

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props, value=None)

    def to_html(self, visited=None):
        if visited is None:
            visited = set()

        if id(self) in visited:
            raise RecursionError("infinite recursion detected")

        visited.add(id(self))

        if not self.tag or len(self.tag) <= 0:
            raise ValueError("missing tag")

        if not self.children:
            raise ValueError("missing children")

        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise ValueError("not a valid HTMLNode")
            html += child.to_html(visited)
        html += f"</{self.tag}>"

        return html

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
