# Benchmark: Gemini vs Gemma vs Liquid

Same 10 prompts sent to each model. Quality is scored 1-5 by me.

## Quality scores (1-5)

| Category  | Gemini | Gemma | Liquid |
|-----------|--------|-------|--------|
| Factual   | 5      | 4     | 1      |
| Reasoning | 5      | 5     | 4      |
| Summarize | 5      | 5     | 4      |
| Writing   | 5      | 4     | 4      |
| Taglish   | 4      | 5     | 1      |
| Code      | 5      | 5     | 5      |
| Average   | 4.8    | 4.7   | 3.2    |

## Speed and cost

| Model  | Model ID                       | Avg seconds | Total cost |
|--------|--------------------------------|-------------|------------|
| Gemini | gemini-3.5-flash-lite          | 7.3         | ~$0.0045   |
| Gemma  | google/gemma-4-26b-a4b-it:free | 25.7        | $0         |
| Liquid | liquid/lfm-3-1.7b:free         | 3.9         | $0         |

Note: Gemma's seconds are inflated by 429 retry waits on the free tier.

## Notes

- Factual: Liquid invented details (a person and wrong distances).
- Taglish: Gemma sounded most natural. Liquid was garbled.
- Liquid used far more output tokens for the same answers.
- Code: all three correct.

## Verdict

- Gemini: best all-round, very cheap.
- Gemma: best free pick, best Taglish. Slow on the free tier.
- Liquid: fast but unreliable. Skip for facts and Taglish.
- Clip-finder: Gemma or Gemini for Taglish.