from flask import Flask, request, jsonify, redirect, url_for
import requests
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Shamzam!"

@app.route('/encode', methods=['POST'])
def encode():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    try:
        file = request.files['file']
        content = file.read()
        encoded_content = base64.b64encode(content).decode('utf-8')
        return jsonify({'encoded_content': encoded_content}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to encode file', 'message': str(e)}), 500

@app.route('/identify', methods=['POST'])
def identify():
    encoded_content = request.json.get('encoded_content')
    try:
        response = requests.post('http://music_identification_service/identify', json={'encoded_content': encoded_content})
        if response.status_code != 200:
            raise Exception('Failed to identify the track')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Music Identification Service', 'message': str(e)}), 500

@app.route('/catalogue/search', methods=['POST'])
def search_catalogue():
    artist = request.json.get('artist')
    title = request.json.get('title')
    try:
        response = requests.get(f'http://catalogue_management_service/search?artist={artist}&title={title}')
        if response.status_code != 200:
            raise Exception('No match found')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': 'Failed to communicate with Catalogue Management Service', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
