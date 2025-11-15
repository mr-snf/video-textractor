import cv2
import yt_dlp
import os
import tempfile
from . import config

def is_url(path):
    """Check if the given path is a URL."""
    return path.startswith('http://') or path.startswith('https://')

def download_video(url, cookies_from_browser=None):
    """Download a video from a URL to a temporary file."""
    temp_dir = tempfile.gettempdir()
    # Use a more unique name to avoid conflicts
    video_path = os.path.join(temp_dir, f'downloaded_video_{os.getpid()}.mp4')
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': video_path,
        'noplaylist': True,
        'quiet': True,
        'overwrites': True,
    }

    if cookies_from_browser:
        ydl_opts['cookies_from_browser'] = (cookies_from_browser,)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading video: {e}")
        print("This might be a private video. If so, please re-run and provide browser cookies.")
        return None
        
    return video_path

def extract_frames(video_path):
    """Extract frames from a video file, one frame per second."""
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    # Handle cases where fps is 0 or very low
    frame_interval = int(fps) if fps > 0 else 1

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            yield frame
        
        frame_count += 1

    cap.release()
