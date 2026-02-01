from textnode import *
import os, shutil, sys
from markdown_blocks import markdown_to_html_node, markdown_to_blocks

def delete_public_tree(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)

def copy_static_content(public, static):
    os.makedirs(public, exist_ok=True)
    for subdir in os.listdir(static):
        relpath = os.path.join(static, subdir)
        if os.path.isfile(relpath):
            shutil.copy(relpath, public)

        elif os.path.isdir(relpath):
            public_copy = os.path.join(public, subdir)
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

def generate_page(from_path, template_path, dest_path, basepath):
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
    template_path_string = template_path_string.replace('href="/', f'href="{basepath}')
    template_path_string = template_path_string.replace('src="/', f'src="{basepath}')


    directory_name = os.path.dirname(dest_path)
    os.makedirs(directory_name, exist_ok=True)

    with open(dest_path, "w") as w:
        w.write(template_path_string)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    entries = os.listdir(dir_path_content)
    for entry in entries:
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
        elif os.path.isfile(from_path) and from_path.endswith(".md"):
            html_dest_path = dest_path.replace(".md", ".html")
            generate_page(from_path, template_path, html_dest_path, basepath)

def main():
    delete_public_tree("docs")
    copy_static_content("docs", "static")
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    generate_pages_recursive("content", "template.html", "docs", basepath)



if __name__ == "__main__":
    main()