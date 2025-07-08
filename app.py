from flask import Flask, request, jsonify, send_file
import tempfile
import os
from metadata_extraction import extract_video_metadata
from format_conversion import convert_video_format

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        file.save(file_path)
    metadata = extract_video_metadata(file_path, file.filename)
    try:
        os.remove(file_path)
    except PermissionError:
        pass
    return jsonify(metadata)

@app.route('/convert', methods=['POST'])
def convert_video():
    if 'video' not in request.files or 'target_format' not in request.form:
        return jsonify({'error': 'Video and target_format are required'}), 400
    file = request.files['video']
    target_format = request.form['target_format'].lower()
    with tempfile.NamedTemporaryFile(delete=False) as input_file:
        input_path = input_file.name
        file.save(input_path)
    output_path = convert_video_format(input_path, target_format)
    return send_file(output_path, as_attachment=True, download_name=f"converted.{target_format}")

if __name__ == '__main__':
    app.run(debug=True)