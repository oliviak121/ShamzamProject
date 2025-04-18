import unittest
import requests
import os
from unittest.mock import patch
from test_helpers import encode_audio_to_base64, clear_database

BASE_URL = "http://localhost:5000"  # URL of the Shamzam service

class TestListAllSongs(unittest.TestCase):
    def setUp(self):
        """Clear the database before each test."""
        clear_database()

    def tearDown(self):
        """Clear the database after each test."""
        clear_database()

    """Happy path for listing all songs."""
    def test_list_all_songs(self):
        # Add songs to the database
        # Song 1
        file_path1 = os.path.join(os.path.dirname(__file__), '../music/tracks/Blinding Lights.wav')
        response = requests.post(f"{BASE_URL}/catalogue/add", json={
            'artist': 'The Weeknd',
            'title': 'Blinding Lights',
            'encoded_song': encode_audio_to_base64(file_path1)
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Track added successfully', response.json()['message'])

        # Song 2
        file_path2 = os.path.join(os.path.dirname(__file__), '../music/tracks/Don\'t Look Back In Anger.wav')
        response = requests.post(f"{BASE_URL}/catalogue/add", json={
            'artist': 'Oasis',
            'title': 'Don\'t Look Back In Anger',
            'encoded_song': encode_audio_to_base64(file_path2)
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Track added successfully', response.json()['message'])

        # Song 3
        file_path3 = os.path.join(os.path.dirname(__file__), '../music/tracks/Everybody (Backstreet\'s Back) (Radio Edit).wav')
        response = requests.post(f"{BASE_URL}/catalogue/add", json={
            'artist': 'Backstreet Boys',
            'title': 'Everybody (Backstreet\'s Back) (Radio Edit)',
            'encoded_song': encode_audio_to_base64(file_path3)
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Track added successfully', response.json()['message'])

        # List all songs
        response = requests.get(f"{BASE_URL}/catalogue/list")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tracks listed', response.json()['message'])

        tracks = response.json()['tracks']
        self.assertEqual(len(tracks), 3) # Ensure there are exactly 3 tracks

        # Extract the titles from the response
        track_titles = {(track['artist'], track['title']) for track in tracks}

        # Define the expected titles
        expected_titles = {
            ('The Weeknd', 'Blinding Lights'),
            ('Oasis', 'Don\'t Look Back In Anger'),
            ('Backstreet Boys', 'Everybody (Backstreet\'s Back) (Radio Edit)')
        }

        # Checks that the titles in the response match the expected titles
        self.assertEqual(track_titles, expected_titles)  

    
    """Unhappy paths for listing all songs."""
    def test_list_no_songs(self):
        """Unhappy path: No songs in the database."""
        response = requests.get(f"{BASE_URL}/catalogue/list")
        self.assertEqual(response.status_code, 404)
        self.assertIn('No tracks found', response.json()['message'])

    def test_list_invalid_method(self):
        """Unhappy path: Invalid request method."""
        response = requests.post(f"{BASE_URL}/catalogue/list")
        self.assertEqual(response.status_code, 405)
        self.assertIn('Method Not Allowed', response.text)

if __name__ == '__main__':
    unittest.main(debug=True)