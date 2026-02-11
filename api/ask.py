import os
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("sk-9UxwxtCFHWALxd8TmiWuEhcl6usedDd464YRycIBYcgUireO"))

@app.get("/api/ask")
def ask_ai(
    key: str = Query(..., description="API access key"),
    ask: str = Query(..., description="User question")
):
    if key != "prince":
        return JSONResponse(
            {"status": False, "error": "Invalid API key"},
            status_code=403
        )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": ask}]
        )

        return {
            "status": True,
            "question": ask,
            "answer": completion.choices[0].message.content,
            "model": "gpt-4o-mini"
        }

    except Exception as e:
        return JSONResponse(
            {"status": False, "error": str(e)},
            status_code=500
        )
