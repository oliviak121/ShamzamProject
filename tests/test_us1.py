import unittest
import requests
import os
from test_helpers import encode_audio_to_base64, clear_database

BASE_URL = "http://localhost:5000"  # URL of the Shamzam service   
file_path = os.path.join(os.path.dirname(__file__), '../music/tracks/Blinding Lights.wav')
encoded_song = encode_audio_to_base64(file_path)
 

class TestAddSongToCatalogue(unittest.TestCase):

    def setUp(self):
        """Clear the database before each test."""
        clear_database()

    def tearDown(self):
        """Clear the database after each test."""
        clear_database()
    
    """Happy path for adding a song."""
    def test_add_song(self):
        data = {
            'artist': 'The Weeknd',
            'title': 'Blinding Lights',
            'encoded_song': encoded_song
        }
        response = requests.post(f"{BASE_URL}/catalogue/add", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Track added successfully', response.json()['message'])

        # Verify the song is in the database
        response = requests.get(f"{BASE_URL}/catalogue/search", json={'artist': 'The Weeknd', 'title': 'Blinding Lights'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Track found', response.json()['message'])

    
    """Unhappy paths for adding a song."""
    def test_add_song_no_artist(self):
        """Unhappy path: Missing artist."""
        data = {
            'title': 'Blinding Lights',
            'encoded_song': encoded_song
        }
        response = requests.post(f"{BASE_URL}/catalogue/add", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Artist is required', response.json()['error'])

    def test_add_song_no_title(self):
        """Unhappy path: Missing title."""
        data = {
            'artist': 'The Weeknd',
            'encoded_song': encoded_song
        }
        response = requests.post(f"{BASE_URL}/catalogue/add", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Title is required', response.json()['error'])

    def test_add_song_already_exists(self):
        """Unhappy path: Track already exists."""
        data = {
            'artist': 'The Weeknd',
            'title': 'Blinding Lights',
            'encoded_song': encoded_song
        }
        # Add the track for the first time
        response = requests.post(f"{BASE_URL}/catalogue/add", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Track added successfully', response.json()['message'])

        # Try to add the same track again
        response = requests.post(f"{BASE_URL}/catalogue/add", json=data)
        self.assertEqual(response.status_code, 409)
        self.assertIn('Track already exists', response.json()['error'])


if __name__ == '__main__':
    unittest.main(debug=True)
