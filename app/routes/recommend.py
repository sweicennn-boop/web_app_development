from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.recommend import Recommendation

recommend_bp = Blueprint('recommend', __name__, url_prefix='/recommendations')

@recommend_bp.route('/')
def list_recommendations():
    """
    瀏覽所有使用者推薦的歌曲 (已審核核准)
    支援 HTTP 方法: GET
    渲染模板: recommend/list.html
    """
    recs = Recommendation.get_all_approved()
    return render_template('recommend/list.html', recommendations=recs)

@recommend_bp.route('/new')
def new_recommendation():
    """
    顯示提交推薦歌曲的空白表單
    支援 HTTP 方法: GET
    渲染模板: recommend/form.html
    """
    return render_template('recommend/form.html')

@recommend_bp.route('/', methods=['POST'])
def create_recommendation():
    """
    接收表單資料，儲存推薦歌曲至資料庫
    支援 HTTP 方法: POST
    成功後重導向至推薦清單或首頁
    """
    title = request.form.get('title')
    artist = request.form.get('artist')
    reason = request.form.get('reason')
    submitter_name = request.form.get('submitter_name')
    
    if not title or not artist:
        flash('「歌名」與「歌手」為必填欄位！', 'danger')
        return redirect(url_for('recommend.new_recommendation'))
        
    rec_id = Recommendation.create(title, artist, reason, submitter_name)
    if rec_id:
        flash('感謝你的推薦！我們會在審核後將其加入清單。', 'success')
        return redirect(url_for('recommend.list_recommendations'))
    else:
        flash('伺服器發生錯誤，推薦失敗，請稍後再試。', 'danger')
        return redirect(url_for('recommend.new_recommendation'))
