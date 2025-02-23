import sqlite3

DATABASE = 'catalogue.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_tables():
    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artist TEXT NOT NULL,
        title TEXT NOT NULL,
        encoded_song BLOB NOT NULL
    );
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(create_tables_sql)
    db.commit()
    cursor.close()
    db.close()

def query_db(query, args=(), one=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def add_track(artist_name, song_name, song_data):
    db = get_db()
    db.execute('INSERT INTO tracks (artist, title, encoded_song) VALUES (?, ?, ?)',
               [artist_name, song_name, song_data])
    db.commit()

def delete_track(track_id):
    db = get_db()
    db.execute('DELETE FROM tracks WHERE id = ?', [track_id])
    db.commit()

def get_tracks():
    return query_db('SELECT id, artist, title FROM tracks')

if __name__ == '__main__':
    create_tables()
