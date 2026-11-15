from dotenv import load_dotenv
from google import genai
from embeddings.cosine import cosine
from embeddings.sentences import SENTENCES
import time, json, os

load_dotenv()
client = genai.Client()


vectors = []
for category, sentences in SENTENCES.items():
    for sentence in sentences:
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=sentence,
        )
        vectors.append(response.embeddings[0].values)
    print(f"{category}: done")
    print(f"--- {len(vectors)} items now")
        
    
with open("gemini_vectors.json", "w", encoding="utf-8") as f:
    json.dump(vectors, f, indent=2, ensure_ascii=False)


print(len(vectors))
print(len(vectors[0]))
