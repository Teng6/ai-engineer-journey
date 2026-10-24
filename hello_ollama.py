import ollama

response = ollama.chat(
    model="llama3.2:3b",
    messages=[{"role": "user", "content": input()}],
    options={"num_gpu": 0},
)

print(response["message"]["content"])
print("prompt tokens:", response["prompt_eval_count"])
print("output tokens:", response["eval_count"])