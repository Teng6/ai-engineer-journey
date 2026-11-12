import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(api_key=os.getenv("HF_TOKEN"))

result = client.text_classification(
    "What is recursion?",
    model="convaiinnovations/laya",
)

print(result)