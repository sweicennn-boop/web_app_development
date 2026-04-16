from .main import main_bp
from .recommend import recommend_bp
from .admin import admin_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(admin_bp)
