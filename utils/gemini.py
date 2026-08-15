import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "gemini-2.5-flash-lite"

def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません。.env ファイルを確認してください。")
    return genai.Client(api_key=api_key)

def generate(prompt: str, model: str = None) -> str:
    if model is None:
        model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    client = _get_client()
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text

def list_available_models() -> list[str]:
    client = _get_client()
    return sorted(
        m.name.removeprefix("models/")
        for m in client.models.list()
        if "generateContent" in (m.supported_actions or [])
    )
