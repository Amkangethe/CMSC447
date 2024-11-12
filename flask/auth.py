from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from db_utils import get_db_connection, User
from sqlite3 import IntegrityError

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required!', 'error')
            return redirect(url_for('auth.signup'))
        
        # Update the hashing method to 'pbkdf2:sha256'
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            with get_db_connection() as conn:
                conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                             (username, hashed_password))
                conn.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('auth.signup'))

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        # Check if user exists and the password matches
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            
            # Flash a message to the user and print to the console
            flash('Login successful!', 'success')
            print(f"User '{username}' logged in successfully.")  # Console output for confirmation
            
            return redirect(url_for('index'))
        else:
            # Flash a message to the user for failed login
            flash('Login failed. Check your username and password.', 'error')
            print(f"Failed login attempt for username: '{username}'")  # Console output for failed login
            
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
