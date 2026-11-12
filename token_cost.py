PRICES = {
    "gemini-3.5-flash": {"input": 1.50, "output": 9.00},
    "gemini-2.5-flash": {"input": 0.30, "output": 2.50},
    "gemini-3.5-flash-lite": {"input": 0.30, "output": 2.50},
    "liquid/lfm-3-1.7b:free": {"input": 0.0, "output": 0.0},
    "openrouter/free": {"input": 0.0, "output": 0.0},
    "google/gemma-4-26b-a4b-it:free": {"input": 0.0, "output": 0.0},
}


def get_usage(interaction):
    u = interaction.usage
    return {
        "input": u.total_input_tokens,
        "output": u.total_output_tokens,
        "thinking": u.total_thought_tokens,
    }
    
def get_usage_openrouter(response):
    u = response.usage
    return {
        "input": u.prompt_tokens,
        "output": u.completion_tokens,
        "thinking": 0,
    }


def estimate_cost(usage, model):
    p = PRICES[model]
    billed_output = usage["output"] + usage["thinking"]
    return (usage["input"] * p["input"] + billed_output * p["output"]) / 1_000_000