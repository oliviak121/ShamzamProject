from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URLs for the catalogue management service and audio identification service
DATABASE_URL = 'http://localhost:5002'
AUDIO_URL = 'http://localhost:5001'

# Routes
@app.route('/catalogue/add', methods=['POST'])
def add_song() -> jsonify:
    """
    Add a new song to the catalogue.
    
    Returns:
        jsonify: JSON response indicating success or failure.
    """
    # Check if the request is JSON
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 415
    
    song_data = request.json
    
    # Check if the required fields are present
    if not song_data:
        return jsonify({'error': 'No data provided'}), 400
    if 'artist' not in song_data:
        return jsonify({'error': 'Artist is required'}), 400
    if 'title' not in song_data:
        return jsonify({'error': 'Title is required'}), 400
    if 'encoded_song' not in song_data:
        return jsonify({'error': 'Encoded song is required'}), 400
    
    # Check if all fields are strings
    for field, value in song_data.items():
        if not isinstance(value, str):
            return jsonify({'error': f'{field.capitalize()} must be a string'}), 400

    try:
        # Forward the song data to the Catalogue Management Service
        response = requests.post(f'{DATABASE_URL}/add', json=song_data)
    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Catalogue Management Service', 'message': str(e)}), 500

    return jsonify(response.json()), response.status_code


@app.route('/catalogue/delete', methods=['DELETE'])
def delete_song() -> jsonify:
    """
    Delete a song in the catalogue by its artist and title.
    
    Returns:
        jsonify: JSON response indicating success or failure.
    """
    # Check if the request is JSON
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 415
    
    song_data = request.json

    # Check if the required fields are present
    if not song_data:
        return jsonify({'error': 'No data provided'}), 400
    if 'artist' not in song_data:
        return jsonify({'error': 'Artist is required'}), 400
    if 'title' not in song_data:
        return jsonify({'error': 'Title is required'}), 400
    
    # Check if all fields are strings
    for field, value in song_data.items():
        if not isinstance(value, str):
            return jsonify({'error': f'{field.capitalize()} must be a string'}), 400
    
    # Sends the song data to the Catalogue Management Service
    try:
        response = requests.delete(f'{DATABASE_URL}/delete', params={'artist': song_data['artist'], 'title': song_data['title']})
    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Catalogue Management Service', 'message': str(e)}), 500

    return jsonify(response.json()), response.status_code


@app.route('/catalogue/list', methods=['GET'])
def list_songs() -> jsonify:
    """
    List all songs in the catalogue.
    
    Returns:
        jsonify: JSON response containing the list of songs or an error message.
    """
    # Forwards the request to the Catalogue Management Service
    try:
        response = requests.get(f'{DATABASE_URL}/tracks')
    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Catalogue Management Service', 'message': str(e)}), 500
    
    return jsonify(response.json()), response.status_code


@app.route('/catalogue/search', methods=['POST'])
def search_catalogue() -> jsonify:
    """
    Search for a song in the catalogue by artist and title.
    
    Returns:
        jsonify: JSON response containing the song details or an error message.
    """
    # Check if the request is JSON
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 415
    
    song_data = request.json
    print(f'song data: {song_data}')

    # Check if the required fields are present
    if not song_data:
        return jsonify({'error': 'No data provided'}), 400
    if 'artist' not in song_data:
        return jsonify({'error': 'Artist is required'}), 400
    if 'title' not in song_data:
        return jsonify({'error': 'Title is required'}), 400
    
    # Sends the song data to the Catalogue Management Service
    try:
        response = requests.post(f'{DATABASE_URL}/search', json=song_data)

        try:
            response_json = response.json()
        except ValueError:
            return jsonify({'error': 'Invalid JSON response from Catalogue Management Service'}), 500

    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Catalogue Management Service', 'message': str(e)}), 500
    
    return jsonify(response.json()), response.status_code


@app.route('/music/identify', methods=['POST'])
def identify():
    """
    Identify a song by sending a music fragment to the audio identification service and then searching the catalogue for the song data.
    
    Returns:
        jsonify: JSON response containing the identification result or an error message.
    """
    # Check if the request is JSON
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 415
    
    music_fragment = request.json

    # Sends the music fragment to the Music Identification Service to get the song details
    try:
        auddio_response = requests.post(f'{AUDIO_URL}/identify', json=music_fragment)

        detected_artist = None
        detected_title = None
        if auddio_response.status_code == 200:
            detected_artist = auddio_response.json().get('artist')
            detected_title = auddio_response.json().get('title')
        else:
            return jsonify({'error': 'Failed to identify music', 'message': auddio_response.json()}), auddio_response.status_code
        
        # Search the Catalogue Management Service for the detected song
        response = requests.post(f'{DATABASE_URL}/search', json={'artist': detected_artist, 'title': detected_title})
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Music Identification Service', 'message': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, 
            port=5000,
            host='localhost')
