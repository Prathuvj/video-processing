import os
from moviepy.editor import VideoFileClip
from pathlib import Path

def resize_video(input_path, original_filename, target_width, target_height):
    clip = VideoFileClip(input_path)
    resized = clip.resize(newsize=(target_width, target_height))
    base_name = os.path.splitext(original_filename)[0]
    output_filename = f"{base_name}_{target_width}x{target_height}.mp4"
    output_path = os.path.join(Path.home() / "Downloads", output_filename)
    resized.write_videofile(output_path, codec='libx264', audio_codec='aac')
    clip.reader.close()
    if clip.audio:
        clip.audio.reader.close_proc()
    return output_path