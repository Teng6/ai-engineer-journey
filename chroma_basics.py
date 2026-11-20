import chromadb
from google import genai
from dotenv import load_dotenv
from Project_4.search_app import embed

load_dotenv()
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="docs")
gemini_client = genai.Client()

query = input("Search: ")
tag = input("Tag: ")

query_vector = embed(query)

results = collection.query(
    query_embeddings=[query_vector],
    n_results=5,
    where={"tag": tag},
)

for doc, dis in zip(results["documents"][0], results["distances"][0]):
    print(f"Document: {doc} -> Distance: {dis:.4f}")