import unittest
import requests
import os
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

        # Extract the encoded song data from the response
        encoded_song = response.json()['encoded_song']

        # Decode the encoded song data and save it as a .wav file in the playlist folder
        output_file_name = "found song.wav"
        decode_base64_to_wav(encoded_song, output_file_name)



if __name__ == '__main__':
    unittest.main(debug=True)   