from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from db_utils import get_db_connection, User
from auth import auth  # Import auth blueprint
import tmdbsimple as tmdb

# Configure TMDB API Key
tmdb.API_KEY = 'a4d876ca3f25f69d049aa011dfce0952'

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'allaniscool'  # Replace with a strong secret key
app.register_blueprint(auth)  # Register authentication blueprint

# Configure Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect to login page if unauthorized
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Load user by ID for Flask-Login
    with get_db_connection() as conn:
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user:
        return User(user['id'], user['username'])
    return None

@app.route('/')
def index():
    # Fetch trending movies from TMDB API
    trending = tmdb.Trending(media_type='movie', time_window='day')
    response = trending.info()

    # Extract movie data
    movies = [
        {
            "title": movie.get("title"),
            "poster_path": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}",
            "overview": movie.get("overview"),
        }
        for movie in response.get("results", [])
    ]

    # If the user is logged in, render the main home page with movies
    if current_user.is_authenticated:
        return render_template('index.html', username=current_user.username, movies=movies)
    # If the user is not logged in, render a landing page with login and signup options
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
