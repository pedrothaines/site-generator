import unittest

from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props_and_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild", props={"class":"b-class"})
        child_node = ParentNode("span", [grandchild_node], props={"class":"span-class"})
        parent_node = ParentNode("div", [child_node], props={"class":"div-class"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="div-class"><span class="span-class"><b class="b-class">grandchild</b></span></div>',
        )

    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode("b", "grandchild2")
        grandchild_node3 = LeafNode("b", "grandchild3")
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2, grandchild_node3])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b><b>grandchild2</b><b>grandchild3</b></span></div>",
        )

    def test_to_html_with_multiple_children_and_grandchildren(self):
        grandchild_node11 = LeafNode("b", "grandchild11")
        grandchild_node12 = LeafNode("b", "grandchild12")
        grandchild_node13 = LeafNode("b", "grandchild13")
        child_node1 = ParentNode("span", [grandchild_node11, grandchild_node12, grandchild_node13])

        grandchild_node21 = LeafNode("b", "grandchild21")
        grandchild_node22 = LeafNode("b", "grandchild22")
        grandchild_node23 = LeafNode("b", "grandchild23")
        child_node2 = ParentNode("p", [grandchild_node21, grandchild_node22, grandchild_node23])

        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild11</b><b>grandchild12</b><b>grandchild13</b></span><p><b>grandchild21</b><b>grandchild22</b><b>grandchild23</b></p></div>",
        )

    def test_to_html_with_empty_tag(self):
        child = LeafNode("p", "text", None)
        node = ParentNode("", [child])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_without_tag(self):
        child = LeafNode("p", "text", None)
        node = ParentNode(None, [child])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_empty_children_list(self):
        node = ParentNode("div", [])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_without_children_list(self):
        node = ParentNode("div", None)
        self.assertRaises(ValueError, node.to_html)

    def test_self_reference_child_inf_recursion(self):
        child = LeafNode("b", "child")
        pnode_self = ParentNode("div", [child])
        pnode_self.children.append(pnode_self)
        self.assertRaises(RecursionError, pnode_self.to_html)

    def test_repr(self):
        grandchild_node = LeafNode("b", "grandchild", props={"class":"b-class"})
        child_node = ParentNode("span", [grandchild_node], props={"class":"span-class"})
        parent_node = ParentNode("div", [child_node], props={"class":"div-class"})
        self.assertEqual(
            parent_node.__repr__(),
            "ParentNode(div, children: [ParentNode(span, children: [LeafNode(b, grandchild, {'class': 'b-class'})], {'class': 'span-class'})], {'class': 'div-class'})",
        )

if __name__ == '__main__':
    unittest.main()
