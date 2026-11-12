# API Compare

| | Gemini | OpenAI | Claude |
|---|---|---|---|
| What you send | `model`, `input` | `model`, `input` | `model`, `max_tokens`, `messages` |
| Where the reply text is | `output_text` | `output_text` | `content[0].text` |
| Where the token usage is | `total_input_tokens` and `total_output_tokens` | `usage.input_tokens` and `usage.output_tokens` | `usage.input_tokens` and `usage.output_tokens` |
