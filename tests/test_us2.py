import unittest
import requests
import os
from test_helpers import encode_audio_to_base64, clear_database

BASE_URL = "http://localhost:5000"  # URL of the Shamzam service   
file_path = os.path.join(os.path.dirname(__file__), '../music/tracks/Blinding Lights.wav')
encoded_song = encode_audio_to_base64(file_path)


class TestRemoveSongFromCatalogue(unittest.TestCase): 
    def setUp(self):
        """Clear the database before each test."""
        clear_database()

    def tearDown(self):
        """Clear the database after each test."""
        clear_database()

    """Happy path for removing a song."""
    def test_remove_song(self):
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
        self.assertEqual(response.status_code, 200)
        self.assertIn('Track deleted successfully', response.json()['message'])

        # Verify the song is actually deleted
        response = requests.get(f"{BASE_URL}/catalogue/search", json={'artist': 'The Weeknd', 'title': 'Blinding Lights'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Track not found', response.json()['error'])

    
    """Unhappy paths for removing a song."""
    def test_remove_non_existent_song(self):
        """Unhappy path: Attempt to delete a non-existent song."""
        response = requests.delete(f"{BASE_URL}/catalogue/delete", json={'artist': 'Non Existent Artist', 'title': 'Non Existent Title'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Track not found', response.json()['error'])

    def test_remove_song_no_artist(self):
        """Unhappy path: Missing artist in the delete request."""
        response = requests.delete(f"{BASE_URL}/catalogue/delete", json={'title': 'Blinding Lights'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Artist is required', response.json()['error'])

    def test_remove_song_invalid_title_type(self):
        """Unhappy path: Invalid data type for title."""
        response = requests.delete(f"{BASE_URL}/catalogue/delete", json={'artist': 'The Weeknd', 'title': 123})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Title must be a string', response.json()['error'])


if __name__ == '__main__':
    unittest.main(debug=True)