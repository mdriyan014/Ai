import os
import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

CHATANYWHERE_URL = "https://api.chatanywhere.tech/v1/chat/completions"
API_KEY = os.getenv("sk-9UxwxtCFHWALxd8TmiWuEhcl6usedDd464YRycIBYcgUireO")

@app.get("/")
def home():
    return {
        "status": True,
        "message": "AI API is running",
        "usage": "/api/ask?key=prince&ask=Hello"
    }

@app.get("/api/ask")
def ask_ai(
    key: str = Query(...),
    ask: str = Query(...)
):
    # simple access key
    if key != "prince":
        return JSONResponse(
            {"status": False, "error": "Invalid API key"},
            status_code=403
        )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": ask}
        ]
    }

    try:
        res = requests.post(
            CHATANYWHERE_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        data = res.json()

        if "choices" not in data:
            return JSONResponse(
                {"status": False, "error": data},
                status_code=500
            )

        answer = data["choices"][0]["message"]["content"]

        return {
            "status": True,
            "question": ask,
            "answer": answer,
            "provider": "chatanywhere.tech",
            "model": "gpt-3.5-turbo"
        }

    except Exception as e:
        return JSONResponse(
            {"status": False, "error": str(e)},
            status_code=500
          )
