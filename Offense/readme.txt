```plaintext
# SQL Injection Simulator

## Overview
This program simulates SQL injection attacks in a controlled environment for educational purposes. It demonstrates a SQL injection on a sqlite3 db file

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
- Currently only supports SQLite3

## Usage
1. Run the script using Python 3.9.7 or later.
2. Follow the on-screen instructions to select attacks, input queries, and view results.
3. Press `r` to return to the main menu or `q` to quit at any time.

## Dependencies
- **Python 3.9.7 or later**
- **SQLite3** (included with Python by default)

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

### Installing Dependencies on Windows
1. Download and install Python from [python.org](https://www.python.org/downloads/).
2. Ensure Python is added to PATH during installation.
3. SQLite3 is included with Python by default.

## Notes
- **Educational Purpose Only**: Do not use this program for malicious purposes.
- Ensure the database file (`test.db` by default) exists and is accessible.

## AI Usage Acknowledgement
This project acknowledges the use of AI tools (e.g., GitHub Copilot, OpenAI GPT) for assistance in code generation, documentation, and debugging.

## License
This work is licensed under the Creative Commons Attribution 4.0 International License. For details, visit [Creative Commons](http://creativecommons.org/licenses/by/4.0/).
```

This`readme.txt` file hasthe **Author** section near the top, clear instructions for running the program on Linux and Windows, and essential details about dependencies, usage, and licensing. The AI Usage Acknowledgement is also included.