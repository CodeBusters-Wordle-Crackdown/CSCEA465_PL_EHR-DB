from flask import Flask, render_template, request, redirect
import sqlite3
import hashlib

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            favorite_color TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Hash Password Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Route for Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Route for Handling Form Submission
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    color = request.form["color"]

    hashed_password = hash_password(password)

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, favorite_color) VALUES (?, ?, ?)",
                       (username, hashed_password, color))
        conn.commit()
        message = "User registered successfully!"
    except sqlite3.IntegrityError:
        message = "Error: Username already taken."
    
    conn.close()
    return render_template("index.html", message=message)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
