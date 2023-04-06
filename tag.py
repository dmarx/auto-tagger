import openai
from pathlib import Path
from typing import List, Tuple

                
def parse_tags(text: List[str]) -> Tuple[set, str]:
    """
    parses tags from document 
    """
    pass
             

class Document:
    def __init__(self, fpath: Path):
        self.fpath = fpath
        self.parse()
    def parse(self):
        lines = self.fpath.read().split('\n')
        self.title = lines[0]
        body = '\n'.join(lines[1:])
        self.tags: set, self.content: str = parse_tags(body)
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


# these thresholds are only very approximately respected and were chosen blindly
def build_partial_prompt(List[Document], max_example_len=200, max_partial_prompt_len=1000):
    """
    Use already-tagged documents as prompt examples.
    Specify universe of known labels as a soft constraint.
    """
    all_tags = set()
    examples = ""
    for i, doc in enumerate(document):
        if (len(doc.content) < max_example_len) and (len(examples) < max_partial_prompt_len):
            examples += f"<content-{i}>{doc.title}\n\n{doc.content}</content-{i}>\n"
            examples += f"<tags-{i}>{doc.tags}</tags-{i}>\n"
        all_tags.update(doc.tags)
    tags_prompt = f"Available tags: {','.join(all_tags)}\n"
    return tags_prompt + examples

  
def build_prompt(doc:Document, partial_prompt: str):
    """
    build prompt to predict tags for a specific document
    """
    i = 99 # arbitrary 'large-ish' number
    prompt = partial_prompt 
    prompt += f"<content-{i}>{doc.title}\n\n{doc.content}</content-{i}>\n"
    prompt += f"<tags-{i}>"
    return prompt

  
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
    partial_prompt = build_partial_prompt(tags_present)
    for doc in tags_absent:
        prompt = build_prompt(doc, partial_prompt)
        tags = predict_tags(doc, prompt)
        doc.tags.update(tags)
        doc.save()

        
if __name__ == '__main__':
    docs = [Document(fpath) for fpath in Path('.').glob('*.md')]
    main(docs)
