import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none_vs_url_set(self):
        node1 = TextNode("hello", "link", None)
        node2 = TextNode("hello", "link", "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_same_url(self):
        node1 = TextNode("hello", "link", "https://example.com")
        node2 = TextNode("hello", "link", "https://example.com")
        self.assertEqual(node1, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()