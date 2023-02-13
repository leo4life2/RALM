import pandas as pd
import tiktoken
import sys
import openai
import numpy as np

from utils.constants import MAX_SECTION_LEN, SEPARATOR, ENCODING, COMPLETIONS_API_PARAMS
from utils.embedding import load_embeddings, compute_doc_embeddings
from utils.similarity import order_document_sections_by_query_similarity

def construct_prompt(question: str, context_embeddings: dict, df: pd.DataFrame) -> str:
    """
    Fetch relevant 
    """
    most_relevant_document_sections = order_document_sections_by_query_similarity(question, context_embeddings)
    
    chosen_sections = []
    chosen_sections_len = 0
    chosen_sections_indexes = []

    encoding = tiktoken.get_encoding(ENCODING)
    separator_len = len(encoding.encode(SEPARATOR))

    for _, section_index in most_relevant_document_sections:
        # Add contexts until we run out of space.        
        document_section = df.loc[section_index]
        
        chosen_sections_len += document_section.tokens + separator_len
        if chosen_sections_len > MAX_SECTION_LEN:
            break
            
        chosen_sections.append(SEPARATOR + document_section.content.replace("\n", " "))
        chosen_sections_indexes.append(str(section_index))
            
    # Useful diagnostic information
    print(f"Selected {len(chosen_sections)} document sections:")
    print("\n".join(chosen_sections_indexes))
    
    header = """Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say "I don't know."\n\nContext:\n"""
    
    return header + "".join(chosen_sections) + "\n\n Q: " + question + "\n A:"

def answer_query_with_context(
    query: str,
    df: pd.DataFrame,
    document_embeddings: dict[(str, str), np.array],
    show_prompt: bool = False
) -> str:
    prompt = construct_prompt(
        query,
        document_embeddings,
        df
    )
    
    if show_prompt:
        print(prompt)

    response = openai.Completion.create(
                prompt=prompt,
                **COMPLETIONS_API_PARAMS
            )

    return response["choices"][0]["text"].strip(" \n")

if __name__ == "__main__":
    INPUT_FILE = sys.argv[1]
    PROMPT = sys.argv[2]

    df = pd.read_csv(INPUT_FILE)
    df = df.set_index(["title", "heading"])

    document_embeddings = compute_doc_embeddings(df)
    # document_embeddings = load_embeddings("data/olympics_sections_document_embeddings.csv")

    answer = answer_query_with_context(PROMPT, df, document_embeddings)
    print("===\nAnswer is: \n\n", answer)