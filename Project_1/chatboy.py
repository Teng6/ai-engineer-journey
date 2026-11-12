from dotenv import load_dotenv
from google import genai
from token_cost import get_usage, estimate_cost
import json, os
from datetime import datetime

load_dotenv()
client = genai.Client()
MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite"]
os.makedirs("chats", exist_ok=True)
chat_file = f"chats/chat_{datetime.now():%Y%m%d_%H%M%S}.json"
history = []

def save_history():
    with open(chat_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)



def main():
    
    model_name = MODELS[0]
    total_input = 0
    total_output = 0
    total_thought = 0
    total_cost = 0
    
    previous_id = None
    
    while True:
        user_input = input("You: ")
        
        if user_input.startswith("/model"):
            print("Pick a model(Number Only)")
            print(f"1. {MODELS[0]}")
            print(f"2. {MODELS[1]}")
            choice = input("Choice: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(MODELS):
                model_name = MODELS[int(choice) - 1]
                print(f"Switched to {model_name}")
            else:
                print(f"Invalid choice, staying on {model_name}")
            continue
        
        if user_input.lower() == "quit":
            break
        
        interaction = client.interactions.create(
            model=model_name,
            input=user_input,
            previous_interaction_id=previous_id,
        )
        
        usage = get_usage(interaction)
        cost = estimate_cost(usage, model_name)
        
        print("New ID: ", interaction.id)
        previous_id = interaction.id
        
        total_input += usage['input']
        total_output += usage['output']
        total_thought += usage['thinking']
        total_cost += cost
        print(f"Chatbot({usage['input']}): {interaction.output_text}")
        
        print("------MD------")
        print(f"input: [{user_input}]")
        print(f"reply: [{interaction.output_text}]")
        print(f"total input: {total_input:>6} | total output: {total_output:>6}")
        print()
        
        history.append({
            "user": user_input,
            "model": model_name,
            "reply": interaction.output_text,
            "input_tokens": usage['input'],
            "output_tokens": usage['output'],
            "cost": f"{cost:.6f}",
        })
        save_history()
    print("---END-------")
    print(f"{'in':>6} {'out':>6} {'think':>6} {'cost($)':>10}")
    print(f"{total_input:>6} {total_output:>6} {total_thought:>6} {total_cost:>10.6f}")

if __name__ == "__main__":
    main()
        