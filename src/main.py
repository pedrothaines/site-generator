import os
import shutil

from utils import extract_title, markdown_to_html_node

SCRIPT_DIR = os.path.dirname(__file__)


def main():
    dst_dir = os.path.join(SCRIPT_DIR, "../public/")
    src_dir = os.path.join(SCRIPT_DIR, "../static/")

    print(f"script_dir..: {SCRIPT_DIR}")
    print(f"dst_dir.....: {dst_dir}")
    print(f"src_dir.....: {src_dir}")

    remove_dir_files(dst_dir)
    copy_contents(dst_dir, src_dir)

    md_filepath = os.path.join(SCRIPT_DIR, "../content/index.md")
    template_filepath = os.path.join(SCRIPT_DIR, "../template.html")
    html_filepath = os.path.join(SCRIPT_DIR, "../public/index.html")

    generate_page(md_filepath, template_filepath, html_filepath)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md_file = open(from_path, "r")
    md_content = md_file.read()
    md_file.close()

    template_file = open(template_path, "r")
    template_content = template_file.read()
    template_file.close()

    html_content = markdown_to_html_node(md_content).to_html()

    title = extract_title(md_content)

    template_content = template_content.replace("{{ Title }}", title, 1)
    template_content = template_content.replace("{{ Content }}", html_content)

    dir = os.path.dirname(dest_path)
    os.makedirs(dir, exist_ok=True)

    html_file = open(dest_path, "w")
    html_file.write(template_content)
    html_file.close()


def remove_dir_files(dir):
    if not os.path.exists(dir):
        return

    files = list(map(lambda f: os.path.join(dir, f), os.listdir(dir)))

    for f in files:
        if os.path.isfile(f):
            os.remove(f)
        elif os.path.isdir(f):
            remove_dir_files(f)
            os.rmdir(f)
        else:
            raise NotImplementedError("unhandled file type")


def copy_contents(dst_dir, src_dir):
    """Recursive function that copies all the contents from a source directory to a destination directory."""

    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"directory {src_dir} does not exist")

    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    files = os.listdir(src_dir)

    for f in files:
        filepath = os.path.join(src_dir, f)

        if os.path.isfile(filepath):
            shutil.copy(filepath, dst_dir)

        elif os.path.isdir(filepath):
            copy_contents(os.path.join(dst_dir, f), filepath)
        else:
            raise NotImplementedError("unhandled file type")


if __name__ == "__main__":
    main()
