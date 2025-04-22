from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image
import os
import time
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set a max file upload size of 5MB
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

# Allowed formats for images
allowed_formats = ['JPEG', 'PNG', 'WEBP']

@app.errorhandler(413)
def file_too_large(error):
    return "File is too large. Max size is 5MB.", 413

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    files = request.files.getlist('image')  # This handles multiple file uploads
    quality = request.form.get('quality', 60, type=int)  # Get quality from form, default to 60
    if not files:
        return "No files uploaded", 400

    # Check the uploaded images' formats
    output_paths = []
    for file in files:
        img = Image.open(file)
        if img.format not in allowed_formats:
            return f"Unsupported image format: {img.format}", 400

        # Save the uploaded image
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        # Compress and save the image
        output_path = os.path.join(UPLOAD_FOLDER, 'compressed_' + file.filename)
        img.save(output_path, optimize=True, quality=quality)
        img.close()
        output_paths.append(output_path)

    # Send multiple compressed files as a zip
    zip_filename = os.path.join(UPLOAD_FOLDER, 'compressed_images.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for output_path in output_paths:
            zipf.write(output_path, os.path.basename(output_path))
            os.remove(output_path)  # Clean up individual files

    # Send the zip file as a response
    return send_file(zip_filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        # Open the image and compress it
        img = Image.open(input_path)
        output_path = os.path.join(UPLOAD_FOLDER, 'compressed_' + file.filename)
        
        # Save the compressed image with the specified quality
        img.save(output_path, optimize=True, quality=60)
        img.close()

        response = send_file(output_path, as_attachment=True)
        time.sleep(1)  # Allow time for file release
        os.remove(input_path)
        os.remove(output_path)

        return response

    return "No file uploaded", 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
