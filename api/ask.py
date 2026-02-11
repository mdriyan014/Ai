
import os
import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

CHATANYWHERE_URL = "https://api.chatanywhere.tech/v1/chat/completions"
CHATANYWHERE_API_KEY = os.getenv("sk-9UxwxtCFHWALxd8TmiWuEhcl6usedDd464YRycIBYcgUireO")

@app.get("/")
def home():
    return {
        "status": True,
        "message": "ChatAnywhere AI API is running",
        "usage": "/api/ask?key=prince&ask=Hello"
    }

@app.get("/api/ask")
def ask_ai(
    key: str = Query(...),
    ask: str = Query(...)
):
    if key != "prince":
        return JSONResponse({"status": False, "error": "Invalid API key"}, status_code=403)

    if not CHATANYWHERE_API_KEY:
        return JSONResponse({"status": False, "error": "CHATANYWHERE_API_KEY not set"}, status_code=500)

    headers = {
        "Authorization": f"Bearer {CHATANYWHERE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": ask}]
    }

    try:
        r = requests.post(CHATANYWHERE_URL, headers=headers, json=payload, timeout=30)
        data = r.json()

        if "choices" not in data:
            return JSONResponse({"status": False, "error": data}, status_code=500)

        return {
            "status": True,
            "question": ask,
            "answer": data["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return JSONResponse({"status": False, "error": str(e)}, status_code=500)
