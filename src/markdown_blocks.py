from enum import Enum

from htmlnode import LeafNode, ParentNode         
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST  
    counter = 1
    for line in lines:
        start = f'{counter}. '
        if not line.startswith(start):
            return BlockType.PARAGRAPH
        counter+=1
    return BlockType.OLIST

from enum import Enum

from htmlnode import LeafNode, ParentNode         
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST  
    counter = 1
    for line in lines:
        start = f'{counter}. '
        if not line.startswith(start):
            return BlockType.PARAGRAPH
        counter+=1
    return BlockType.OLIST

def markdown_to_html_node(markdown):
    new_blocks = markdown_to_blocks(markdown)
    BLOCK_TAG_MAP = {
        BlockType.PARAGRAPH: "p",
        BlockType.ULIST: "ul",
        BlockType.QUOTE: "blockquote",
        BlockType.OLIST: "ol",
    }
    block_nodes = []
    for block in new_blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            lines = block.split("\n")
            inner_lines = lines[1:-1]
            raw_code = "\n".join(inner_lines) + "\n"

            code_text = TextNode(raw_code, TextType.CODE)
            code_node = text_node_to_html_node(code_text)
            new_node = ParentNode("pre", [code_node])

        elif block_type == BlockType.HEADING:
            level = 0
            for ch in block:
                if ch == "#":
                    level += 1
                else:
                    break
            text = block[level + 1 :]
            textnodes = text_to_textnodes(text)
            children = [text_node_to_html_node(tn) for tn in textnodes]
            new_node = ParentNode(f"h{level}", children)

        elif block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            text = " ".join(lines)
            textnodes = text_to_textnodes(text)
            children = [text_node_to_html_node(tn) for tn in textnodes]
            new_node = ParentNode("p", children)

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            stripped = []
            for line in lines:
                if line.startswith(">"):
                    stripped.append(line.lstrip(">").strip())
                else:
                    stripped.append(line)
            text = " ".join(stripped)
            textnodes = text_to_textnodes(text)
            children = [text_node_to_html_node(tn) for tn in textnodes]
            new_node = ParentNode("blockquote", children)

        elif block_type == BlockType.ULIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                if item.startswith("- "):
                    item_text = item[2:]
                else:
                    item_text = item
                textnodes = text_to_textnodes(item_text)
                children = [text_node_to_html_node(tn) for tn in textnodes]
                li_nodes.append(ParentNode("li", children))
            new_node = ParentNode("ul", li_nodes)

        elif block_type == BlockType.OLIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                if ". " in item:
                    _, item_text = item.split(". ", 1)
                else:
                    item_text = item
                textnodes = text_to_textnodes(item_text)
                children = [text_node_to_html_node(tn) for tn in textnodes]
                li_nodes.append(ParentNode("li", children))
            new_node = ParentNode("ol", li_nodes)

        else:
            textnodes = text_to_textnodes(block)
            children = [text_node_to_html_node(tn) for tn in textnodes]
            tag = BLOCK_TAG_MAP[block_type]
            new_node = ParentNode(tag, children)

        block_nodes.append(new_node)

    root = ParentNode("div", block_nodes)
    return root


