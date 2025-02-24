import base64
import logging
import requests
import os

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def clear_database():
    """Clears the database by making an API call to the Catalogue Management Service."""
    url = 'http://localhost:5002/clear_database' # URL of the Catalogue Management Service
    response = requests.post(url)
    if response.status_code != 200:
        raise Exception("Failed to clear the database: " + response.text)
    
def encode_audio_to_base64(file_path):
    """Encodes an audio file to a base64 string."""
    try:
        with open(file_path, "rb") as audio_file:
            audio_content = audio_file.read()
        return base64.b64encode(audio_content).decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise

def decode_base64_to_wav(encoded_string, output_file_name):
    """Decodes a base64 string back into a .wav file and saves it to the playlist folder."""
    try:
        audio_content = base64.b64decode(encoded_string)
        playlist_folder = os.path.join(os.path.dirname(__file__), '../playlist')
        os.makedirs(playlist_folder, exist_ok=True)
        output_file_path = os.path.join(playlist_folder, output_file_name)
        with open(output_file_path, "wb") as audio_file:
            audio_file.write(audio_content)
        logger.info(f"File saved to {output_file_path}")
    except Exception as e:
        logger.error(f"Failed to write file {output_file_name}: {e}")
        raise