from textnode import *
import os, shutil
from markdown_blocks import markdown_to_html_node, markdown_to_blocks

def delete_public_tree(public):
    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)

def copy_static_content(public, static):

    path=static+"/"
    print(path)
    for subdir in os.listdir(static):
        relpath=path+subdir
        if os.path.isfile(relpath):
            shutil.copy(relpath, public)

        elif os.path.isdir(relpath):
            public_copy = public + "/" + subdir
            os.makedirs(public_copy, exist_ok=True)
            copy_static_content(public_copy, relpath)
        else:
            raise Exception ("neither file nor directory")

def extract_title(markdown):
    separated = markdown_to_blocks(markdown)
    for line in separated:
        if line == "":
            continue
        split_line = line.strip()
        if split_line.startswith("# "):
            split_line = split_line[2:]
            split_line = split_line.strip()
            return split_line
    raise Exception("No h1 header in the beginning")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    r = open(from_path, "r")
    from_path_string = r.read() #markdown string
    r.close()

    f = open(template_path, "r")
    template_path_string = f.read()
    f.close()
    
    html_string = markdown_to_html_node(from_path_string)
    html_string = html_string.to_html()
    
    new_title = extract_title(from_path_string)

    template_path_string = template_path_string.replace("{{ Title }}", new_title)
    template_path_string = template_path_string.replace("{{ Content }}", html_string)

    directory_name = os.path.dirname(dest_path)
    os.makedirs(directory_name, exist_ok=True)

    with open(dest_path, "w") as w:
        w.write(template_path_string)

def main():
    copy_static_content("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

    




if __name__ == "__main__":
    main()