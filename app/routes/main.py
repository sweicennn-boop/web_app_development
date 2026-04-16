from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示首頁（心情與天氣按鈕介面）
    支援 HTTP 方法: GET
    渲染模板: index.html
    """
    pass

@main_bp.route('/result')
def result():
    """
    根據 query string 參數隨機選擇歌曲並顯示選歌結果
    支援 HTTP 方法: GET
    取得參數: type (mood/weather), tag (標籤名稱)
    渲染模板: result.html
    """
    pass
