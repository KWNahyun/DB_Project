from flask import render_template, request, jsonify, abort, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Book, Rental
from datetime import datetime
from login_manager import login_manager

def setup_routes(app):

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return '도서 대여 관리 시스템'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user = User.query.filter_by(username=request.form['username']).first()
            if user and user.check_password(request.form['password']):
                login_user(user)
                return jsonify({'message': '로그인을 성공하였습니다. 도서 목록 페이지로 이동합니다.'}), 200
            return jsonify({'error': '아이디가 없거나 패스워드가 다릅니다.'}), 401
        return redirect(url_for('home'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            # 회원가입 폼에서 입력받은 데이터 가져오기
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            student_id = request.form['student_id']
            phone = request.form['phone']
            department = request.form['department']
            year = request.form['year']

            # 중복 사용자 체크
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                return jsonify({'error': '사용자 이름 또는 이메일이 이미 사용 중입니다.'}), 400

            # 새 사용자 생성
            user = User(
                username=username,
                email=email,
                student_id=student_id,
                phone=phone,
                department=department,
                year=year
            )
            user.set_password(password)  # 비밀번호 해시 설정

            try:
                db.session.add(user)
                db.session.commit()
                return jsonify({'message': '회원가입이 성공하였습니다. 기입한 아이디와 패스워드로 로그인할 수 있습니다.'}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': '회원가입 중 오류가 발생했습니다. 다시 시도해주세요.'}), 500

        return redirect(url_for('home'))

    @app.route('/library')
    @login_required
    def library():
        books = Book.query.all()
        return render_template('library.html', books=books)

    @app.route('/rent/<int:book_id>', methods=['POST'])
    @login_required
    def rent_book(book_id):
        book = Book.query.get(book_id)
        if book and book.availability:
            book.availability = False
            rental = Rental(
                user_id=current_user.id,
                book_id=book.id,
                rental_date=datetime.now(),
                return_date=datetime.now(),
                status='대출 중'
            )
            db.session.add(rental)
            db.session.commit()
            return redirect(url_for('library'))
        return redirect(url_for('library'))

    @app.route('/return/<int:book_id>', methods=['POST'])
    @login_required
    def return_book(book_id):
        book = Book.query.get(book_id)
        if book:
            rental = Rental.query.filter_by(book_id=book.id, user_id=current_user.id, status='대출 중').first()
            if rental:
                book.availability = True
                rental.actual_return_date = datetime.now()
                rental.status = '반납 완료'
                db.session.commit()
                return redirect(url_for('library'))
        return redirect(url_for('library'))

    @app.route('/mypage')
    @login_required
    def mypage():
        rentals = Rental.query.filter_by(user_id=current_user.id).all()
        return render_template('mypage.html', user=current_user, rentals=rentals)

    @app.route('/add_book', methods=['GET'])
    @login_required
    def add_book():
        return render_template('add_book.html')

    @app.route('/submit_book', methods=['POST'])
    @login_required
    def submit_book():
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        publication_year = request.form['publication_year']
        isbn = request.form['isbn']
        availability = bool(int(request.form['availability']))

        # 도서 등록
        new_book = Book(
            title=title,
            author=author,
            genre=genre,
            publication_year=publication_year,
            isbn=isbn,
            availability=availability
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('library'))
