import os
import shutil
from src.markdown_blocks import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_html_node,
    extract_title,
)
from src.htmlnode import HTMLNode, ParentNode

from static_to_public import *

# copy functions you wanna test and riddle them with print statements, keep them uncommented here for future tests, while tweaking main files.

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path} ")
    content_list = static_to_public(from_path, dest_path, content_items, depth=0, max_depth=5)

    with open(template_path, "r") as f:
        template = f.read()
    
    print("content_list:", content_list)   # ['content/index.md']
    
    
    for path in content_list:
        with open(path, "r") as f:
            markdown = f.read()
        node = markdown_to_html_node(markdown)
        html_string = ParentNode.to_html(node)
        title = extract_title(markdown)    #returns Tolkien Fan Club
        template = template.replace("{{ Title }}", title, 1)
        template = template.replace("{{ Content }}", html_string, 1)

        print("path:", path)               # content/index.md
        
        
        print("html_string:", html_string) # returns <div>None</div>
        print("title:", title)             # probably returns None
        

        public_path = path.replace("content/", "public/")
        os.makedirs(os.path.dirname(public_path), exist_ok=True)
        with open(public_path, "w") as f:
            f.write(template)

        print("public_path:", public_path) # returns public/index.md

        #messy prints here if possible
        #print("markdown:", markdown)       # works
        #print("node:", node)                # messy, lots of nodes
        #print("template:", template)       # works

generate_page(from_path, template_path, dest_path)


"""generate_page DATA(clean calls)
content_list: ['content/index.md']
path: content/index.md
html_string: <div>None</div>
title: Tolkien Fan Club
public_path: public/index.md
"""



"""node print call
node: ParentNode(div, children: [ParentNode(h1, children: [LeafNode(None, Tolkien Fan Club, None)], None), 
ParentNode(p, children: [LeafNode(img, , {'src': '/images/tolkien.png', 'alt': 'JRR Tolkien sitting'})], None), 
ParentNode(p, children: [LeafNode(None, Here's the deal, , None), LeafNode(b, I like Tolkien, None), LeafNode(None, ., None)], None), 
ParentNode(blockquote, children: [LeafNode(None, "I am in fact a Hobbit in all but size."  -- J.R.R. Tolkien, None)], None), 
ParentNode(h2, children: [LeafNode(None, Blog posts, None)], None), ParentNode(ul, children: [ParentNode(li, children: [LeafNode(a, Why Glorfindel is More Impressive than Legolas, 
{'href': '/blog/glorfindel'})], None), ParentNode(li, children: [LeafNode(a, Why Tom Bombadil Was a Mistake, {'href': '/blog/tom'})], None), ParentNode(li, children: 
[LeafNode(a, The Unparalleled Majesty of "The Lord of the Rings", {'href': '/blog/majesty'})], None)], None), ParentNode(h2, children: [LeafNode(None, Reasons I like Tolkien, None)], None), 
ParentNode(ul, children: [ParentNode(li, children: [LeafNode(None, You can spend years studying the legendarium and still not understand its depths, None)], None), ParentNode(li, children: 
[LeafNode(None, It can be enjoyed by children and adults alike, None)], None), ParentNode(li, children: [LeafNode(None, Disney , None), LeafNode(i, didn't ruin it, None), 
LeafNode(None,  (okay, but Amazon might have), None)], None), ParentNode(li, children: [LeafNode(None, It created an entirely new genre of fantasy, None)], None)], None), 
ParentNode(h2, children: [LeafNode(None, My favorite characters (in order), None)], None), ParentNode(ol, children: [ParentNode(li, children: [LeafNode(None, Gandalf, None)], None), 
ParentNode(li, children: [LeafNode(None, Bilbo, None)], None), ParentNode(li, children: [LeafNode(None, Sam, None)], None), ParentNode(li, children: [LeafNode(None, Glorfindel, None)], None), 
ParentNode(li, children: [LeafNode(None, Galadriel, None)], None), ParentNode(li, children: [LeafNode(None, Elrond, None)], None), ParentNode(li, children: [LeafNode(None, Thorin, None)], None), 
ParentNode(li, children: [LeafNode(None, Sauron, None)], None), ParentNode(li, children: [LeafNode(None, Aragorn, None)], None)], None), ParentNode(p, children: [LeafNode(None, Here's what , None), 
LeafNode(code, elflang, None), LeafNode(None,  looks like (the perfect coding language):, None)], None), ParentNode(pre, children: [ParentNode(code, children: [LeafNode(None, func main(){
    fmt.Println("Aiya, Ambar!")
}
, None)], None)], None), ParentNode(p, children: [LeafNode(None, Want to get in touch? , None), LeafNode(a, Contact me here, {'href': '/contact'}), 
LeafNode(None, ., None)], None), ParentNode(p, children: [LeafNode(None, This site was generated with a custom-built , None), 
LeafNode(a, static site generator, {'href': 'https://www.boot.dev/courses/build-static-site-generator-python'}), LeafNode(None,  from the course on , None), 
LeafNode(a, Boot.dev, {'href': 'https://www.boot.dev'}), LeafNode(None, ., None)], None)], None)
"""