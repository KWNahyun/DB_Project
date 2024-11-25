# ./app/main/index.py
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.index'))  # 기본 경로에서 '/main'으로 리디렉션

@main.route('/main', methods=['GET'])
def index():
    return render_template('/main/index.html')
