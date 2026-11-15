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


PROVIDERS = {
    "gemini": {
        "ask": ask_gemini,
        "models": ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-3.5-flash-lite"],
    },
    "openrouter": {
        "ask": ask_openrouter,
        "models": ["liquid/lfm-3-1.7b:free", "openrouter/free"],
    },
}

def pick_provider():
    provider_names = list(PROVIDERS)

    print("Pick a provider: (NUMBER ONLY)")
    for i, name in enumerate(provider_names, 1):
        print(f"{i}. {name}")
    
    choice = input("You: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(provider_names):
        return provider_names[int(choice) - 1]
    else:
        print(f"Invalid choice")
        return None

def pick_model(provider):
    model_names = list(PROVIDERS[provider]['models'])

    print("Pick a model: (NUMBER ONLY)")
    for i, name in enumerate(model_names, 1):
        print(f" {i}. {name}")

    choice = input("You: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(model_names):
        return model_names[int(choice) - 1]
    else: 
        print(f"In valid choice")
        return None


def main():
    
    provider = "gemini"
    model_name = "gemini-3.5-flash"
    
    while True:
        
        user_input = input("You: ")
        
        if user_input.strip() == "/models":
            new_provider = pick_provider()
            if new_provider == None:
                continue
            
            new_model = pick_model(new_provider):
            if new_model == None:
                continue
            
            provider = new_provider
            model_name = new_model
            print(f"Switched to {provider}/{model_name}")
            continue
        
        if user_input.strip().lower() == "/quit":
            break
        
        if provider == "gemini"
            