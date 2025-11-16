import os
from openai import OpenAI
from dotenv import load_dotenv
from . import config

# Load environment variables from a .env file if it exists
load_dotenv()

def _create_llm_client():
    """Creates and configures the OpenAI client based on the provider in config."""
    if config.LLM_PROVIDER == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key or api_key == "your-api-key-here":
            print("\nWarning: OPENAI_API_KEY is not set or is a placeholder.")
            print("Please create a .env file and add your key.")
            print("Skipping LLM text cleaning. The output may contain noise.")
            return None
        return OpenAI(api_key=api_key)
    
    elif config.LLM_PROVIDER == "local":
        # For local LLMs via Ollama, the API key is not required but the client expects a value.
        return OpenAI(base_url=config.LOCAL_LLM_URL, api_key="ollama")
    
    else:
        print(f"\nWarning: Invalid LLM_PROVIDER '{config.LLM_PROVIDER}' in config.py.")
        print("Skipping LLM text cleaning.")
        return None

def _split_text_into_chunks(text: str, chunk_size: int) -> list[str]:
    """Splits text into chunks of a specified size without breaking words."""
    chunks = []
    while len(text) > chunk_size:
        # Find the last space within the chunk size
        split_index = text.rfind(' ', 0, chunk_size)
        if split_index == -1:
            # No spaces found, force a split
            split_index = chunk_size
        chunks.append(text[:split_index])
        text = text[split_index:].lstrip()
    chunks.append(text)
    return chunks

def clean_text_with_llm(raw_text: str) -> str:
    """
    Uses a configured LLM to clean and refine raw text extracted via OCR,
    processing the text in chunks to handle large inputs.
    """
    client = _create_llm_client()
    if not client:
        return raw_text

    model_name = config.OPENAI_MODEL if config.LLM_PROVIDER == "openai" else config.LOCAL_LLM_MODEL
    
    chunks = _split_text_into_chunks(raw_text, config.TEXT_CHUNK_SIZE)
    cleaned_chunks = []
    
    print(f"\nCleaning extracted text with {config.LLM_PROVIDER} model: {model_name}...")

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

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that cleans and corrects OCR text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
            )
            
            cleaned_chunk = response.choices[0].message.content.strip()
            cleaned_chunks.append(cleaned_chunk)

        except Exception as e:
            print(f"\nAn error occurred while processing chunk {i + 1}: {e}")
            print("Appending original chunk instead.")
            cleaned_chunks.append(chunk) # Fallback to the original chunk on error
    
    print("Text cleaning complete.")
    return "\n\n".join(cleaned_chunks)
