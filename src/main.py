import os
import shutil

from utils import extract_title

SCRIPT_DIR = os.path.dirname(__file__)


def main():
    dst_dir = os.path.join(SCRIPT_DIR, "../public/")
    src_dir = os.path.join(SCRIPT_DIR, "../static/")

    print(f"script_dir..: {SCRIPT_DIR}")
    print(f"dst_dir.....: {dst_dir}")
    print(f"src_dir.....: {src_dir}")

    remove_dir_files(dst_dir)
    copy_contents(dst_dir, src_dir)

    md = """
# The Writer

This is an interesting history...

Or, is it?

We may have some unordered lists in the way.

- uitem 1
- uitem 2 with some **bold** text

Bye.
"""
    title = extract_title(md)
    print(title)


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
            os.mkdir(os.path.join(dst_dir, f))
            copy_contents(os.path.join(dst_dir, f), filepath)
        else:
            raise NotImplementedError("unhandled file type")


if __name__ == "__main__":
    main()
