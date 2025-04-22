import os
import io
import pytest
from PIL import Image
import sys

# Add root directory to sys.path for module discovery
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app, UPLOAD_FOLDER  # <-- Fixed this line

import time

@pytest.fixture
def client():
   app.config['TESTING'] = True
   with app.test_client() as client:
       yield client

def create_test_image():
   img = Image.new('RGB', (100, 100), color='red')
   byte_io = io.BytesIO()
   img.save(byte_io, format='JPEG')
   byte_io.seek(0)
   return byte_io

def test_image_compression(client):
   data = {
       'image': (create_test_image(), 'test_image.jpg')
   }
   response = client.post('/compress', content_type='multipart/form-data', data=data)

   assert response.status_code == 200
   assert response.headers['Content-Disposition'].startswith('attachment;')

   compressed_path = os.path.join(UPLOAD_FOLDER, 'compressed_test_image.jpg')
   assert os.path.exists(compressed_path)

   time.sleep(1)

   os.remove(os.path.join(UPLOAD_FOLDER, 'test_image.jpg'))
   os.remove(compressed_path)
