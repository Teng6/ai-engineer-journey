import os, json, time
from dotenv import load_dotenv
from google import genai
from openai import OpenAI
from token_cost import get_usage_openrouter, get_usage, estimate_cost
from benchmark.prompts import PROMPTS

load_dotenv()

MODEL = {
    "gemini": "gemini-3.5-flash-lite",
    "gemma": "google/gemma-4-26b-a4b-it:free",
    "liquid": "liquid/lfm-3-1.7b:free",
}

def gemini(prompt):
    client = genai.Client()
    interaction = client.interactions.create(
        model = MODEL["gemini"],
        input = prompt,
    )
    reply = interaction.output_text
    usage = get_usage(interaction)

    return reply, usage

def openrouter(model_name, prompt):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    response = client.chat.completions.create(
        model=MODEL[model_name],
        messages = [{"role": "user", "content": prompt}],
    )
    reply = response.choices[0].message.content
    usage = get_usage_openrouter(response)
    
    return reply, usage

def call_model(name, prompt):
    for attempt in range(4):
        try:
            if name == "gemini":
                return gemini(prompt)
            return openrouter(name, prompt)
        except Exception as e:
            if "429" not in str(e) or attempt == 3:
                raise
            time.sleep(20)


def main():
    history = []
    for name in MODEL:
        for category, prompts in PROMPTS.items():
            for prompt in prompts:
                start = time.time()
                try:
                    reply, usage = call_model(name, prompt)
                except Exception as e:
                    reply, usage = f"ERROR: {e}", None
                seconds = round(time.time() - start, 2)
                history.append({
                    'model': name,
                    'category': category,
                    'input': prompt,
                    'answer': reply,
                    'usage': usage,
                    'cost': estimate_cost(usage, MODEL[name]) if usage else None
                })
                
                status = "FAIL" if usage == None else "ok"
                print(name, category, status, seconds, "s")
                time.sleep(13)
                with open("results.json", "w", encoding="utf-8") as f:
                    json.dump(history, f, indent=2, ensure_ascii=False)


main()
