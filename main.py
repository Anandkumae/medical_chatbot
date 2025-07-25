import requests
import json

api_key = "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"
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "messages": [
        {"role": "system", "content": "You are a medical assistant giving general info only."},
        {"role": "user", "content": "What are the symptoms of malaria?"}
    ],
    "temperature": 0.7,
    "max_tokens": 500
}
response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.json()["choices"][0]["message"]["content"])
