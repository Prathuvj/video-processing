import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

st.title("🎬 Video Processing App")

operation = st.selectbox("Choose Operation", [
    "Extract Metadata", "Convert Format", "Generate Thumbnail", "Resize Video", "Trim Video"
])

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

if uploaded_file:
    if operation == "Extract Metadata":
        if st.button("Get Metadata"):
            files = {'video': uploaded_file}
            response = requests.post(f"{API_URL}/upload", files=files)
            st.json(response.json())

    elif operation == "Convert Format":
        format_choice = st.selectbox("Target Format", ["mp4", "avi", "mov"])
        if st.button("Convert"):
            files = {'video': uploaded_file}
            data = {'target_format': format_choice}
            response = requests.post(f"{API_URL}/convert", files=files, data=data)
            st.json(response.json())

    elif operation == "Generate Thumbnail":
        mode = st.radio("Choose Thumbnail Mode", ["frame", "gemini"])
        files = {'video': uploaded_file}

        if mode == "frame":
            timestamp = st.number_input("Timestamp (in seconds)", min_value=0.0, value=1.0)
            data = {'mode': 'frame', 'timestamp': str(timestamp)}
        else:
            data = {'mode': 'gemini'}

        if st.button("Generate"):
            response = requests.post(f"{API_URL}/thumbnail", files=files, data=data)
            st.json(response.json())

    elif operation == "Resize Video":
        width = st.number_input("Width", min_value=1, value=1280)
        height = st.number_input("Height", min_value=1, value=720)
        if st.button("Resize"):
            files = {'video': uploaded_file}
            data = {'width': str(width), 'height': str(height)}
            response = requests.post(f"{API_URL}/resize", files=files, data=data)
            st.json(response.json())

    elif operation == "Trim Video":
        start = st.number_input("Start Time (s)", min_value=0.0, value=1.0)
        end = st.number_input("End Time (s)", min_value=0.0, value=5.0)
        if st.button("Trim"):
            files = {'video': uploaded_file}
            data = {'start': str(start), 'end': str(end)}
            response = requests.post(f"{API_URL}/trim", files=files, data=data)
            st.json(response.json())