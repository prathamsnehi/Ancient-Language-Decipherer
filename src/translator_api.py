import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

genai.configure(api_key=API_KEY)

# Use Gemini 3 Flash Preview as the default model
_model = genai.GenerativeModel('gemini-3-flash-preview')

def detect_reading_direction(image_path: str) -> str:
    """
    Uses Gemini Vision to analyze the figures in a hieroglyph image
    and determines whether they are facing 'left' or 'right'.
    Returns 'left', 'right', or 'unknown'.
    """
    try:
        sample_file = genai.upload_file(path=image_path)
        prompt = (
            "Look at the figures (e.g., people, animals, birds) in this ancient Egyptian hieroglyph image. "
            "Which direction are the living figures facing? "
            "Reply with exactly one word: 'left', 'right', or 'unknown'."
        )
        response = _model.generate_content([prompt, sample_file])
        
        # Clean up the file from the API storage
        genai.delete_file(sample_file.name)
        
        answer = response.text.strip().lower()
        if "left" in answer:
            return "left"
        elif "right" in answer:
            return "right"
        else:
            return "unknown"
            
    except Exception as e:
        print(f"Error detecting reading direction via Gemini: {e}")
        return "unknown"

def translate_gardiner_codes(gardiner_ids: list[str]) -> dict:
    """
    Takes a sequence of Gardiner IDs and uses Gemini to produce a contextualized translation
    and historical insights.
    Returns a dictionary with keys: 'literal_translation', 'smoothed_translation', 'historical_insight'.
    """
    if not gardiner_ids:
        return {
            "literal_translation": "",
            "smoothed_translation": "",
            "historical_insight": "No hieroglyphs were provided to translate."
        }
        
    sequence_str = " ".join(gardiner_ids)
    
    prompt = f"""
    You are an expert Egyptologist specializing in the translation of Middle Egyptian hieroglyphs, particularly those found on everyday artifacts like ostraca.
    
    I have extracted the following sequence of Gardiner Sign List IDs from an artifact:
    {sequence_str}
    
    Please provide a translation and analysis of this sequence. Keep in mind the following linguistic quirks of Egyptian hieroglyphs:
    1. Determinatives: Some signs are not pronounced but are placed at the end of a word to clarify its meaning.
    2. Phonograms vs Ideograms: Some signs represent sounds (uniliteral, biliteral, triliteral), while others are literal representations of objects.
    3. Contextual meaning: The translation should make sense in the context of "Everyday Life" of common workers, not just pharaohs or monumental decrees.
    4. Honorific transposition: If signs for gods or kings are present, they might be written first but read later.
    
    Analyze the sequence considering these rules and provide the output strictly as a valid JSON object with the following keys:
    - "literal_translation": A breakdown of the literal meaning of each sign or grouped word.
    - "smoothed_translation": A fluent, human-readable English translation of the entire sequence.
    - "summary": A brief, easy-to-understand summary explaining the gist of what this hieroglyphic text is trying to convey, avoiding any confusing or literal phrasing.
    - "historical_insight": A brief paragraph explaining the historical context of this phrase as it relates to the daily life of ancient Egyptian commoners or workers.
    
    Output ONLY the JSON object, with no markdown formatting blocks like ```json.
    """
    
    try:
        response = _model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up in case the LLM returned markdown blocks anyway
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        result = json.loads(response_text.strip())
        return result
    except Exception as e:
        print(f"Error during translation API call: {e}")
        return {
            "literal_translation": "Error calling translation API.",
            "smoothed_translation": "Error generating smoothed translation.",
            "summary": "Error generating summary.",
            "historical_insight": "An error occurred while analyzing the historical context."
        }

if __name__ == "__main__":
    # Quick test
    sample_ids = ["M17", "G43", "X1", "N35"] # Example sequence (ỉwtn)
    print(f"Translating: {sample_ids}")
    res = translate_gardiner_codes(sample_ids)
    print(json.dumps(res, indent=2))
