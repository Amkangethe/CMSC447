from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from db_utils import get_db_connection, User
import sqlite3 
auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Server-side password validation
        if len(password) < 6 or not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password) or not any(char in "!@#$%^&*(),.?\":{}|<>" for char in password):
            flash('Password must be at least 6 characters long and contain at least one letter, one digit, and one symbol.', 'error')
            return render_template('signup.html', name=name, username=username, email=email)

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            with get_db_connection() as conn:
                conn.execute('INSERT INTO users (name, username, email, password) VALUES (?, ?, ?, ?)',
                             (name, username, email, hashed_password))
                conn.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        
        except sqlite3.IntegrityError as e:
            # Check if the error is due to the unique constraint on username or email
            if "users.username" in str(e):
                flash('Username already exists. Please choose a different one.', 'error')
            elif "users.email" in str(e):
                flash('Email already registered. Please use a different email.', 'error')
            else:
                flash('An error occurred during registration. Please try again.', 'error')
            
            # Return the signup form directly with the username and email populated
            return render_template('signup.html', name=name, username=username, email=email)

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        # Check if user exists and password is correct
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            #flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            # If login fails, flash an error message
            flash('Invalid username or password.', 'error')
            # Render the login page with the username still populated
            return render_template('login.html')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    #flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/check_availability', methods=['GET'])
def check_availability():
    username = request.args.get('username')
    email = request.args.get('email')
    response = {'available': True}  # Default response

    with get_db_connection() as conn:
        if username:
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            response['available'] = user is None  # True if username is available
        elif email:
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            response['available'] = user is None  # True if email is available

    return response

