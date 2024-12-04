from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from db_utils import get_db_connection, User
from auth import auth  # Import auth blueprint
import tmdbsimple as tmdb
from views import views  # Import the views blueprint



# Configure TMDB API Key
tmdb.API_KEY = 'a4d876ca3f25f69d049aa011dfce0952'

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'allaniscool'  # Replace with a strong secret key
app.register_blueprint(auth)  # Register authentication blueprint
app.register_blueprint(views)

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
    # Fetch popular movies using TMDB API
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
    return render_template('home.html', trending_movies=movies_data)

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/profile')
@login_required
def profile():
    return redirect(url_for('auth.profile'))

@app.route('/friends')
@login_required
def friends():
    return redirect(url_for('auth.friends'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
