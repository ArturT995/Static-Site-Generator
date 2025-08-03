import os
import shutil

root_path = "static"
path_items = os.listdir(path="static")
dest_path = "public"

shutil.rmtree(dest_path)

os.mkdir(dest_path)
dest_items = os.listdir(path="public")


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

# depth/max depth are "=" (optional) they will already have fixed values
# the safeguard is then automatically in place, but you can tweak it if you want
# by passing different values in the call
static_to_public(root_path, dest_path, path_items)

"""DATA
path: images
path_items: ['images', 'index.css']
path_names: static/images
new_paths: ['tolkien.png']
path: tolkien.png
path_items: ['tolkien.png']
path_names: static/images/tolkien.png
paths_list: ['static/images/tolkien.png']
path: index.css
path_items: ['images', 'index.css']
path_names: static/index.css
paths_list: ['static/images/tolkien.png', 'static/index.css']


"""


# detect source directory files and directories
    # if directory run detector on that
    # if file copy
#if os.path.exists



# if same file in destination with same file path, overwrite it
    #



# copy files to public
    # if directory mkdir for directories and run copier on those
    # if file copy it

