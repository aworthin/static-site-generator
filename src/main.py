import os
import shutil
from textnode import TextType, TextNode

static_dir = "./static"
public_dir = "./public"

def main():
    create_site(static_dir, public_dir)

def create_site(static_dir, public_dir):
    if os.path.exists(public_dir):
        print(f"Removing directory {public_dir}")
        shutil.rmtree(public_dir)

    print("Copying static files to public directory")
    copy_dir(static_dir, public_dir)

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
