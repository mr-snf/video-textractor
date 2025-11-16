import os

# --- Project Directories ---
# The root directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
# The directory where output files will be saved
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
DEFAULT_PDF_FILENAME = "extracted_text.pdf"


# --- OCR Configuration ---
# Languages for EasyOCR to detect
OCR_LANGUAGES = ['en']


# --- LLM Text Cleaning Configuration ---
# Choose your LLM provider: "openai" or "local"
# - "openai": Uses the OpenAI API (requires OPENAI_API_KEY).
# - "local": Uses a local model via Ollama (requires Ollama to be running).
LLM_PROVIDER = "openai"

# --- OpenAI Settings (if LLM_PROVIDER is "openai") ---
OPENAI_MODEL = "gpt-3.5-turbo"

# --- Local LLM Settings (if LLM_PROVIDER is "local") ---
# The model to use with Ollama (e.g., "llama3:8b", "phi3:mini")
LOCAL_LLM_MODEL = "llama3:8b" 
# The base URL for the Ollama server's OpenAI-compatible API
LOCAL_LLM_URL = "http://localhost:11434/v1"

# --- Chunking Configuration ---
# The number of characters per chunk to send to the LLM.
# A smaller size is safer for models with small context windows.
TEXT_CHUNK_SIZE = 2500
