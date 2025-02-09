from flask import Blueprint, render_template, request, redirect, session, url_for
from models import User
import hashlib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if session.get('user_id') is None:
        return render_template('login.html')
    return redirect('/items/list')

@auth_bp.route('/logincheck', methods=['POST'])
def logincheck():
    email = request.form['email']
    password = request.form['password']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = User.query.filter_by(email=email, password=hashed_password).first()

    if user:
        session['user_id'] = user.id
        session['user_name'] = user.name
        return redirect(url_for('items.list'))
    else:
        return render_template('login.html', error='Invalid email or password')

@auth_bp.route('/logout')
def logout():
    session.clear()  # セッションを完全クリア
    return redirect('/auth/')
