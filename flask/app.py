from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from db_utils import get_db_connection, User
from auth import auth  # Import auth blueprint

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
app.register_blueprint(auth)  # Register authentication blueprint

# Flask-Login configuration
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect to login page if unauthorized
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with get_db_connection() as conn:
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user:
        return User(user['id'], user['username'])
    return None

@app.route('/')
def index():
    # If the user is logged in, render the main home page
    if current_user.is_authenticated:
        return render_template('index.html', username=current_user.username)
    # If the user is not logged in, render a landing page with login and signup options
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)

