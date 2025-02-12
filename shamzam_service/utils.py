import base64
from flask import current_app, jsonify

def encode_audio_to_base64(audio_file_path):
    """
    Encodes an audio file to a base64 string.
    
    :param audio_file_path: The path to the audio file.
    :return: A base64 encoded string of the audio file.
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            audio_content = audio_file.read()
        return base64.b64encode(audio_content).decode('utf-8')
    except IOError as e:
        current_app.logger.error(f"Failed to read file {audio_file_path}: {e}")
        return None

def decode_base64_to_audio(base64_string, output_file_path):
    """
    Decodes a base64 string back to an audio file.
    
    :param base64_string: The base64 string to decode.
    :param output_file_path: The path where the decoded audio file will be saved.
    :return: None
    """
    try:
        audio_content = base64.b64decode(base64_string)
        with open(output_file_path, "wb") as audio_file:
            audio_file.write(audio_content)
    except IOError as e:
        current_app.logger.error(f"Failed to write file {output_file_path}: {e}")

def response_with_error(message, status_code=400):
    """
    Helper function to format error responses in a consistent manner.
    
    :param message: The error message to return.
    :param status_code: HTTP status code to use for the response, default is 400.
    :return: A Flask response object with JSON formatted error message.
    """
    response = jsonify({'error': message})
    response.status_code = status_code
    return response

def log_error(message):
    """
    Logs an error message to the current app's logger.
    
    :param message: The error message to log.
    """
    current_app.logger.error(message)
