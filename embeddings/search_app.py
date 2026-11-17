from dotenv import load_dotenv
from google import genai
from cosine import cosine
from docs import docs
import json

load_dotenv()
client = genai.Client()
k = 3

with open("vectors.json", "r", encoding="utf-8") as f:
    vectors = json.load(f)

def embed(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values

def query():
    while True:
        scores = []
        user_input = input("Search: ").lower()

        if user_input == "quit":
            break
        
        q = embed(user_input)
        
        print("Loading...")
        
        for vec, doc in zip(vectors, docs):
            result = cosine(q, vec)
            scores.append((result, doc))
        
        scores.sort(reverse=True)

        for i, (res, doc) in enumerate(scores[:k], 1):
            print(f"{i}. {doc} ({res:.2f})")
        print()

query()