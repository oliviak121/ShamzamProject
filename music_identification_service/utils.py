import requests
import logging
from flask import jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_api_call(url, data):
    """
    Makes a POST request to an external API and handles the response.

    :param url: URL to which the request is to be sent.
    :param data: Data to be sent in the request.
    :return: JSON response from the API.
    """
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return {'error': 'HTTP error occurred', 'message': str(e)}
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error occurred: {e}")
        return {'error': 'Connection error occurred', 'message': str(e)}
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout occurred: {e}")
        return {'error': 'Timeout occurred', 'message': str(e)}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during requests to {url}: {e}")
        return {'error': 'An error occurred during the request', 'message': str(e)}

def format_error(message, status_code=400):
    """
    Formats an error message for JSON responses.

    :param message: Error message to be formatted.
    :param status_code: HTTP status code to accompany the error message.
    :return: A Flask response object with a JSON formatted error message.
    """
    response = jsonify({'error': message})
    response.status_code = status_code
    return response
