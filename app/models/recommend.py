from .db import get_db_connection

class Recommendation:
    @staticmethod
    def create(title, artist, reason=None, submitter_name=None):
        """新增一筆使用者推薦記錄"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO recommendations (title, artist, reason, submitter_name)
                   VALUES (?, ?, ?, ?)''',
                (title, artist, reason, submitter_name)
            )
            rec_id = cursor.lastrowid
            conn.commit()
            return rec_id
        except Exception as e:
            print(f"Error creating recommendation: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """取得所有推薦記錄"""
        try:
            conn = get_db_connection()
            recs = conn.execute('SELECT * FROM recommendations ORDER BY created_at DESC').fetchall()
            return [dict(row) for row in recs]
        except Exception as e:
            print(f"Error getting all recommendations: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(rec_id):
        """取得單筆推薦記錄"""
        try:
            conn = get_db_connection()
            rec = conn.execute('SELECT * FROM recommendations WHERE id = ?', (rec_id,)).fetchone()
            return dict(rec) if rec else None
        except Exception as e:
            print(f"Error getting recommendation by id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all_approved():
        """取得所有已審核通過的推薦記錄"""
        try:
            conn = get_db_connection()
            recs = conn.execute("SELECT * FROM recommendations WHERE status = 'approved' ORDER BY created_at DESC").fetchall()
            return [dict(row) for row in recs]
        except Exception as e:
            print(f"Error getting approved recommendations: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(rec_id, title, artist, reason=None, submitter_name=None):
        """更新推薦記錄內容"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE recommendations SET title = ?, artist = ?, reason = ?, submitter_name = ? WHERE id = ?',
                (title, artist, reason, submitter_name, rec_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating recommendation: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update_status(rec_id, status):
        """更新推薦記錄狀態 (pending/approved/rejected)"""
        try:
            conn = get_db_connection()
            conn.execute('UPDATE recommendations SET status = ? WHERE id = ?', (status, rec_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating recommendation status: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
        
    @staticmethod
    def delete(rec_id):
        """刪除單筆推薦記錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM recommendations WHERE id = ?', (rec_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting recommendation: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
