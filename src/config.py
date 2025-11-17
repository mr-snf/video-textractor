import os

# --- Project Directories ---
# The root directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The directory where output files will be saved
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
DEFAULT_PDF_FILENAME = "extracted_text.pdf"


# --- OCR Configuration ---
# Languages for EasyOCR to detect
OCR_LANGUAGES = ["en"]


# --- LLM Text Cleaning Configuration ---
# Choose your LLM provider: "openai", "gemini", or "local"
# - "openai": Uses the OpenAI API (requires OPENAI_API_KEY).
# - "gemini": Uses the Google Gemini API (requires GEMINI_API_KEY).
# - "local": Uses a local model via Ollama (requires Ollama to be running).
LLM_PROVIDER = "local"

# --- OpenAI Settings (if LLM_PROVIDER is "openai") ---
OPENAI_MODEL = "gpt-3.5-turbo"

# --- Gemini Settings (if LLM_PROVIDER is "gemini") ---
GEMINI_MODEL = "gemini-2.0-flash"

# --- Local LLM Settings (if LLM_PROVIDER is "local") ---
# The model to use with your local server (Ollama, LM Studio, etc.).
# We recommend "phi3:mini" for its speed and effectiveness.
LOCAL_LLM_MODEL = "phi3:mini"
# The base URL for the local server's OpenAI-compatible API.
# - For Ollama: "http://localhost:11434/v1"
# - For LM Studio: "http://localhost:1234/v1"
LOCAL_LLM_URL = "http://localhost:11434/v1"

# --- Chunking Configuration ---
# The number of characters per chunk to send to the LLM.
# A smaller size is safer for models with small context windows.
TEXT_CHUNK_SIZE = 2500
