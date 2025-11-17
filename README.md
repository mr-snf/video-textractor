# Video Textractor

Video Textractor is a Python application designed to extract text from any video, whether it's stored locally on your computer or available online from sites like YouTube. It processes the video, uses Optical Character Recognition (OCR) to identify text in the frames, and saves the output into a well-formatted PDF file.

## Features

- **Local and Online Videos**: Works with both local video files and URLs from various streaming websites.
- **Streaming Site Support**: Leverages `yt-dlp` to download videos from a wide range of sources, including YouTube.
- **Private Video Access**: Can access private or login-required videos by using cookies from your web browser (supports Chrome, Firefox, Edge, and others).
- **Accurate OCR**: Uses the `EasyOCR` library for robust and accurate text extraction.
- **GPU Acceleration**: Automatically uses an available NVIDIA GPU (via CUDA) to dramatically speed up the text extraction process.
- **Advanced Text Cleaning**: Optionally uses a local or remote Large Language Model (LLM) to clean and de-noise the extracted text, correcting OCR errors and formatting it into coherent paragraphs.
- **PDF Generation**: Automatically generates a clean PDF document (`extracted_text.pdf`) containing all the extracted text.

## Tech Stack

- **Python 3**
- **PyTorch**: For the deep learning backend of the OCR.
- **EasyOCR**: For text recognition.
- **OpenAI Client**: For interfacing with both OpenAI and local LLMs.
- **yt-dlp**: For downloading online videos.
- **OpenCV-Python**: For video processing and frame extraction.
- **FPDF2**: For generating the final PDF document.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd video-textractor
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install PyTorch (Choose one):**
    The OCR process is powered by PyTorch. Installing the correct version for your hardware is critical for performance.

    -   **For NVIDIA GPU Users (Recommended for best performance):**
        ```powershell
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
        ```

    -   **For CPU-Only Users:**
        ```powershell
        pip install torch torchvision torchaudio
        ```

4.  **Install Remaining Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The first time you run the application, `EasyOCR` will automatically download the necessary language models. This might take a few moments.*

5.  **Install FFmpeg (Recommended):**
    For the best results, especially with high-quality YouTube videos, it is highly recommended to install FFmpeg. This allows the application to download and merge the best quality video and audio streams.

    -   **Windows (using Chocolatey or Winget):**
        ```powershell
        # Using Chocolatey
        choco install ffmpeg
        # OR using Winget
        winget install "FFmpeg (Essentials Build)"
        ```

    -   **macOS (using Homebrew):**
        ```bash
        brew install ffmpeg
        ```

    -   **Linux (using APT for Debian/Ubuntu):**
        ```bash
        sudo apt update && sudo apt install ffmpeg
        ```

## LLM Configuration

This project can use a Large Language Model (LLM) to significantly improve the quality of the extracted text by correcting OCR errors, removing gibberish, and formatting the text into coherent paragraphs. You can choose between three providers in the `src/config.py` file.

### 1. Local LLM (Recommended: Fast, Private, Free)

You can use a variety of applications to serve LLMs locally. Both **Ollama** and **LM Studio** are excellent choices as they provide an OpenAI-compatible server out of the box.

#### Using Ollama

1.  **Install Ollama**: Download and install from the [official Ollama website](https://ollama.com/). It will run as a background service.
2.  **Pull a Model**: Open a terminal and download a recommended model like `phi3:mini`.
    ```bash
    ollama pull phi3:mini
    ```
3.  **Configure the App**: In `src/config.py`, make sure the settings are configured for Ollama:
    ```python
    LLM_PROVIDER = "local"
    LOCAL_LLM_URL = "http://localhost:11434/v1"
    LOCAL_LLM_MODEL = "phi3:mini"
    ```

#### Using LM Studio

1.  **Install LM Studio**: Download and install from the [official LM Studio website](https://lmstudio.ai/).
2.  **Download a Model**: In the LM Studio app, search for and download a GGUF model. We recommend **"Phi-3-mini-GGUF"**.
3.  **Start the Server**: Go to the "Local Server" tab (the `<->` icon), select your model at the top, and click **"Start Server"**.
4.  **Configure the App**: In `src/config.py`, update the URL to point to the LM Studio server:
    ```python
    LLM_PROVIDER = "local"
    LOCAL_LLM_URL = "http://localhost:1234/v1"
    # The LOCAL_LLM_MODEL setting is not used by LM Studio
    ```

### 2. OpenAI

Uses the OpenAI API. This requires an API key and will incur costs.

1.  **Set API Key**: Create a `.env` file (from `.env.example`) and add your `OPENAI_API_KEY`.
2.  **Configure the App**: In `src/config.py`, set `LLM_PROVIDER = "openai"`. You can also change the `OPENAI_MODEL` if you wish.

### 3. Gemini

Uses the Google Gemini API. This also requires an API key and will incur costs.

1.  **Set API Key**: In your `.env` file, add your `GEMINI_API_KEY`.
2.  **Configure the App**: In `src/config.py`, set `LLM_PROVIDER = "gemini"`.

## Usage

1.  **Configure the Application:**
    Open `src/config.py` to customize settings, especially the `LLM_PROVIDER` and `LOCAL_LLM_URL` as described above.

2.  **Run the application from the root directory:**
    ```bash
    python run.py
    ```

3.  **Follow the on-screen prompts:**
    -   **Enter the path to the video file or a URL:** Provide a local file path (e.g., `C:\videos\my_video.mp4`) or a URL (e.g., `https://www.youtube.com/watch?v=...`).
    -   **Does this video require a login? (yes/no):** If you provided a URL for a private or members-only video, type `yes`.
    -   **Enter the browser to use for cookies...:** If you answered yes, specify the browser where you are logged in (e.g., `chrome`, `firefox`).

The final output will be saved as `output/extracted_text.pdf`.

## How It Works

1.  **Video Handling**: If a URL is provided, `yt-dlp` downloads the video. If it's a local file, it's used directly.
2.  **Frame Extraction**: The video is processed frame by frame using `OpenCV`.
3.  **Text Extraction**: Each frame is passed to `EasyOCR`, which uses a deep learning model to recognize and extract any text.
4.  **Text Denoising (LLM)**: The raw, unordered text is sent in chunks to the configured LLM (Ollama, OpenAI, or Gemini), which cleans it up.
5.  **PDF Generation**: The cleaned text is compiled into a final, readable PDF document.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
