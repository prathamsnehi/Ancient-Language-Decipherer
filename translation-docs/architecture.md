# Architecture of the Hybrid Translation Pipeline

Welcome to the inner workings of the "Voices of the Silent 99%" project! This document explains the pipeline step-by-step, shedding light on the technologies used to turn a picture of ancient rock into a readable English story.

### Implementation Legend

To clarify the origins of this codebase:

- 🏛️ **Original Baseline:** Core components built previously by James Piggott / Morris Franken (Computer Vision & ML foundations).
- 🛠️ **Refactored:** Existing scripts that were heavily modernized or re-architected to support automation.
- ✨ **New Implementation:** Entirely new layers built specifically for the "Voices of the Silent 99%" project to bridge vision to readable language.

The pipeline is broken down into three major stages: **Computer Vision**, **Machine Learning**, and **Generative AI**.

---

## Stage 1: Image Processing & Orientation (Computer Vision + Vision API) \[🛠️ Refactored / ✨ New Implementation]

**File:** `src/image_processing.py` and `src/translator_api.py`**Technology:** OpenCV & Google Gemini Vision API
_(Originally an interactive click-and-drag tool, completely refactored to fully automated segmentation with AI-driven dynamic direction)._

Before a neural network can read a hieroglyph, the computer needs to isolate the symbols from the noisy background of the stone (the _ostracon_) and determine the correct reading direction.

1. **Dynamic Orientation Check:** Ancient Egyptian reading direction depends on the figures. We use Gemini 3.1 Vision to look at the uncropped image and determine which way the living figures are facing. If they face right (or if unknown), the text is read right-to-left. If left, it's left-to-right.
2. **Grayscale & Blurring:** We first remove color information (`cvtColor`) because hieroglyph shapes are defined by shadows and depth, not color. We then apply a **Gaussian Blur** to mathematically smooth out tiny specks of noise in the stone so they aren't mistaken for symbols.
3. **Adaptive Thresholding:** Instead of using a single global rule to decide what is "dark" (carving) and what is "light" (stone), adaptive thresholding calculates the lighting conditions in small local regions. This is crucial for ancient artifacts where lighting is often uneven. It outputs a stark black-and-white image where the glyphs pop out.
4. **Contour Detection:** The computer mathematically draws boundaries (`findContours`) around continuous shapes. We draw a "Bounding Box" around each shape.
5. **Sorting:** A custom algorithm sorts these bounding boxes dynamically based on the direction determined in Step 1, ensuring the symbols are ordered logically before being passed to the AI.

> **Learn More:**

---

## Stage 2: Symbol Classification (Machine Learning) \[🏛️ Original Baseline / 🛠️ Refactored]

**Files:** `src/inference_model.py` and `src/train_model.py`**Technology:** TensorFlow & Keras (Deep Learning Frameworks)
_(The core CNN and dataset are from the original baseline. inference_model.py was refactored to output actual Gardiner IDs and integrate with our new pipeline)._

Once we have a neatly cropped image of a single glyph, we need to identify what it is using a **Convolutional Neural Network (CNN)**.

1. **What is a CNN?** A CNN is an AI architecture inspired by the human visual cortex. It passes the image through various "filters" to detect edges, curves, and textures. As the image goes deeper into the network, it learns to recognize complex shapes (like a bird, a basket, or a snake).
2. **The Model (hieroglyph_model.keras):** This model was trained on thousands of labeled hieroglyph images. When it sees a new cropped image, it outputs a set of probabilities for 179 different classes.
3. **Argmax & Gardiner Codes:** We use a math function (`np.argmax`) to pick the class with the highest probability. The pipeline then maps this class to a **Gardiner Sign List ID** (e.g., `G43` for the quail chick, `N35` for water). Sir Alan Gardiner created this standard classification system in 1927.

> **Learn More:**

---

## Stage 3: The Semantic Translation (Generative AI) \[✨ New Implementation]

**File:** `src/translator_api.py`**Technology:** Google Gemini API (Large Language Models)
_(Entirely new module built to add a contextual semantic layer)._

We now have a sequence of Gardiner IDs (e.g., `M17 G43 X1 N35`), but that isn't a translation. Egyptian hieroglyphs are incredibly complex—they use _phonograms_ (sounds), _ideograms_ (literal objects), and _determinatives_ (silent symbols added to the end of words to specify meaning, like adding a "man" symbol to clarify a name).

To solve this without writing thousands of complex grammar rules, we use a Large Language Model (LLM).

1. **Prompt Engineering:** We send a highly specific prompt to Google's Gemini 2.5 Flash model. We don't just ask for a translation; we tell the AI to _act_ as an expert Egyptologist. We explicitly remind it about determinatives, honorific transpositions (writing a God's name first out of respect, but reading it last), and phonetic rules.
2. **Contextualization:** We ask the AI to translate the sequence specifically through the lens of "Everyday Life" to fit your HIST 111 project. It prevents the AI from assuming the text is a royal decree and instead roots the translation in commoner logs, worker rations, or letters.
3. **Structured Output (JSON):** We ask the AI to return the data in a strict `JSON` format so our Python script can reliably extract the literal translation, the smoothed English sentence, and the historical insight to print nicely in your terminal.

> **Learn More:**

---

## Stage 4: Pipeline Orchestration \[✨ New Implementation]

**File:** `src/main.py`**Technology:** Python
_(Rewritten completely from scratch to orchestrate the vision-to-language flow)._

This is the "glue" script. It handles the command-line interface, passes the image to Stage 1, feeds the results to Stage 2, pauses to let you manually override bad guesses, and finally queries Gemini in Stage 3 to print out the gorgeous final result!
