import os
from moviepy.editor import VideoFileClip
from pathlib import Path

def trim_video(input_path, original_filename, start_time, end_time):
    clip = VideoFileClip(input_path).subclip(start_time, end_time)
    base_name = os.path.splitext(original_filename)[0]
    output_filename = f"{base_name}_{start_time}s_to_{end_time}s.mp4"
    output_path = os.path.join(Path.home() / "Downloads", output_filename)
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    clip.reader.close()
    if clip.audio:
        clip.audio.reader.close_proc()
    return output_path