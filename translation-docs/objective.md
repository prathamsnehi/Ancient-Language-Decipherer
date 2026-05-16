# Project Objective: "Voices of the Silent 99%"

## Hieroglyph Translation for Everyday Life Objects

### 1. Context & Scope

- **Academic Context:** HIST 111 (World History to 1500) Final Project.
- **Theme:** "The Stuff of Everyday Life." Moving away from "Great People" (Pharaohs) to the "Vast Majority" (common workers).
- **Core Challenge:** Translating "noisy" inscriptions from non-elite artifacts like Ostraca (pottery shards) and domestic tools, which current models struggle to recognize due to irregular backgrounds and cursive styles (Hieratic).
- **Deliverable Type:** A functional Python-based API/Model pipeline that outputs perceivable English, supported by a 3-page research paper.

### 2. Primary Technical Goal

Build a "Hybrid Translation Pipeline" that leverages existing Computer Vision (CV) for character recognition and a Large Language Model (LLM) for semantic smoothing and historical interpretation.

### 3. Implementation Roadmap (6-Day Sprint)

- **Base Framework:** James Piggott’s `Ancient-Language-Decipherer`.
- **Stage 1 (Vision):** Utilize the Piggott/Franken baseline to extract Gardiner Sign List IDs from images.
- **Stage 2 (Correction):** Implement a bypass/manual override for "noisy" artifacts where CV accuracy is low, ensuring the pipeline can proceed to translation.
- **Stage 3 (LLM Layer):** Create a prompt-engineering layer that sends Gardiner IDs + Historical Context to an LLM (Gemini/GPT) to produce readable English.
- **Stage 4 (API/Output):** Expose this as a simple API or local script that takes an image path and returns:
  1. Identified Gardiner Codes.
  2. Smoothed English Translation.
  3. "Everyday Life" Historical Insight.

### 4. The "Innovation" (Research Marketing Point)

While established models (Nasser et al. 2025) provide literal translations of formal monumental texts, this project introduces a **Contextual Semantic Layer (LLM)**. This layer is specifically tuned to "noisy" everyday artifacts, bridging the gap between raw symbol identification and human-readable stories for a non-expert audience.

### 5. Key File Operations for Editor

- **`image_processing.py`**: Refactor to handle high-contrast filtering for Ostraca images.
- **`translator_api.py`**: (New) Create a script to handle LLM API calls and prompt construction.
- **`main.py`**: The central execution script that coordinates the vision-to-language flow.

### 6. Reference Standards

- **Classification:** Gardiner Sign List.
- **Accuracy Benchmark:** Nasser et al. 2025 (BLEU 42.2).
- **History Citation:** Chicago Manual of Style.
