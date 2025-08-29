from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    new_blocks = []

    blocks = markdown.split("\n\n")

    for block in blocks:
        if block != "":
            new_blocks.append(block.strip())
    
    return new_blocks

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