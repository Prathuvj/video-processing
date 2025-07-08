import os
import tempfile
from flask import Flask, request, jsonify
from metadata_extraction import extract_video_metadata
from format_conversion import convert_video_format
from thumbnail_generation import generate_thumbnail_from_frame, generate_thumbnail_using_gemini_from_video

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video part'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file.save(temp_file.name)
        metadata = extract_video_metadata(temp_file.name, file.filename)
    os.remove(temp_file.name)
    return jsonify(metadata)

@app.route('/convert', methods=['POST'])
def convert_video():
    if 'video' not in request.files or 'target_format' not in request.form:
        return jsonify({'status': 'Failed', 'error': 'Video and target_format required'}), 400
    try:
        file = request.files['video']
        original_filename = file.filename
        target_format = request.form['target_format'].lower()
        with tempfile.NamedTemporaryFile(delete=False) as infile:
            file.save(infile.name)
            infile_path = infile.name
        output_path = convert_video_format(infile_path, original_filename, target_format)
        return jsonify({'status': 'Successful', 'file_path': output_path})
    except Exception as e:
        return jsonify({'status': 'Failed', 'error': str(e)}), 500

@app.route('/thumbnail', methods=['POST'])
def generate_thumbnail():
    mode = request.form.get('mode')
    if mode == 'frame':
        if 'video' not in request.files or 'timestamp' not in request.form:
            return jsonify({'status': 'Failed', 'error': 'video and timestamp required for frame mode'}), 400
        file = request.files['video']
        timestamp = float(request.form['timestamp'])
        with tempfile.NamedTemporaryFile(delete=False) as infile:
            file.save(infile.name)
            infile_path = infile.name
        output_path = generate_thumbnail_from_frame(infile_path, timestamp, output_name="frame_thumbnail.jpg")
        return jsonify({'status': 'Successful' if output_path else 'Failed', 'file_path': output_path})
    
    elif mode == 'gemini':
        if 'video' not in request.files:
            return jsonify({'status': 'Failed', 'error': 'video required for gemini mode'}), 400
        file = request.files['video']
        with tempfile.NamedTemporaryFile(delete=False) as infile:
            file.save(infile.name)
            infile_path = infile.name
        output_path = generate_thumbnail_using_gemini_from_video(infile_path, file.filename)
        return jsonify({'status': 'Successful' if output_path else 'Failed', 'file_path': output_path})
    
    else:
        return jsonify({'status': 'Failed', 'error': 'Invalid mode'}), 400

if __name__ == '__main__':
    app.run(debug=True)