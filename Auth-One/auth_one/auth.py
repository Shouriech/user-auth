import functools
from flask import render_template, request, redirect, url_for, flash, session, g, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from auth_one.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?,?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered"
            else:
                return redirect(url_for("auth.login"))
        flash(error)
        
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
                ).fetchone()
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home.home'))
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    pass


@bp.route('/logout')
def logout():
    pass


def login_required(view):
    pass



