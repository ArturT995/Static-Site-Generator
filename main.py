from static_to_public import *


def main():
    print("Hello from static-site-generator!")
    static_to_public(root_path, dest_path, path_items)
    generate_pages(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
