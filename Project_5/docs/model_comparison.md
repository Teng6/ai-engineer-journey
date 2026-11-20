# Model Comparison

Collected 6 Nov 2026. Prices are USD per 1M tokens (standard tier). Figures come from provider pages as quoted by third-party trackers and guides, so confirm on each official pricing page before relying on them.

| Model | Provider | Closed/Open | Context length | Cut-off | Price in / out | Free tier | Strengths | Weaknesses |
|---|---|---|---|---|---|---|---|---|
| Gemini 3.6 Flash | Google | Closed | 1M tokens (65.5K max output) | Mar 2026 | $1.50 / $7.50 | Yes, rate-limited via AI Studio (no card); Google may use free-tier content to improve its products | Newest Flash; Google reports gains over 3.5 Flash on coding, computer use, knowledge work. Tested: correct 2-sentence summary and valid JSON | Priciest of the cheap tier; free tier not for private data; about 85% of output tokens were hidden thinking on a simple task |
| Gemini 3.5 Flash-Lite | Google | Closed | 1M tokens | Unknown (not confirmed) | $0.30 / $2.50 | Yes, rate-limited via AI Studio | Fast and cheap, built for high-volume work (not tested) | Weaker than Flash on hard tasks; cut-off not confirmed |
| Claude Haiku 5.5 | Anthropic | Closed | 1M tokens (128K max output) | Jun 2026 | From $0.10 / $0.50 (shorter prompts; higher rate for long prompts, not confirmed) | No ongoing free tier; small one-time credits for new API accounts | Built for classification, extraction, routing; cheap with a huge context (not tested) | Long prompts bill at a higher rate; no free API use |
| GPT-6 Luna | OpenAI | Closed | 1.05M tokens (128K max output) | May 2026 | $0.10 / $0.50 (prompts over 272K: $0.20 / $0.75 for the whole request) | Largely gone; $5 sign-up credit usually needs a card | Cheapest GPT-6 tier, strong for focused high-volume tasks (not tested) | No audio/video input; OpenAI points hardest work to Sol/Astra |
| llama3.2:3b (Ollama) | Meta | Open weights (Llama 3.2 Community License) | 128K native; Ollama defaults to 4,096 unless raised | Dec 2023 | $0 (runs on your machine, ~2.0 GB) | Free, no limits besides your hardware | Private, offline, no per-token cost | Oldest model; weak on complex reasoning; custom license, not fully open source. Test failed on my machine: output was random tokens after 469s |

Also tested (not in the table above): Gemini 3.5 Flash, $1.50 / $9.00, 1M context, cut-off Jan 2025, free tier via AI Studio.

## Test

One prompt, same for every model: summarize a short news paragraph in exactly 2 sentences, then extract people, dates and cost as JSON. Run twice via the Gemini API. Cost counts thinking tokens as output tokens.

| Model | Run | Seconds | Tokens in / out / thinking | Cost (USD) |
|---|---|---|---|---|
| Gemini 3.6 Flash | 1 | 10.9 | 99 / 149 / 964 | 0.0085 |
| Gemini 3.6 Flash | 2 | 10.2 | 99 / 152 / 853 | 0.0077 |
| Gemini 3.5 Flash | 1 | 9.8 | 99 / 144 / 923 | 0.0098 |
| Gemini 3.5 Flash | 2 | 39.5 | 99 / 155 / 835 | 0.0091 |
| llama3.2:3b | 1 | 469.5 | 114 / 1406 / n/a | $0 (output was garbage) |

- Both Gemini models gave exactly 2 sentences and identical, correct JSON on both runs.
- 3.6 Flash run 2 wrongly credited the Mayor with the parking review. 3.5 Flash phrasing was slightly awkward. Neither was clearly better.
- The 39.5s run for 3.5 Flash looks like server load, not the model (it took 9.8s the first time).
- Not tested: Gemini 3.5 Flash-Lite, Claude Haiku 5.5, GPT-6 Luna.
- llama3.2:3b produced random tokens from the first word, a broken run on this machine (likely a bad download or GPU/driver problem, not confirmed). It needs a retry.

## Verdict

- **Best overall (tested):** Gemini 3.6 Flash. Same quality as 3.5 Flash, newer, and about 15-20% cheaper per call in these runs.
- **Cheapest for bulk work:** Gemini 3.5 Flash-Lite ($0.30 / $2.50) on price alone. Untested, so confirm quality before relying on it. Claude Haiku 5.5 and GPT-6 Luna ($0.10 / $0.50) are cheaper on paper but also untested.
- **Best for reasoning:** not tested here. Gemini 3.6 Flash is the strongest tested option.
- **Best for local and private use:** no result yet. llama3.2:3b failed on this machine. Retry after re-pulling it, or try gemma3:4b or qwen3:4b.
- **Cost lever:** thinking tokens were about 85-87% of each call's output on a simple extraction. Lowering the thinking level matters more than switching models for bulk work.
