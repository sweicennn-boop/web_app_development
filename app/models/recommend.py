from .db import get_db_connection

class Recommendation:
    @staticmethod
    def create(title, artist, reason=None, submitter_name=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO recommendations (title, artist, reason, submitter_name)
               VALUES (?, ?, ?, ?)''',
            (title, artist, reason, submitter_name)
        )
        rec_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return rec_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        recs = conn.execute('SELECT * FROM recommendations ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(row) for row in recs]

    @staticmethod
    def get_by_id(rec_id):
        conn = get_db_connection()
        rec = conn.execute('SELECT * FROM recommendations WHERE id = ?', (rec_id,)).fetchone()
        conn.close()
        return dict(rec) if rec else None

    @staticmethod
    def get_all_approved():
        conn = get_db_connection()
        recs = conn.execute("SELECT * FROM recommendations WHERE status = 'approved' ORDER BY created_at DESC").fetchall()
        conn.close()
        return [dict(row) for row in recs]

    @staticmethod
    def update_status(rec_id, status):
        conn = get_db_connection()
        conn.execute('UPDATE recommendations SET status = ? WHERE id = ?', (status, rec_id))
        conn.commit()
        conn.close()
        
    @staticmethod
    def delete(rec_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM recommendations WHERE id = ?', (rec_id,))
        conn.commit()
        conn.close()
