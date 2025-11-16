# Video Textractor

Video Textractor is a Python application designed to extract text from any video, whether it's stored locally on your computer or available online from sites like YouTube. It processes the video, uses Optical Character Recognition (OCR) to identify text in the frames, and saves the output into a well-formatted PDF file.

## Features

- **Local and Online Videos**: Works with both local video files and URLs from various streaming websites.
- **Streaming Site Support**: Leverages `yt-dlp` to download videos from a wide range of sources, including YouTube.
- **Private Video Access**: Can access private or login-required videos by using cookies from your web browser (supports Chrome, Firefox, Edge, and others).
- **Accurate OCR**: Uses the `EasyOCR` library for robust and accurate text extraction.
- **GPU Acceleration**: Automatically uses an available NVIDIA GPU (via CUDA) to dramatically speed up the text extraction process.
- **PDF Generation**: Automatically generates a clean PDF document (`extracted_text.pdf`) containing all the extracted text.

## Tech Stack

- **Python 3**
- **PyTorch**: For the deep learning backend of the OCR.
- **EasyOCR**: For text recognition.
- **yt-dlp**: For downloading online videos.
- **OpenCV-Python**: For video processing and frame extraction.
- **FPDF**: For generating the final PDF document.

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
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
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

## Usage

1.  **Run the application from the root directory:**
    ```bash
    python run.py
    ```

2.  **Follow the on-screen prompts:**
    -   **Enter the path to the video file or a URL:** Provide a local file path (e.g., `C:\videos\my_video.mp4`) or a URL (e.g., `https://www.youtube.com/watch?v=...`).
    -   **Does this video require a login? (yes/no):** If you provided a URL for a private or members-only video, type `yes`.
    -   **Enter the browser to use for cookies...:** If you answered yes, type the name of the browser where you are logged in (e.g., `chrome`, `firefox`).

The application will then process the video and save the output as `extracted_text.pdf` in the `output/` directory.
