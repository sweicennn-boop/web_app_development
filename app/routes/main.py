from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.song import Song
from ..models.tag import Tag

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示首頁（心情與天氣按鈕介面）
    支援 HTTP 方法: GET
    渲染模板: index.html
    """
    moods = Tag.get_by_type('mood')
    weathers = Tag.get_by_type('weather')
    return render_template('index.html', moods=moods, weathers=weathers)

@main_bp.route('/result')
def result():
    """
    根據 query string 參數隨機選擇歌曲並顯示選歌結果
    支援 HTTP 方法: GET
    取得參數: type (mood/weather), tag (標籤名稱)
    渲染模板: result.html
    """
    tag_type = request.args.get('type')
    tag_name = request.args.get('tag')
    
    if not tag_type or not tag_name:
        flash('請選擇一個心情或天氣標籤！', 'warning')
        return redirect(url_for('main.index'))
        
    song = Song.get_random_by_tag(tag_name, tag_type)
    
    if not song:
        flash(f'抱歉，目前資料庫中沒有符合「{tag_name}」情境的歌曲。', 'info')
        return redirect(url_for('main.index'))
        
    return render_template('result.html', song=song, current_type=tag_type, current_tag=tag_name)
