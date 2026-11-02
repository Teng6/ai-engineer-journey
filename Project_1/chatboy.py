from dotenv import load_dotenv
from google import genai
from token_cost import get_usage, estimate_cost

load_dotenv()
client = genai.Client()
MODEL = "gemini-2.5-flash"


def main():
    
    total_input = 0
    total_output = 0
    total_thought = 0
    total_cost = 0
    
    previous_id = None
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "quit":
            break
        
        interaction = client.interactions.create(
            model=MODEL,
            input=user_input,
            previous_interaction_id=previous_id,
        )
        
        usage = get_usage(interaction)
        cost = estimate_cost(usage, MODEL)
        
        print("New ID: ", interaction.id)
        previous_id = interaction.id
        
        total_input += usage['input']
        total_output += usage['output']
        total_thought += usage['thinking']
        total_cost += cost
        print(f"Chatbot({usage['input']}): {interaction.output_text}")
    
    print(f"{'in':>6} {'out':>6} {'think':>6} {'cost($)':>10}")
    print(f"{total_input:>6} {total_output:>6} {total_thought:>6} {total_cost:>10.6f}")
if __name__ == "__main__":
    main()
        