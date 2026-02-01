from markdown_blocks import *
from htmlnode import *
from inline_markdown import *



def markdown_to_html_node(markdown):
    new_blocks = markdown_to_blocks(markdown)
    BLOCK_TAG_MAP = {
            BlockType.PARAGRAPH: "p",
            BlockType.HEADING: "h1",
            BlockType.HEADING2: "h2",
            BlockType.HEADING3: "h3",
            BlockType.HEADING4: "h4",
            BlockType.HEADING5: "h5",
            BlockType.HEADING6: "h6",
            BlockType.ULIST: "ul",
            BlockType.QUOTE: "blockquote",
            BlockType.OLIST: "ol",
        }
    block_nodes=[]
    for block in new_blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.CODE:
            lines = block.split("\n")
            inner_lines = lines[1:-1]
            raw_code = "\n".join(inner_lines) + "\n"

            code_text = TextNode(raw_code, TextType.CODE)   
            code_node = text_node_to_html_node(code_text)   
            new_node = HTMLNode("pre", None, [code_node])   
        else:
            block = text_to_textnodes(block)
            children = [text_node_to_html_node(tn) for tn in block]
            tag = BLOCK_TAG_MAP[block_type]
            new_node = HTMLNode(tag, None, children)
        block_nodes.append(new_node)
    root = HTMLNode("div", None, block_nodes)
    return root

