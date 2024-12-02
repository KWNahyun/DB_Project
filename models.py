from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))

    student_id = db.Column(db.Integer, unique=True, nullable=False)  # 학번
    phone = db.Column(db.String(20), nullable=False)  # 전화번호
    department = db.Column(db.String(100), nullable=False)  # 학과
    year = db.Column(db.Integer, nullable=False)  # 학년

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(50), unique=True, nullable=False)
    availability = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Book {self.title}>'

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 외래 키 (학생 정보 테이블)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)  # 외래 키 (도서 정보 테이블)
    rental_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    actual_return_date = db.Column(db.Date)
    status = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', backref=db.backref('rentals', lazy=True))
    book = db.relationship('Book', backref=db.backref('rentals', lazy=True))

    def __repr__(self):
        return f'<Rental {self.book.title} by {self.user.username}>'