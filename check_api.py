import os
import sys
from google import genai
from dotenv import load_dotenv

load_dotenv()

def check(api_key: str):
    client = genai.Client(api_key=api_key)

    print("=== Available Models ===")
    try:
        models = list(client.models.list())
        for m in models:
            if hasattr(m, 'supported_actions') and m.supported_actions and "generateContent" in m.supported_actions:
                print(f"  {m.name}")
    except Exception as e:
        print(f"Model list error: {e}")
        return

    print("\n=== API Key Test ===")
    for model_id in ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-flash-lite-latest", "gemini-flash-latest", "gemini-2.0-flash-lite"]:
        try:
            resp = client.models.generate_content(model=model_id, contents="Say 'OK' only.")
            print(f"  [{model_id}] SUCCESS -> {resp.text.strip()}")
        except Exception as e:
            msg = str(e)
            if "429" in msg:
                limit_zero = "limit: 0" in msg
                print(f"  [{model_id}] 429 Quota error (limit=0: {limit_zero})")
            elif "404" in msg:
                print(f"  [{model_id}] 404 Model not found")
            elif "400" in msg:
                print(f"  [{model_id}] 400 Invalid API key")
            else:
                print(f"  [{model_id}] Error: {msg[:120]}")

if __name__ == "__main__":
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY が設定されていません。.env ファイルに GEMINI_API_KEY=... を記載してください。")
        sys.exit(1)
    check(api_key)
