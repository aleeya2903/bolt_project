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
        prompt = f"""Transform this rant into a beautiful 4-stanza free verse poem. Output ONLY the poem text with no introduction, explanation, or commentary.

RANT:
{rant_text}

Requirements:
- Exactly 4 stanzas
- Free verse style (no forced rhyme scheme)
- Capture the emotional essence and frustration
- Transform anger into poetic expression
- Use vivid imagery and metaphors
- Each stanza should be 2-4 lines

OUTPUT ONLY THE POEM - NO OTHER TEXT."""

        # Generate content using Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite-preview-06-17",
            contents=prompt
        )
        
        # Extract and clean the poem text
        poem = response.text.strip()
        
        # Remove any potential prefixes or suffixes that might still appear
        # Common phrases that AI might add despite instructions
        unwanted_prefixes = [
            "here's the poem:", "here is the poem:", "poem:", "here's a poem:",
            "here is a poem:", "the poem:", "this is the poem:", "here's your poem:",
            "here is your poem:", "your poem:", "the transformed poem:"
        ]
        
        unwanted_suffixes = [
            "this poem captures", "the poem reflects", "i hope this captures",
            "this transformation", "the verse above"
        ]
        
        # Clean up the poem text
        poem_lower = poem.lower()
        for prefix in unwanted_prefixes:
            if poem_lower.startswith(prefix):
                poem = poem[len(prefix):].strip()
                break
        
        # Remove any trailing explanatory text
        lines = poem.split('\n')
        cleaned_lines = []
        for line in lines:
            line_lower = line.lower().strip()
            # Stop if we hit explanatory text
            if any(suffix in line_lower for suffix in unwanted_suffixes):
                break
            if line.strip():  # Only add non-empty lines
                cleaned_lines.append(line)
        
        poem = '\n'.join(cleaned_lines).strip()
        
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