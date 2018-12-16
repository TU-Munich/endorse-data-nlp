import tika
import re

tika.initVM()
from tika import parser


def clean_content(content: str):
    """
    Clean the content of the file
    Remove all blank lines and all tabs and spaces
    :param content: the content as a string
    :return: the cleaned content
    """
    # todo: use this faster python parser
    content = re.sub(r'^\n\n*', '', content)
    content = re.sub(r'\s\s*', ' ', content)
    content = re.sub(r'\n\n*', '\n', content)
    content = re.sub(r'\t\t*', '\t', content)
    return content


def parse_file(path: str):
    """
    Parse a file with the help of the tika service
    :param path: the path to the specific file
    :return: the parsed file
    """
    parsed = parser.from_file(path)
    # Clean the content
    parsed["content"] = clean_content(str(parsed["content"]))
    return parsed
