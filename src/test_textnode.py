import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_equal_nodes(self):
        node1 = TextNode("hello", "text")
        node2 = TextNode("hello", "text")
        self.assertEqual(node1, node2)

    def test_different_text(self):
        node1 = TextNode("hello", "text")
        node2 = TextNode("world", "text")
        self.assertNotEqual(node1, node2)

    def test_different_text_type(self):
        node1 = TextNode("hello", "text")
        node2 = TextNode("hello", "bold")
        self.assertNotEqual(node1, node2)

    def test_url_none_vs_url_set(self):
        node1 = TextNode("hello", "link", None)
        node2 = TextNode("hello", "link", "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_same_url(self):
        node1 = TextNode("hello", "link", "https://example.com")
        node2 = TextNode("hello", "link", "https://example.com")
        self.assertEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()