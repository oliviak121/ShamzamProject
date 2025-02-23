from flask import Flask, request, jsonify
import requests
import os

audd_api_key = os.environ['AUDD_API_KEY']

app = Flask(__name__)

@app.route('/identify', methods=['POST'])
def identify():
    encoded_content = request.json.get('encoded_content')

    if not encoded_content:
        return jsonify({'error': 'No encoded_content provided'}), 400
    
    try:
        # Prepare the data payload including the API key
        data = {
            'api_token': audd_api_key,
            'audio': encoded_content,
            'return': 'music'  
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
        data = response.json()

        # Check if a result exists
        if 'result' in data and data['result']:
            result = data['result']  
            return jsonify({'artist': result.get('artist'), 'title': result.get('title')}), 200
        else:
            return jsonify({'message': 'No results found'}), 404

    except Exception as e:
        return jsonify({'error': 'Failed to process identification', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, 
            port=5001,
            host='localhost')
