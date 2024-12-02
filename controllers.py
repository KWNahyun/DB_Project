from flask import render_template, request, jsonify, abort, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Book, Rental
from datetime import datetime
from login_manager import login_manager

def setup_routes(app):

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 기존 라우트
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
            # 에러 메시지를 JSON 형태로 반환
            return jsonify({'error': '아이디가 없거나 패스워드가 다릅니다.'}), 401
        return redirect(url_for('home'))


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home')) # 로그아웃 후 메인 페이지로 리다이렉트

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # 회원가입 실패시 에러 메시지를 JSON 형태로 반환 (프론트엔드 페이지에서 해당 메세지를 기반으로 팝업을 띄움)
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                return jsonify({'error': '사용자 이름 또는 이메일이 이미 사용 중입니다.'}), 400

            user = User(username=username, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            return jsonify({'message': '회원가입이 성공하였습니다. 기입한 아이디와 패스워드로 로그인할 수 있습니다.'}), 201
        return redirect(url_for('home')) # 비정상요청의 경우 인 페이지로 리다이렉트
    
    # 도서 목록 페이지
    @app.route('/library')
    @login_required
    def library():
        books = Book.query.all()  # 모든 도서 목록을 가져옵니다.
        return render_template('library.html', books=books)

    # 도서 대여
    @app.route('/rent/<int:book_id>', methods=['POST'])
    @login_required
    def rent_book(book_id):
        book = Book.query.get(book_id)
        if book and book.availability:  # 도서가 존재하고 대여 가능하면
            # 대출 처리
            book.availability = False  # 대여 후, 대여 가능 여부를 False로 변경
            rental = Rental(
                user_id=current_user.id,  # 현재 로그인한 사용자의 ID
                book_id=book.id,
                rental_date=datetime.now(),
                return_date=datetime.now(),  # 예시로, 반환일을 오늘로 설정 (나중에 수정 가능)
                status='대출 중'
            )
            db.session.add(rental)
            db.session.commit()  # 데이터베이스에 커밋하여 저장
            return redirect(url_for('library'))  # 도서관 페이지로 리다이렉트
        return redirect(url_for('library'))  # 대여할 수 없는 경우 도서관 페이지로 리다이렉트

    # 도서 반납
    @app.route('/return/<int:book_id>', methods=['POST'])
    @login_required
    def return_book(book_id):
        book = Book.query.get(book_id)
        if book:  # 도서가 존재하면
            rental = Rental.query.filter_by(book_id=book.id, user_id=current_user.id, status='대출 중').first()
            if rental:  # 대출 중인 대출 기록이 있으면
                book.availability = True  # 반납 후, 대여 가능 여부를 True로 변경
                rental.actual_return_date = datetime.now()  # 반납일 기록
                rental.status = '반납 완료'  # 상태 업데이트
                db.session.commit()  # 데이터베이스에 커밋하여 저장
                return redirect(url_for('library'))  # 도서관 페이지로 리다이렉트
        return redirect(url_for('library'))  # 반납할 도서가 없으면 도서관 페이지로 리다이렉트    

    @app.route('/mypage')
    @login_required
    def mypage():
        rentals = Rental.query.filter_by(user_id=current_user.id).all()
        return render_template('mypage.html', user=current_user, rentals=rentals)
