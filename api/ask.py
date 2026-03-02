import json
import requests

CHATANYWHERE_API_KEY = "YOUR_CHATANYWHERE_API_KEY"
ACCESS_KEY = "dark"
MODEL = "gpt-3.5-turbo"
API_URL = "https://api.chatanywhere.tech/v1/chat/completions"

def handler(request):

    key = request.args.get("key")
    question = request.args.get("ask")

    if key != ACCESS_KEY:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Invalid API key"})
        }

    if not question:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No question provided"})
        }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {CHATANYWHERE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            return {
                "statusCode": response.status_code,
                "body": json.dumps({"error": response.text})
            }

        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "question": question,
                "answer": reply
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
