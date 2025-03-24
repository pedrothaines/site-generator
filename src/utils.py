import re
from textnode import TextType, TextNode
from htmlnode import LeafNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("pre", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(
                f"invalid text node type to convert ({text_node.text_type})"
            )


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if old_nodes is None:
        raise ValueError("old_nodes is None")

    if not isinstance(text_type, TextType):
        raise ValueError(f"invalid TextType (text_type: {text_type})")

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        s = node.text.split(delimiter)

        if len(s) == 1:
            new_nodes.append(TextNode(s[0], TextType.TEXT))
        elif len(s) % 2 == 0:
            raise Exception("missing closing delimiter")
        else:
            for i in range(0, len(s)):
                if s[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(s[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(s[i], text_type))

    return new_nodes


def extract_markdown_images(text):
    if text is None:
        raise ValueError("missing text to extract images from")

    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    if text is None:
        raise ValueError("missing text to extract links from")

    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
