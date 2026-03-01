import httpx
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from time import time

app = FastAPI()

# ================= CONFIG =================
CHATANYWHERE_URL = "https://api.chatanywhere.tech/v1/chat/completions"
CHATANYWHERE_API_KEY = "YOUR_CHATANYWHERE_API_KEY"

ACCESS_KEY = "dark"
OWNER_UID = "13577606265"

MAX_MEMORY = 10
RATE_LIMIT = 8
RATE_WINDOW = 60

# ================= TEMP MEMORY =================
user_memories = {}
rate_store = {}

# ================= SYSTEM PROMPT =================
SYSTEM_PROMPT = """
You are a smart and direct AI assistant.

Creator Information:
- Name: Riyan
- Country: Bangladesh
- Status: Class 10 Student
- Also does coding sometimes.

Privacy Rules:
- Only share basic public information about the creator.
- Never share exact location, school name, address, phone, or real-time activity.
- If asked about current activity, say you don’t have real-time access.
- Answer shortly.
- No unnecessary explanation.
- Be confident and natural.
"""

# ================= RATE LIMIT =================
def check_rate(uid):
    now = int(time())
    bucket = rate_store.get(uid, [])
    bucket = [t for t in bucket if t > now - RATE_WINDOW]

    if len(bucket) >= RATE_LIMIT:
        return False

    bucket.append(now)
    rate_store[uid] = bucket
    return True


# ================= HOME =================
@app.get("/")
def home():
    return {
        "status": True,
        "usage": "/api/ask?key=dark&uid=123&ask=hello"
    }


# ================= MAIN AI ROUTE =================
@app.get("/api/ask")
async def ask_ai(
    key: str = Query(...),
    uid: str = Query(...),
    ask: str = Query(...)
):

    if key != ACCESS_KEY:
        return JSONResponse(
            {"status": False, "error": "Invalid key"},
            status_code=403
        )

    if not check_rate(uid):
        return JSONResponse(
            {"status": False, "error": "Rate limit exceeded"},
            status_code=429
        )

    # Create memory for uid
    if uid not in user_memories:
        user_memories[uid] = []

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Owner special mode
    if uid == OWNER_UID:
        messages.append({
            "role": "system",
            "content": "The user is the creator Riyan. Give slightly more intelligent but still concise responses."
        })

    # Add memory
    for msg in user_memories[uid]:
        messages.append(msg)

    messages.append({"role": "user", "content": ask})

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 180
    }

    headers = {
        "Authorization": f"Bearer {CHATANYWHERE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.post(
                CHATANYWHERE_URL,
                headers=headers,
                json=payload
            )

        data = response.json()

        if "choices" not in data:
            return {"status": False, "error": data}

        answer = data["choices"][0]["message"]["content"].strip()

        # Save conversation
        user_memories[uid].append({"role": "user", "content": ask})
        user_memories[uid].append({"role": "assistant", "content": answer})

        # Keep last 10 messages only
        user_memories[uid] = user_memories[uid][-MAX_MEMORY:]

        return {
            "status": True,
            "uid": uid,
            "answer": answer
        }

    except Exception as e:
        return {"status": False, "error": str(e)}
