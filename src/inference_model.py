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
        
        if os.path.exists(DATASET_PATH):
            # tf.keras.preprocessing.image_dataset_from_directory sorts folders alphabetically
            _class_names = sorted([d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))])
        else:
            raise RuntimeError(f"Dataset path {DATASET_PATH} not found to infer class names.")

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
