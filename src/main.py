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
)

from block import block_to_block_type

def main():
    print("hello")

    md_block = """1. First item
3. Skipped item (should be 2)
4. Third item"""
    print(block_to_block_type(md_block))

if __name__ == "__main__":
    main()
