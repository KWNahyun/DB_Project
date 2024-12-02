from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from login_manager import login_manager
from controllers import setup_routes

app = Flask(__name__)

# 구성 설정
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dayeon:dayeon@localhost/my_library'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nahyun:nahyun@localhost/my_library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

# 데이터베이스 및 로그인 관리자 초기화
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# 라우팅 설정
setup_routes(app)

# 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)  # 디버그 모드 강제 활성화