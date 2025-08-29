from textnode import TextNode, TextType
import re

def text_to_textnodes(text):
    pass

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.PLAIN))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)            

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        image_links = extract_markdown_images(original_text)
        if len(image_links) == 0:
            new_nodes.append(old_node)
            continue

        for (image_alt, image_link) in image_links:
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_node = TextNode(sections[0], TextType.PLAIN)
                new_nodes.append(new_node)
                new_node = TextNode(image_alt, TextType.IMAGE, image_link)
                new_nodes.append(new_node)
            if sections[0] == "" and sections[1] == "":
                new_node = TextNode(image_alt, TextType.IMAGE, image_link)
                new_nodes.append(new_node)

            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if len (links) == 0:
            new_nodes.append(old_node)
            continue

        for (link_text, link_url) in links:
            sections = original_text.split(f"[{link_text}]({link_url})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_node = TextNode(sections[0], TextType.PLAIN)
                new_nodes.append(new_node)
                new_node = TextNode(link_text, TextType.LINK, link_url)
                new_nodes.append(new_node)
            if sections[0] == "" and sections[1] == "":
                new_node = TextNode(link_text, TextType.LINK, link_url)
                new_nodes.append(new_node)

            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN))

    return new_nodes

def extract_markdown_images(text):
    output_list = []

    output_list = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return output_list

def extract_markdown_links(text):
    output_list = []

    output_list = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return output_list   