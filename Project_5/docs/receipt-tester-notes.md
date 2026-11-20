# Receipt Extractor Tester: Learning Notes

## How we're learning (read this first)

- **Goal:** rebuild a big test file (`run_tests.py`) from scratch, **one small step at a time**.
- **Rules:**
  - One step at a time. Do **not** dump everything at once.
  - Do **not** give the finished code. Give a **reference card**: the tool, what goes inside it, what it gives back, and the rules.
  - Anything that is code goes in a **code block**.
  - Skeletons with blanks are fine. The learner fills them in.
  - Test each piece **alone** with hand-typed data before connecting it.
  - If there's an error, paste it. Explain what it means without fixing it for them.
- **Current position: Step 5e** (sorting items so order doesn't matter).

---

## The big picture

The original program tests a receipt-reading AI.

1. **Load** test cases from `cases.json` (each has an `input` receipt and the `expected` answer).
2. **Generate**: run the AI on each case and save the results.
3. **Compare**: check each AI answer against the expected answer.
4. **Report**: print the score and write it to `results.md`.

A receipt has 4 fields: `store`, `date`, `items`, `total`.

---

## Roadmap

| Step | What you build | Status |
|---|---|---|
| 1 | Load `cases.json`, print count and first case | Done |
| 2 | Loop with `enumerate`, print store names | Done |
| 3 | Compare one field (store) in a function | Done |
| 4 | Compare date and total too | Done |
| 5a | Items: compare the **count** | Done |
| 5b | Items: compare **one item to one item** (`item_match`) | Done |
| 5c | Items: pair items with `zip` | Done |
| 5d | Items: one True/False for the whole list (`items_match`) | Done |
| **5e** | **Items: ignore the order (`sorted` + `key`)** | **In progress** |
| 6 | Combine the 4 checks into one `compare()` returning a dictionary; `all()` | Next |
| 7 | Loop over all cases and count passes (`+=`) | |
| 8 | Per-field accuracy and overall percentage | |
| 9 | Write results to `results.md` (`open(..., "w")`) | |
| 10 | Handle cases that should fail (`"UNKNOWN"` store), `if`/`else` | |
| 11 | Call the real AI and save outputs; `try`/`except`, `time.sleep` | |
| 12 | Wrap in `main()`; `if __name__ == "__main__"` | |

Steps 6 to 9 mostly reuse what's already learned. The real AI call (Step 11) comes last, so no API key is needed until then.

---

## Step 1: Load a JSON file

**Tools:**

- **`import json`**: loads the toolbox for JSON. Goes at the top, on its own line. No quotes.
- **`open("file.json", encoding="utf-8")`**: opens a file. 1st argument is the file name as **text** (quotes). `encoding="utf-8"` is a **keyword argument** (`name=value`) that sets the character set so symbols like `₱` don't break. Gives back a file object.
- **`with ... as f:`**: runs a block while the file is open, then closes it automatically. Ends with `:`. Lines that use the file are **indented** (4 spaces).
- **`json.load(f)`**: reads the open file and turns it into Python data (a list here). Must be **inside** the `with` block. Save the result in a variable.
- **`len(x)`**: counts items in a list. Gives back a number.
- **`print(x)`**: shows a value. Text needs quotes, variables don't.
- **`my_list[0]`**: first item. **Counting starts at 0.**

**The path matters:** the file name in `open()` is a path. If the file is in a folder, include it, e.g. `"tests/cases.json"`. If it's next to your `.py` file, the name alone is enough.

**Common errors:**

- `FileNotFoundError`: wrong name or folder.
- `JSONDecodeError`: typo in the JSON (missing comma or bracket). The error says which line.

---

## Step 2: Loop through cases

- **`for item in my_list:`**: repeats the indented block once per item. Ends with `:`.
- **`enumerate(my_list, 1)`**: gives you the **position number and the item** each round. The 2nd argument is the starting number (without it, counting starts at 0). Needs **two names** in the `for`, number first:

```python
for i, case in enumerate(my_list, 1):
    ...
```

- **Dictionary** (data stored as `key: value` pairs, like a contact card). Read a value with square brackets and the key as **text**: `case["expected"]`.
- **Nested dictionaries:** chain the brackets, each one goes one level deeper: `case["expected"]["store"]`.
- **f-strings:** put the letter `f` before the opening quote, then `{variable}` inside the text:

```python
print(f"{i}: {case['expected']['store']}")
```

- **Quotes inside an f-string:** if the f-string uses double quotes, use **single quotes** for the keys inside the braces. (Double inside double only works on Python 3.12+.)

**Style notes:**

- Use `is None` (not `== None`) to check for `None`.
- Name variables for what they hold: `case`, not `name`.
- `for i in range(len(entries))` with `entries[i]` works, but `enumerate` is shorter.

---

## Step 3: A function that compares one field

- **`def name(param1, param2):`** creates your own reusable tool. Ends with `:`, body is indented.
- **`return value`**: sends a value back and stops the function. Without it, the function gives back `None`.
- **`.strip()`**: removes spaces from the **start and end** of text (not the middle).
- **`.lower()`**: turns letters lowercase. Chain them: `text.strip().lower()`.
- **`==`** compares and gives `True`/`False`. **One `=`** stores a value, **two `==`** asks "are these equal?".
- **Call a function** with arguments in the same order as the parameters.
- Python reads top to bottom, so **define the function above where you call it**.

**The key design idea: machine vs. person**

| Job | Does what | Prints? |
|---|---|---|
| **The function** (the machine) | Takes inputs, **returns** a result | No |
| **The loop** (the person) | Feeds entries in, reads results, prints | Yes |

A function that **returns** is reusable. You can print it, count it, or save it later.

**Mistakes we found and fixed:**

- `cases["actual"]` on a **list** fails. Lists only open with **numbers**; text keys only work on dictionaries. Loop first so you get one dictionary per round.
- `sorted(a, b)` is wrong. `sorted()` takes **one** list.
- `zip` on text walks letter by letter. `zip` is for two **lists** (used later, in Step 5c).
- Missing `.strip().lower()` makes `"  JOLLIBEE "` and `"jollibee"` different.
- Passing `case["actual"]["store"]` (only the text) when the function expects the **whole dictionary** causes an error. Pass what the function expects.

---

## Step 4: Date and total

- **Date** is text like `"2026-03-02"`, so plain `==` is enough.
- **Total** is a **float** (decimal). Don't compare floats with `==`, because computers store decimals slightly inaccurately (`0.1 + 0.2 == 0.3` is `False`).
- **`abs(x)`**: removes the minus sign, so a gap is always positive.
- Compare the gap: `abs(a - b) < 0.01` means "within one centavo".
- **Direction matters:** `< 0.01` means "close enough", which is what we want. `> 0` means "different", which is backwards.

**Working version (the learner's):**

```python
def stores_match(actual, expected):
    return [
        actual["store"].strip().lower() == expected["store"].strip().lower(),
        actual["date"] == expected["date"],
        item_list(actual, expected),
        abs(actual["total"] - expected["total"]) < 0.01,
    ]
```

---

## Step 5: Items (the hardest field)

An item is a small dictionary. `items` is a **list of dictionaries**:

```json
"items": [{ "name": "Rice", "qty": 2, "price": 50.0 }]
```

A receipt can have 1, 3 or 10 items, and the AI might get the count or the order wrong.

### 5a: Compare the count

```python
def item_list(actual, expected):
    return len(actual["items"]) == len(expected["items"])
```

Note: `True if x else False` is redundant. The comparison already gives `True`/`False`, so `return` it directly.

### 5b: Compare one item to one item

- **`and`** joins conditions. The result is `True` only if **every** condition is `True`.

| Field | How | Why |
|---|---|---|
| `name` | strip + lower both sides, then `==` | AI may change spaces or capitals |
| `qty` | plain `==` | whole number |
| `price` | `abs(difference) < 0.01` | decimal |

**Working version (the learner's):**

```python
def item_match(actual, expected):
    return actual["name"].strip().lower() == expected["name"].strip().lower() and actual["qty"] == expected["qty"] and abs(actual["price"] - expected["price"]) < 0.01
```

Here `actual` and `expected` are **single item dictionaries**, so there's no `["items"]` and no `case`.

### 5c: Pair items with `zip`

**`zip(list1, list2)`** walks through two lists together, one item from each per round.

```python
for a, e in zip(["x", "y"], [1, 2]):
    print(a, e)
# x 1
# y 2
```

- Two names in the `for`, in the same order as the lists.
- It stops at the **shorter** list, so check the count first.
- Printing `a` and `e` shows whole dictionaries, which is expected (each is one item).

### 5d: One True/False for the whole list

- **`not`** flips `True`/`False`.
- **`!=`** means "not equal".
- **`return` inside a loop** ends the whole function immediately (early exit).
- **`return` after the loop** (same indent as `for`) only runs if the loop finished without returning early.

**Working version (the learner's):**

```python
def items_match(actual, expected):
    if len(actual["items"]) != len(expected["items"]):
        return False

    for a, e in zip(actual["items"], expected["items"]):
        if not item_match(a, e):
            return False

    return True
```

**Indentation lesson:** the final `return True` lines up with `for`, **not** inside it. Putting `return False` at the bottom made it run every time.

**Mistakes we found and fixed:**

- Mixing two jobs (comparing a pair and looping the list) in one function. Write the single-pair function first.
- Looping over a **dictionary** gives its **keys**, not items.
- Inside the loop, the loop variable is already one thing, so `case["actual"]["items"]` no longer exists.
- Opening a **list** with a text key like `a["name"]` fails. Only a dictionary (one item) works that way.

### 5e: Ignore the order (CURRENT STEP)

**Problem:** the AI might list the same items in a different order. These two receipts should count as a match, but the current `items_match` returns `False`:

```python
a = {"items": [{"name": "Rice", "qty": 2, "price": 50.0}, {"name": "Egg", "qty": 1, "price": 8.0}]}
e = {"items": [{"name": "Egg", "qty": 1, "price": 8.0}, {"name": "Rice", "qty": 2, "price": 50.0}]}

print(items_match(a, e))   # should become True
```

**Fix idea:** sort **both** lists the same way before pairing them.

**New tool: `sorted()`**

- Returns a **new** sorted list. The original is unchanged.
- 1st argument: the list.
- **`key=`** argument: tells it what to sort by. Without it, Python can't sort dictionaries.
- The key is a **small function** that takes one item and returns what to sort by.
- Write the function name **without parentheses** (`key=item_key`). You hand Python the function, and Python calls it on each item.

```python
def item_key(item):
    return ______        # the item's name, cleaned (strip + lower)

sorted(some_list, key=item_key)
```

**Your task:**

1. Write `item_key`.
2. In `items_match`, after the count check, sort both lists with `sorted(..., key=item_key)` and save them in new variables.
3. Change the `zip` to use the new sorted variables.

**Expected:** the test above prints `True`.

---

## Test data: `fake.json`

```json
[
  {
    "actual":   { "store": "  JOLLIBEE ", "date": "2026-03-01", "items": [{ "name": "Chickenjoy", "qty": 1, "price": 99.0 }], "total": 99.0 },
    "expected": { "store": "jollibee", "date": "2026-03-01", "items": [{ "name": "Chickenjoy", "qty": 1, "price": 99.0 }], "total": 99.0 }
  },
  {
    "actual":   { "store": "SM Supermarket", "date": "2026-03-02", "items": [{ "name": "Rice", "qty": 2, "price": 50.0 }], "total": 100.0 },
    "expected": { "store": "sm supermarket", "date": "2026-03-02", "items": [{ "name": "Rice", "qty": 2, "price": 50.0 }], "total": 100.0 }
  },
  {
    "actual":   { "store": "Mercury Drug", "date": "2026-03-03", "items": [{ "name": "Paracetamol", "qty": 1, "price": 5.0 }], "total": 5.0 },
    "expected": { "store": "Watsons", "date": "2026-03-03", "items": [{ "name": "Paracetamol", "qty": 1, "price": 5.0 }], "total": 5.0 }
  },
  {
    "actual":   { "store": "7-Eleven", "date": "2026-03-05", "items": [{ "name": "Coffee", "qty": 1, "price": 35.0 }], "total": 35.0 },
    "expected": { "store": "7-ELEVEN  ", "date": "2026-03-04", "items": [{ "name": "Coffee", "qty": 1, "price": 35.0 }], "total": 35.0 }
  }
]
```

**What each entry tests:**

- #1: store matches after strip + lower
- #2: store matches after lower
- #3: different stores
- #4: store matches, but the date is different (03-05 vs 03-04)

**Known weakness:** every entry has exactly 1 item, so the count check can never fail. Add entries with different counts and different orders to test items properly.

---

## Current full state of the learner's code

```python
import json


def item_list(actual, expected):
    return len(actual["items"]) == len(expected["items"])


def item_match(actual, expected):
    return actual["name"].strip().lower() == expected["name"].strip().lower() and actual["qty"] == expected["qty"] and abs(actual["price"] - expected["price"]) < 0.01


def items_match(actual, expected):
    if len(actual["items"]) != len(expected["items"]):
        return False

    for a, e in zip(actual["items"], expected["items"]):
        if not item_match(a, e):
            return False

    return True


def stores_match(actual, expected):
    return [
        actual["store"].strip().lower() == expected["store"].strip().lower(),
        actual["date"] == expected["date"],
        item_list(actual, expected),   # to be replaced by items_match after 5e
        abs(actual["total"] - expected["total"]) < 0.01,
    ]


with open("fake.json", encoding="utf-8") as f:
    entries = json.load(f)


for i, case in enumerate(entries, 1):
    print(f"Checked:{i} -> ", stores_match(case["actual"], case["expected"]))
```

---

## Quick glossary

| Term | Plain meaning |
|---|---|
| **import** | load a toolbox someone else wrote |
| **JSON** | a text format for lists and key-value data |
| **list** | an ordered group of things, opened with a **number** |
| **dictionary** | `key: value` pairs, opened with a **key** |
| **variable** | a name that holds a value |
| **function** | your own reusable tool (`def`) |
| **parameter** | a name for an input inside a function |
| **argument** | the actual value you pass when calling it |
| **keyword argument** | an argument written as `name=value` |
| **return** | send a value back out of a function |
| **float** | a decimal number |
| **indentation** | the spaces that show which lines belong inside a block |
| **early return** | `return` inside a loop to stop as soon as the answer is known |
