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
    chunks = []
    full_text, page_starts = read_pdf(path)
    file_name = os.path.basename(path)
    texts = split_text(full_text)
    step = 850
    
    for i, text in enumerate(texts):
        start = i * step
        end = start + len(text) - 1
        start_page = find_page(start, page_starts)
        end_page = find_page(end, page_starts)

        if start_page == end_page:
            location = f"{start_page}"
        else:
            location = f"{start_page} - {end_page}"
        
        chunks.append({
            "id": f"{file_name}-{i}",
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
