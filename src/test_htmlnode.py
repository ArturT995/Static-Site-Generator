import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

testnode = HTMLNode(
    tag="a",
    value="Click me",
    children= None,
    props={"href": "https://www.google.com", "target": "_blank"}
)

class TestTextNode(unittest.TestCase):
    def test_values(self):
        self.assertEqual(
            testnode.tag,
            "a",
        )
        self.assertEqual(
            testnode.value,
            "Click me",
        )
        self.assertEqual(
            testnode.children,
            None,
        )
        self.assertEqual(
            testnode.props,
            {"href": "https://www.google.com", "target": "_blank"},
        )
    def test_repr(self):
        self.assertEqual(
            testnode.__repr__(),
            "HTMLNode(Tag: a, Value: Click me, Children: None, Props: {'href': 'https://www.google.com', 'target': '_blank'}",
        )
           
    def test_props_to_html(self):
        output = testnode.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(output, expected)

    # Leaf Node Tests

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_No_Tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
    def test_leaf_to_html_No_Value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    def test_leaf_to_html_props(self):
        node = LeafNode("p", "Hello, world!", {"id": "hello", "class": "hello"})
        self.assertEqual(node.to_html(), '<p id="hello" class="hello">Hello, world!</p>')
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    # Parent Node Tests

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_nested_parents(self):
        child_node = LeafNode("span", "child")
        parent1 = ParentNode("div", [child_node])
        parent2 = ParentNode("div", [parent1])
        self.assertEqual(
            parent2.to_html(),
            "<div><div><span>child</span></div></div>",
        )
    
    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("b", "child1")
        child2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>child1</b><span>child2</span></div>",
        )

    def test_insane(self):
            child1 = LeafNode("b", "child1")
            child2 = LeafNode("span", "child2")
            child3 = LeafNode("span", "child3")
            parent1 = ParentNode("div", [child3])
            parent2 = ParentNode("div", [child1, child2])
            parent3 = LeafNode("div", "parent3")
            grandparent = ParentNode("a",[parent1, parent2, parent3], {"href": "https://www.google.com", "target": "_blank"})
            self.assertEqual(
                grandparent.to_html(),
                '<a href="https://www.google.com" target="_blank"><div><span>child3</span></div><div><b>child1</b><span>child2</span></div><div>parent3</div></a>',
            )
if __name__ == "__main__":
    unittest.main()