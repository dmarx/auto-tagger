import openai
from pathlib import Path
from typing import List


class Document:
    def __init__(self, fpath: Path):
        self.fpath = fpath
        self.parse()
    def parse(self):
        lines = self.fpath.read().split('\n')
        self.title = lines[0]
        self.tags: set, self.content: str = parse_tags_from_lines(lines[1:])
    @property
    def has_tags(self):
        return len(self.tags) > 0
    def __str__(self):
        tags = '  \n'.join(self.tags)
        return '\n\n'.join([self.title, tags, self.content])
    def save(self):
        with open(self.fpath, 'w') as f:
            f.write(str(self))


def sort_docs(docs):
    """
    separates document collection into two groups: docs with tags, and docs without tags
    """
    tags_present = []
    tags_absent = []
    for doc in docs:
        if doc.has_tags:
            tags_present.append(doc)
        else:
            tags_absent.append(doc)
                           
                
def parse_tags_from_lines(lines: List[str]):
    """
    parses tags from document lines
    """
    pass
                
    
def build_prompt(docs_and_tags):
    """
    consumes output from `parse_tags_from_doc()` and formats it for the LLM
    """
    pass


def predict_tags(doc, prompt):
    """
    guess tags for document
    """
    pass


def main(docs):
    """
    parse documents, build an LLM tagger, tag docs that don't already have tags.
    """
    tags_present, tags_absent = sort_docs(docs)
    prompt = build_prompt(tags_present)
    for doc in tags_absent:
        tags = predict_tags(doc, prompt)
        doc.tags.update(tags)
        doc.save()

        
if __name__ == '__main__':
    docs = [Document(fpath) for fpath in Path('.').glob('*.md')]
    main(docs)
