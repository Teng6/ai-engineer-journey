from dotenv import load_dotenv
from pypdf import PdfReader
import os

def split_text(text, size=1000, overlap=150):
    if overlap >= size:
        raise ValueError("Overlap must be smaller than the size")
    
    pieces = []
    start = 0
    while start < len(text):
        pieces.append(text[start:start + size])
        if start + size >= len(text):
            break
        start += size - overlap
    return pieces

def split_sections(text):
    sections = []
    heading = "(no heading)"
    current = ""
    in_code = False
    
    for line in text.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
        if line.startswith("#") and not in_code:
            if current:
                sections.append((heading, current))
            heading = line.lstrip("#").strip()
            current = ""
        else:
            current += line + "\n"
    sections.append((heading, current))
    return sections

def chunk_markdown(path):
    with open(path, "r", encoding="utf-8") as f:
        texts = f.read()
    sections = split_sections(texts)
    file_name = os.path.basename(path)
    chunks = []
    
    n = 0
    
    for title, text in sections:
        if text.strip() == "":
            continue
        if len(text) <= 1000:
            pieces = [text]
        else:
            pieces = split_text(text)
        
        for piece in pieces:
            chunks.append({
                "id": file_name + "-" + str(n),
                "text": piece,
                "file": file_name,
                "location": title,
            })
            n += 1
    
    return chunks

def find_page(position, page_starts):
    page = 0
    for start in page_starts:
        if position >= start:
            page += 1
    return page

def chunk_pdf(path):
    file_name = os.path.basename()
    full_text, page_starts = read_pdf(path)
    pieces = split_text(full_text)
    
    
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
