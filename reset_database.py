from models import db, User, Book, Rental
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from flask import Flask

# Flask 애플리케이션 생성
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dayeon:dayeon@localhost/my_library'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nahyun:nahyun@localhost/my_library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 데이터베이스 초기화
db.init_app(app)

def reset_database():
    with app.app_context():
        # 기존 데이터 삭제 및 테이블 재생성
        db.drop_all()
        db.create_all()

        # 예시 사용자 추가
        user1 = User(
            username="test_user",
            email="test_user@example.com",
            student_id=12345,
            phone="010-1234-5678",
            department="컴퓨터공학과",
            year=3
        )
        user1.set_password("password")

        user2 = User(
            username="kim_student",
            email="kim@example.com",
            student_id=12346,
            phone="010-9876-5432",
            department="전자공학과",
            year=2
        )
        user2.set_password("kim123")

        user3 = User(
            username="lee_advanced",
            email="lee@example.com",
            student_id=12347,
            phone="010-1234-1111",
            department="기계공학과",
            year=4
        )
        user3.set_password("lee456")

        user4 = User(
            username="park_coder",
            email="park@example.com",
            student_id=12348,
            phone="010-2222-3333",
            department="소프트웨어학과",
            year=1
        )
        user4.set_password("park789")

        user5 = User(
            username="nahyun",
            email="ssalttuck01@gmail.com",
            student_id=20233070,
            phone="010-2639-1569",
            department="AI융합학부",
            year=2
        )
        user5.set_password("1111")

        admin_user = User(
            username="admin",
            email="admin@example.com",
            student_id=0,
            phone="관리자 전화 없음",
            department="관리자",
            year=0
        )
        admin_user.set_password("admin123")

        db.session.add_all([user1, user2, user3, user4, user5, admin_user])

        # 예시 도서 추가
        books = [
            Book(title="(Do it!) HTML+CSS+자바스크립트 웹 표준의 정석", author="고경희", genre="웹디자인/홈페이지", publication_year=2024, isbn="9791163036227", availability=True),
            Book(title="AI 시대의 프로그래머", author="톰 타울리", genre="인공지능", publication_year=2024, isbn="9791169212830", availability=True),
            Book(title="쉽게 풀어쓴 C언어 Express", author="천인국", genre="프로그래밍 언어", publication_year=2023, isbn="9788970506678", availability=True),
            Book(title="밑바닥부터 시작하는 딥러닝", author="사이토 고키", genre="딥러닝/머신러닝", publication_year=2017, isbn="9788968484636", availability=True),
            Book(title="친절한 SQL 튜닝", author="조시형", genre="데이터베이스", publication_year=2018, isbn="9791196395704", availability=True),
            Book(title="클린 코드 Clean Code", author="로버트 C. 마틴", genre="IT교양서", publication_year=2013, isbn="9788966260959", availability=True),
            Book(title="데이터 과학을 위한 통계", author="피터 브루스, 앤드루 브루스, 피터 게데크", genre="자료분석/빅데이터", publication_year=2021, isbn="9791162244180", availability=True),
            Book(title="혼자 공부하는 머신러닝+딥러닝", author="박해선", genre="딥러닝/머신러닝", publication_year=2020, isbn="9791162243664", availability=True),
            Book(title="파이토치 트랜스포머를 활용한 자연어 처리와 컴퓨터비전 심층학습", author="윤대희, 김동화, 송종민, 진현두", genre="딥러닝/머신러닝", publication_year=2023, isbn="9791158394400", availability=True),
            Book(title="Do it! 점프 투 파이썬", author="박응용", genre="프로그래밍 언어", publication_year=2023, isbn="9791163034735", availability=True),
            Book(title="Do it! 점프 투 자바", author="박응용", genre="프로그래밍 언어", publication_year=2023, isbn="9791163034872", availability=True),
            Book(title="Do it! 점프 투 플라스크", author="박응용", genre="프로그래밍 언어", publication_year=2020, isbn="9791163031970", availability=True)
        ]

        db.session.add_all(books)

        # 데이터베이스 커밋
        db.session.commit()
        print("Database has been reset and example data added.")

if __name__ == "__main__":
    reset_database()
