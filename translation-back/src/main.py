import argparse
import sys
import os

from image_processing import segment_image
from inference_model import predict_image
from translator_api import translate_gardiner_codes, detect_reading_direction

def main():
    parser = argparse.ArgumentParser(description="Hybrid Translation Pipeline for Ancient Hieroglyphs")
    parser.add_argument("--image", type=str, help="Path to the pre-cropped hieroglyph image.", required=True)
    args = parser.parse_args()

    image_path = args.image
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        sys.exit(1)

    print(f"--- Stage 1: Vision (Processing {image_path}) ---")
    
    print("Determining reading direction using Gemini Vision...")
    face_direction = detect_reading_direction(image_path)
    print(f"Detected figure orientation: {face_direction}")
    
    if face_direction == "left":
        reading_direction = "ltr"
    else:
        # If right or unknown, default to rtl
        reading_direction = "rtl"
        
    print(f"Setting segmentation reading direction to: {reading_direction.upper()}")
    
    try:
        segments = segment_image(image_path, direction=reading_direction)
        print(f"Found {len(segments)} distinct glyph segments.")
    except Exception as e:
        print(f"Image processing failed: {e}")
        sys.exit(1)

    predicted_ids = []
    for i, segment in enumerate(segments):
        try:
            g_id = predict_image(segment)
            predicted_ids.append(g_id)
            print(f"  Segment {i+1}: Predicted {g_id}")
        except Exception as e:
            print(f"  Segment {i+1}: Prediction failed ({e})")
            predicted_ids.append("UNKNOWN")

    print("\n--- Stage 2: Correction ---")
    predicted_seq = " ".join(predicted_ids)
    print(f"Extracted Sequence: {predicted_seq}")
    override = input("Press Enter to accept this sequence, or type a space-separated sequence of Gardiner IDs to override: ").strip()
    
    if override:
        final_ids = override.split()
        print(f"Using Manual Override: {' '.join(final_ids)}")
    else:
        final_ids = predicted_ids
        print("Using Extracted Sequence.")

    print("\n--- Stage 3: LLM Translation ---")
    print("Consulting Gemini Expert...")
    result = translate_gardiner_codes(final_ids)

    print("\n================ FINAL TRANSLATION ================")
    print(f"Codes: {' '.join(final_ids)}\n")
    print(f"Literal Translation:\n{result.get('literal_translation', 'N/A')}\n")
    print(f"Smoothed English:\n{result.get('smoothed_translation', 'N/A')}\n")
    print(f"Summary (The Gist):\n{result.get('summary', 'N/A')}\n")
    print(f"Historical Insight (Everyday Life):\n{result.get('historical_insight', 'N/A')}")
    print("===================================================\n")

if __name__ == "__main__":
    main()
