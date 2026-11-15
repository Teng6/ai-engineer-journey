import os, json
from dotenv import load_dotenv
from embeddings.sentences import SENTENCES
import requests

load_dotenv()

vectors = []

for category, sentences in SENTENCES.items():
    response = requests.post(
        "https://api.jina.ai/v1/embeddings",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"
        },
    json = {
        "model": "jina-embeddings-v5-text-small",
        "input": sentences,
        }
    )
    data = response.json()
    vectors.extend(item['embedding'] for item in data['data'])
    print(f"{category}: is done -> total: {len(vectors)}")

with open("jina_vectors.json", "w", encoding="utf-8") as f:
    json.dump(vectors, f, indent=2, ensure_ascii=False)
    

print(f"Finished! Total now: {len(vectors)}")
print("--successfully written in json--")
