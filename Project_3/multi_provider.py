from dotenv import load_dotenv
from google import genai
from token_cost import get_usage, estimate_cost, get_usage_openrouter
import json, os
from datetime import datetime
from openai import OpenAI

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
        model=model_name,
        input=user_input,
        previous_interaction_id=previous_id,
    )
    
    reply = interaction.output_text
    usage = get_usage(interaction)
    id = interaction.id
    
    return reply, usage, id

def ask_openrouter(model_name, messages):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
    )
    
    reply = response.choices[0].message.content
    usage = get_usage_openrouter(response)
    
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
    
    print("Pick a provider (NUMBER ONLY):")
    for i, name in enumerate(provider_names, 1):
        print(f"{i}. {name}")
        
    choice = input("Your choice: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(provider_names):
        return provider_names[int(choice) - 1]
    else:
        print(f"Invalid choice")
        return None

def pick_model(provider):
    model_names = list(PROVIDERS[provider]["models"])
    
    print("Pick a model (NUMBER ONLY)")
    for i, model in enumerate(model_names, 1):
        print(f"{i}. {model}")
    
    choice = input("Your choice: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(model_names):
        return model_names[int(choice) - 1]
    else:
        print(f"Invalid choice")
        return None
   
def main():
    
    model_name = PROVIDERS["gemini"]["models"][0]
    provider = "gemini"
    total_input = 0
    total_output = 0
    total_thought = 0
    total_cost = 0
    
    previous_id = None
    messages = []
    
    while True:
        user_input = input("You: ")
        
        if user_input == "/models":
            new_provider = pick_provider()
            if new_provider is None:
                continue
            
            new_model = pick_model(new_provider)
            if new_model is None:
                continue
            
            provider = new_provider
            model_name = new_model
            print(f"Switched to {provider}/{model_name}")
            continue
                
        if user_input.lower() == "quit":
            break
        
        if provider == "gemini":
            reply, usage, previous_id = ask_gemini(model_name, user_input, previous_id)
        else:
            messages.append({"role": "user", "content": user_input})
            reply, usage, _ = ask_openrouter(model_name, messages)
            messages.append({"role": "assistant", "content": reply})
        
        print(f"AI: {reply}")
        total_input += usage["input"]
        total_output += usage["output"]
        total_thought += usage["thinking"]
        turn_cost = estimate_cost(usage, model_name)
        total_cost += turn_cost
        
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": reply, "model": model_name})
        save_history()
        print(f"[input {usage['input']:>6} | out {usage['output']:>6} | think {usage['thinking']:>6} | ${turn_cost:.6f}]")
    
    
    print(f"TOTAL:\n[input: {total_input:>6} |output: {total_output:>6} |thought: {total_thought:>6}]")
    print(f"TOTAL COST: ${total_cost:.6f}")
    
if __name__ == "__main__":
    main()