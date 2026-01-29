from textnode import TextNode, TextType
from inline_markdown import *
from inline_markdown import *
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
        )

if __name__ == "__main__":
    unittest.main()