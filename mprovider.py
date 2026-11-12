from dotenv import load_dotenv
from google import genai
from openai import OpenAI
from token_cost_copy import get_gemini_usage, get_openrouter_usage, estimate_cost
from datetime import datetime
import json, os

load_dotenv()

os.makedirs("chats", exist_ok=True)
chat_file = f"chats/chat_{datetime.now():%Y%m%d_%H%M%S}.json"
history = []

def save_history():
    with open(chat_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def ask_gemini(model_name, user_input, previous_id):
    client = genai.Client()
    interaction = client.interactions.create(
        model = model_name,
        input = user_input,
        previous_interaction_id = previous_id,
    )
    
    reply = interaction.output_text
    usage = get_gemini_usage(interaction)
    id = interaction.id
    
    return reply, usage, id

def ask_openrouter(model_name, messages):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
    )
    
    reply = response.choices[0].message.content
    usage = get_openrouter_usage(response)
    
    return reply, usage, None

