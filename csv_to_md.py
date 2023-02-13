import pandas as pd
import sys

# Convert CSV of structure title - heading - content tokens into a markdown file

INPUT_FILE = sys.argv[1]
OUTPUT_NAME = sys.argv[2]

df = pd.read_csv(INPUT_FILE)
df = df.set_index(["title", "heading"])

# group by title into a dictionary
dict = {}

for index, row in df.iterrows():
    title = index[0]
    heading = index[1]
    content = row['content']
    
    if title not in dict:
        dict[title] = {}
    
    dict[title][heading] = (content)

# write to markdown file
with open(OUTPUT_NAME, 'w') as f:
    for title in dict:
        f.write(f"## {title}\n\n")
        for heading in dict[title]:
            f.write(f"### {heading}\n\n")
            f.write(f"{dict[title][heading]}\n\n")