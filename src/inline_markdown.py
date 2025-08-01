import re
from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode
from src.text_to_html import text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        image_tuples_list = extract_markdown_images(text)
        split_nodes = []
        sections = []
        img_sections = []
        current_text = node.text
        for i in range(len(image_tuples_list)):
            img = "![" + image_tuples_list[i][0] + "]" + "(" + image_tuples_list[i][1]+ ")"
            alt = image_tuples_list[i][0]
            link = image_tuples_list[i][1]
            img_split = current_text.split(img, 1)
            sections.append(img_split[0])
            sections.append(img)
            current_text = img_split[1]
            img_sections.append(alt)
            img_sections.append(link)
            if i == len(image_tuples_list)-1 and len(img_split[1]) > 0:
                sections.append(img_split[1])
        #print("sections test here:", sections)
        #print("img_sections test here:", img_sections)
        link_index = 1
        alt_index = 0
        if len(img_sections) % 2 != 0:
            raise ValueError("invalid markdown, link section not closed")
        link_index = 1
        alt_index = 0
        bigger_list = max(len(img_sections), len(sections))
        for i in range(bigger_list):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            if i % 2 != 0:
                split_nodes.append(TextNode(img_sections[alt_index], TextType.IMAGE, img_sections[link_index]))
                link_index += 2   #1 3 5   
                alt_index += 2
        #print("split nodes test here:",split_nodes)
        new_nodes.extend(split_nodes)
        #for node in new_nodes:
        #    print(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        image_tuples_list = extract_markdown_links(text)
        split_nodes = []
        sections = []
        img_sections = []
        current_text = node.text
        #print("image_tuples_list test here:",image_tuples_list)
        for i in range(len(image_tuples_list)):
            img = "[" + image_tuples_list[i][0] + "]" + "(" + image_tuples_list[i][1]+ ")"
            alt = image_tuples_list[i][0]
            link = image_tuples_list[i][1]
            img_split = current_text.split(img, 1)
            sections.append(img_split[0])
            sections.append(img)
            current_text = img_split[1]
            img_sections.append(alt)
            img_sections.append(link)
            if i == len(image_tuples_list)-1 and len(img_split[1]) > 0:
                sections.append(img_split[1])
        
        #print("sections test here:", sections)
        #print("img_sections test here:", img_sections)
        link_index = 1
        alt_index = 0
        if len(img_sections) % 2 != 0:
            raise ValueError("invalid markdown, link section not closed")
        bigger_list = max(len(img_sections), len(sections))
        for i in range(bigger_list):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            if i % 2 != 0:
                split_nodes.append(TextNode(img_sections[alt_index], TextType.LINK, img_sections[link_index]))
                link_index += 2   #1 3 5   
                alt_index += 2
        #print("split nodes test here:",split_nodes)
        new_nodes.extend(split_nodes)
        #for node in new_nodes:
        #    print(node)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(
            text, TextType.TEXT
        )
    delimiter_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    delimiter_italic = split_nodes_delimiter(delimiter_bold, "_", TextType.ITALIC)
    delimiter_code = split_nodes_delimiter(delimiter_italic, "`", TextType.CODE)
    image = split_nodes_image(delimiter_code)
    nodes = split_nodes_link(image)
    return nodes

"""
node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
result = split_nodes_image([node])
print(result)
"""

# block_markdown.py
from enum import Enum

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks_list = []
    for block in blocks:
        #print(repr(block))

        #block.strip()
        #block.lstrip("\n")
        if len(block) == 0:
            continue
        block = block.strip()
        blocks_list.append(block)
    return blocks_list


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    ITALIC = "italic"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if len(block) == 0:
        return None
    if "# " in block[0:6] and block[0] == "#":
        return BlockType.HEADING
    if "```" in block[0:4] and "```" in block[4:len(block)+1]:
        return BlockType.CODE
    if block[0] == ">":
        return BlockType.QUOTE
    if block[0:2] == "- ":
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        lines = block.split("\n")
        counter = 1
        for line in lines:
            if not line.startswith(f"{counter}. "):
                return BlockType.PARAGRAPH
            counter += 1
        return BlockType.ORDERED_LIST         

    return BlockType.PARAGRAPH

def text_to_children(block, block_type):
    children_list = []
    
    if block_type == BlockType.CODE:
        lines = block.splitlines()
        content = "\n".join(lines[1:-1]) + "\n"
        prenode = HTMLNode("code", content)

        children_list.append(HTMLNode("pre", children=[prenode]))
    
    if block_type == BlockType.PARAGRAPH:
        clean_block = " ".join(block.strip().splitlines())
        text_nodes = text_to_textnodes(clean_block)
        html_children = [text_node_to_html_node(node) for node in text_nodes]
        children_list.append(HTMLNode("p", children=html_children))

    if block_type == BlockType.HEADING:
        n = len(block) - len(block.lstrip('#'))
        content = block.lstrip('#').strip()
        children_list.append(HTMLNode(f"h{n}", value=content))
    
    if block_type == BlockType.QUOTE:
        content = block.lstrip('>').strip()
        children_list.append(HTMLNode("blockquote", value=content))
    
    if block_type == BlockType.UNORDERED_LIST:
        children = []
        for i in block.split("\n"):
            line = i.strip()
            if line.startswith("- "):
                content = line[2:].strip()
                children.append(HTMLNode("li", value=content))
        children_list.append(HTMLNode("ul", children=children))

    if block_type == BlockType.ORDERED_LIST:
        children = []
        for i in block.split("\n"):
            line = i.strip()
            if ". " in line and line.split(". ", 1)[0].isdigit():
                line = line.split(". ", 1)
                content = line[1].strip()
                children.append(HTMLNode("li", value=content))
        children_list.append(HTMLNode("ol", children=children))
    return children_list
    


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes_list = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        children = text_to_children(block, block_type)
        nodes_list.extend(children)
    parent = HTMLNode(tag="div", children=nodes_list)
    
    return parent

