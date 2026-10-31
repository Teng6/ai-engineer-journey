import os
import re
import time
import random

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("GEMINI_API_KEY missing. Add it to your .env file.")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash"
RETRYABLE = {429, 500, 502, 503, 504}


def get_status(e):
    """Find the HTTP status code on an error, falling back to the message text."""
    for attr in ("code", "status_code", "status"):
        val = getattr(e, attr, None)
        if isinstance(val, int):
            return val
    m = re.search(r"Error code: (\d{3})", str(e))
    return int(m.group(1)) if m else None


def call_with_retry(fn, max_retries=5):
    """Retry transient errors with exponential backoff + jitter."""
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            code = get_status(e)
            retryable = code in RETRYABLE or code is None  # None = network/timeout
            if not retryable or attempt == max_retries - 1:
                raise
            wait = (2 ** attempt) + random.random()
            if code == 429:
                print(f"Rate limited (429). Waiting {wait:.1f}s...")
            else:
                print(f"ERROR {code}: {e}. Retrying in {wait:.1f}s...")
            time.sleep(wait)


def ask(prompt, temperature=0.7):
    stream = call_with_retry(lambda: client.interactions.create(
        model=MODEL,
        input=prompt,
        stream=True,
        generation_config={"temperature": temperature},
    ))
    for event in stream:
        if event.event_type == "step.delta" and event.delta.type == "text":
            print(event.delta.text, end="", flush=True)
    print()


if __name__ == "__main__":
    ask("Explain how AI works in 3 sentences.")