from enum import Enum

from inline_markdown import text_to_textnodes
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("#") and not line.startswith(("##","###","####","#####","######")):
            return line[1:].strip()
        
    raise Exception("No H1 header found")

def markdown_to_blocks(markdown):
    text_blocks = []

    splits = markdown.split("\n\n")

    for split in splits:
        if split != "":
            text_blocks.append(split.strip())
    
    return text_blocks

def block_to_block_type(markdown):
    lines = markdown.split("\n")

    if markdown.startswith(("#","##","###","####","#####","######")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
      
    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    if markdown.startswith("1. "):
        line_count = 1
        for line in lines:
            if not line.startswith(f"{line_count}. "):
                return BlockType.PARAGRAPH
            line_count += 1
        return BlockType.OLIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    text_blocks = markdown_to_blocks(markdown)
    children = []
    for text_block in text_blocks:
        html_node = block_to_html_node(text_block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(text_block):
    block_type = block_to_block_type(text_block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(text_block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(text_block)
    if block_type == BlockType.CODE:
        return code_to_html_node(text_block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(text_block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(text_block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(text_block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(text_block):
    lines = text_block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(text_block):
    level = 0
    for char in text_block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(text_block):
        raise ValueError(f"invalid heading level: {level}")
    text = text_block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(text_block):
    if not text_block.startswith("```") or not text_block.endswith("```"):
        raise ValueError("invalid code block")
    text = text_block[4:-3]
    raw_text_node = TextNode(text, TextType.PLAIN)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(text_block):
    items = text_block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(text_block):
    items = text_block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(text_block):
    lines = text_block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)