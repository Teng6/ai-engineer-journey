import chromadb
from Project_4.search_app import embed

client = chromadb.PersistentClient(path="Project_5/chroma_db")
collection = client.get_or_create_collection(name="knowledge_base")


while True:
    query = input("Search: ")
    
    query_vector = embed(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )
    
    for doc, dis, met in zip(results["documents"][0], results["distances"][0], results["metadatas"][0]):
        print(f"{met["filename"]}, {met['section']}, {dis}")
        print(f"{doc:100}")