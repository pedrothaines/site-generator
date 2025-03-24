from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utils import text_node_to_html_node


def main():
    print("hello")
    node = TextNode("This is some text.", TextType.TEXT)
    node_html = text_node_to_html_node(node)
    print(node_html)


if __name__ == '__main__':
    main()
