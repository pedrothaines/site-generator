import re
from textnode import TextType, TextNode
from htmlnode import LeafNode
from block import BlockType, block_to_block_type
from htmlnode import HTMLNode, ParentNode, LeafNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
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


def text_to_textnodes(text):
    if text is None:
        raise ValueError("missing text (string) to convert to textnodes")

    if text == "":
        return []

    node = TextNode(text, TextType.TEXT)

    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    if markdown is None:
        raise ValueError("missing markdown (string) to convert to blocks")

    blocks = markdown.split("\n\n")
    blocks = list(map(lambda b: b.strip(), blocks))
    blocks = list(filter(lambda b: b != "", blocks))

    return blocks


def markdown_to_html_node(markdown):
    """Convert a full markdown document to a single parent HTMLNode."""

    parent_node = ParentNode("div", children=[])

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                heading_level = 0
                for c in block:
                    if c == "#":
                        heading_level += 1
                    else:
                        break

                p = ParentNode(f"h{heading_level}", children=[])

                text_nodes = text_to_textnodes(block[heading_level:].strip())
                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    p.children.append(html_node)

                parent_node.children.append(p)

            case BlockType.PARAGRAPH:
                p = ParentNode("p", children=[])
                text_nodes = text_to_textnodes(block.replace("\n", " "))
                for text_node in text_nodes:
                    html_node = text_node_to_html_node(text_node)
                    p.children.append(html_node)

                parent_node.children.append(p)

            case BlockType.UNORDERED_LIST:
                p = ParentNode("ul", children=[])

                list_items = []

                for line in block.split("\n"):
                    if line.strip().startswith("- "):
                        item_text = line.strip()[2:]
                        list_items.append(item_text)

                for item in list_items:
                    parent_item = ParentNode("li", children=[])
                    text_nodes = text_to_textnodes(item)

                    for text_node in text_nodes:
                        html_node = text_node_to_html_node(text_node)
                        parent_item.children.append(html_node)

                    p.children.append(parent_item)

                parent_node.children.append(p)

            case BlockType.ORDERED_LIST:
                p = ParentNode("ol", children=[])

                list_items = []

                for idx, line in enumerate(block.split("\n")):
                    if line.strip().startswith(f"{idx + 1}. "):
                        item_text = line.strip()[len(str(idx + 1)) + 2 :]
                        list_items.append(item_text)

                for item in list_items:
                    parent_item = ParentNode("li", children=[])
                    text_nodes = text_to_textnodes(item)

                    for text_node in text_nodes:
                        html_node = text_node_to_html_node(text_node)
                        parent_item.children.append(html_node)

                    p.children.append(parent_item)

                parent_node.children.append(p)

            case BlockType.QUOTE:
                p = ParentNode("blockquote", children=[])
                # paragraph = ParentNode("p", children=[])
                # p.children.append(paragraph)

                quote_lines = []

                for line in block.split("\n"):
                    if line.strip().startswith(">"):
                        line_text = line.replace(">", "", 1).strip()
                        quote_lines.append(line_text + " ")

                quote_lines[-1] = quote_lines[-1].strip()

                for line in quote_lines:
                    text_nodes = text_to_textnodes(line)

                    for text_node in text_nodes:
                        html_node = text_node_to_html_node(text_node)
                        # paragraph.children.append(html_node)
                        p.children.append(html_node)

                parent_node.children.append(p)

            case BlockType.CODE:
                p = ParentNode("pre", children=[])
                code = LeafNode("code", block.replace("```", "").replace("\n", "", 1))
                p.children.append(code)

                parent_node.children.append(p)

    return parent_node


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            if block.startswith("# "):
                return block[2:].strip()

    raise Exception("markdown title (h1) not found")
