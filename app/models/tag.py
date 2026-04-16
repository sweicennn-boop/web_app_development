from .db import get_db_connection

class Tag:
    @staticmethod
    def create(name, type):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tags (name, type) VALUES (?, ?)',
            (name, type)
        )
        tag_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return tag_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        tags = conn.execute('SELECT * FROM tags').fetchall()
        conn.close()
        return [dict(row) for row in tags]

    @staticmethod
    def get_by_id(tag_id):
        conn = get_db_connection()
        tag = conn.execute('SELECT * FROM tags WHERE id = ?', (tag_id,)).fetchone()
        conn.close()
        return dict(tag) if tag else None

    @staticmethod
    def get_by_type(type_name):
        conn = get_db_connection()
        tags = conn.execute('SELECT * FROM tags WHERE type = ?', (type_name,)).fetchall()
        conn.close()
        return [dict(row) for row in tags]
    
    @staticmethod
    def delete(tag_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM tags WHERE id = ?', (tag_id,))
        conn.commit()
        conn.close()
