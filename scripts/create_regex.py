'''

    create_regex.py

    Create a regex of all tokens that are needed
    to be recognized.

    Note: SHARED_DELIMITER_CHARS is used to store
    delimiters and characters that are used for both
    Python, HTML, and Malange.

'''

import keyword

KEYWORDS = list(keyword.kwlist) + ["include"]

def create_regex():

    RESERVED_KEYWORDS = r""
    HTML_TAGS         = r""
    MALANGE_BLOCKS    = r""
    SPECIAL_CHARS     = r""


    # Let's create a regex for reserved keywords.
    for key in KEYWORDS:


if __name__ == "__main__":
    text = create_regex()
    f = open("regex.txt", "a")
    f.write(text)
    f.close()
