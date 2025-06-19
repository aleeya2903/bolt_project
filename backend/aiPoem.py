import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Gemini AI configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def convert_rant_to_poem_gemini(rant_text):
    """
    Takes a rant string and uses the Gemini AI model to convert
    it into a poem.
    """
    if not GEMINI_API_KEY:
        return "Error: Gemini API key not found. Please set the GEMINI_API_KEY environment variable."

    try:
        # Initialize the Gemini client
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Create the prompt for poem generation
        prompt = f"""You are a thoughtful and melancholic poet named 'Rant-o-Verse'. Your special skill is to read angry, raw, and chaotic rants and transform their core emotion into a beautiful, structured poem.

Please transform the following Reddit rant into a 4-stanza, free-verse poem that captures its frustration while maintaining poetic beauty and structure.

---
RANT:
{rant_text}
---

Transform this into a poem that:
- Has 4 stanzas
- Uses free verse style
- Captures the emotional essence
- Maintains poetic flow and rhythm
- Transforms anger into artistic expression"""

        # Generate content using Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        
        # Extract and clean the poem text
        poem = response.text.strip()
        
        return poem

    except Exception as e:
        print(f"Gemini AI error occurred: {e}")
        return "The muses are silent... an error occurred while connecting to Gemini AI."


# Keep the old function name for backward compatibility
def convert_rant_to_poem_mistral_new(rant_text):
    """
    Backward compatibility function - now uses Gemini instead of Mistral
    """
    return convert_rant_to_poem_gemini(rant_text)


# --- Test the implementation ---
if __name__ == "__main__":
    my_random_rant = "Why is it so hard to cancel a gym membership? It's like they want you to pay forever. I called, they told me to come in. I went in, they told me to send a certified letter. It's 2024, this is insane! I just want to stop giving them my money!"

    print("--- RANT ---")
    print(my_random_rant)

    print("\n--- POEM by Gemini AI ---")
    generated_poem = convert_rant_to_poem_gemini(my_random_rant)
    print(generated_poem)