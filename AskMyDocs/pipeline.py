from dotenv import load_dotenv
from google import genai
from .chunking import chunk_pdf, chunk_markdown
from .rag_prompt import format_sources, build_message, SYSTEM_PROMPT, REWRITE_PROMPT
from .test_prompt import gemini
import os
import chromadb

load_dotenv()

def embed(texts):
    client = genai.Client()
    response = client.models.embed_content(
        model='gemini-embedding-001',
        contents=texts,
    )
    result = [e.values for e in response.embeddings]

    return result

#The chunked files are then moved to the Chroma DB
def get_collection():
    client = chromadb.PersistentClient(path="AskMyDocs/database/notes_db")
    collection = client.get_or_create_collection(name="notes")
    return collection

#Loads the file and chunks em
def load_file(path):
    file = os.path.basename(path).lower()
    if file.endswith(".md"):
        chunks = chunk_markdown(path)
    elif file.endswith(".pdf"):
        chunks = chunk_pdf(path)
    else:
        raise ValueError(f"Unknown file type: {file}")
    
    texts = [c['text'] for c in chunks]
    embedded_texts = embed(texts)
    collection = get_collection()
    collection.add(
        ids=[c['id'] for c in chunks],
        documents=texts,
        embeddings=embedded_texts,
        metadatas=[{"file": c['file'], "location": c['location']} for c in chunks]
    )
    
    return len(chunks)

#Search for the similar top k
def search(question, n=3):
    embedded_question = embed([question])[0]
    collection = get_collection()
    results = collection.query(
        query_embeddings=[embedded_question],
        n_results=n
    )
    chunks = []
    texts = results['documents'][0]
    metadatas = results['metadatas'][0]
    for text, meta in zip(texts, metadatas):
        chunks.append({
            "text": text,
            "file": meta['file'],
            "location": meta['location'],
        })
    return chunks
    
#The final output
def ask(question):
    chunks = search(question)
    message = build_message(question, chunks)
    result = gemini(SYSTEM_PROMPT, message)
    
    if "not in your notes" in result.lower():
        print(result)
        return result
    else:
        sources = format_sources(chunks)    
        print(result)
        print(sources)
        return result
    
#Rewriting follow up questions
def rewrite_question(history, question):
    if not history:
        return question
    
    parts = []
    
    for turn in history:
        parts.append(f"Question: {turn['question']}")
        parts.append(f"Answer: {turn['answer']}")
    
    history_text = "\n".join(parts)
    message = f"Chat history:\n {history_text}\n\nNew Question: {question}"
    result = gemini(REWRITE_PROMPT, message)
    return result.strip()

#The query
def chat():
    history = []
    while True:
        question = input("You: ")
        if question == "quit":
            break
        full_question = rewrite_question(history, question)
        print(f"REWRITTEN: {full_question}")
        answer = ask(full_question)
        history.append({
            "question": full_question,
            "answer": answer,
        })
        

def main():
    chat()

if __name__ == "__main__":
    main()