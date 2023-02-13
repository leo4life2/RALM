import pandas as pd
import sys
import re
import tiktoken
from utils.constants import ENCODING

INPUT_FILE = sys.argv[1]
OUTPUT_NAME = sys.argv[2]

def count_tokens(text: str) -> int:
    """count the number of tokens in a string"""
    return len(tokenizer.encode(text))

def df_to_csv():
    # First create a dataframe with columns "title", "heading", "content", "tokens"
    df = pd.DataFrame(columns=["title", "heading", "content", "tokens"])

    # Then go through the markdown file and add rows to the dataframe
    f =  open(INPUT_FILE, 'r')
    all_text = f.read()
    if not all_text.endswith("\n\n"):
        all_text += "\n\n"
    f.close()

    title_split = re.split(r"## |### ", all_text)
    # (.*)\n\n# is the regex for a title. It is its own line.
    # (.*)\n\n(.*) is the regex for a heading, but it is immediately followed by the content

    tokenizer = encoding = tiktoken.get_encoding(ENCODING)

    curr_title = ""
    for line in title_split:
        if line == "":
            continue
        else:
            # If there is more text after the first occurence of \n\n, then it is a heading and content
            if line.find("\n\n") < len(line) - 2:
                heading, content, _ = line.split("\n\n", 2)

                if curr_title == "":
                    raise Exception("Heading came before title: " + line)

                tokens = len(tokenizer.encode(content))
                df = pd.concat([df, pd.DataFrame({"title": [curr_title], "heading": [heading], "content": [content], "tokens": [tokens]})], ignore_index=True)

            # Otherwise, it is a title
            elif line.endswith("\n\n"):
                curr_title = line.strip()

    df.to_csv(OUTPUT_NAME, index=False)

if __name__ == "__main__":
    df_to_csv()