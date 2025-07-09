import os
import cv2
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
    """Uses Gemini 2.0 preview model to generate a thumbnail from a video."""

    from google.api_core.exceptions import InvalidArgument

    print(f"[INFO] Uploading video: {video_path}")

    if not video_path.endswith(".mp4"):
        temp_path = f"{video_path}.mp4"
        os.rename(video_path, temp_path)
        video_path = temp_path
        print(f"[INFO] Renamed temp file to: {video_path}")

    try:
        with open(video_path, "rb") as f:
            video_file = client.files.upload(file=f)
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return None

    print("[INFO] File uploaded to Gemini, calling generate_content...")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": (
                                "Generate a high-quality, visually compelling thumbnail image "
                                "that summarizes the key content or theme of this video."
                            )
                        },
                        video_file
                    ]
                }
            ]
        )

        if response.parts and hasattr(response.parts[0], "inline_data"):
            image_data = response.parts[0].inline_data.data
            out_path = Path.home() / "Downloads" / output_name
            out_path.write_bytes(image_data)
            print(f"[SUCCESS] AI thumbnail saved to {out_path}")
            return str(out_path)
        else:
            print("[WARN] No image data in Gemini response.")
            print(response)

    except InvalidArgument as e:
        print(f"[ERROR] Gemini request failed: {e}")
    except Exception as e:
        print(f"[ERROR] General exception during Gemini call: {e}")

    return None