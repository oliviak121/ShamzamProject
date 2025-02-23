import unittest
import requests
import os
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