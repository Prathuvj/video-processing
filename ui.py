import threading
import gradio as gr
import requests

BASE_URL = "http://localhost:5000"

def extract_metadata(video_file):
    with open(video_file.name, "rb") as f:
        response = requests.post(f"{BASE_URL}/upload", files={"video": f})
    return response.json()

def convert_format(video_file, target_format):
    with open(video_file.name, "rb") as f:
        response = requests.post(f"{BASE_URL}/convert", files={"video": f}, data={"target_format": target_format})
    return response.json()

def generate_thumbnail(video_file, mode, timestamp):
    data = {"mode": mode}
    if mode == "frame":
        data["timestamp"] = str(timestamp)
    with open(video_file.name, "rb") as f:
        response = requests.post(f"{BASE_URL}/thumbnail", files={"video": f}, data=data)
    return response.json()

def resize_video(video_file, width, height):
    with open(video_file.name, "rb") as f:
        response = requests.post(f"{BASE_URL}/resize", files={"video": f}, data={"width": str(width), "height": str(height)})
    return response.json()

def trim_video(video_file, start, end):
    with open(video_file.name, "rb") as f:
        response = requests.post(f"{BASE_URL}/trim", files={"video": f}, data={"start": str(start), "end": str(end)})
    return response.json()

def launch_ui():
    with gr.Blocks(title="Video Processing UI") as demo:
        with gr.Tab("Metadata"):
            video1 = gr.Video()
            out1 = gr.JSON()
            btn1 = gr.Button("Extract Metadata")
            btn1.click(fn=extract_metadata, inputs=video1, outputs=out1)

        with gr.Tab("Convert Format"):
            video2 = gr.Video()
            format_input = gr.Dropdown(["mp4", "avi", "mov"], label="Target Format")
            out2 = gr.JSON()
            btn2 = gr.Button("Convert")
            btn2.click(fn=convert_format, inputs=[video2, format_input], outputs=out2)

        with gr.Tab("Generate Thumbnail"):
            video3 = gr.Video()
            mode = gr.Radio(["frame", "gemini"], label="Mode", value="frame")
            timestamp = gr.Number(label="Timestamp (only for frame mode)", value=1.0)
            out3 = gr.JSON()
            btn3 = gr.Button("Generate Thumbnail")
            btn3.click(fn=generate_thumbnail, inputs=[video3, mode, timestamp], outputs=out3)

        with gr.Tab("Resize"):
            video4 = gr.Video()
            width = gr.Number(label="Width", value=1280)
            height = gr.Number(label="Height", value=720)
            out4 = gr.JSON()
            btn4 = gr.Button("Resize")
            btn4.click(fn=resize_video, inputs=[video4, width, height], outputs=out4)

        with gr.Tab("Trim"):
            video5 = gr.Video()
            start = gr.Number(label="Start Time (s)", value=0)
            end = gr.Number(label="End Time (s)", value=5)
            out5 = gr.JSON()
            btn5 = gr.Button("Trim")
            btn5.click(fn=trim_video, inputs=[video5, start, end], outputs=out5)

    demo.launch(server_port=7860, share=False)

if __name__ == "__main__":
    threading.Thread(target=launch_ui).start()