# Receipt Extractor

Turns messy receipt text into validated JSON using Gemini and Pydantic.

## Run
python extractor.py
python run_tests.py

## Accuracy (20 test cases)
Overall: 18/20 = 90%
- store: 94%
- date: 100%
- items: 94%
- total: 100%