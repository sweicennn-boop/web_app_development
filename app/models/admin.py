from .db import get_db_connection

class Admin:
    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
        conn.close()
        return dict(admin) if admin else None

    @staticmethod
    def create(username, password_hash):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO admins (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        admin_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return admin_id
