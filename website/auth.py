import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        check_password = request.form['check-password']
        db = get_db()
        error = None

        if not username:
            error = 'Заполните поле для имени пользователя'
        if not password:
            error = 'Заполните поле для пароля'
        if not check_password:
            error = 'Повторите пароль'
        if password != check_password:
            error = 'Пароли не совпадают'

        if error is None:
            try:
                db.execute("INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
                           (username, email, generate_password_hash(password)))
                db.commit()
            except db.IntegrityError:
                error = f'Пользователь с именем {username} уже существует'
            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()

        if user is None:
            error = 'Неправильно имя'
        elif not check_password_hash(user['password'], password):
            error = 'Неправильный пароль'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.register'))

        flash(error)

    return render_template('auth/login.html')


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()


def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect('auth.login')
        return view(**kwargs)

    return wrapped_view
