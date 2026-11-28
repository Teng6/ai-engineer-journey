from dotenv import load_dotenv


SYSTEM_PROMPT = """

you will get pieces of text
use only the pieces
if no answer, say "not in your notes."
keep the answer short, key points only
follow the method in the pieces

"""
REWRITE_PROMPT = """

you get a chat history and a new question
make the new question a full question that stands alone
use the history to fill in what is missing
if the question is already full, return it the same
do not answer the question
return only the question, nothing else

"""


def build_message(question, chunks):
    parts = []
    for chunk in chunks:
        heading = f"{chunk['file']}-{chunk['location']}"
        parts.append(f'({heading})\n{chunk['text']}')   
    joined = "\n\n".join(parts)
    return f"Chunks:\n{joined}\n\nQuestion: {question}"

def format_sources(chunks):
    lines = []
    for i, chunk in enumerate(chunks, 1):
        lines.append(f'{i}. {chunk['file']}-{chunk['location']}\n"{chunk['text']}"')
    
    return "\n".join(lines)
    