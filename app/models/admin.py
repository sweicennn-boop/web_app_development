from .db import get_db_connection

class Admin:
    @staticmethod
    def create(username, password_hash):
        """建立管理員帳號"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO admins (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )
            admin_id = cursor.lastrowid
            conn.commit()
            return admin_id
        except Exception as e:
            print(f"Error creating admin: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """取得所有管理員記錄"""
        try:
            conn = get_db_connection()
            admins = conn.execute('SELECT * FROM admins').fetchall()
            return [dict(row) for row in admins]
        except Exception as e:
            print(f"Error getting all admins: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(admin_id):
        """取得單筆管理員記錄"""
        try:
            conn = get_db_connection()
            admin = conn.execute('SELECT * FROM admins WHERE id = ?', (admin_id,)).fetchone()
            return dict(admin) if admin else None
        except Exception as e:
            print(f"Error getting admin by id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_username(username):
        """透過帳號名稱取得管理員記錄 (登入用)"""
        try:
            conn = get_db_connection()
            admin = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
            return dict(admin) if admin else None
        except Exception as e:
            print(f"Error getting admin by username: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(admin_id, username, password_hash):
        """更新管理員帳號密碼"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE admins SET username = ?, password_hash = ? WHERE id = ?',
                (username, password_hash, admin_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating admin: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(admin_id):
        """刪除管理員帳號"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM admins WHERE id = ?', (admin_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting admin: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
