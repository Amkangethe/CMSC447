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

        # Server-side password validation
        if len(password) < 6 or not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password) or not any(char in "!@#$%^&*(),.?\":{}|<>" for char in password):
            flash('Password must be at least 6 characters long and contain at least one letter, one digit, and one symbol.', 'error')
            return render_template('signup.html', name=name, username=username, email=email)

        # Hash the password if it meets criteria
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            with get_db_connection() as conn:
                conn.execute('INSERT INTO users (name, username, email, password) VALUES (?, ?, ?, ?)',
                             (name, username, email, hashed_password))
                conn.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        
        except sqlite3.IntegrityError as e:
            # Check for unique constraint violation on username or email
            if "users.username" in str(e):
                flash('Username already exists. Please choose a different one.', 'error')
            elif "users.email" in str(e):
                flash('Email already registered. Please use a different email.', 'error')
            else:
                flash('An error occurred during registration. Please try again.', 'error')
            
            # Return the signup form with existing input data
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
            session['user_id'] = user['id']  # Store user ID in session
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('login.html', username=username)

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/help')
def help():
    return render_template('help.html')

def get_movie_image(title):
    """
    Fetches the poster image URL for a movie by its title.
    """
    search = tmdb.Search()
    response = search.movie(query=title)
    results = response['results']
    if results:
        # Get the first result and its poster path
        poster_path = results[0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/50x75.png?text=No+Image"  # Fallback if no image found

@auth.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    
    if not user_id:
        flash("User not logged in.", "error")
        return redirect(url_for('auth.login'))

    try:
        with get_db_connection() as conn:
            # Fetch user information and related data
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            if not user:
                flash("User not found.", "error")
                return redirect(url_for('auth.login'))
            
            # Fetch liked and disliked films with title and genre
            liked_films = conn.execute(
                'SELECT title, genre FROM films WHERE user_id = ? AND liked = 1', (user_id,)
            ).fetchall()
            disliked_films = conn.execute(
                'SELECT title, genre FROM films WHERE user_id = ? AND liked = 0', (user_id,)
            ).fetchall()
            
            # Add image URL for each film
            liked_films_with_images = [
                {**dict(film), 'image_url': get_movie_image(film['title'])} for film in liked_films
            ]
            disliked_films_with_images = [
                {**dict(film), 'image_url': get_movie_image(film['title'])} for film in disliked_films
            ]
            
            # Log output for debugging
            print("User:", user)
            print("Liked Films with Images:", liked_films_with_images)
            print("Disliked Films with Images:", disliked_films_with_images)
            
    except sqlite3.Error as e:
        print("Database error:", e)
        flash("An error occurred when accessing the database.", "error")
        return redirect(url_for('auth.login'))

    # Render profile with data
    return render_template(
        'profile.html', 
        user=user, 
        liked_films=liked_films_with_images, 
        disliked_films=disliked_films_with_images
    )



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


@auth.route('/friends')
@login_required
def friends():
    # Placeholder route for the friends page
    return render_template('friends.html')  # Ensure friends.html exists

