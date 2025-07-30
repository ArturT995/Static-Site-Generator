import unittest

from src.htmlnode import LeafNode
from src.textnode import TextNode, TextType
from src.text_to_html import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {'src': 'https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp', "alt": "This is an image"})

#def __init__(self, tag, value, props = None): html
#def __init__(self, text, text_type, url=None): text