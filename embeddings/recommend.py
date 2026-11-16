import json
from docs import docs
from cosine import cosine

with open("vectors.json", "r", encoding="utf-8") as f:
    vectors = json.load(f)
    
liked = 0

scores = []

for i in range(len(docs)):
    score = cosine(vectors[liked], vectors[i])
    scores.append((score, docs[i]))
    
scores.sort(reverse=True)

for result, doc in scores[1:4]:
    print(result, doc)
