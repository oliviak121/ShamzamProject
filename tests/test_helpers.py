import base64
from flask import current_app, jsonify
import logging
import requests

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def encode_audio_to_base64(file_path):
    """Encodes an audio file to a base64 string."""
    try:
        with open(file_path, "rb") as audio_file:
            audio_content = audio_file.read()
        return base64.b64encode(audio_content).decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise
    
def clear_database():
    """Clears the database by making an API call to the Catalogue Management Service."""
    url = 'http://localhost:5002/clear_database' # URL of the Catalogue Management Service
    response = requests.post(url)
    if response.status_code != 200:
        raise Exception("Failed to clear the database: " + response.text)
