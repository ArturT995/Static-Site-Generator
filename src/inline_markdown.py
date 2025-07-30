import re
from src.textnode import TextNode, TextType


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
        #print(sections)
        #print("img_sections test here:",img_sections)
        link_index = 1
        alt_index = 0
        for i in range(len(img_sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
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
        text = node.text
        image_tuples_list = extract_markdown_links(text)
        split_nodes = []
        sections = []
        img_sections = []
        current_text = node.text
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
        #print(sections)
        #print("img_sections test here:",img_sections)
        link_index = 1
        alt_index = 0
        for i in range(len(img_sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(img_sections[alt_index], TextType.LINK, img_sections[link_index]))
                link_index += 2   #1 3 5   
                alt_index += 2
        #print("split nodes test here:",split_nodes)
        new_nodes.extend(split_nodes)
        #for node in new_nodes:
        #    print(node)
    return new_nodes

"""
node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
result = split_nodes_image([node])
print(result)
"""