### 1. **README for `server.py` Script**
```plaintext
# SQL Injection Test Server

## Overview
This script implements a simple Flask-based web server that exposes a SQLite3 database for testing SQL injection attacks. It allows clients to send SQL queries via HTTP POST requests and returns the query results in JSON format. The server is designed for educational purposes to demonstrate how SQL injection vulnerabilities can be exploited and mitigated in a controlled environment.

## Key Features
- Creates a SQLite3 database with a `users` table and inserts dummy data.
- Provides an HTTP endpoint to execute SQL queries sent by clients.
- Returns query results or error messages in JSON format.
- Allows the user to configure the host, port, and database filepath via a main menu.
- Allows the user to quit at any time by pressing a configurable quit key (`q` by default).

## Usage
1. Run the script:
   ```bash
   python server.py
   ```

2. Follow the on-screen prompts to configure the server:
   - Enter the database filepath (or press `q` to quit).
   - If no filepath is provided, you can create a new database.
   - Enter the host address (default: `0.0.0.0`).
   - Enter the port number (default: `8080`).

3. The server will start and listen for incoming SQL queries.

## Example Usage
- Start the server:
  ```bash
  python server.py
  ```

- Send a SQL query to the server using `curl`:
  ```bash
  curl -X POST http://localhost:8080 -d "query=SELECT * FROM users"
  ```

- Expected response:
  ```json
  {"result": [[1, "admin", "admin123"], [2, "user", "user123"]]}
  ```

## Dependencies
- Python 3.9.7 or later
- Flask (`pip install flask`)
- SQLite3 (included with Python by default)
- Optional: `tkinter` for file dialogs (usually included with Python on most systems)

## Notes
- This script is for educational purposes only and should not be used for malicious purposes.
- Ensure the database filepath is valid and accessible.
- The server is not designed for production use and lacks security features.

## License
This work is licensed under the Creative Commons Attribution 4.0 International License. For details, visit [Creative Commons](http://creativecommons.org/licenses/by/4.0/).
```
######################################################################################################
######################################################################################################
---

### 2. **Step-by-Step Instructions for Testing Attack Method 2**


# Step-by-Step Instructions for Testing Attack Method 2

This guide explains how to use the `server.py` and `vulnerable_sql.py` scripts to test **Attack Method 2: Targeting Docker-Hosted SQLite3**.

## Prerequisites
1. **Python 3.9.7 or later** installed on your system.
2. **Flask** installed (`pip install flask`).
3. **SQLite3** (included with Python by default).
4. Both `server.py` and `vulnerable_sql.py` scripts downloaded and accessible.

---

## Step 1: Set Up the Test Server (`server.py`)

1. **Run the `server.py` script**:
   ```bash
   python server.py
   ```

2. **Configure the server**:
   - When prompted, enter the database filepath (or press `q` to quit).
     - Example: `my_database.db`
   - If no filepath is provided, you will be asked if you want to create a new database. Enter `y` to create one.
   - Enter the host address (default: `0.0.0.0`).
   - Enter the port number (default: `8080`).

3. **Server starts**:
   - The server will start and display a message like:
     ```
     Starting server on 0.0.0.0:8080 with database 'my_database.db'...
     ```

4. **Verify the server is running**:
   - Use `curl` or a browser to send a test query:
     ```bash
     curl -X POST http://localhost:8080 -d "query=SELECT * FROM users"
     ```
   - Expected response:
     ```json
     {"result": [[1, "admin", "admin123"], [2, "user", "user123"]]}
     ```

---

## Step 2: Test Attack Method 2 Using `vulnerable_sql.py`

1. **Run the `vulnerable_sql.py` script**:
   ```bash
   python vulnerable_sql.py
   ```

2. **Select Attack Method 2**:
   - From the main menu, select `2. Target Docker-Hosted SQLite3`.

3. **Enter the server URL**:
   - When prompted, enter the server URL (e.g., `http://localhost:8080`).

4. **Input a malicious query**:
   - Enter a SQL injection query, such as:
     ```
     'OR '1' = '1
     ```

5. **View the results**:
   - The script will send the query to the server and display the results.
   - Example output:
     ```
     Attack Results:
     (1, 'admin', 'admin123')
     (2, 'user', 'user123')
     ```

---

## Step 3: Clean Up

1. **Stop the server**:
   - Press `Ctrl+C` in the terminal where the `server.py` script is running to stop the server.

2. **Delete the database file (optional)**:
   - If you created a new database, you can delete it after testing:
     ```bash
     rm my_database.db
     ```

---

## Example Walkthrough

### Set Up the Server
1. Run `server.py`:
   ```bash
   python server.py
   ```
2. Configure the server:
   ```
   Enter the database filepath (default: test.db, or press 'q' to quit): my_database.db
   Enter the host address (e.g., 0.0.0.0 for all interfaces, or 127.0.0.1 for localhost, or press 'q' to quit): 0.0.0.0
   Enter the port number (e.g., 8080, or press 'q' to quit): 8080
   Starting server on 0.0.0.0:8080 with database 'my_database.db'...
   ```

### Test Attack Method 2
1. Run `vulnerable_sql.py`:
   ```bash
   python vulnerable_sql.py
   ```
2. Select Attack Method 2:
   ```
   Enter the attack number or name (or press 'r' to return to the main menu): 2
   ```
3. Enter the server URL:
   ```
   Enter the server URL (e.g., http://localhost:8080): http://localhost:8080
   ```
4. Input a malicious query:
   ```
   Enter the username/query to probe (or press 'r' to return to the main menu): 'OR '1' = '1
   ```
5. View the results:
   ```
   Attack Results:
   (1, 'admin', 'admin123')
   (2, 'user', 'user123')
   ```

---

## Notes
- Ensure the server is running before testing Attack Method 2.
- Use this setup only for educational purposes in a controlled environment.
- Do not use these scripts for malicious purposes.

---

## License
This work is licensed under the Creative Commons Attribution 4.0 International License. For details, visit [Creative Commons](http://creativecommons.org/licenses/by/4.0/).
```

---

### Summary:
1. **`README` for `server.py`**:
   - Provides an overview, key features, usage instructions, and dependencies for the `server.py` script.

2. **Step-by-Step Instructions**:
   - A detailed guide on how to use both `server.py` and `vulnerable_sql.py` to test **Attack Method 2**.

Let me know if you need further adjustments! 😊