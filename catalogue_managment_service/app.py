from flask import Flask, request, jsonify
import sqlite3
from config import DATABASE

app = Flask(__name__)

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.route('/search', methods=['GET'])
def search():
    artist = request.args.get('artist')
    title = request.args.get('title')
    try:
        db = get_db()
        cursor = db.execute('SELECT * FROM tracks WHERE artist = ? AND title = ?', (artist, title))
        tracks = cursor.fetchall()
        return jsonify([dict(track) for track in tracks]), 200
    except Exception as e:
        return jsonify({'error': 'Database error', 'message': str(e)}), 500

@app.route('/add', methods=['POST'])
def add_track():
    data = request.json
    try:
        db = get_db()
        db.execute('INSERT INTO tracks (artist, title, encoded_song) VALUES (?, ?, ?)',
                   (data['artist'], data['title'], data['encoded_song']))
        db.commit()
        return jsonify({'message': 'Track added successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to add track', 'message': str(e)}), 500


@app.route('/delete/<int:track_id>', methods=['DELETE'])
def delete_track(track_id):
    try:
        db = get_db()
        db.execute('DELETE FROM tracks WHERE id = ?', (track_id,))
        db.commit()
        return jsonify({'message': 'Track deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to delete track', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
