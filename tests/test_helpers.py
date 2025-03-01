import base64
import logging
import requests
import os

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def clear_database() -> None:
    """
    Clears the database by making an API call to the Catalogue Management Service.
    
    Raises:
        Exception: If the database could not be cleared.
    """
    url = 'http://localhost:5002/clear_database' # URL of the Catalogue Management Service
    response = requests.delete(url)
    if response.status_code != 200:
        raise Exception("Failed to clear the database: " + response.text)
    
def encode_audio_to_base64(file_path: str) -> str:
    """
    Encodes an audio file to a base64 string.
    
    Args:
        file_path (str): Path to the audio file.
    
    Returns:
        str: Base64 encoded string of the audio file.
    
    Raises:
        Exception: If the file could not be read.
    """
    try:
        with open(file_path, "rb") as audio_file:
            audio_content = audio_file.read()
        return base64.b64encode(audio_content).decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise

def decode_base64_to_wav(encoded_string: str, output_file_name: str) -> None:
    """
    Decodes a base64 string back into a .wav file and saves it to the playlist folder.
    
    Args:
        encoded_string (str): Base64 encoded string of the audio file.
        output_file_name (str): Name of the output .wav file.
    
    Raises:
        Exception: If the file could not be written.
    """
    try:
        audio_content = base64.b64decode(encoded_string)
        playlist_folder = os.path.join(os.path.dirname(__file__), '../playlist/')
        os.makedirs(playlist_folder, exist_ok=True)
        output_file_path = os.path.join(playlist_folder, output_file_name)
        with open(output_file_path, "wb") as audio_file:
            audio_file.write(audio_content)
        logger.info(f"File saved to {output_file_path}")
    except Exception as e:
        logger.error(f"Failed to write file {output_file_name}: {e}")
        raise