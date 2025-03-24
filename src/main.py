from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utils import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link
)


def main():
    print("hello")
    node = TextNode("Here is a [link](url.com/some/article).", TextType.TEXT)
    nodes = split_nodes_link([node])

    for n in nodes:
        print(n)

if __name__ == "__main__":
    main()
