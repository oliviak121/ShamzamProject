from flask import Flask, request, jsonify
import requests
import os
import base64

audd_api_key = os.environ['AUDD_API_KEY']

app = Flask(__name__)

@app.route('/identify', methods=['POST'])
def identify():
    encoded_content = request.json.get('encoded_fragment')
    
    # Check if the encoded_content is a valid Base64 encoded string
    try:
        base64.b64decode(encoded_content, validate=True)
    except Exception:
        return jsonify({'error': 'Invalid content format: must be Base64 encoded string'}), 400
    
    # Decode the fragment to get ready to send to Audd.io
    decoded_wav = base64.b64decode(encoded_content)
    
    try:
        # Prepare the data payload including the API key
        key = {'api_token': audd_api_key  }
        files = {"file" : ("fragment.wav", decoded_wav, "audio/wav")}
        
        # Make the API call to Audd.io
        response = requests.post('https://api.audd.io/', data=key, files=files)

        # Handle rate limit response
        if response.status_code == 429:
            return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
        
        # Handle other API errors if any
        if response.status_code != 200:
            return jsonify({'error': 'API call failed', 'status_code': response.status_code}), response.status_code

        # Parse the JSON response from Audd.io
        audd_response = response.json()

        # Check if a result exists
        if 'result' in audd_response and audd_response['result']:
            result = audd_response['result']
            artist = result.get('artist')
            title = result.get('title')

            # Return the result to the Shamzam service
            return jsonify({'artist': artist, 'title': title}), 200
        
        else:
            return jsonify({'error': 'Track not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Failed to process identification', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, 
            port=5001,
            host='localhost')
