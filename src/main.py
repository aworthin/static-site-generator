import os
import shutil
from block_markdown import markdown_to_html_node, extract_title
from textnode import TextType, TextNode

static_dir = "./static"
public_dir = "./public"
content_dir = "./content"
template_file = "./template.html"

def main():
    create_site(static_dir, public_dir)

def create_site(static_dir, public_dir):
    if os.path.exists(public_dir):
        print(f"Removing directory {public_dir}")
        shutil.rmtree(public_dir)

    print("Copying static files to public directory")
    copy_dir(static_dir, public_dir)

    generate_page(os.path.join(content_dir,"index.md"), template_file, os.path.join(public_dir, "index.html"))

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if os.path.exists(from_path):
        try:
            from_file_contents = ""
            with open(from_path, "r") as f:
                from_file_contents = f.read()
        except Exception as e:
            return f'Error reading file "{from_path}": {e}'
        
    if  os.path.exists(template_path):
        try:
            template_file_contents = ""
            with open(template_path, "r") as f:
                template_file_contents = f.read()
        except Exception as e:
            return f'Error reading file "{template_path}": {e}'
    
    html_node = markdown_to_html_node(from_file_contents)
    html_output = html_node.to_html()
    title = extract_title(from_file_contents)
    template_output = template_file_contents.replace("{{ Title }} ", title)
    template_output = template_output.replace("{{ Content }}", html_output) 

    if not os.path.exists(os.path.dirname(dest_path)):
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    if os.path.exists(dest_path) and os.path.isdir(dest_path):
        return f'Error: "{dest_path}" is a directory, not a file'
    try:
        with open(dest_path, "w") as f:
            f.write(template_output)
    except Exception as e:
        return f"Error: writing to file: {e}"

def copy_dir(source, dest):
    if not os.path.exists(dest):
        print(f"Creating dir {dest}")
        os.mkdir(dest)

    print(f"Copying files from {source} to {dest}")
    for file in os.listdir(source):
        orig_file = os.path.join(source, file)
        new_file = os.path.join(dest, file)

        if os.path.isfile(orig_file):
            print(f"Copy {orig_file} to {new_file}")
            shutil.copy(orig_file, new_file)
        if os.path.isdir(orig_file):
            copy_dir(orig_file, new_file)

if __name__ == "__main__":
    main()
