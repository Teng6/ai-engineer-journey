from dotenv import load_dotenv
from google import genai
from token_cost import get_usage, estimate_cost

load_dotenv()
client = genai.Client()
MODEL = "gemini-3.5-flash"

prompts = [
    "What is 2+2?",
    "Explain recursion",
    "Explain how a hash table works, including collisions, resizing, and time complexity",
]

print(f"{'prompt':<40} {'in':>6} {'out':>6} {'think':>6} {'cost($)':>10}")
for prompt in prompts:
    interaction = client.interactions.create(model=MODEL, input=prompt)
    usage = get_usage(interaction)
    cost = estimate_cost(usage, MODEL)
    print(f"{prompt[:38]:<40} {usage['input']:>6} {usage['output']:>6} {usage['thinking']:>6} {cost:>10.6f}")