from textnode import TextNode, TextType
from splitnode import split_nodes_delimiter
import unittest

class TestTextNode(unittest.TestCase):

    def test_no_delimiter_present(self):
        nodes = [TextNode("just plain text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        assert result == nodes

    def test_single_pair_in_middle(self):
        nodes = [TextNode("text before `code` text after", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        assert result == [
            TextNode("text before ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text after", TextType.TEXT),
        ]

    def test_delimiter_at_start(self):
        nodes = [TextNode("`code` trailing", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        assert result == [
            TextNode("code", TextType.CODE),
            TextNode(" trailing", TextType.TEXT),
        ]

    def test_delimiter_at_end(self):
        nodes = [TextNode("leading `code`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        assert result == [
            TextNode("leading ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

    def test_multiple_pairs(self):
        nodes = [
            TextNode("a `one` b `two` c", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        assert result == [
            TextNode("a ", TextType.TEXT),
            TextNode("one", TextType.CODE),
            TextNode(" b ", TextType.TEXT),
            TextNode("two", TextType.CODE),
            TextNode(" c", TextType.TEXT),
        ]

    def test_unmatched_delimiter_raises(self):
        nodes = [TextNode("this is `broken", TextType.TEXT)]

        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "`", TextType.CODE)


    def test_non_text_node_untouched(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("and `code` here", TextType.TEXT),
        ]

        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        assert result == [
            TextNode("already bold", TextType.BOLD),
            TextNode("and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]

    def test_code_delimiter(self):
        nodes = [TextNode("this is `code`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        assert result == [
            TextNode("this is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

    def test_italic_delimiter(self):
        nodes = [TextNode("this is _italic_", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

        assert result == [
            TextNode("this is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]

    def test_bold_delimiter(self):
        nodes = [TextNode("this is **bold**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        assert result == [
            TextNode("this is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]

if __name__ == "__main__":
    unittest.main()