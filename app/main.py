from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import time

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

        # Open the image and compress it
        img = Image.open(input_path)
        output_path = os.path.join(UPLOAD_FOLDER, 'compressed_' + file.filename)
        
        # Save the compressed image
        img.save(output_path, optimize=True, quality=60)
        
        # Close the image to release any file handles
        img.close()

        # Send the compressed file as a response
        response = send_file(output_path, as_attachment=True)

        # Allow the system to handle file deletion after sending response
        # You may want to use a background task or schedule the deletion
        # but here we will just delay to give time for the file to be released
        time.sleep(1)
        
        # Optionally, delete the files after sending the response
        os.remove(input_path)
        os.remove(output_path)

        return response

    return "No file uploaded", 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
