# Receipt extractor: learning notes

Use this file to continue in a new chat. Paste it in and say "continue with the generate block."

## How I want to be taught
- Go block by block, line by line, argument by argument. Do not dump everything at once.
- Explain why each line exists and why alternatives aren't used.
- Plain language, define every term. I get lost easily with jargon.
- After each block, quiz me (4 choices, non-obvious answers).

## What the project is
Two files in the same folder:
- `extractor.py`: sends messy receipt text to Gemini and gets back clean structured data (a `Receipt`).
- Test runner (first file, name not given): runs test cases through the extractor and scores the accuracy.
- Also needed: `cases.json` (test cases with `input` and `expected`), a `tests/` folder, and a `.env` file with the API key.

## extractor.py (finished, I understand it)
- Pydantic models `Item` (name, qty, price per single unit) and `Receipt` (store, optional date, items, total) are the blueprint. `Field(description=...)` gives instructions to the AI.
- `Receipt.model_json_schema()` turns the blueprint into JSON that is sent as `response_format`, so Gemini answers in matching JSON.
- `extract_with_retry` loops up to `MAX_ATTEMPTS = 2`.
  - `model_validate_json(raw)` checks the answer. On `ValidationError`, `except` saves the error, builds a new prompt with the bad answer and the error, then `continue` goes to the next attempt.
  - If valid: checks `store == "UNKNOWN"`, which raises a `ValueError` because it was not a receipt (no retry). Otherwise `return receipt`, which sits inside the loop, so a first-try success ends the function right there.
  - If both attempts fail, the final `raise ValueError(...)` after the loop runs.
- `load_dotenv()` reads `.env` into environment variables so the API key never appears in code. `genai.Client()` finds the key automatically. A `.env` file is not the same as a virtual environment. Add `.env` to `.gitignore`.
- `if __name__ == "__main__":` only runs when the file is run directly, not when it is imported.

## Test runner: progress

### Block 1 (DONE, quiz 10/11)
```python
import json, os, time
from extractor import extract_with_retry

OUT = "tests/outputs.json"
FIELDS = ["store", "date", "items", "total"]
```
- `json`: saves and loads the results file. `os`: `os.path.exists(OUT)` checks if the file exists. `time`: `time.sleep(13)` pauses.
- Commas in `import json, os, time` are just shorthand for three import lines.
- `from extractor import ...`: `extractor` is my own file `extractor.py` (same folder). Importing runs that file's top-level code, which is why `load_dotenv()` runs even though the runner never calls it.
- `OUT`: ALL CAPS is a "constant" habit (not enforced by Python). It lives in a variable so the path is changed in one place instead of three. The `tests/` folder must already exist or saving errors.
- `FIELDS`: only used by the runner's scoring loops so the four names aren't retyped. It has nothing to do with Pydantic or Gemini (the one I got wrong).

### Remaining blocks (TODO, in this order)
1. `generate(cases)`: the loop, `enumerate`, the three try/except branches (ok, clean_fail, crash), `model_dump(mode="json")`, `time.sleep(13)`, writing `outputs.json`.
2. `items_match(actual, expected)`: length check, `key` lambda, `sorted`, `zip`, tolerance `abs(...) >= 0.01`.
3. `compare(actual, expected)`: per-field True/False.
4. `main()`: loading cases and the cache (`os.path.exists`), `should_fail`, per-case scoring, `field_right` / `field_total`, printing, writing `results.md`.
5. `if __name__ == "__main__": main()`.

## Where I got lost / things to re-explain if needed
- `generate` is the part that confused me most. Start slow there.

---

## Appendix: full code

### Test runner

```python
import json, os, time
from extractor import extract_with_retry

OUT = "tests/outputs.json"
FIELDS = ["store", "date", "items", "total"]


def generate(cases):
    outputs = []
    for i, case in enumerate(cases, 1):
        try:
            result = extract_with_retry(case["input"]).model_dump(mode="json")
            outputs.append({"n": i, "status": "ok", "result": result})
        except ValueError as e:
            outputs.append({"n": i, "status": "clean_fail", "result": None, "error": str(e)})
        except Exception as e:
            outputs.append({"n": i, "status": "crash", "result": None, "error": str(e)})
        print(f"called #{i}: {outputs[-1]['status']}")
        time.sleep(13)  
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(outputs, f, indent=2, ensure_ascii=False)
    return outputs


def items_match(actual, expected):
    if len(actual) != len(expected):
        return False
    key = lambda it: it["name"].strip().lower()
    for a, e in zip(sorted(actual, key=key), sorted(expected, key=key)):
        if key(a) != key(e) or a["qty"] != e["qty"] or abs(a["price"] - e["price"]) >= 0.01:
            return False
    return True


def compare(actual, expected):
    return {
        "store": actual["store"].strip().lower() == expected["store"].strip().lower(),
        "date": actual["date"] == expected["date"],
        "items": items_match(actual["items"], expected["items"]),
        "total": abs(actual["total"] - expected["total"]) < 0.01,
    }


def main():
    with open("cases.json", encoding="utf-8") as f:
        cases = json.load(f)

    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            outputs = json.load(f)
        print("Loaded saved outputs (no API calls)")
    else:
        outputs = generate(cases)

    passed_count = 0
    field_right = {k: 0 for k in FIELDS}
    field_total = 0  
    lines = []

    for case, out in zip(cases, outputs):
        n = out["n"]
        expected = case["expected"]
        should_fail = expected["store"] == "UNKNOWN"

        if should_fail:
            passed = out["status"] == "clean_fail"
            detail = "" if passed else f"  ({out['status']})"
        else:
            field_total += 1
            if out["status"] == "ok":
                fields = compare(out["result"], expected)
            else:
                fields = {k: False for k in FIELDS}
            for k in FIELDS:
                field_right[k] += fields[k]
            passed = all(fields.values())
            wrong = [k for k, v in fields.items() if not v]
            detail = "" if passed else f"  wrong: {', '.join(wrong)}" + (
                f" [{out['status']}]" if out["status"] != "ok" else "")

        passed_count += passed
        lines.append(f"#{n:02d} {'PASS' if passed else 'FAIL'}{detail}")

    print("\n".join(lines))
    overall = passed_count / len(cases) * 100
    print(f"\nOverall: {passed_count}/{len(cases)} = {overall:.0f}%")
    print("Per-field accuracy (on non-failure cases):")
    for k in FIELDS:
        print(f"  {k}: {field_right[k]}/{field_total} = {field_right[k] / field_total * 100:.0f}%")

    # Step 6: baseline
    with open("results.md", "w", encoding="utf-8") as f:
        f.write("# Baseline\n\n")
        f.write(f"Overall: {passed_count}/{len(cases)} = {overall:.0f}%\n\n")
        for k in FIELDS:
            f.write(f"- {k}: {field_right[k] / field_total * 100:.0f}%\n")
        f.write("\n```\n" + "\n".join(lines) + "\n```\n")


if __name__ == "__main__":
    main()
```

### extractor.py

```python
from google import genai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from datetime import date
from dotenv import load_dotenv

load_dotenv()
MAX_ATTEMPTS = 2
client = genai.Client()

class Item(BaseModel):
    name: str = Field(description="Product name in Title Case, with obvious typos corrected")
    qty: int
    price: float = Field(description="Price per single unit")
    
class Receipt(BaseModel):
    store: str = Field(description='Store name. Use "UNKNOWN" if the text is not a receipt')
    date: Optional[date]
    items: List[Item]
    total: float

def extract_with_retry(text: str) -> Receipt:
    prompt = f"Extract the receipt data. Fix obvious typos and use proper capitalization:\n{text}"
    last_error = None
    
    for attempt in range(1, MAX_ATTEMPTS + 1):
        interaction = client.interactions.create(
            model = "gemini-2.5-flash",
            input=prompt,
            response_format={
                "type":"text",
                "mime_type":"application/json",
                "schema":Receipt.model_json_schema(),
            },
        )
        raw = interaction.output_text
        
        try:
            receipt = Receipt.model_validate_json(raw)
        except ValidationError as e:
            last_error = e
            prompt = (
                f"Extract the receipt data from the text below.\n"
                f"Your previous answer was invalid.\n"
                f"Previous answer: {raw}\n"
                f"Error: {e}\n"
                f"Fix it and return valid JSON.\n\n"
                f"Text:\n {text}"
            )
            continue
        
        if receipt.store == "UNKNOWN":
            raise ValueError("No receipt found in the text")
        return receipt
    
    raise ValueError(f"Failed after {MAX_ATTEMPTS} attempts. Last error: {last_error}")



if __name__ == "__main__":
    tests = {
        "messy_1": "walmrt 3/11/26\napples 4 @0.50\nmilk 1 3.20\ntotal 5.20",
        "messy_2": "CAFE LUNA | Nov 2 2026\n2 latte 4.5 each\n1 muffin 3\nTotal: 12.00",
        "no_receipt": "hey are we still on for dinner tomorrow? i'll bring the dessert",
    }
    for name, text in tests.items():
        try:
            print(name, "->", extract_with_retry(text))
        except Exception as e:
            print(name, "->", "FAILED:", e)
```
