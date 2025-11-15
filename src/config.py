import os

# The root directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

# The directory where output files will be saved
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
DEFAULT_PDF_FILENAME = "extracted_text.pdf"

# Languages for EasyOCR to detect
OCR_LANGUAGES = ['en']
