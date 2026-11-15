from dotenv import load_dotenv
from cosine import cosine
from google import genai
from docs import docs
import json, os


load_dotenv()
client = genai.Client()

with open("vectors.json", "r", encoding="utf-8") as f:
    vectors = json.load(f)

query = input("You: ")

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query,
)

query_vector = response.embeddings[0].values

scores = []

for doc, vec in zip(docs, vectors):
    result = cosine(query_vector, vec)
    scores.append((result, doc))

print(len(scores))

print("SORTED")

scores.sort(reverse=True)
k = 3


for rank, (score, doc) in enumerate(scores[:k], 1):
    print(f"{rank}. {score:.3f} -> {doc}")