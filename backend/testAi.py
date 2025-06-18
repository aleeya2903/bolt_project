import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/together/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

response = query({
    "messages": [
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    "model": "mistralai/Mistral-7B-Instruct-v0.3"
})

print(response["choices"][0]["message"])