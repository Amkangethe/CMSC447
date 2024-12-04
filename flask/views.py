from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user
from db_utils import get_db_connection, User
import tmdbsimple as tmdb

# Configure TMDB API Key
tmdb.API_KEY = 'a4d876ca3f25f69d049aa011dfce0952'

# Create a Blueprint for views
views = Blueprint('views', __name__)

@views.route('/')
def index():
    """
    Landing page that displays trending movies using TMDB API.
    """
    movies_api = tmdb.Movies()
    trending_movies = movies_api.popular()['results']
    
    # Extract relevant data for each movie
    movies_data = [
        {
            'title': movie['title'],
            'poster_path': f"https://image.tmdb.org/t/p/w200{movie['poster_path']}" if movie['poster_path'] else None,
        }
        for movie in trending_movies
    ]
    return render_template('index.html', trending_movies=movies_data)

@views.route('/home-login')
@login_required
def home_login():
    """
    Home page for logged-in users, displaying personalized content.
    """
    return render_template('home-login.html', user=current_user)

@views.route('/profile')
@login_required
def profile():
    """
    Profile page for the current user.
    """
    user_id = session.get('user_id')
    # Fetch user data and movie interactions from the database
    with get_db_connection() as conn:
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('profile.html', user=user)

@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Page to edit user profile details.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        bio = request.form.get('bio')
        profile_pic = request.files.get('profile_pic')

        # Save the profile changes to the database
        with get_db_connection() as conn:
            conn.execute(
                'UPDATE users SET username = ?, bio = ? WHERE id = ?',
                (username, bio, session['user_id'])
            )
            conn.commit()
        
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('views.profile'))

    return render_template('edit-profile.html', user=current_user)

@views.route('/friends')
@login_required
def friends():
    """
    Friends page displaying the user's friends list and interactions.
    """
    return render_template('friends.html')

@views.route('/help')
def help_page():
    """
    Help page accessible to all users.
    """
    return render_template('help.html')

@views.route('/help-login')
@login_required
def help_login():
    """
    Help page accessible to logged-in users.
    """
    return render_template('help-login.html')
