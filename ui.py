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

def create_ui():
    with gr.Blocks(title="Video Processing UI") as demo:
        gr.Markdown("## Step 1: Upload a Video")
        video_input = gr.Video()

        gr.Markdown("## Step 2: Choose Operation")
        operation = gr.Dropdown(
            ["Extract Metadata", "Convert Format", "Generate Thumbnail", "Resize", "Trim"],
            label="Operation"
        )

        with gr.Column(visible=False) as metadata_panel:
            btn1 = gr.Button("Extract Metadata")
            out1 = gr.JSON()
            btn1.click(fn=extract_metadata, inputs=video_input, outputs=out1)

        with gr.Column(visible=False) as convert_panel:
            format_input = gr.Dropdown(["mp4", "avi", "mov"], label="Target Format")
            btn2 = gr.Button("Convert Format")
            out2 = gr.JSON()
            btn2.click(fn=convert_format, inputs=[video_input, format_input], outputs=out2)

        with gr.Column(visible=False) as thumbnail_panel:
            mode = gr.Radio(["frame", "gemini"], label="Mode", value="frame")
            timestamp = gr.Number(label="Timestamp (for frame mode)", value=1.0)
            btn3 = gr.Button("Generate Thumbnail")
            out3 = gr.JSON()
            btn3.click(fn=generate_thumbnail, inputs=[video_input, mode, timestamp], outputs=out3)

        with gr.Column(visible=False) as resize_panel:
            width = gr.Number(label="Width", value=1280)
            height = gr.Number(label="Height", value=720)
            btn4 = gr.Button("Resize Video")
            out4 = gr.JSON()
            btn4.click(fn=resize_video, inputs=[video_input, width, height], outputs=out4)

        with gr.Column(visible=False) as trim_panel:
            start = gr.Number(label="Start Time (s)", value=0)
            end = gr.Number(label="End Time (s)", value=5)
            btn5 = gr.Button("Trim Video")
            out5 = gr.JSON()
            btn5.click(fn=trim_video, inputs=[video_input, start, end], outputs=out5)

        def show_panels(op):
            return {
                metadata_panel: op == "Extract Metadata",
                convert_panel: op == "Convert Format",
                thumbnail_panel: op == "Generate Thumbnail",
                resize_panel: op == "Resize",
                trim_panel: op == "Trim"
            }

        operation.change(fn=show_panels, inputs=operation, outputs=[
            metadata_panel, convert_panel, thumbnail_panel, resize_panel, trim_panel
        ])

    return demo