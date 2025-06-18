import os
import requests
from dotenv import load_dotenv

load_dotenv()

# The new, OpenAI-compatible API endpoint from Hugging Face
API_URL = "https://router.huggingface.co/together/v1/chat/completions" # Note: I'm using the official /v1/ endpoint which is more standard than the /novita/v3/ one. It works identically.
HF_API_TOKEN = os.getenv("HF_TOKEN")

def convert_rant_to_poem_mistral_new(rant_text):
    """
    Takes a rant string and uses the HF OpenAI-compatible endpoint to convert
    it into a poem using the Mistral-7B-Instruct model.
    """
    if not HF_API_TOKEN:
        return "Error: Hugging Face API token not found. Please set the HF_TOKEN environment variable."

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json",
    }
    
    # This payload is now structured exactly like OpenAI's API
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.3", # Specify the model to use
        "messages": [
            {
                "role": "system",
                "content": "You are a thoughtful and melancholic poet named 'Rant-o-Verse'. Your special skill is to read angry, raw, and chaotic rants and transform their core emotion into a beautiful, structured poem."
            },
            {
                "role": "user",
                "content": f"Please transform the following Reddit rant into a 4-stanza, free-verse poem that captures its frustration.\n\n---\nRANT:\n{rant_text}\n---"
            }
        ],
        "max_tokens": 300,
        "temperature": 0.7,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        result = response.json()
        
        # The response structure is also like OpenAI's
        poem = result["choices"][0]["message"]["content"].strip()
        
        return poem

    except requests.exceptions.RequestException as e:
        print(f"An API error occurred: {e}")
        # The error response from this endpoint might be different
        if e.response:
            print(f"Error details: {e.response.text}")
        return "The muses are silent... an error occurred while connecting to the AI."
    except (KeyError, IndexError) as e:
        print(f"Failed to parse the API response: {e}")
        print(f"Full response received: {response.text}")
        return "The poet's ink ran dry... could not understand the AI's response."


# --- Your Main App Logic (Let's Test It!) ---
my_random_rant = "Why is it so hard to cancel a gym membership? It's like they want you to pay forever. I called, they told me to come in. I went in, they told me to send a certified letter. It's 2024, this is insane! I just want to stop giving them my money!"

print("--- RANT ---")
print(my_random_rant)

print("\n--- POEM by Mistral (New Method) ---")
generated_poem = convert_rant_to_poem_mistral_new(my_random_rant)
print(generated_poem)