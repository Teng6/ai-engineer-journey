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

def extract(text: str) -> Receipt:
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
            print(name, "->", extract(text))
        except Exception as e:
            print(name, "->", "FAILED:", e)

