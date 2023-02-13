# RALM

Based on

- <https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb>
- <https://github.com/openai/openai-cookbook/blob/5b5f22812158002f19e24fcb5c9a391a6551c1e2/examples/fine-tuned_qa/olympics-1-collect-data.ipynb>

## Usage

### 1. Install dependencies

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`

### 2. Create markdown file for context fetching

Look at `data/markdown/froofy_hugger.md` or `data/markdown/olympics.md` for examples.
The markdown file MUST have the following structure:

```markdown
## Title
### Subtitle
Paragraph
### Subtitle
Paragraph
## Title
...
```

In short, the markdown file must have `##` headers and `###` subheaders. Text MUST be a single paragraph, and must be under a `###` subheader.

### 3. Create context csv file

```bash
python3 md_to_csv.py data/markdown/YOUR_MD_FILE.md OUTPUT_CSV_FILE.csv
```

### 4. Run RA-complete code

```bash
python3 retrieval_augmented_complete.py CSV_FILE.csv "YOUR_PROMPT_HERE"
```

## Areas for improvement

- reduce_long simply truncates the text, which is not ideal. Could potentially improve this by summarizing long paragraphs.
- prompt engineering: refer to the leaked bing chatbot prompts as guidlines