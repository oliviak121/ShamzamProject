import unittest
import requests
import os
from test_helpers import encode_audio_to_base64, clear_database

BASE_URL = "http://localhost:5000"  # URL of the Shamzam service   
file_path = os.path.join(os.path.dirname(__file__), '../music/tracks/Blinding Lights.wav')
encoded_song = encode_audio_to_base64(file_path)


class RemoveSongFromCatalogue(unittest.TestCase): 
    def setUp(self):
        """Clear the database before each test."""
        clear_database()

    def tearDown(self):
        """Clear the database after each test."""
        clear_database()

    def test_remove_song(self):
        """Happy path for removing a song."""
        data = {
            'artist': 'The Weeknd',
            'title': 'Blinding Lights',
            'encoded_song': encoded_song
        }
        # Add the song to the database
        response = requests.post(f"{BASE_URL}/catalogue/add", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Track added successfully', response.json()['message'])

        # Delete the song from the database
        response = requests.delete(f"{BASE_URL}/catalogue/delete", json={'artist': 'The Weeknd', 'title': 'Blinding Lights'})
        print(f"Delete response status code: {response.status_code}")
        print(f"Delete response text: {response.text}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Track deleted successfully', response.json()['message'])

        # Verify the song is actually deleted
        response = requests.post(f"{BASE_URL}/catalogue/search", json={'artist': 'The Weeknd', 'title': 'Blinding Lights'})
        print(f"Verify delete response status code: {response.status_code}")
        print(f"Verify delete response text: {response.text}")
        self.assertEqual(response.status_code, 404)
        self.assertIn('Track not found', response.json()['error'])


if __name__ == '__main__':
    unittest.main(debug=True)