import openai
from pathlib import Path
from typing import List, Tuple

                
def get_tags(line: str):
    """
    parse all tags present in a document line
    """
    pass
  
def remove_tags_from_line(tags_in_line, line):
    """
    return the line of text with all tag elements removed
    """
    pass
  
  
def parse_tags(text: str) -> Tuple[set, str]:
    """
    parses tags from document.
    TO DO: set this up in a way that the user can configure logic. regex maybe?
    """
    tags = []
    lines_of_text_with_tags_removed = []
    for line in text.split('\n'):
        tags_in_line = get_tags(line)
        if tags_in_line:
            line = remove_tags_from_line(tags_in_line, line)
            tags.extend(tags_in_line)
        lines_of_text_with_tags_removed.append(line)
    doc_without_tags = '\n'.join(lines_of_text_with_tags_removed)
    return tags, doc_without_tags
             

class Document:
    def __init__(self, fpath: Path):
        self.fpath = fpath
        self.parse()
    def parse(self):
        #lines = self.fpath.read().split('\n')
        with open(self.fpath, 'r') as f:
            lines = f.read().split('\n')
        self.title = lines[0]
        body = '\n'.join(lines[1:])
        self.tags, self.content = parse_tags(body)
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
    return tags_present, tags_absent


# these thresholds are only very approximately respected and were chosen blindly
def build_prompt_head(documents: List[Document], max_example_len: int=200, max_partial_prompt_len: int=1000):
    """
    Use already-tagged documents as prompt examples.
    Specify universe of known labels as a soft constraint.
    """
    all_tags = set()
    examples = ""
    j=0
    for i, doc in enumerate(documents):
        if (len(doc.content) < max_example_len) and (len(examples) < max_partial_prompt_len):
            examples += f"<content-{i}>{doc.title}\n\n{doc.content}</content-{i}>\n"
            examples += f"<tags-{i}>{doc.tags}</tags-{i}>\n"
            j=i
        all_tags.update(doc.tags)
    tags_prompt = f"Available tags: {','.join(all_tags)}\n"
    return j+1, tags_prompt + examples

  
def build_prompt(doc: Document, prompt_head: str):
    """
    build prompt to predict tags for a specific document
    """
    #i = 99 # arbitrary 'large-ish' number
    i, prompt_head = prompt_head
    prompt = prompt_head 
    prompt += f"<content-{i}>{doc.title}\n\n{doc.content}</content-{i}>\n"
    prompt += f"<tags-{i}>"
    return prompt

  
def predict_completion(prompt):
    """
    guess tags for document
    """
    response = openai.Completion.create(
        model='gpt-3.5-turbo',
        prompt=prompt,
    )
    return response['choices'][0]['message']['content']

  
def predict_chat_completion(prompt):
    """
    guess tags for document
    """
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=prompt,
    )
    return response['choices'][0]['message']['content']

  
def isolate_tags_from_completion(completion):
    pass

def build_chat_prompt(doc: Document, prompt_head: str):
    """
    build prompt to predict tags for a specific document.
    modified for chat models
    """
    #i = 99 # arbitrary 'large-ish' number
    i, system_prompt = prompt_head
    #prompt = prompt_head 
    user_prompt = f"<content-{i}>{doc.title}\n\n{doc.content}</content-{i}>\n"
    user_prompt += f"<tags-{i}>"
    messages = [
      {'role':'system', 'content':system_prompt},
      {'role':'user',   'content':user_prompt},
    ]
    return messages
    
  
def main(docs):
    """
    parse documents, build an LLM tagger, tag docs that don't already have tags.
    """
    tags_present, tags_absent = sort_docs(docs)
    prompt_head = build_prompt_head(tags_present)
    for doc in tags_absent:
        #prompt = build_prompt(doc, prompt_head)
        #completion = predict_completion(prompt)
        prompt = build_chat_prompt(doc, prompt_head)        
        completion = predict_chat_completion(prompt)
        tags = isolate_tags_from_completion(completion)
        doc.tags.update(tags)
        doc.save()

        
if __name__ == '__main__':
    FOLDER= 'examples' #'.'
    docs = [Document(fpath) for fpath in Path(FOLDER).glob('*.md')]
    main(docs)
