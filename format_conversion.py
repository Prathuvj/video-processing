import os
from moviepy.editor import VideoFileClip
from pathlib import Path

def convert_video_format(input_path, original_filename, target_format):
    clip = VideoFileClip(input_path)

    base_name = os.path.splitext(original_filename)[0]
    downloads_path = str(Path.home() / "Downloads")
    output_filename = f"{base_name}.{target_format}"
    output_path = os.path.join(downloads_path, output_filename)

    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    clip.reader.close()
    if clip.audio:
        clip.audio.reader.close_proc()

    return output_path