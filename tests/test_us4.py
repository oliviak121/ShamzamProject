import unittest
import requests
import os
from unittest.mock import patch
from test_helpers import encode_audio_to_base64, clear_database, decode_base64_to_wav

BASE_URL = "http://localhost:5000"  # URL of the Shamzam service
FRAGMENT_FOLDER = os.path.join(os.path.dirname(__file__), '../music/fragments')


class TestIdentifyFragment(unittest.TestCase):
    def setUp(self):
        """Clear the database before each test."""
        clear_database()

    def tearDown(self):
        """Clear the database after each test."""
        clear_database()

    """Happy path for identifying a music fragment."""
    def test_identify_music_fragment(self):
        # Add a song to the catalogue 
        file_path1 = os.path.join(os.path.dirname(__file__), '../music/tracks/Blinding Lights.wav')
        data = {
            'artist': 'The Weeknd',
            'title': 'Blinding Lights',
            'encoded_song': encode_audio_to_base64(file_path1)
        }
        response = requests.post(f"{BASE_URL}/catalogue/add", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Track added successfully', response.json()['message'])

        # Path to the music fragment
        fragment_path = os.path.join(FRAGMENT_FOLDER, '~Blinding Lights.wav')

        # Encode the fragment to base64
        encoded_fragment = encode_audio_to_base64(fragment_path)

        # Send the encoded fragment to the Shamzam service
        response = requests.post(f"{BASE_URL}/music/identify", json={'encoded_fragment': encoded_fragment})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Track found', response.json()['message'])

        # Extract the encoded full track from the response
        encoded_track = response.json()['encoded_song']
        found_artist = response.json()['artist']
        found_title = response.json()['title']

        # Decode the encoded song data and save it as a .wav file in the playlist folder
        output_file_name = f"{found_artist}-{found_title}.wav"
        decode_base64_to_wav(encoded_track, output_file_name)

    """Unhappy paths for identifying a music fragment."""
    def test_fragment_not_in_catalogue(self):
        """"Unhappy path: Attempt to identify a fragment that is not in the catalogue."""
        # Path to the music fragment
        fragment_path = os.path.join(FRAGMENT_FOLDER, '~Blinding Lights.wav')

        # Encode the fragment to base64
        encoded_fragment = encode_audio_to_base64(fragment_path)

        # Send the encoded fragment to the Shamzam service
        response = requests.post(f"{BASE_URL}/music/identify", json={'encoded_fragment': encoded_fragment})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Track not found in catalogue', response.json()['error'])

    def test_fragment_not_encoded_or_invalid_type(self):
        """Unhappy path: Attempt to identify a fragment with an invalid data type."""
        response = requests.post(f"{BASE_URL}/music/identify", json={'encoded_fragment': 'not_encoded'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid content format: must be Base64 encoded string', response.json()['message']['error'])

        response = requests.post(f"{BASE_URL}/music/identify", json={'encoded_fragment': 123})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid content format: must be Base64 encoded string', response.json()['message']['error'])

    @patch('requests.post')
    def test_identify_api_failure(self, mock_post):
        """Unhappy path: API call to Audd.io failure."""
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = {'error': 'API call failed'}

        fragment_path = os.path.join(FRAGMENT_FOLDER, '~Blinding Lights.wav')
        encoded_fragment = encode_audio_to_base64(fragment_path)
        response = requests.post(f"{BASE_URL}/music/identify", json={'encoded_fragment': encoded_fragment})

        self.assertEqual(response.status_code, 500)
        self.assertIn('API call failed', response.json()['error'])
    

if __name__ == '__main__':
    unittest.main(debug=True)   