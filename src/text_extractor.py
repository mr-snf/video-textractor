import easyocr
import config

# Initialize the EasyOCR reader once
reader = easyocr.Reader(config.OCR_LANGUAGES) # This will download the model on first run

def extract_text_from_frame(frame):
    """Extract text from a single video frame using EasyOCR."""
    # EasyOCR works directly with BGR images from OpenCV
    result = reader.readtext(frame)
    
    # The result is a list of (bounding_box, text, confidence)
    # We'll just extract the text
    text = [item[1] for item in result]
    
    return " ".join(text).strip()
