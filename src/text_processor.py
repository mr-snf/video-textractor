import os
import cv2
import numpy as np
import config
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables from a .env file if it exists
load_dotenv()


def _create_llm_client():
    """Creates and configures the LLM client based on the provider in config."""
    if config.LLM_PROVIDER == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key or api_key == "your-api-key-here":
            print("\nWarning: OPENAI_API_KEY is not set or is a placeholder.")
            print("Skipping LLM text cleaning.")
            return None
        return OpenAI(api_key=api_key)

    elif config.LLM_PROVIDER == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key or api_key == "your-api-key-here":
            print("\nWarning: GEMINI_API_KEY is not set or is a placeholder.")
            print("Skipping LLM text cleaning.")
            return None
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(config.GEMINI_MODEL)

    elif config.LLM_PROVIDER == "local":
        return OpenAI(base_url=config.LOCAL_LLM_URL, api_key="ollama")

    else:
        print(f"\nWarning: Invalid LLM_PROVIDER '{config.LLM_PROVIDER}' in config.py.")
        print("Skipping LLM text cleaning.")
        return None


def _get_model_name():
    """Returns the appropriate model name based on the configured provider."""
    if config.LLM_PROVIDER == "openai":
        return config.OPENAI_MODEL
    elif config.LLM_PROVIDER == "gemini":
        return config.GEMINI_MODEL
    elif config.LLM_PROVIDER == "local":
        return config.LOCAL_LLM_MODEL
    return "Unknown Model"


def _split_text_into_chunks(text: str, chunk_size: int) -> list[str]:
    """Splits text into chunks of a specified size without breaking words."""
    chunks = []
    while len(text) > chunk_size:
        split_index = text.rfind(" ", 0, chunk_size)
        if split_index == -1:
            split_index = chunk_size
        chunks.append(text[:split_index])
        text = text[split_index:].lstrip()
    chunks.append(text)
    return chunks


def denoise_text_with_llm(raw_text: str) -> str:
    """
    Uses a configured LLM to clean and refine raw text extracted via OCR,
    processing the text in chunks to handle large inputs.
    """
    client = _create_llm_client()
    if not client:
        return raw_text

    model_name = _get_model_name()
    chunks = _split_text_into_chunks(raw_text, config.TEXT_CHUNK_SIZE)
    cleaned_chunks = []

    print(
        f"\nCleaning extracted text with {config.LLM_PROVIDER} model: {model_name}..."
    )

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1} of {len(chunks)}...")
        try:
            prompt = (
                "The following text was extracted from a video using OCR and contains a lot of noise and gibberish. "
                "Please clean it up. Your task is to:\n"
                "1. Remove any nonsensical words, random characters, and formatting errors.\n"
                "2. Correct obvious OCR mistakes.\n"
                "3. Join text fragments into coherent sentences and paragraphs.\n"
                "4. Preserve the original meaning and intent.\n"
                "Return only the cleaned, corrected text and nothing else.\n\n"
                "Here is the raw text:\n\n"
                f'"{chunk}"'
            )

            if config.LLM_PROVIDER in ["openai", "local"]:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that cleans and corrects OCR text.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.5,
                )
                cleaned_chunk = response.choices[0].message.content.strip()
            elif config.LLM_PROVIDER == "gemini":
                response = client.generate_content(prompt)
                cleaned_chunk = response.text.strip()

            cleaned_chunks.append(cleaned_chunk)

        except Exception as e:
            print(f"An error occurred while processing chunk {i + 1}: {e}")
            # Fallback to the original chunk if cleaning fails
            cleaned_chunks.append(chunk)

    print("\nText cleaning complete.")
    return "\n".join(cleaned_chunks)


def preprocess_for_ocr(frame: np.ndarray) -> np.ndarray:
    """
    Applies a series of preprocessing steps to an image frame to improve OCR accuracy.
    """
    # 1. Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. Apply a bilateral filter to reduce noise while preserving edges
    denoised = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    # 3. Apply adaptive thresholding to binarize the image
    # This helps with varying lighting conditions.
    binary = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2,
    )

    return binary
