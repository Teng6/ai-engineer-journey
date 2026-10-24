from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

interaction = client.interactions.create(
    model = "gemini-3.5-flash",
    input = "Why is it so hard for CS students to get a job nowadays? is it because of AI surge or is it more of a technical skill issue?"
)

u = interaction.usage

print("Answer:", interaction.output_text)
print()
print(f"Input Tokens: {u.total_input_tokens}")
print(f"Output Tokens: {u.total_output_tokens}")
print(f"Thought Tokens: {u.total_thought_tokens}")
print(f"Total Tokens: {u.total_tokens}")