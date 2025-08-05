import os
import sys
import shutil


root_path = "./static"
dest_path = "./docs"
template_path = "./template.html"
from_path = "./content"

shutil.rmtree(dest_path)
os.mkdir(dest_path)

path_items = os.listdir(path=f"{root_path}")
dest_items = os.listdir(path=f"{dest_path}")

from static_to_public import generate_pages, static_to_public

def main():
    print("Hello from static-site-generator!")

    static_to_public(root_path, dest_path, path_items)
    generate_pages(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
