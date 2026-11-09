import json, os, time
from Project_2.extractor import extract

OUT = "tests/outputs.json"
CASES = "tests/cases.json"
FIELDS = ["store", "date", "items", "total"]
os.makedirs("tests", exist_ok=True)

def generate(cases):
    outputs = []

    for i, case in enumerate(cases, 1):
        try:
            result = extract(case["input"]).model_dump(mode="json")
            outputs.append({"n": i, "status": "ok", "result": result})
        except ValueError as e:
            outputs.append({"n": i, "status": "clean_fail", "result": None, "error": str(e)})
        except Exception as e:
            outputs.append({"n": i, "status": "crash", "result": None, "error": str(e)})
        
        print(f"Case: {i} -> {outputs[-1]["status"]}")
        time.sleep(13)
        
    with open(OUT, "w", encoding="utf-8") as f:
       json.dump(outputs, f, indent=2, ensure_ascii=False)
    
    return outputs
    

def items_match(actual, expected):
    if len(actual) != len(expected):
        return False
    
    key = lambda it: it['name'].strip().lower()
    
    for a, e in zip(sorted(actual, key=key), sorted(expected, key=key)):
        if key(a) != key(e) or a["qty"] != e['qty'] or abs(a['price'] - e['price']) >= 0.01:
            return False
    
    return True


def compare(actual, expected):
    return {
        'store': actual["store"].strip().lower() == expected["store"].strip().lower(),
        'date': actual['date'] == expected['date'],
        'items': items_match(actual['items'], expected['items']),
        'total': abs(actual['total'] - expected['total']) < 0.01,
    }
    
    
def main():
    with open(CASES, encoding="utf-8") as f:
        cases = json.load(f)
        
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            outputs = json.load(f)
        print(f"loaded saved outputs (no API calls)")
    else:
        outputs = generate(cases)
    
    passed_count = 0
    field_right = {k: 0 for k in FIELDS}
    field_total = 0
    lines = []
    
    
    for case, out in zip(cases, outputs):
        n = out['n']
        expected = case['expected']
        should_fail = expected is None or expected['store'] == "UNKNOWN"
        
        if should_fail:
            passed = out['status'] == 'clean_fail'
            detail = "" if passed else out['status']
        else:
            field_total += 1
            if out['status'] == "ok":
                fields = compare(out['result'], expected)
            else:
                fields = {k: False for k in FIELDS}
            for k in FIELDS:
                field_right[k] += fields[k]

            passed = all(fields.values())
            wrong = [k for k, v in fields.items() if not v]
            detail = "" if passed else f" wrong: {', '.join(wrong)}"
        
        passed_count += passed
        lines.append(f"#{n:02d} {'PASS' if passed else 'FAIL'}{detail}")        
    
    print("\n".join(lines))
    overall = passed_count / len(cases) * 100
    print(f"\nOverall: {passed_count}/{len(cases)} = {overall:.0f}%")
    print("Per-field accuracy (non-failure cases):")
    
    for k in FIELDS:
        print(f"  {k}: {field_right[k]}/{field_total} = {field_right[k] / field_total * 100:.0f}%")
    
    with open("results.md", "w", encoding="utf-8") as f:
        f.write("# Baseline\n\n")
        f.write(f"Overall: {passed_count}/{len(cases)} = {overall:.0f}%\n")
        for k in FIELDS:
            f.write(f"- {k}: {field_right[k] / field_total * 100:.0f}%\n")
        f.write("\n---\n" + "\n".join(lines) + "\n---\n")

if __name__ == "__main__":
    main()
        