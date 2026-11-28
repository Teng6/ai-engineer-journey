from AskMyDocs.rag_prompt import build_message, SYSTEM_PROMPT, format_sources
from dotenv import load_dotenv
from google import genai

load_dotenv()

fake_chunks = [
    {
        "id": "math.md-0",
        "text": "To find the area of a rectangle, multiply length by width. Example: length 5, width 3, area is 15.",
        "file": "math.md",
        "location": "Rectangle",
    }
]


question = "What do I multiply the length by?"
message = build_message(question, fake_chunks)

def gemini(system_prompt, message):
    client = genai.Client()
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=message,
        system_instruction=system_prompt,
    )
    result = interaction.output_text
    
    return result

result = gemini(SYSTEM_PROMPT, message)
