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
# - Runs on port 8080 and is accessible from any IP address.

# This code was developed with the assistance of AI tools, including GitHub Copilot, Deep Seek r1, and OpenAI GPT, 
# for code generation, documentation, and debugging. These tools were used to enhance productivity 
# and improve the quality of the code and documentation.
# Import necessary libraries

from flask import Flask, request, jsonify  # Flask for creating the web server, request and jsonify for handling HTTP requests and responses
import sqlite3  # SQLite3 for interacting with the SQLite database

# Create a Flask application instance
app = Flask(__name__)

# Function to initialize the SQLite3 database
def init_db():
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
    db_connection = sqlite3.connect('test.db')
    
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
        db_connection = sqlite3.connect('test.db')
        
        # Create a cursor object to execute SQL commands
        db_cursor = db_connection.cursor()
        
        # Execute the provided SQL query
        db_cursor.execute(query)
        
        # Fetch all results from the executed query
        db_result = db_cursor.fetchall()
        
        # Close the database connection
        db_connection.close()
        
        # Return the query results as a JSON response
        return jsonify({"result": db_result})
    
    except Exception as e:
        # If an error occurs, return the error message as a JSON response
        return jsonify({"error": str(e)}), 500  # HTTP 500 Internal Server Error

# Run the Flask application if this script is executed directly
if __name__ == '__main__':
    # Initialize the database (create table and insert dummy data)
    init_db()
    
    # Start the Flask development server
    # - host='0.0.0.0' makes the server accessible from any IP address
    # - port=8080 specifies the port to listen on
    app.run(host='0.0.0.0', port=8080)