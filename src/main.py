import os
import shutil
import sys
from block_markdown import markdown_to_html_node, extract_title
from textnode import TextType, TextNode

static_dir = "./static"
public_dir = "./docs"
content_dir = "./content"
template_file = "./template.html"
default_basepath = "/"

def main():
    base_path = default_basepath
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    create_site(static_dir, public_dir, base_path)

def create_site(static_dir, public_dir, base_path):
    if os.path.exists(public_dir):
        print(f"Removing directory {public_dir}")
        shutil.rmtree(public_dir)

    print("Copying static files to public directory")
    copy_dir(static_dir, public_dir)

    generate_pages_recursive(content_dir, template_file, public_dir, base_path)

def generate_pages_recursive(content_path, template_path, dest_path, base_path):
    print(f"Generating content for directory {content_path}")
    for file in os.listdir(content_path):
        content_file = os.path.join(content_path, file)
        dest_file = os.path.join(dest_path, file)

        if os.path.isfile(content_file) and content_file.endswith(".md"):
            dest_file = dest_file.replace(".md", ".html")
            generate_page(content_file, template_path, dest_file, base_path)

        if os.path.isdir(content_file):
            generate_pages_recursive(content_file, template_path, dest_file, base_path)

def generate_page(content_path, template_path, dest_path, base_path):
    print(f"Generating page from {content_path} to {dest_path} using {template_path}")
    if os.path.exists(content_path):
        try:
            from_file_contents = ""
            with open(content_path, "r") as f:
                from_file_contents = f.read()
                f.close()
        except Exception as e:
            return f'Error reading file "{content_path}": {e}'
        
    if  os.path.exists(template_path):
        try:
            template_file_contents = ""
            with open(template_path, "r") as f:
                template_file_contents = f.read()
                f.close()
        except Exception as e:
            return f'Error reading file "{template_path}": {e}'
    
    html_node = markdown_to_html_node(from_file_contents)
    html_output = html_node.to_html()
    title = extract_title(from_file_contents)
    template_file_contents = template_file_contents.replace("{{ Title }} ", title)
    template_file_contents = template_file_contents.replace("{{ Content }}", html_output) 
    template_file_contents = template_file_contents.replace('href="/', 'href="' + base_path)
    template_file_contents = template_file_contents.replace('src="/', 'src="' + base_path)

    if not os.path.exists(os.path.dirname(dest_path)):
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    if os.path.exists(dest_path) and os.path.isdir(dest_path):
        return f'Error: "{dest_path}" is a directory, not a file'
    try:
        with open(dest_path, "w") as f:
            f.write(template_file_contents)
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
