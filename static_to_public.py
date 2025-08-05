import os
import shutil
from src.markdown_blocks import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_html_node,
    extract_title,
)
from src.htmlnode import HTMLNode, ParentNode

root_path = "static"
path_items = os.listdir(path="static")
dest_path = "public"

shutil.rmtree(dest_path)

os.mkdir(dest_path)
dest_items = os.listdir(path="public")

template_path = "template.html"
from_path = "content"
content_items = os.listdir(path="content")

def generate_pages(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path} ")
    content_list = static_to_public(from_path, dest_path, content_items, depth=0, max_depth=5)

    with open(template_path, "r") as f:
        template = f.read()

    for path in content_list:
        
        with open(path, "r") as f:
            markdown = f.read()
        
        node = markdown_to_html_node(markdown) #returns a ParentNode
        html_string = ParentNode.to_html(node)
        title = extract_title(markdown)
        result = template.replace("{{ Title }}", title, 1)
        result = result.replace("{{ Content }}", html_string, 1)
        if path.endswith(".md"):
            path = path.replace(".md",".html")
        public_path = path.replace("content/", "public/").replace(".md", ".html")
        os.makedirs(os.path.dirname(public_path), exist_ok=True)


        with open(public_path, "w") as f:
            f.write(result)



def static_to_public(root_path, dest_path, path_items, depth=0, max_depth=5):
    if depth > max_depth:
        raise Exception(f"Recursion depth exceeded {max_depth}")

    paths_list = []
    new_paths_name = []

    for path in path_items:
        path_names = os.path.join(root_path, path)
        dest_names = os.path.join(dest_path, path)
        
        if os.path.isdir(path_names):
            if not os.path.exists(dest_names):
                os.mkdir(dest_names)
            new_paths = os.listdir(path=f"{path_names}")
            recursive_result = static_to_public(path_names, dest_names, new_paths, depth + 1, max_depth)
            paths_list.extend(recursive_result)

        else:
            shutil.copy(path_names, dest_names)
            paths_list.append(path_names)


    return paths_list

generate_pages(from_path, template_path, dest_path)
