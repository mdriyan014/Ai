import os
import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

# ChatAnywhere API config
CHATANYWHERE_URL = "https://api.chatanywhere.tech/v1/chat/completions"
CHATANYWHERE_API_KEY = os.getenv("CHATANYWHERE_API_KEY")  # ✅ CORRECT

# Home route (optional but helpful)
@app.get("/")
def home():
    return {
        "status": True,
        "message": "ChatAnywhere AI API is running",
        "usage": "/api/ask?key=prince&ask=Hello"
    }

# Main AI endpoint
@app.get("/api/ask")
def ask_ai(
    key: str = Query(..., description="API access key"),
    ask: str = Query(..., description="User question")
):
    # simple access protection
    if key != "prince":
        return JSONResponse(
            {"status": False, "error": "Invalid API key"},
            status_code=403
        )

    # check env variable
    if not CHATANYWHERE_API_KEY:
        return JSONResponse(
            {"status": False, "error": "CHATANYWHERE_API_KEY not set"},
            status_code=500
        )

    headers = {
        "Authorization": f"Bearer {CHATANYWHERE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": ask}
        ]
    }

    try:
        response = requests.post(
            CHATANYWHERE_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        data = response.json()

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
