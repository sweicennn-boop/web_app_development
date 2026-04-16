from .db import get_db_connection

class Tag:
    @staticmethod
    def create(name, type_name):
        """新增一筆標籤記錄（心情或天氣）"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO tags (name, type) VALUES (?, ?)',
                (name, type_name)
            )
            tag_id = cursor.lastrowid
            conn.commit()
            return tag_id
        except Exception as e:
            print(f"Error creating tag: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """取得所有標籤記錄"""
        try:
            conn = get_db_connection()
            tags = conn.execute('SELECT * FROM tags').fetchall()
            return [dict(row) for row in tags]
        except Exception as e:
            print(f"Error getting all tags: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(tag_id):
        """取得單筆標籤記錄"""
        try:
            conn = get_db_connection()
            tag = conn.execute('SELECT * FROM tags WHERE id = ?', (tag_id,)).fetchone()
            return dict(tag) if tag else None
        except Exception as e:
            print(f"Error getting tag by id: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_type(type_name):
        """根據類型（mood/weather）取得標籤清單"""
        try:
            conn = get_db_connection()
            tags = conn.execute('SELECT * FROM tags WHERE type = ?', (type_name,)).fetchall()
            return [dict(row) for row in tags]
        except Exception as e:
            print(f"Error getting tags by type: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(tag_id, name, type_name):
        """更新單筆標籤記錄"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE tags SET name = ?, type = ? WHERE id = ?',
                (name, type_name, tag_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating tag: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
    
    @staticmethod
    def delete(tag_id):
        """刪除單筆標籤記錄"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM tags WHERE id = ?', (tag_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting tag: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
