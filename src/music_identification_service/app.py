from flask import Flask, request, jsonify
import requests
import os
import base64

app = Flask(__name__)

# Get the Audd.io API key from the environment
audd_api_key = os.environ['AUDD_API_KEY'] 

# Routes
@app.route('/identify', methods=['POST'])
def identify() -> jsonify:
    """
    Identify the artist and title of a music fragment by sending it to the Audd.io API.
    
    Returns:
        jsonify: JSON response containing the identification result or an error message.
    """
    # Check if the request is JSON
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 415
    
    encoded_content = request.json.get('encoded_fragment')
    
    # Check if the encoded_content is a valid Base64 encoded string
    try:
        base64.b64decode(encoded_content, validate=True)
    except Exception:
        return jsonify({'error': 'Invalid content format: must be Base64 encoded string'}), 400
    
    try:
        # Prepare the data payload including the API key
        data = {
            'api_token': audd_api_key,
            'audio': encoded_content
        }

        # Make the API call to Audd.io
        response = requests.post('https://api.audd.io/', data=data)

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
            return jsonify({'error': 'Audd.io unable to find matches for fragment in their database.'}), 404

    except Exception as e:
        return jsonify({'error': 'Failed to process identification', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, 
            port=5001,
            host='localhost')
