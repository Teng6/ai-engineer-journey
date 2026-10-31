from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="Write a one-line tagline for filipino market simulator game",
)

