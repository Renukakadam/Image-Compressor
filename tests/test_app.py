import os
import io
import pytest
from PIL import Image
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.app import app, UPLOAD_FOLDER


from app.app import app, UPLOAD_FOLDER
import time


@pytest.fixture
def client():
   app.config['TESTING'] = True
   with app.test_client() as client:
       yield client


def create_test_image():
   # Create an in-memory image
   img = Image.new('RGB', (100, 100), color='red')
   byte_io = io.BytesIO()
   img.save(byte_io, format='JPEG')
   byte_io.seek(0)
   return byte_io


def test_image_compression(client):
   # Simulate uploading an image
   data = {
       'image': (create_test_image(), 'test_image.jpg')
   }
   response = client.post('/compress', content_type='multipart/form-data', data=data)


   # Assert response is successful
   assert response.status_code == 200
   assert response.headers['Content-Disposition'].startswith('attachment;')


   # Check if compressed image file exists in uploads folder
   compressed_path = os.path.join(UPLOAD_FOLDER, 'compressed_test_image.jpg')
   assert os.path.exists(compressed_path)


   # Introduce a small delay to ensure the file is closed properly
   time.sleep(1)  # Sleep for 1 second before cleanup


   # Cleanup test files
   os.remove(os.path.join(UPLOAD_FOLDER, 'test_image.jpg'))
   os.remove(compressed_path)
