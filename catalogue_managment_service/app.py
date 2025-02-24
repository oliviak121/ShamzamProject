from flask import Flask, request, jsonify
import sqlite3
#from config import DATABASE
from database import create_tables, DATABASE
import base64

app = Flask(__name__)

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

create_tables()

@app.route('/add', methods=['POST'])
def add_track():
    
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
def delete_track():
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
def list_tracks():
    try:
        db = get_db()
        cursor = db.execute('SELECT artist, title FROM tracks')
        tracks = cursor.fetchall()
        print(f'tracks: {tracks}')

        if not tracks:
            return jsonify({'message': 'No tracks found'}), 404
        
        return jsonify({'message': 'Tracks listed', 'tracks' : [{'artist': track['artist'], 'title': track['title']} for track in tracks]}), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to list tracks', 'message': str(e)}), 500
    

@app.route('/search', methods=['GET'])
def search():
    song_data = request.json

    try:
        db = get_db()
        cursor = db.execute('SELECT * FROM tracks WHERE artist = ? AND title = ?', (song_data['artist'], song_data['title']))
        track = cursor.fetchone()

        if not track:
            return jsonify({'error': 'Track not found'}), 404
        
        return jsonify({'message': 'Track found', 'tracks': dict(track)}), 200
    
    except Exception as e:
        return jsonify({'error': 'Database error', 'message': str(e)}), 500


@app.route('/clear_database', methods=['POST'])
def clear_database():
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
