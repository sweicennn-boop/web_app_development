from .db import get_db_connection

class Song:
    @staticmethod
    def create(title, artist, style=None, audio_url=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO songs (title, artist, style, audio_url)
               VALUES (?, ?, ?, ?)''',
            (title, artist, style, audio_url)
        )
        song_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return song_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        songs = conn.execute('SELECT * FROM songs').fetchall()
        conn.close()
        return [dict(row) for row in songs]

    @staticmethod
    def get_by_id(song_id):
        conn = get_db_connection()
        song = conn.execute('SELECT * FROM songs WHERE id = ?', (song_id,)).fetchone()
        conn.close()
        return dict(song) if song else None

    @staticmethod
    def update(song_id, title, artist, style=None, audio_url=None):
        conn = get_db_connection()
        conn.execute(
            '''UPDATE songs SET title = ?, artist = ?, style = ?, audio_url = ? WHERE id = ?''',
            (title, artist, style, audio_url, song_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(song_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM songs WHERE id = ?', (song_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_random_by_tag(tag_name, tag_type):
        conn = get_db_connection()
        query = '''
            SELECT s.* FROM songs s
            JOIN song_tags st ON s.id = st.song_id
            JOIN tags t ON st.tag_id = t.id
            WHERE t.name = ? AND t.type = ?
            ORDER BY RANDOM() LIMIT 1
        '''
        song = conn.execute(query, (tag_name, tag_type)).fetchone()
        conn.close()
        return dict(song) if song else None
