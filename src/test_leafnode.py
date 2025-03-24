import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_values(self):
        node = LeafNode("p", "This is a paragraph.", None)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph.")
        self.assertEqual(node.props, None)

    def test_no_value(self):
        node = LeafNode("div", None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag_raw_text(self):
        node = LeafNode(None, "This is some text.", None)
        self.assertEqual(node.to_html(), "This is some text.")

    def test_to_html_p_no_prop(self):
        node = LeafNode("p", "This is a paragraph.", None)
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_to_html_p_one_prop(self):
        properties = {
            "class": "my-p-class"
        }
        node = LeafNode("p", "This is a paragraph.", props=properties)
        self.assertEqual(node.to_html(), '<p class="my-p-class">This is a paragraph.</p>')

    def test_to_html_a_two_props(self):
        properties = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        node = LeafNode("p", "This is a paragraph.", props=properties)
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" target="_blank">This is a paragraph.</p>')

if __name__ == '__main__':
    unittest.main()
