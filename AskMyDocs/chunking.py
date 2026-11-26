from dotenv import load_dotenv
from pypdf import PdfReader
import os


def split_text(text, size=1000, overlap=150):
    chunks = []
    start = 0
    step = size - overlap 
    
    while start < len(text):
        chunks.append(text[start:start + size])
        if start + size >= len(text):
            break
        start += step
     
    return chunks

def chunk_markdown(path):
    chunks = []
    heading = "(no heading)"
    file_name = os.path.basename(path)
    text = ""
    in_code = False

    with open(path, "r", encoding="utf-8") as f:
        texts = f.read()
    
    ## chunking part
    for line in texts.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if line.startswith('#') and not in_code:
            if text:
                chunks.append((heading, text))
                
            heading = line.lstrip('#').strip()
            text = ""
        else:
            text += line + "\n"
    if text:
        chunks.append((heading, text))
    
    ## check if its longer than 1000
    final_chunk = []
    counter = 0
    for heading, text in chunks:
        if len(text) > 1000:
            pieces = split_text(text)
        else:
            pieces = [text]
        
        ## inside this loop, we make the dict now.
        for piece in pieces:
            final_chunk.append({
                "id": file_name + "-" + str(counter),
                "text": piece,
                "file": file_name,
                "location": heading,
            })
            counter += 1
    return final_chunk
    
def find_page(position, page_starts):
    page = 0
    for start in page_starts:
        if position >= start:
            page += 1
    return page

def chunk_pdf(path):
    full_text, page_starts = read_pdf(path)
    chunks = []
    file_name = os.path.basename(path)
    
    texts = split_text(full_text)
    
    for i, text in enumerate(texts):
        start = i * 850
        end = start + len(text) - 1 
        p_start = find_page(start, page_starts)
        p_end = find_page(end, page_starts)

        if p_start == p_end:
            location = f"{p_start}"
        else:
            location = f"{p_start} - {p_end}"
        
        chunks.append({
            "id": file_name + "-" + str(i),
            "text": text,
            "file": file_name,
            "location": location,
        })
        
    return chunks

def read_pdf(path):
    reader = PdfReader(path)
    full_text = ""
    page_starts = []
    
    for page in reader.pages:
        page_starts.append(len(full_text))
        full_text += page.extract_text() + "\n"
        
    return full_text, page_starts



page_starts = [0, 900, 1800]
position = 500

print(find_page(position, page_starts))
