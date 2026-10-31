PRICES = {
    "gemini-3.5-flash": {"input": 1.50, "output": 9.00}
}


def get_usage(interaction):
    u = interaction.usage
    return {
        "input": u.total_input_tokens,
        "output": u.total_output_tokens,
        "thinking": u.total_thought_tokens,
    }


def estimate_cost(usage, model):
    p = PRICES[model]
    billed_output = usage["output"] + usage["thinking"]
    return (usage["input"] * p["input"] + billed_output * p["output"]) / 1_000_000