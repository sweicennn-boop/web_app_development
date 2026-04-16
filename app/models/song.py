from .db import get_db_connection

class Song:
    @staticmethod
    def create(title, artist, style=None, audio_url=None):
        """新增一筆歌曲記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO songs (title, artist, style, audio_url)
                   VALUES (?, ?, ?, ?)''',
                (title, artist, style, audio_url)
            )
            song_id = cursor.lastrowid
            conn.commit()
            return song_id
        except Exception as e:
            print(f"Error creating song: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """取得所有歌曲記錄"""
        try:
            conn = get_db_connection()
            songs = conn.execute('SELECT * FROM songs').fetchall()
            return [dict(row) for row in songs]
        except Exception as e:
            print(f"Error getting all songs: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(song_id):
        """取得單筆歌曲記錄"""
        try:
            conn = get_db_connection()
            song = conn.execute('SELECT * FROM songs WHERE id = ?', (song_id,)).fetchone()
            return dict(song) if song else None
        except Exception as e:
            print(f"Error getting song by id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(song_id, title, artist, style=None, audio_url=None):
        """更新單筆歌曲記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                '''UPDATE songs SET title = ?, artist = ?, style = ?, audio_url = ? WHERE id = ?''',
                (title, artist, style, audio_url, song_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating song: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(song_id):
        """刪除單筆歌曲記錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM songs WHERE id = ?', (song_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting song: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_random_by_tag(tag_name, tag_type):
        """根據標籤（心情或天氣）隨機取得一首對應的歌曲"""
        try:
            conn = get_db_connection()
            query = '''
                SELECT s.* FROM songs s
                JOIN song_tags st ON s.id = st.song_id
                JOIN tags t ON st.tag_id = t.id
                WHERE t.name = ? AND t.type = ?
                ORDER BY RANDOM() LIMIT 1
            '''
            song = conn.execute(query, (tag_name, tag_type)).fetchone()
            return dict(song) if song else None
        except Exception as e:
            print(f"Error getting random song by tag: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()
