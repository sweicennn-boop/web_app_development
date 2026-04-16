from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from ..models.admin import Admin
from ..models.song import Song
import hashlib

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('請先登入管理員帳號！', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """處理管理員登入"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.get_by_username(username)
        if admin:
            # 為了簡易驗證，使用 SHA-256 (實際專案建議用 bcrypt)
            pwd_hash = hashlib.sha256(password.encode()).hexdigest()
            if pwd_hash == admin['password_hash']:
                session['admin_logged_in'] = True
                session['admin_username'] = username
                flash('登入成功！', 'success')
                return redirect(url_for('admin.dashboard'))
                
        flash('帳號或密碼錯誤。', 'danger')
        
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """登出管理員"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('您已成功登出。', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/songs')
@login_required
def dashboard():
    """顯示歌曲管理儀表板"""
    songs = Song.get_all()
    return render_template('admin/dashboard.html', songs=songs)

@admin_bp.route('/songs/new')
@login_required
def new_song():
    """顯示新增歌曲表單"""
    return render_template('admin/song_form.html', song=None)

@admin_bp.route('/songs', methods=['POST'])
@login_required
def create_song():
    """接收新增表單，存入資料庫"""
    title = request.form.get('title')
    artist = request.form.get('artist')
    style = request.form.get('style')
    audio_url = request.form.get('audio_url')
    
    if not title or not artist:
        flash('歌名與歌手為必填欄位！', 'danger')
        return redirect(url_for('admin.new_song'))
        
    Song.create(title, artist, style, audio_url)
    flash('歌曲新增成功！', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/songs/<int:song_id>/edit')
@login_required
def edit_song(song_id):
    """顯示編輯歌曲表單 (預填舊資料)"""
    song = Song.get_by_id(song_id)
    if not song:
        flash('找不到該歌曲', 'danger')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/song_form.html', song=song)

@admin_bp.route('/songs/<int:song_id>/update', methods=['POST'])
@login_required
def update_song(song_id):
    """接收表單，更新指定歌曲資料"""
    title = request.form.get('title')
    artist = request.form.get('artist')
    style = request.form.get('style')
    audio_url = request.form.get('audio_url')
    
    if not title or not artist:
        flash('歌名與歌手為必填欄位！', 'danger')
        return redirect(url_for('admin.edit_song', song_id=song_id))
        
    result = Song.update(song_id, title, artist, style, audio_url)
    if result:
        flash('歌曲更新成功！', 'success')
    else:
        flash('歌曲更新失敗！', 'danger')
        
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/songs/<int:song_id>/delete', methods=['POST'])
@login_required
def delete_song(song_id):
    """刪除指定歌曲"""
    result = Song.delete(song_id)
    if result:
        flash('歌曲已刪除！', 'success')
    else:
        flash('歌曲刪除失敗！', 'danger')
    return redirect(url_for('admin.dashboard'))
