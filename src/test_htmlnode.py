import unittest

from htmlnode import HTMLNode

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


if __name__ == "__main__":
    unittest.main()