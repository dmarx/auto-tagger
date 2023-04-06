from dataclasses import dataclass
import openai
from pathlib import Path


@dataclass
class Document:
    fpath: Path
    content: str


def parse_tags_from_doc(doc):
    """
    returns a list of dicts associating documents with their tags
    """
    pass

def build_prompt(docs_and_tags):
    """
    consumes output from `parse_tags_from_doc()` and formats it for the LLM
    """
    pass

def sort_docs(docs):
    """
    separates document collection into two groups: docs with tags, and docs without tags
    """
    pass

def predict_tags(doc, prompt):
    """
    guess tags for document
    """
    pass

def add_tags(doc, tags):
    """
    add new tags to document
    """
    pass

def main(docs):
    """
    parse documents, build an LLM tagger, tag docs that don't already have tags.
    """
    tags_present, tags_absent = sort_docs(docs)
    docs_and_tags = [parse_tags_from_doc(doc) for doc in tags_present]
    prompt = build_prompt(docs_and_tags)
    for doc in tags_absent:
        tags = predict_tags(doc, prompt)
        add_tags(doc, tags)
   
if __name__ == '__main__':
    docs = [Document(fpath=path, content=path.read()) for path in Path('.').glob('*.md')]
    main(docs)
