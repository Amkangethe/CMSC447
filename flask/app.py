from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'database.db'
conn = None  # Global database connection object

def get_db_connection():
    """Reuse a single SQLite connection to avoid 'database is locked' error."""
    global conn
    if conn is None:
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create tables if they do not exist."""
    if not os.path.exists(DATABASE):
        with get_db_connection() as conn:
            conn.executescript('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            );
            ''')
            conn.commit()

@app.route('/')
def index():
    """Home page route: fetches all items from the database and renders them."""
    try:
        conn = get_db_connection()
        items = conn.execute('SELECT * FROM items').fetchall()
        return render_template('index.html', items=items)
    except sqlite3.Error as e:
        print("Database error:", e)  # Log the error for debugging
        return "Database error occurred. Please try again later.", 500

@app.route('/add', methods=['POST'])
def add_item():
    """Route to add a new item to the database via a form submission."""
    name = request.form.get('name')
    description = request.form.get('description')
    if not name:
        return "Name is required!", 400
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        return redirect(url_for('index'))
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return "Failed to add item. Please try again.", 500

if __name__ == '__main__':
    init_db()  # Ensure the database and table exist before running the server
    app.run(debug=True, threaded=True, port=8000)
