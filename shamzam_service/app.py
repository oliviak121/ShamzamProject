from flask import Flask, request, jsonify, redirect, url_for
import requests
import base64

app = Flask(__name__)

DATABASE_URL = 'http://localhost:5002'
AUDIO_URL = 'http://localhost:5001'

@app.route('/')
def index():
    return "Welcome to Shamzam!"

@app.route('/identify', methods=['POST'])
def identify():
    encoded_content = request.json.get('encoded_content')
    if not encoded_content:
        return jsonify({'error': 'No encoded content provided'}), 400
    
    try:
        response = requests.post(AUDIO_URL, json={'encoded_content': encoded_content})
        if response.status_code != 200:
            raise Exception('Failed to identify the track')
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Music Identification Service', 'message': str(e)}), 500

@app.route('/catalogue/search', methods=['POST'])
def search_catalogue():
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
    
    # Sends the song data to the Catalogue Management Service
    try:
        response = requests.get(f'{DATABASE_URL}/search', json=song_data)
    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Catalogue Management Service', 'message': str(e)}), 500
    
    return jsonify(response.json()), response.status_code


@app.route('/catalogue/add', methods=['POST'])
def add_song():
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

    # Sends the song data to the Catalogue Management Service
    try:
        response = requests.post(f'{DATABASE_URL}/add', json=song_data)
    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Catalogue Management Service', 'message': str(e)}), 500

    return jsonify(response.json()), response.status_code


@app.route('/catalogue/delete', methods=['DELETE'])
def delete_song():
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
    
    # Sends the song data to the Catalogue Management Service
    try:
        response = requests.delete(f'{DATABASE_URL}/delete', params={'artist': song_data['artist'], 'title': song_data['title']})
    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Catalogue Management Service', 'message': str(e)}), 500

    return jsonify(response.json()), response.status_code


@app.route('/catalogue/list', methods=['GET'])
def list_songs():
    try:
        response = requests.get(f'{DATABASE_URL}/list')
        if response.status_code == 200:
            return jsonify(response.json()), 200
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return jsonify({'error': 'Catalogue Management Service error', 'message': str(e)}), e.response.status_code
    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Catalogue Management Service', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, 
            port=5000,
            host='localhost')
