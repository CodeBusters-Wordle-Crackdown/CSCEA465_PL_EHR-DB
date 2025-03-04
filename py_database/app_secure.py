from flask import Flask, render_template, request, redirect
import sqlite3
import hashlib
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

app = Flask(__name__)

# SALT for key derivation (should be stored securely)
SALT = b'some_fixed_salt'  # Change this in production!

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect("users_secure.db")
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

def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def derive_key(password):
    """Derive a secure encryption key from the user's password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_color(password, color):
    """Encrypt the favorite color using AES encryption derived from the password."""
    key = derive_key(password)
    fernet = Fernet(key)
    return fernet.encrypt(color.encode()).decode()

def decrypt_color(password, encrypted_color):
    """Decrypt the favorite color using the password-derived key."""
    try:
        key = derive_key(password)
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_color.encode()).decode()
    except Exception:
        return None  # Return None if decryption fails (wrong password)

@app.route("/")
def home():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    color = request.form["color"]

    hashed_password = hash_password(password)  # Hash the password for storage
    encrypted_color = encrypt_color(password, color)  # Encrypt the color using the password

    conn = sqlite3.connect("users_secure.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, favorite_color) VALUES (?, ?, ?)",
                       (username, hashed_password, encrypted_color))
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

        hashed_password = hash_password(password)  # Hash input password

        conn = sqlite3.connect("users_secure.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            user = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                                  (username, hashed_password)).fetchone()
            conn.close()
            
            if user:
                encrypted_color = user['favorite_color']
                decrypted_color = decrypt_color(password, encrypted_color)  # Try to decrypt
                
                if decrypted_color:
                    message = f"{user['username']}'s favorite color is: {decrypted_color}"
                else:
                    message = "Error: Failed to decrypt favorite color (wrong password)."
            else:
                message = "Error: Invalid username or password"
        except Exception as e:
            message = "Something went wrong :("
        
        return render_template("login.html", message=message)

    return render_template('login.html')

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)  # Change debug=False in production
