import os
import sys
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Add the src folder to the Python path so we can import our pipeline modules
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)
src_dir = os.path.join(project_root, "src")
sys.path.append(src_dir)

# Now we can import the pipeline logic
from image_processing import segment_image
from inference_model import predict_image
from translator_api import translate_gardiner_codes, detect_reading_direction

app = FastAPI(title="Hieroglyph Translation API", description="API for Translating Ancient Egyptian Hieroglyphs")

# Setup CORS for future frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = os.path.join(backend_dir, "temp_uploads")
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/api/translate")
async def translate_endpoint(image: UploadFile = File(...)):
    if not image.filename:
        raise HTTPException(status_code=400, detail="No selected file")
        
    temp_file_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_{image.filename}")
    
    try:
        # Save uploaded image temporarily to disk
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
        # --- Stage 1: Vision (Multimodal & Segmentation) ---
        face_direction = detect_reading_direction(temp_file_path)
        reading_direction = "ltr" if face_direction == "left" else "rtl"
        
        segments = segment_image(temp_file_path, direction=reading_direction)
        
        if not segments:
            raise HTTPException(status_code=400, detail="No hieroglyphs could be detected in the image.")
            
        # --- Stage 2: ML Inference (CNN) ---
        final_ids = []
        for seg in segments:
            predicted_id = predict_image(seg)
            final_ids.append(predicted_id)
            
        # --- Stage 3: LLM Contextual Translation ---
        # Gemini handles concurrency seamlessly on PAYG tiers
        translation_result = translate_gardiner_codes(final_ids)
        
        # Extract and format the specific fields requested
        response_data = {
            "literal_translation": translation_result.get("literal_translation", "N/A"),
            "summary": translation_result.get("summary", "N/A"),
            "historical_insight": translation_result.get("historical_insight", "N/A")
        }
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Always clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
