import unittest
from textnode import TextNode, TextType
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


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a BOLD text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a BOLD text node")

    def test_italic(self):
        node = TextNode("This is an ITALIC text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an ITALIC text node")

    def test_code(self):
        node = TextNode("This is an CODE text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is an CODE text node")

    def test_link(self):
        node = TextNode(
            "This is a LINK text node", TextType.LINK, "https://www.google.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a LINK text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode(
            "This is an IMAGE text node", TextType.IMAGE, "https://www.google.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.google.com", "alt": "This is an IMAGE text node"},
        )

    def test_invalid_type(self):
        node = TextNode("This is a text node", "INVALID")
        self.assertRaises(ValueError, text_node_to_html_node, node)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_empty_node_list(self):
        nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(len(nodes), 0)

    def test_none_node_list(self):
        self.assertRaises(ValueError, split_nodes_delimiter, None, "`", TextType.CODE)

    def test_invalid_texttype(self):
        node = TextNode("just text", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "*", "invalid")

    def test_missing_closing_delimiter(self):
        node = TextNode("some missing **bold closing delimiter here", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)

    def test_normal_text_only(self):
        node = TextNode("just some normal text here", TextType.TEXT)

        for text_type in TextType:
            nodes = split_nodes_delimiter([node], "*", text_type)
            self.assertEqual(len(nodes), 1)
            self.assertEqual(nodes[0].text, "just some normal text here")
            self.assertEqual(nodes[0].text_type, TextType.TEXT)
            self.assertEqual(nodes[0].url, None)

    def test_bold_only(self):
        node = TextNode("**bold text here**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "bold text here")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
        self.assertEqual(nodes[0].url, None)

    def test_bold_and_normal_text_left(self):
        node = TextNode("here is some **bold text**", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 2)

        self.assertEqual(nodes[0].text, "here is some ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[0].url, None)

        self.assertEqual(nodes[1].text, "bold text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].url, None)

    def test_bold_and_normal_text_right(self):
        node = TextNode("**bold text** here for you", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 2)

        self.assertEqual(nodes[0].text, "bold text")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
        self.assertEqual(nodes[0].url, None)

        self.assertEqual(nodes[1].text, " here for you")
        self.assertEqual(nodes[1].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].url, None)

    def test_bold_and_normal_text_left_right(self):
        node = TextNode("here is some **bold text** for you", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 3)

        self.assertEqual(nodes[0].text, "here is some ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[0].url, None)

        self.assertEqual(nodes[1].text, "bold text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].url, None)

        self.assertEqual(nodes[2].text, " for you")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[2].url, None)

    def test_bold_multiple_and_normal_text(self):
        node = TextNode(
            "here we have **bold text** and here even **more bold text**, wow",
            TextType.TEXT,
        )
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "here we have ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[0].url, None)

        self.assertEqual(nodes[1].text, "bold text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].url, None)

        self.assertEqual(nodes[2].text, " and here even ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[2].url, None)

        self.assertEqual(nodes[3].text, "more bold text")
        self.assertEqual(nodes[3].text_type, TextType.BOLD)
        self.assertEqual(nodes[3].url, None)

        self.assertEqual(nodes[4].text, ", wow")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[4].url, None)

    def test_italic_single(self):
        node = TextNode("_italic text here_", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "italic text here")
        self.assertEqual(nodes[0].text_type, TextType.ITALIC)
        self.assertEqual(nodes[0].url, None)

    def test_code_single(self):
        node = TextNode("`code text here`", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "code text here")
        self.assertEqual(nodes[0].text_type, TextType.CODE)
        self.assertEqual(nodes[0].url, None)

    def test_bold_and_italic(self):
        node = TextNode(
            "here we have **bold text** and here some _italic_ text", TextType.TEXT
        )
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "here we have ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[0].url, None)

        self.assertEqual(nodes[1].text, "bold text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].url, None)

        self.assertEqual(nodes[2].text, " and here some ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[2].url, None)

        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[3].url, None)

        self.assertEqual(nodes[4].text, " text")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[4].url, None)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_image_none_text(self):
        self.assertRaises(ValueError, extract_markdown_images, None)

    def test_extract_markdown_image_empty_text(self):
        matches = extract_markdown_images("")

        self.assertListEqual(
            [],
            matches,
        )

    def test_extract_markdown_image_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_image_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![another image](test.com/asdas.png)"
        )

        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another image", "test.com/asdas.png"),
            ],
            matches,
        )

    def test_extract_markdown_image_text_is_numbers_only(self):
        matches = extract_markdown_images(
            "This is text with an ![1](https://i.imgur.com/zjjcJKZ.png) and another ![123](test.com/asdas.png)"
        )

        self.assertListEqual(
            [
                ("1", "https://i.imgur.com/zjjcJKZ.png"),
                ("123", "test.com/asdas.png"),
            ],
            matches,
        )

    def test_extract_markdown_image_text_missing_url(self):
        matches = extract_markdown_images(
            "This is text with an ![image]() and another ![123]()"
        )

        self.assertListEqual(
            [
                ("image", ""),
                ("123", ""),
            ],
            matches,
        )

    def test_extract_markdown_image_text_should_not_extract_link(self):
        matches = extract_markdown_images(
            "This is text with an ![image](image.com/adas.jpeg) and a [link](https://www.google.com/)"
        )

        self.assertListEqual(
            [
                ("image", "image.com/adas.jpeg"),
            ],
            matches,
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_link_none_text(self):
        self.assertRaises(ValueError, extract_markdown_links, None)

    def test_extract_markdown_link_empty_text(self):
        matches = extract_markdown_links("")

        self.assertListEqual(
            [],
            matches,
        )

    def test_extract_markdown_link_text_beginning_of_text(self):
        matches = extract_markdown_links("[link](http://www.google.com/)")

        self.assertListEqual(
            [
                ("link", "http://www.google.com/"),
            ],
            matches,
        )

    def test_extract_markdown_link_single(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.example.com)"
        )

        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_link_multiple(self):
        matches = extract_markdown_links(
            "This is text with an [link](http://test.net) and another [another link](www.google.com)"
        )

        self.assertListEqual(
            [
                ("link", "http://test.net"),
                ("another link", "www.google.com"),
            ],
            matches,
        )

    def test_extract_markdown_link_text_is_numbers_only(self):
        matches = extract_markdown_links(
            "This is text with an [1](sometest.com) and another [123](anothertest.com/some/more/stuff)"
        )

        self.assertListEqual(
            [
                ("1", "sometest.com"),
                ("123", "anothertest.com/some/more/stuff"),
            ],
            matches,
        )

    def test_extract_markdown_link_text_missing_url(self):
        matches = extract_markdown_links(
            "This is text with an [some link]() and another [link missing url]()"
        )

        self.assertListEqual(
            [
                ("some link", ""),
                ("link missing url", ""),
            ],
            matches,
        )

    def test_extract_markdown_link_text_should_not_extract_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image](image.com/adas.jpeg) and a [link](https://www.google.com/)"
        )

        self.assertListEqual(
            [
                ("link", "https://www.google.com/"),
            ],
            matches,
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_node_without_image(self):
        node = TextNode("just some text", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(nodes[0], node)

    def test_no_input(self):
        self.assertRaises(ValueError, split_nodes_image, None)

    def test_empty_nodes_list(self):
        nodes = split_nodes_image([])
        self.assertEqual(nodes, [])

    def test_image_only(self):
        node = TextNode("![image only](someurl.com/image.png)", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(
            nodes[0], TextNode("image only", TextType.IMAGE, "someurl.com/image.png")
        )

    def test_multiple_images_only(self):
        node = TextNode(
            "![image 1](someurl.com/image1.png)![image 2](someurl.com/image2.png)",
            TextType.TEXT,
        )
        nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image 1", TextType.IMAGE, "someurl.com/image1.png"),
                TextNode("image 2", TextType.IMAGE, "someurl.com/image2.png"),
            ],
            nodes,
        )

    def test_multiple_images_and_text(self):
        node = TextNode(
            "Here is an ![image 1](someurl.com/image1.png) and here is another ![image 2](someurl.com/image2.png).",
            TextType.TEXT,
        )
        nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("image 1", TextType.IMAGE, "someurl.com/image1.png"),
                TextNode(" and here is another ", TextType.TEXT),
                TextNode("image 2", TextType.IMAGE, "someurl.com/image2.png"),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )

    def test_multiple_images_and_text_with_repeated_images(self):
        node = TextNode(
            "Here is an ![image 1](someurl.com/image1.png) and here is another ![image 2](someurl.com/image2.png). Here is the first ![image 1](someurl.com/image1.png).",
            TextType.TEXT,
        )
        nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("image 1", TextType.IMAGE, "someurl.com/image1.png"),
                TextNode(" and here is another ", TextType.TEXT),
                TextNode("image 2", TextType.IMAGE, "someurl.com/image2.png"),
                TextNode(". Here is the first ", TextType.TEXT),
                TextNode("image 1", TextType.IMAGE, "someurl.com/image1.png"),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_node_without_link(self):
        node = TextNode("just some text", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(nodes[0], node)

    def test_no_input(self):
        self.assertRaises(ValueError, split_nodes_link, None)

    def test_empty_nodes_list(self):
        nodes = split_nodes_link([])
        self.assertEqual(nodes, [])

    def test_link_only(self):
        node = TextNode("[some link](someurl.com/some/article)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(
            nodes[0], TextNode("some link", TextType.LINK, "someurl.com/some/article")
        )

    def test_multiple_links_only(self):
        node = TextNode(
            "[link 1](someurl.com/example1)[link 2](someurl.com/example2)",
            TextType.TEXT,
        )
        nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link 1", TextType.LINK, "someurl.com/example1"),
                TextNode("link 2", TextType.LINK, "someurl.com/example2"),
            ],
            nodes,
        )

    def test_multiple_links_and_text(self):
        node = TextNode(
            "Here is an [link1](someurl.com/somedata/1) and here is another [link2](someurl.com/about.html).",
            TextType.TEXT,
        )
        nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "someurl.com/somedata/1"),
                TextNode(" and here is another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "someurl.com/about.html"),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )

    def test_multiple_links_and_text_with_repeated_link(self):
        node = TextNode(
            "Here is an [link 1](someurl.com/test1) and here is another [link 2](someurl.com/test2/). Here is the first [link 1](someurl.com/test1).",
            TextType.TEXT,
        )
        nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("link 1", TextType.LINK, "someurl.com/test1"),
                TextNode(" and here is another ", TextType.TEXT),
                TextNode("link 2", TextType.LINK, "someurl.com/test2/"),
                TextNode(". Here is the first ", TextType.TEXT),
                TextNode("link 1", TextType.LINK, "someurl.com/test1"),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_none_input(self):
        self.assertRaises(ValueError, text_to_textnodes, None)

    def test_empty_string(self):
        nodes = text_to_textnodes("")
        self.assertListEqual([], nodes)

    def test_multi_markdown_string_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![example image](https://site.com/image.jpeg) and a [link](https://google.com)"
        nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "example image", TextType.IMAGE, "https://site.com/image.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
            ],
            nodes,
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_none_input(self):
        self.assertRaises(ValueError, markdown_to_blocks, None)

    def test_empty_string(self):
        blocks = markdown_to_blocks("")
        self.assertListEqual([], blocks)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
