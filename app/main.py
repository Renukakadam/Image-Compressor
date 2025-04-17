from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    file = request.files['image']
    if file:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        img = Image.open(input_path)
        output_path = os.path.join(UPLOAD_FOLDER, 'compressed_' + file.filename)
        img.save(output_path, optimize=True, quality=60)

        return send_file(output_path, as_attachment=True)

    return "No file uploaded", 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
