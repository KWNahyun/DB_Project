#./app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # 블루프린트 등록
    from app.main.index import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
