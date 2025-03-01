from flask import Flask, request, jsonify
import sqlite3
from sqlite3 import Connection, Cursor

app = Flask(__name__)

DATABASE = 'catalogue.db'

# Helper functions:
def get_db() -> Connection:
    """
    Establish a connection to the SQLite database.
    
    Returns:
        Connection: SQLite database connection object.
    """
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def create_tables() -> None:
    """
    Create the 'tracks' table in the database if it does not already exist.
    """
    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS tracks (
        artist TEXT NOT NULL,
        title TEXT NOT NULL,
        encoded_song BLOB NOT NULL,
        PRIMARY KEY (artist, title)
    );
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(create_tables_sql)
    db.commit()
    cursor.close()
    db.close()

# Initialise the database
create_tables()

# Routes
@app.route('/add', methods=['POST'])
def add_track() -> jsonify:
    """
    Add a new track to the database.
    
    Returns:
        jsonify: JSON response indicating success or failure.
    """
    # Get the song data from the request
    data = request.json

    try:
        db = get_db()
        # Check if the track already exists
        cursor = db.execute('SELECT * FROM tracks WHERE artist = ? AND title = ?', (data['artist'], data['title']))
        existing_track = cursor.fetchone()
        if existing_track:
            return jsonify({'error': 'Track already exists'}), 409
        
        # Insert the new track
        db.execute('INSERT INTO tracks (artist, title, encoded_song) VALUES (?, ?, ?)',
                   (data['artist'], data['title'], data['encoded_song']))
        db.commit()
        return jsonify({'message': 'Track added successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to add track', 'message': str(e)}), 500


@app.route('/delete', methods=['DELETE'])
def delete_track() -> jsonify:
    """
    Delete a track from the database.
    
    Returns:
        jsonify: JSON response indicating success or failure.
    """
    artist = request.args.get('artist')
    title = request.args.get('title')

    try:
        db = get_db()

        # Check if the track exists
        cursor = db.execute('SELECT * FROM tracks WHERE artist = ? AND title = ?', (artist, title))
        track = cursor.fetchone()
        if not track:
            return jsonify({'error': 'Track not found'}), 404
        
        # Delete the track
        db.execute('DELETE FROM tracks WHERE artist = ? AND title = ?', (artist, title))
        db.commit()
        return jsonify({'message': 'Track deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to delete track', 'message': str(e)}), 500
    

@app.route('/tracks', methods=['GET'])
def list_tracks() -> jsonify:
    """
    List all tracks in the database.
    
    Returns:
        jsonify: JSON response containing the list of tracks or an error message.
    """
    try:
        db = get_db()
        cursor = db.execute('SELECT artist, title FROM tracks')
        tracks = cursor.fetchall()

        if not tracks:
            return jsonify({'message': 'No tracks found'}), 404
        
        return jsonify({'message': 'Tracks listed', 'tracks' : [{'artist': track['artist'], 'title': track['title']} for track in tracks]}), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to list tracks', 'message': str(e)}), 500
    

@app.route('/search', methods=['POST'])
def search() -> jsonify:
    """
    Search for a track in the database by artist and title.
    
    Returns:
        jsonify: JSON response containing the track details - including encoded song, or an error message.
    """
    song_data = request.json

    try:
        db = get_db()
        cursor = db.execute('SELECT * FROM tracks WHERE artist = ? AND title = ?', (song_data['artist'], song_data['title']))
        track = cursor.fetchone()

        if not track:
            return jsonify({'error': 'Track not found in catalogue'}), 404
        
        return jsonify({'message': 'Track found', 'artist': track['artist'], 'title': track['title'], 'encoded_song': track['encoded_song']}), 200
    
    except Exception as e:
        return jsonify({'error': 'Database error', 'message': str(e)}), 500


@app.route('/clear_database', methods=['DELETE'])
def clear_database() -> jsonify:
    """
    Clear all tracks from the database.
    
    Returns:
        jsonify: JSON response indicating success or failure.
    """
    try:
        db = get_db()
        db.execute('DELETE FROM tracks')  
        db.commit()
        db.close()
        return jsonify({'message': 'Database cleared successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to clear database', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, 
            port=5002,
            host='localhost')
