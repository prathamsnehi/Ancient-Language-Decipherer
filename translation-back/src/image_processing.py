import cv2
import numpy as np

def segment_image(image_path, target_width=1000, direction='rtl'):
    """
    Takes an image containing hieroglyphs, processes it, and extracts
    individual glyphs sorted in the specified reading order ('rtl' or 'ltr').
    Returns a list of cropped image arrays representing the individual glyphs.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image at {image_path}")
        
    # Scale image to standard width while maintaining aspect ratio
    img_height, img_width = img.shape[:2]
    scale = target_width / img_width
    width = int(img_width * scale)
    height = int(img_height * scale)
    scaled_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    
    # Convert to grayscale
    gray = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Adaptive thresholding to extract foreground features
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    bounding_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Filter out very small noise contours (e.g., less than 15x15 pixels)
        if w > 15 and h > 15:
            bounding_boxes.append((x, y, w, h))
            
    # Sort bounding boxes (top-to-bottom, then horizontal based on direction)
    def sort_contours(boxes, y_tolerance=40):
        if not boxes:
            return []
        
        # Sort by y-coordinate first
        boxes = sorted(boxes, key=lambda b: b[1])
        
        rows = []
        current_row = [boxes[0]]
        
        for box in boxes[1:]:
            # Group into the same row if y-coordinate is within tolerance
            if abs(box[1] - current_row[0][1]) < y_tolerance:
                current_row.append(box)
            else:
                rows.append(current_row)
                current_row = [box]
        rows.append(current_row)
        
        sorted_boxes = []
        is_rtl = (direction == 'rtl')
        for row in rows:
            # Sort each row horizontally (descending if rtl, ascending if ltr)
            row = sorted(row, key=lambda b: b[0], reverse=is_rtl)
            sorted_boxes.extend(row)
            
        return sorted_boxes

    sorted_boxes = sort_contours(bounding_boxes)
    
    segmented_glyphs = []
    for x, y, w, h in sorted_boxes:
        # Crop glyph and append to list
        # Add a small padding if possible
        pad = 5
        y_start = max(0, y - pad)
        y_end = min(height, y + h + pad)
        x_start = max(0, x - pad)
        x_end = min(width, x + w + pad)
        
        glyph_crop = scaled_img[y_start:y_end, x_start:x_end]
        segmented_glyphs.append(glyph_crop)
        
    return segmented_glyphs
