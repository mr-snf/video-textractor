from video_handler import is_url, download_video, extract_frames
from text_extractor import extract_text_from_frame
from pdf_generator import generate_pdf
import os

class VideoTextractor:
    def __init__(self, video_path, cookies_browser=None):
        self.video_path = video_path
        self.cookies_browser = cookies_browser
        self.is_downloaded = False
        self.extracted_text = []

    def _handle_video_source(self):
        """Determines if the video is a URL or local file and processes accordingly."""
        if is_url(self.video_path):
            print("Downloading video...")
            self.video_path = download_video(self.video_path, self.cookies_browser)
            if not self.video_path:
                raise ConnectionError("Failed to download the video.")
            self.is_downloaded = True
        elif not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Error: The file '{self.video_path}' does not exist.")

    def _extract_text(self):
        """Extracts text from the video frames."""
        print("Extracting frames and text...")
        for frame in extract_frames(self.video_path):
            text = extract_text_from_frame(frame)
            if text:
                self.extracted_text.append(text)

    def _generate_output(self):
        """Generates the PDF output if text was extracted."""
        if self.extracted_text:
            full_text = "\n".join(self.extracted_text)
            generate_pdf(full_text)
        else:
            print("No text could be extracted from the video.")

    def _cleanup(self):
        """Removes the temporary downloaded video file."""
        if self.is_downloaded and self.video_path and os.path.exists(self.video_path):
            os.remove(self.video_path)
            print("Cleaned up temporary video file.")

    def run(self):
        """Executes the full video text extraction workflow."""
        try:
            self._handle_video_source()
            self._extract_text()
            self._generate_output()
        finally:
            self._cleanup()

def main():
    """Main function to get user input and run the VideoTextractor."""
    video_path = input("\nEnter the path to the video file or a URL: ")
    cookies_browser = None

    if is_url(video_path):
        needs_cookies = input("Does this video require a login? (yes/no): ").lower()
        if needs_cookies == 'yes':
            cookies_browser = input("Enter the browser to use for cookies (e.g., chrome, firefox, edge): ")
    
    extractor = VideoTextractor(video_path, cookies_browser)
    extractor.run()

if __name__ == "__main__":
    main()
