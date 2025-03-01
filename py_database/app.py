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

# Route for Home Page
@app.route("/")
def home():
    return render_template("register.html")

# Route for Handling Form Submission
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    color = request.form["color"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, favorite_color) VALUES (?, ?, ?)",
                       (username, password, color))
        conn.commit()
        message = "User registered successfully!"
    except sqlite3.IntegrityError:
        message = "Error: Username already taken."
    
    conn.close()
    return render_template("register.html", message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database (fix)
        conn = sqlite3.connect("users.db")
        conn.row_factory = sqlite3.Row  # Enables dictionary-style access
        cursor = conn.cursor()

        # Fetch user data
        try:
            user = cursor.execute(f"SELECT * FROM users WHERE username = \"{username}\" AND password = \"{password}\"").fetchall()
                
            conn.close()
            message = ""
            if user:
                for u in user:
                    message += (f"{u['username']}'s favorite color is: {u['favorite_color']} \n")  # Access using dictionary key
            else:
                message = "Error: Invalid username or password"
        except Exception as e:
            message = "Something went wrong :("     # Vague error message, for a truly "blind" attack
            #message = e        # Expose to front end what the error message is


        return render_template("login.html", message=message)

    return render_template('login.html')

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
