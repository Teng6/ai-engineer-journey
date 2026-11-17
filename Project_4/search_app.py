from dotenv import load_dotenv
from google import genai
from embeddings.cosine import cosine
from embeddings.docs import docs
import json

load_dotenv()
client = genai.Client()
top_k = 3

with open("embeddings/vectors.json", "r", encoding="utf-8") as f:
    vectors = json.load(f)

def embed(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )
    return response.embeddings[0].values

def search(text):
    query = embed(text)
    scores = []
    for doc, vec in zip(docs, vectors):
        result = cosine(query, vec)
        scores.append((result, doc))
    scores.sort(reverse=True)
    return scores[:top_k]

def query(): 
    while True:
        user_input = input("Search: ").lower()
        if user_input == "quit":
            break
        
        print("\nLOADING")
        for rank, (res, doc) in enumerate(search(input), 1):
            print(f"{rank}. {doc} ({res:.4f})")
        print()
    
    
if __name__ == "__main__":
    query()