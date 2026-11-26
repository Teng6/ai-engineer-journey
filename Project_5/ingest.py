from pypdf import PdfReader
from google import genai
from dotenv import load_dotenv
from Project_4.search_app import embed
import chromadb
import os

load_dotenv()
reader = PdfReader("Project_5/docs/rag_notes.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

client = chromadb.PersistentClient(path="Project_5/chroma_db")
collection = client.get_or_create_collection(name="knowledge_base")
gemini_client = genai.Client()


def load_file(path):
    if path.endswith(".pdf"):
        read = PdfReader(path)
        text = ""
        for page in read.pages:
            text += page.extract_text() + "\n"
        return text
    else:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

def split_sections(text):
    title = "" 
    current = ""
    sections = []
    for line in text.split("\n"):
        if line.startswith("#"):
            if current:
                sections.append((title, current))
            title = line
            current = ""
        else:
            current += line + "\n"
    sections.append((title, current))
    return sections

sections = []
for file in os.listdir("Project_5/docs"):
    full_path = "Project_5/docs/" + file
    text = load_file(full_path)
    if file.endswith("md"):
        sections = split_sections(text)
    else:
        sections = [("whole file", text)]
    
    i = 0
    for name, body in sections:
        if body.strip() == "":
            continue
        collection.add(
            ids=[file + "-" + str(i)],
            documents=[body],
            embeddings=[embed(body)],
            metadatas=[{"filename": file, "section": name}],
        )
        i += 1

print(collection.count())