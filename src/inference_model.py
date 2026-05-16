import os
import numpy as np
import tensorflow as tf
import cv2

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'hieroglyph_model.keras')
DATASET_PATH = os.path.join(os.path.dirname(__file__), '../data/converteddataset')

_model = None
_class_names = []

def _load_model_and_classes():
    global _model, _class_names
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(f"Model file not found at {MODEL_PATH}. Please run train_model.py first.")
        
        _model = tf.keras.models.load_model(MODEL_PATH)
        
        _class_names = ['A55', 'Aa15', 'Aa26', 'Aa27', 'Aa28', 'D1', 'D10', 'D156', 'D19', 'D2', 'D21', 'D28', 'D34', 'D35', 'D36', 'D39', 'D4', 'D46', 'D52', 'D53', 'D54', 'D56', 'D58', 'D60', 'D62', 'E1', 'E17', 'E23', 'E34', 'E9', 'F12', 'F13', 'F16', 'F18', 'F21', 'F22', 'F23', 'F26', 'F29', 'F30', 'F31', 'F32', 'F34', 'F35', 'F4', 'F40', 'F9', 'G1', 'G10', 'G14', 'G17', 'G21', 'G25', 'G26', 'G29', 'G35', 'G36', 'G37', 'G39', 'G4', 'G40', 'G43', 'G5', 'G50', 'G7', 'H6', 'I10', 'I5', 'I9', 'L1', 'M1', 'M12', 'M16', 'M17', 'M18', 'M195', 'M20', 'M23', 'M26', 'M29', 'M3', 'M4', 'M40', 'M41', 'M42', 'M44', 'M8', 'N1', 'N14', 'N16', 'N17', 'N18', 'N19', 'N2', 'N24', 'N25', 'N26', 'N29', 'N30', 'N31', 'N35', 'N36', 'N37', 'N41', 'N5', 'O1', 'O11', 'O28', 'O29', 'O31', 'O34', 'O4', 'O49', 'O50', 'O51', 'P1', 'P13', 'P6', 'P8', 'P98', 'Q1', 'Q3', 'Q7', 'R4', 'R8', 'S24', 'S28', 'S29', 'S34', 'S42', 'T14', 'T20', 'T21', 'T22', 'T28', 'T30', 'U1', 'U15', 'U28', 'U33', 'U35', 'U7', 'UNKNOWN', 'V13', 'V16', 'V22', 'V24', 'V25', 'V28', 'V30', 'V31', 'V4', 'V6', 'V7', 'W11', 'W14', 'W15', 'W18', 'W19', 'W22', 'W24', 'W25', 'X1', 'X6', 'X8', 'Y1', 'Y2', 'Y3', 'Y5', 'Z1', 'Z11', 'Z7']

def predict_image(image_array):
    """
    Predicts the Gardiner ID for a single cropped glyph image.
    image_array: A numpy array representing the image (BGR from cv2)
    """
    _load_model_and_classes()
    
    # Model expects 75 height, 50 width
    img_height = 75
    img_width = 50
    
    # Resize the input image
    img = cv2.resize(image_array, (img_width, img_height))
    
    # Convert BGR (OpenCV default) to RGB (Keras default)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Expand dims to create batch of 1
    img_array = np.expand_dims(img, axis=0)
    
    # Predict (model has built-in Rescaling layer)
    predictions = _model.predict(img_array, verbose=0)
    class_index = np.argmax(predictions, axis=1)[0]
    
    # Map to Gardiner ID
    gardiner_id = _class_names[class_index]
    return gardiner_id

if __name__ == "__main__":
    # Quick test if run directly
    test_img_path = os.path.join(DATASET_PATH, 'S29', os.listdir(os.path.join(DATASET_PATH, 'S29'))[0])
    img = cv2.imread(test_img_path)
    if img is not None:
        prediction = predict_image(img)
        print(f"Test image predicted as: {prediction} (Expected: S29)")
