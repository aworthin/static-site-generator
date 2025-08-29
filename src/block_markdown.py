
def markdown_to_blocks(markdown):
    new_blocks = []

    blocks = markdown.split("\n\n")

    for block in blocks:
        if block != "":
            new_blocks.append(block.strip())
    
    return new_blocks