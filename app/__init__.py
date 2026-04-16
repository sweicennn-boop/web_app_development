from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 註冊 Blueprints
    from .routes import register_blueprints
    register_blueprints(app)
    
    return app

def init_db():
    from .models.db import get_db_connection
    conn = get_db_connection()
    
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    
    conn.commit()
    conn.close()
    print("Database initialized successfully from schema.sql.")
