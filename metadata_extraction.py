import os
import cv2
from moviepy.editor import VideoFileClip

# Function to extract metadata from a video file
def extract_video_metadata(path, original_filename):
    clip = VideoFileClip(path)
    duration = round(clip.duration, 2)
    clip.reader.close()
    if clip.audio:
        clip.audio.reader.close_proc()

    cap = cv2.VideoCapture(path)
    size = os.path.getsize(path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    ext = os.path.splitext(original_filename)[1].replace('.', '')

    return {
        'Duration (s)': duration,
        'Resolution': f'{width}x{height}',
        'File Size (MB)': round(size / (1024 * 1024), 2),
        'Frame Rate (fps)': round(fps, 2),
        'File Format': ext
    }