import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY missing in .env")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_insight(prompt: str) -> str:
    """
    Gemini 2.0 Flash using SYNC API.
    generate_content() is NOT async — must be called normally.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"LLM ERROR → {e}"