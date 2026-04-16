from flask import Blueprint

recommend_bp = Blueprint('recommend', __name__, url_prefix='/recommendations')

@recommend_bp.route('/')
def list_recommendations():
    """
    瀏覽所有使用者推薦的歌曲 (已審核核准)
    支援 HTTP 方法: GET
    渲染模板: recommend/list.html
    """
    pass

@recommend_bp.route('/new')
def new_recommendation():
    """
    顯示提交推薦歌曲的空白表單
    支援 HTTP 方法: GET
    渲染模板: recommend/form.html
    """
    pass

@recommend_bp.route('/', methods=['POST'])
def create_recommendation():
    """
    接收表單資料，儲存推薦歌曲至資料庫
    支援 HTTP 方法: POST
    成功後重導向至推薦清單或首頁
    """
    pass
