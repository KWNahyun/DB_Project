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

        db.session.add_all([user1, user2, user3, user4, user5])

        # 예시 도서 추가
        book1 = Book(
            title="컴퓨터 구조 및 설계: ARM",
            author="David A. Patterson",
            genre="IT",
            publication_year=2018,
            isbn="9788964213452",
            availability=True
        )
        book2 = Book(
            title="파이썬 프로그래밍 기초",
            author="Guido van Rossum",
            genre="Programming",
            publication_year=2020,
            isbn="9781234567890",
            availability=False
        )
        db.session.add_all([book1, book2])

        # 예시 대출 기록 추가
        rental1 = Rental(
            user_id=1,  # user1 ID
            book_id=2,  # book2 ID
            rental_date=datetime.now(),
            return_date=datetime.now() + timedelta(days=14),
            status="대출 중"
        )
        db.session.add(rental1)

        # 데이터베이스 커밋
        db.session.commit()
        print("Database has been reset and example data added.")

if __name__ == "__main__":
    reset_database()
