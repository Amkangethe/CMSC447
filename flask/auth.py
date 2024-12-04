from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from db_utils import get_db_connection, User
import sqlite3
import tmdbsimple as tmdb

# Configure TMDB API Key
tmdb.API_KEY = 'a4d876ca3f25f69d049aa011dfce0952'

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate and hash the password
        if len(password) < 6 or not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password) or not any(char in "!@#$%^&*(),.?\":{}|<>" for char in password):
            flash('Password must meet criteria.', 'error')
            return render_template('signup.html', name=name, username=username, email=email)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            with get_db_connection() as conn:
                conn.execute('INSERT INTO users (name, username, email, password) VALUES (?, ?, ?, ?)',
                             (name, username, email, hashed_password))
                conn.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError as e:
            flash('An error occurred. Please try again.', 'error')
            return render_template('signup.html', name=name, username=username, email=email)

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('login.html', username=username)

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    with get_db_connection() as conn:
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('profile.html', user=user)

@auth.route('/friends')
@login_required
def friends():
    return render_template('friends.html')
