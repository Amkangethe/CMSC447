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
app.register_blueprint(views)  # Register views blueprint

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

if __name__ == '__main__':
    app.run(debug=True, port=8000)