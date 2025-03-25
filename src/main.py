from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utils import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    markdown_to_html_node,
)

from block import block_to_block_type


def main():
    md = """
# Here is the title.

Now a paragraph with **some bold text**.

Items:

- item 1
- item 2 with _italic text_
- item 3

And also some tasks:
1. first task
2. second task

Such a journey...
"""
    html = markdown_to_html_node(md)
    print(html.to_html())


if __name__ == "__main__":
    main()
