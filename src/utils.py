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


def split_nodes_image(old_nodes):
    if old_nodes is None:
        raise ValueError("missing nodes to split images from")

    new_nodes = []

    for node in old_nodes:
        node_text = node.text

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        txt_after_img = ""

        for img_txt, img_url in images:
            img_str_len = len(f"![{img_txt}]({img_url})")

            lower_index = node_text.find(f"![{img_txt}]({img_url})")
            higher_index = lower_index + img_str_len

            txt_before_img = node_text[:lower_index]
            txt_after_img = node_text[higher_index:]

            if txt_before_img != "":
                new_nodes.append(TextNode(txt_before_img, TextType.TEXT))

            new_nodes.append(TextNode(img_txt, TextType.IMAGE, img_url))

            node_text = node_text.replace(
                f"{txt_before_img}![{img_txt}]({img_url})", "", 1
            )

        if txt_after_img != "":
            new_nodes.append(TextNode(txt_after_img, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    if old_nodes is None:
        raise ValueError("missing nodes to split links from")

    new_nodes = []

    for node in old_nodes:
        node_text = node.text

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        txt_after_link = ""

        for link_txt, link_url in links:
            link_str_len = len(f"[{link_txt}]({link_url})")

            lower_index = node_text.find(f"[{link_txt}]({link_url})")
            higher_index = lower_index + link_str_len

            txt_before_link = node_text[:lower_index]
            txt_after_link = node_text[higher_index:]

            if txt_before_link != "":
                new_nodes.append(TextNode(txt_before_link, TextType.TEXT))

            new_nodes.append(TextNode(link_txt, TextType.LINK, link_url))

            node_text = node_text.replace(
                f"{txt_before_link}[{link_txt}]({link_url})", "", 1
            )

        if txt_after_link != "":
            new_nodes.append(TextNode(txt_after_link, TextType.TEXT))

    return new_nodes
