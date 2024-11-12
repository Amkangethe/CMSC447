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
    # Use popular movies as a substitute for trending
    movies_api = tmdb.Movies()
    trending_movies = movies_api.popular()['results']  # Fetch popular movies
    
    # Extract relevant data for each movie
    movies_data = [
        {
            'title': movie['title'],
            'poster_path': f"https://image.tmdb.org/t/p/w200{movie['poster_path']}" if movie['poster_path'] else None,
        }
        for movie in trending_movies
    ]
    
    return render_template('index.html', trending_movies=movies_data)

def get_movie_images(movie_id):
    """
    Fetches movie images (poster, backdrop) for a given movie ID.
    """
    movie = tmdb.Movies(movie_id)
    image_data = movie.images()
    
    # TMDb image base URL (change size as needed: 'w500' is for width 500px)
    base_url = "https://image.tmdb.org/t/p/w500"
    
    # Extract poster and backdrop paths
    poster_path = image_data['posters'][0]['file_path'] if image_data['posters'] else None
    backdrop_path = image_data['backdrops'][0]['file_path'] if image_data['backdrops'] else None
    
    # Construct full URLs
    poster_url = f"{base_url}{poster_path}" if poster_path else None
    backdrop_url = f"{base_url}{backdrop_path}" if backdrop_path else None
    
    return {
        'poster_url': poster_url,
        'backdrop_url': backdrop_url,
    }

if __name__ == '__main__':
    app.run(debug=True, port=8000)
