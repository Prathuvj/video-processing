import os
import cv2
import time
import mimetypes
from pathlib import Path
from dotenv import load_dotenv
from google.genai import Client

load_dotenv()
client = Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_thumbnail_from_frame(video_path, timestamp, output_name="frame_thumbnail.jpg"):
    """Extracts a single frame from a video at a specific timestamp and saves it as an image."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("[ERROR] Could not open video file.")
        return None
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = int(float(timestamp) * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    success, frame = cap.read()
    cap.release()
    
    if success:
        valid_extensions = ['.jpg', '.jpeg', '.png']
        ext = Path(output_name).suffix.lower()
        if ext not in valid_extensions:
            output_name = Path(output_name).stem + ".jpg"
        
        output_path = Path.home() / "Downloads" / output_name
        cv2.imwrite(str(output_path), frame)
        print(f"[SUCCESS] Frame thumbnail saved to {output_path}")
        return str(output_path)
        
    print("[ERROR] Failed to extract frame from video.")
    return None


def generate_thumbnail_using_gemini_from_video(video_path, output_name="ai_thumbnail.jpg"):
    """Uploads a video to Gemini and generates an AI-enhanced thumbnail."""
    print(f"[INFO] Uploading video: {video_path}")

    mime_type, _ = mimetypes.guess_type(video_path)
    if not mime_type:
        mime_type = "video/mp4"
        print(f"[WARN] Could not determine MIME type. Defaulting to '{mime_type}'.")

    try:
        video_file = client.files.upload(file=video_path, mime_type=mime_type)
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return None

    print("[INFO] Waiting for video to finish processing...")
    while video_file.state.name == "PROCESSING":
        time.sleep(5)
        video_file = client.files.get(video_file.name)

    if video_file.state.name == "FAILED":
        print("[ERROR] Video processing failed.")
        return None

    print("[INFO] Video uploaded and processed.")

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                "Generate a compelling and high-quality thumbnail for this video. The thumbnail should be visually striking and represent the key themes of the video.",
                video_file
            ]
        )
        
        if response.parts and hasattr(response.parts[0], "inline_data"):
             image_data = response.parts[0].inline_data.data
             out_path = Path.home() / "Downloads" / output_name
             out_path.write_bytes(image_data)
             print(f"[SUCCESS] AI thumbnail saved to {out_path}")
             return str(out_path)
        else:
             print("[WARN] No image data found in Gemini response. Full response:")
             print(response)

    except Exception as e:
        print(f"[ERROR] Gemini content generation request failed: {e}")
        client.files.delete(video_file.name)
        print(f"[INFO] Deleted uploaded file: {video_file.name}")

    return None