# SQL Injection Test Server
# ------------------------
# This code implements a simple Flask-based web server that exposes a SQLite3 database
# for testing SQL injection attacks. The server allows clients to send SQL queries via
# HTTP POST requests and returns the query results in JSON format. It is designed for
# educational purposes to demonstrate how SQL injection vulnerabilities can be exploited
# and mitigated in a controlled environment.
#
# Key Features:
# - Creates a SQLite3 database with a 'users' table and inserts dummy data.
# - Provides an HTTP endpoint to execute SQL queries sent by clients.
# - Returns query results or error messages in JSON format.
# - Allows the user to configure the host, port, and database filepath via a main menu.
# - Allows the user to quit at any time by pressing a configurable quit key.
#
# This code was developed with the assistance of AI tools, including GitHub Copilot and OpenAI GPT, 
# for code generation, documentation, and debugging. These tools were used to enhance productivity 
# and improve the quality of the code and documentation.

# Import necessary libraries
from flask import Flask, request, jsonify  # Flask for creating the web server, request and jsonify for handling HTTP requests and responses
import sqlite3  # SQLite3 for interacting with the SQLite database
import os  # For filepath validation
try:
    from tkinter import Tk, filedialog  # For filepath dialog (optional)
except ImportError:
    filedialog = None  # Fallback if tkinter is not available

# Create a Flask application instance
app = Flask(__name__)

# Quit key (can be changed as needed)
quit_key = 'q'

# Prompts for user interaction
db_filepath_prompt = f"Enter the database filepath (default: test.db, or press '{quit_key}' to quit): "
create_db_prompt = f"No database filepath provided. Do you want to create a new database? (y/n, or press '{quit_key}' to quit): "
new_db_name_prompt = f"Enter a name for the new database (e.g., my_database.db, or press '{quit_key}' to quit): "
invalid_db_filepath_prompt = f"Invalid filepath. Please try again or press '{quit_key}' to quit."
host_prompt = f"Enter the host address (e.g., 0.0.0.0 for all interfaces, or 127.0.0.1 for localhost, or press '{quit_key}' to quit): "
port_prompt = f"Enter the port number (e.g., 8080, or press '{quit_key}' to quit): "
invalid_port_prompt = f"Invalid port number. Using default 8080. Press '{quit_key}' to quit."

# Function to initialize the SQLite3 database
def init_db(db_filepath):
    # SQL statement to create the 'users' table if it doesn't already exist
    sql_create_table_prompt = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,  # Unique ID for each user
            username TEXT,           # Username field
            password TEXT            # Password field
        )
    '''
    
    # List of SQL statements to insert dummy data into the 'users' table
    sql_insert_entry_prompts = [
        "INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')",  # Insert admin user
        "INSERT OR IGNORE INTO users (username, password) VALUES ('user', 'user123')"      # Insert regular user
    ]
    
    # Connect to the SQLite database (or create it if it doesn't exist)
    db_connection = sqlite3.connect(db_filepath)
    
    # Create a cursor object to execute SQL commands
    db_cursor = db_connection.cursor()
    
    # Execute the SQL statement to create the 'users' table
    db_cursor.execute(sql_create_table_prompt)
    
    # Insert dummy data into the 'users' table using a loop
    for sql_insert in sql_insert_entry_prompts:
        db_cursor.execute(sql_insert)  # Execute each insert statement
    
    # Commit the changes to the database
    db_connection.commit()
    
    # Close the database connection
    db_connection.close()

# Define a route for the root URL ("/") that accepts POST requests
@app.route('/', methods=['POST'])
def handle_query():
    # Get the SQL query from the request's form data
    query = request.form.get('query')
    
    # If no query is provided, return an error response
    if not query:
        return jsonify({"error": "No query provided"}), 400  # HTTP 400 Bad Request
    
    try:
        # Connect to the SQLite database
        db_connection = sqlite3.connect(db_filepath)
        
        # Create a cursor object to execute SQL commands
        db_cursor = db_connection.cursor()
        
        # Execute the provided SQL query
        db_cursor.execute(query)
        
        # Fetch all results from the executed query
        result = db_cursor.fetchall()
        
        # Close the database connection
        db_connection.close()
        
        # Return the query results as a JSON response
        return jsonify({"result": result})
    
    except Exception as e:
        # If an error occurs, return the error message as a JSON response
        return jsonify({"error": str(e)}), 500  # HTTP 500 Internal Server Error

# Function to validate the database filepath
def validate_db_filepath(filepath):
    # Check if the filepath is valid and writable
    try:
        # Attempt to create or open the file
        with open(filepath, 'a'):
            pass
        return True
    except Exception:
        return False

# Function to prompt the user for a filepath using a file dialog (if available)
def get_filepath_dialog():
    if filedialog:
        root = Tk()
        root.withdraw()  # Hide the root window
        filepath = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")],
            title="Save Database As"
        )
        return filepath
    else:
        return None

# Main menu function to prompt the user for host, port, and database filepath
def main_menu():
    print("=== SQL Injection Test Server ===")
    print("Configure the server settings:")
    
    # Prompt the user for the database filepath
    global db_filepath  # Make db_filepath accessible globally
    while True:
        db_filepath = input(db_filepath_prompt).strip()
        if db_filepath.lower() == quit_key:
            print("Exiting the program. Goodbye!")
            exit()
        elif not db_filepath:
            # If no filepath is provided, ask if the user wants to create a new database
            create_new = input(create_db_prompt).strip().lower()
            if create_new == quit_key:
                print("Exiting the program. Goodbye!")
                exit()
            elif create_new == 'y':
                # Prompt for a new database name
                new_db_name = input(new_db_name_prompt).strip()
                if new_db_name.lower() == quit_key:
                    print("Exiting the program. Goodbye!")
                    exit()
                elif not new_db_name:
                    new_db_name = "test.db"  # Default to 'test.db'
                
                # Use a file dialog to select the filepath (if available)
                if filedialog:
                    db_filepath = get_filepath_dialog()
                    if not db_filepath:
                        print("No filepath selected. Using default 'test.db'.")
                        db_filepath = "test.db"
                else:
                    db_filepath = new_db_name
                
                # Create the new database
                init_db(db_filepath)
                break
            else:
                # Use the default database
                db_filepath = "test.db"
                break
        elif os.path.exists(db_filepath):
            # Use the provided filepath if it exists
            break
        else:
            # If the filepath is invalid, prompt again
            print(invalid_db_filepath_prompt)
    
    # Prompt the user for the host string
    while True:
        host = input(host_prompt).strip()
        if host.lower() == quit_key:
            print("Exiting the program. Goodbye!")
            exit()
        elif not host:
            host = "0.0.0.0"  # Default to all interfaces
            break
        else:
            break
    
    # Prompt the user for the port number
    while True:
        port = input(port_prompt).strip()
        if port.lower() == quit_key:
            print("Exiting the program. Goodbye!")
            exit()
        elif not port:
            port = 8080  # Default to port 8080
            break
        else:
            try:
                port = int(port)  # Convert the input to an integer
                if port < 1 or port > 65535:  # Validate port range
                    print(invalid_port_prompt)
                    continue
                break
            except ValueError:
                print(invalid_port_prompt)
                continue
    
    print(f"\nStarting server on {host}:{port} with database '{db_filepath}'...")
    return host, port

# Run the Flask application if this script is executed directly
if __name__ == '__main__':
    # Display the main menu and get the host, port, and database filepath configuration
    host, port = main_menu()
    
    # Start the Flask development server with the configured host and port
    app.run(host=host, port=port)