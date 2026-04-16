from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    顯示並處理管理員登入
    GET: 渲染登入表單
    POST: 驗證帳密並設定 session
    渲染模板: admin/login.html
    """
    pass

@admin_bp.route('/logout')
def logout():
    """
    登出管理員，清除 session
    """
    pass

@admin_bp.route('/songs')
def dashboard():
    """
    顯示歌曲管理儀表板（列出所有歌曲）
    渲染模板: admin/dashboard.html
    """
    pass

@admin_bp.route('/songs/new')
def new_song():
    """
    顯示新增歌曲表單
    渲染模板: admin/song_form.html
    """
    pass

@admin_bp.route('/songs', methods=['POST'])
def create_song():
    """
    接收新增表單，存入資料庫
    成功重導向至 /admin/songs
    """
    pass

@admin_bp.route('/songs/<int:song_id>/edit')
def edit_song(song_id):
    """
    顯示編輯歌曲表單 (預填舊資料)
    渲染模板: admin/song_form.html
    """
    pass

@admin_bp.route('/songs/<int:song_id>/update', methods=['POST'])
def update_song(song_id):
    """
    接收表單，更新指定歌曲資料
    成功重導向至 /admin/songs
    """
    pass

@admin_bp.route('/songs/<int:song_id>/delete', methods=['POST'])
def delete_song(song_id):
    """
    刪除指定歌曲
    成功重導向至 /admin/songs
    """
    pass
