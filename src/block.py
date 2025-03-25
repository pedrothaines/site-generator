from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")

    if markdown_block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING

    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE

    if lines[0].startswith(">"):
        for i in range(1, len(lines)):
            if not lines[i].startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if lines[0].startswith("- "):
        for i in range(1, len(lines)):
            if not lines[i].startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if lines[0].startswith("1. "):
        for i in range(1, len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
