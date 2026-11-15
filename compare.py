import json, os
from dotenv import load_dotenv
from cosine import cosine

load_dotenv()

with open("gemini_vectors.json", encoding='utf-8') as f:
    gemini = json.load(f)

with open("jina_vectors.json", encoding='utf-8') as f:
    jina = json.load(f)

def average(list):
    print(f"getting vectors...")
    
    same = []
    different = []

    for i in range(len(list)):
        for j in range(i + 1, len(list)):
            result = cosine(list[i], list[j])
            if i // 10 == j // 10:
                same.append(result)
            else:
                different.append(result)
    
    return sum(same) / len(same), sum(different) / len(different)


print(average(gemini))
print(average(jina))
    
    

        
        