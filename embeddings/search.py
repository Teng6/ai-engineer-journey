from dotenv import load_dotenv
from google import genai
from docs import docs
from cosine import cosine
import json, time

load_dotenv()

client = genai.Client()

vectors = []

for text in docs:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )
    result = response.embeddings[0].values
    vectors.append(result)
    time.sleep(1)

with open("vectors.json", "w", encoding="utf-8") as f:
    json.dump(vectors, f, ensure_ascii=False)



print(len(vectors))
print(len(vectors[0]))




