from flask import Flask, request, jsonify
import tempfile
import os
from metadata import extract_video_metadata

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file.save(temp_file.name)
        metadata = extract_video_metadata(temp_file.name)
    os.remove(temp_file.name)
    return jsonify(metadata)

if __name__ == '__main__':
    app.run(debug=True)