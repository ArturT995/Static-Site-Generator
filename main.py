import os
import sys
import shutil

basepath = "/"


if len(sys.argv) > 1:
    basepath = sys.argv[1]

root_path = "./static"
dest_path = "./docs"
template_path = "./template.html"
from_path = "./content"


dest_path = dest_path.replace("/", basepath)
root_path = root_path.replace("/", basepath)
template_path = template_path.replace("/", basepath)
from_path = from_path.replace("/", basepath)

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
