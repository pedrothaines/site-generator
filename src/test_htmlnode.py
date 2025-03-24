import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode(tag="a", value="This is an anchor.", children=None, props=None)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "This is an anchor.")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr_no_props(self):
        node = HTMLNode(tag="p", value="This is a paragraph.", children=None, props=None)
        self.assertEqual(node.__repr__(), f"HTMLNode(p, This is a paragraph., children: {None}, {None})")

    def test_repr_with_props(self):
        properties = {
            "class":"mybtn-class",
            "data-testid": "btn1"
        }
        node = HTMLNode(tag="p", value="This is a paragraph.", children=None, props=properties)
        self.assertEqual(node.__repr__(), f"HTMLNode(p, This is a paragraph., children: {None}, {properties})")

    def test_props_to_html_no_prop(self):
        node = HTMLNode(tag="a", value="This is an anchor.", children=None, props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        node = HTMLNode(tag="a", value="This is an anchor.", children=None, props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_two_prop(self):
        properties = {
            "href":"https://www.google.com",
            "target": "_blank"
        }

        node = HTMLNode(tag="a", value="This is an anchor.", children=None, props=properties)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

if __name__ == '__main__':
    unittest.main()
