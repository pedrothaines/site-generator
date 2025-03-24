import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq_when_url_is_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_neq_diff_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_diff_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node diff", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_neq_diff_url(self):
        node = TextNode("This is a text node", TextType.LINK, "http://www.google.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

if __name__ == '__main__':
    unittest.main()
