
```plaintext
# CSCEA465 Peer Learning Assignment: SQL Injection Simulator

## Overview
This program simulates SQL injection attacks in a controlled environment for educational purposes. It demonstrates SQL injection on SQLite3 databases, including Docker-hosted SQLite3 databases.

## Author
- **Team**: Database B
  - **Team Lead**: Constantine
  - **Offense Team**: Clint, Constantine
  - **Defense Team**: Gwen, Nicasio

## Running the Program

### On Linux
1. Clone the repository:
   ```bash
   git clone https://github.com/CodeBusters-Wordle-Crackdown/CSCEA465_PL_EHR-DB
   cd CSCEA465_PL_EHR-DB/Offense
   ```

2. Run the script:
   ```bash
   python3 vulnerable_sql.py
   ```

3. Follow the on-screen instructions.

### On Windows
1. Clone the repository:
   ```cmd
   git clone https://github.com/CodeBusters-Wordle-Crackdown/CSCEA465_PL_EHR-DB
   cd CSCEA465_PL_EHR-DB\Offense
   ```

2. Run the script:
   ```cmd
   python vulnerable_sql.py
   ```

3. Follow the on-screen instructions.

## Key Features
- Simulates SQL injection attacks.
- Allows dynamic query input (default, manual, or predefined).
- User-friendly menu for selecting attacks and viewing results.
- Displays debugging information for database connections and queries.
- Supports SQLite3 databases, including Docker-hosted SQLite3 databases.
- **New Attack Type**: Added support for targeting Docker-hosted SQLite3 databases.

## Usage
1. Run the script using Python 3.9.7 or later.
2. Follow the on-screen instructions to select attacks, input queries, and view results.
3. Press `r` to return to the main menu or `q` to quit at any time.

### New Attack Type: Targeting Docker-Hosted SQLite3
This new attack type allows users to simulate SQL injection attacks against Docker-hosted SQLite3 databases. The attack targets a server running a SQLite3 database in a Docker container.

#### How It Works
1. **Server Targeting**: The program connects to a specified server (e.g., `http://localhost:8080`).
2. **Exploitation**: It sends a malicious SQL query to the server.
3. **Results**: The results of the attack are displayed, showing whether the attack was successful.

#### Example Usage
1. Select the "Target Docker-Hosted SQLite3" option from the main menu.
2. Enter the server URL (or press Enter to use the default `http://localhost:8080`).
3. Input the malicious query or use the default query.
4. The program will send the query to the server and display the results.

## Dependencies
- **Python 3.9.7 or later**
- **SQLite3** (included with Python by default)
- **Docker** (optional, for testing Docker-hosted SQLite3 databases)
- **requests** library (for making HTTP requests to the server)

### Installing Dependencies on Linux
1. Update your package list:
   ```bash
   sudo apt update
   ```

2. Install Python 3 and pip:
   ```bash
   sudo apt install python3 python3-pip
   ```

3. Install SQLite3 (if not already installed):
   ```bash
   sudo apt install sqlite3
   ```

4. Install Docker (optional, for server testing):
   ```bash
   sudo apt install docker.io
   ```

5. Install the `requests` library:
   ```bash
   pip3 install requests
   ```

### Installing Dependencies on Windows
1. Download and install Python from [python.org](https://www.python.org/downloads/).
2. Ensure Python is added to PATH during installation.
3. SQLite3 is included with Python by default.
4. Download and install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop) (optional, for server testing).
5. Install the `requests` library:
   ```cmd
   pip install requests
   ```

## Notes
- **Educational Purpose Only**: Do not use this program for malicious purposes.
- Ensure the database file (`test.db` by default) exists and is accessible.
- For Docker-hosted SQLite3 attacks, ensure the server is running and accessible.

## Example Usage
```python
if __name__ == "__main__":
    # Create an instance of the class
    sql_attacks = SQLInjectionAttacks()

    # Run the main menu
    sql_attacks.main_menu()
```

## AI Usage Acknowledgement
This project acknowledges the use of AI tools (e.g., GitHub Copilot, OpenAI GPT) for assistance in code generation, documentation, and debugging.

## License
This work is licensed under the Creative Commons Attribution 4.0 International License. For details, visit [Creative Commons](http://creativecommons.org/licenses/by/4.0/).
```

### Key Updates to the README:
1. **New Attack Type**:
   - Added a section for the new attack type: **Targeting Docker-Hosted SQLite3**.
   - Explained how the attack works and provided an example usage.

2. **Dependencies**:
   - Added `requests` library as a dependency for making HTTP requests to the server.
   - Added Docker as an optional dependency for testing Docker-hosted SQLite3 databases.

3. **Usage**:
   - Updated the usage section to include instructions for the new attack type.

4. **Key Features**:
   - Added the new attack type to the list of key features.

5. **Notes**:
   - Added a note about ensuring the server is running and accessible for Docker-hosted SQLite3 attacks.
To test **Attack Type 2 (Target Docker-Hosted SQLite3)**, you need to set up a Docker container running a simple server that exposes a SQLite3 database. Below are the detailed steps to create the Docker container, run the test server, and conduct the attack.

---------------------------------------------------------------------

## Steps to Test Attack Type 2

### 1. **Set Up the Test Server**
You need to create a simple Flask server that exposes a SQLite3 database via an HTTP endpoint. This server will run inside a Docker container.

#### Create the Flask Server
1. Create a directory for the server:
   ```bash
   mkdir sqlite3-server
   cd sqlite3-server
   ```

2. Create a file named `server.py` with the following content:
   ```python
   from flask import Flask, request, jsonify
   import sqlite3

   app = Flask(__name__)

   # Initialize SQLite3 database
   def init_db():
       conn = sqlite3.connect('test.db')
       cursor = conn.cursor()
       cursor.execute('''
           CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               username TEXT,
               password TEXT
           )
       ''')
       # Insert some dummy data
       cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
       cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('user', 'user123')")
       conn.commit()
       conn.close()

   # Endpoint to handle SQL queries
   @app.route('/', methods=['POST'])
   def handle_query():
       query = request.form.get('query')
       if not query:
           return jsonify({"error": "No query provided"}), 400

       try:
           conn = sqlite3.connect('test.db')
           cursor = conn.cursor()
           cursor.execute(query)
           result = cursor.fetchall()
           conn.close()
           return jsonify({"result": result})
       except Exception as e:
           return jsonify({"error": str(e)}), 500

   if __name__ == '__main__':
       init_db()
       app.run(host='0.0.0.0', port=8080)
   ```

3. Create a `requirements.txt` file for Flask:
   ```plaintext
   Flask==2.3.2
   ```

4. Create a `Dockerfile` to containerize the server:
   ```Dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY . /app
   RUN pip install -r requirements.txt
   EXPOSE 8080
   CMD ["python", "server.py"]
   ```

---

### 2. **Build and Run the Docker Container**
1. Build the Docker image:
   ```bash
   docker build -t sqlite3-server .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 8080:8080 --name sqlite3-server sqlite3-server
   ```

3. Verify the container is running:
   ```bash
   docker ps
   ```

4. Test the server by sending a POST request:
   ```bash
   curl -X POST http://localhost:8080 -d "query=SELECT * FROM users"
   ```
   You should see a response like:
   ```json
   {"result":[[1,"admin","admin123"],[2,"user","user123"]]}
   ```

---

### 3. **Run the SQL Injection Simulator**
1. Ensure the `vulnerable_sql.py` script is ready (with the new `target_server` attack type).

2. Run the script:
   ```bash
   python3 vulnerable_sql.py
   ```

3. Select **Attack Type 2 (Target Docker-Hosted SQLite3)** from the menu.

4. When prompted for the server URL, enter:
   ```
   http://localhost:8080
   ```

5. Input a malicious query, such as:
   ```
   'OR '1' = '1
   ```

6. The program will send the query to the Docker-hosted SQLite3 server and display the results.

---

### 4. **Example Attack**
1. **Input Query**:
   ```
   'OR '1' = '1
   ```

2. **Expected Output**:
   The program will return all rows from the `users` table, demonstrating a successful SQL injection attack.

---

### 5. **Clean Up**
1. Stop and remove the Docker container:
   ```bash
   docker stop sqlite3-server
   docker rm sqlite3-server
   ```

2. Remove the Docker image (optional):
   ```bash
   docker rmi sqlite3-server
   ```

---

## Summary of Steps
1. **Set Up the Test Server**:
   - Create a Flask server that exposes a SQLite3 database.
   - Use a Dockerfile to containerize the server.

2. **Run the Docker Container**:
   - Build and run the Docker container.
   - Verify the server is running and accessible.

3. **Run the SQL Injection Simulator**:
   - Use the `vulnerable_sql.py` script to target the Docker-hosted SQLite3 database.
   - Input malicious queries to simulate SQL injection attacks.

4. **Clean Up**:
   - Stop and remove the Docker container after testing.

This setup allows you to test **Attack Type 2** in a controlled environment, demonstrating how SQL injection can be exploited against a Docker-hosted SQLite3 database.
