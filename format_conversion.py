import os
from moviepy.editor import VideoFileClip
import tempfile

def convert_video_format(input_path, target_format):
    clip = VideoFileClip(input_path)
    output_path = tempfile.NamedTemporaryFile(suffix=f".{target_format}", delete=False).name
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    clip.reader.close()
    if clip.audio:
        clip.audio.reader.close_proc()
    return output_path