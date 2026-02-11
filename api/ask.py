import os
import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

# ================= CONFIG =================

CHATANYWHERE_URL = "https://api.chatanywhere.tech/v1/chat/completions"

# 🔐 Vercel Environment Variable থেকে নেবে
CHATANYWHERE_API_KEY = os.getenv("CHATANYWHERE_API_KEY")

# আপনার local access key
LOCAL_ACCESS_KEY = "prince"

# =========================================


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
    # 🔐 Access key check
    if key != LOCAL_ACCESS_KEY:
        return JSONResponse(
            {"status": False, "error": "Invalid access key"},
            status_code=403
        )

    # 🔴 Check API key
    if not CHATANYWHERE_API_KEY:
        return JSONResponse(
            {"status": False, "error": "Server API key not configured"},
            status_code=500
        )

    headers = {
        "Authorization": f"Bearer {CHATANYWHERE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": ask}
        ],
        "temperature": 0.7
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

        return {
            "status": True,
            "question": ask,
            "answer": data["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return JSONResponse(
            {"status": False, "error": str(e)},
            status_code=500
    )
