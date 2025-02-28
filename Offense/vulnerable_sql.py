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

Key Classes and Functions:
  - SQLInjectionAttacks: Main class for managing SQL injection attacks.
  - get_user_credentials: Simulates an SQL injection attack to extract user credentials.
  - display_menu: Displays a formatted menu of available attacks.
  - get_user_choice: Prompts the user to select an attack by number or name.
  - get_query_input: Prompts the user to input a query or select from predefined options.
  - main_menu: Main loop for interacting with the user.
"""

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
            }
            # Add more attacks here as needed
        }
        self.successful_attacks = 0  # Counter for successful attacks
        self.unsuccessful_attacks = 0  # Counter for unsuccessful attacks
        self.max_length = 0  # Maximum length of menu lines (used for scaling)
        self.current_default_query = ""  # Track default query for handlers

        # Initialize handler dispatch dictionary
        self.handlers = {
            '1': self.handle_default_query,
            '2': self.handle_manual_input,
            '3': self.handle_predefined_queries
        }

        # Prompts to the user
        self.prompt_welcome = "Welcome to the SQL Injection Simulator!"
        self.prompt_description = "This program demonstrates SQL injection attacks in a controlled environment."
        self.prompt_instructions = "Follow the instructions below to simulate an attack."
        self.prompt_quit_instruction = "Press 'q' at any time to return to the main menu."
        self.prompt_attack_choice = "\nEnter the attack number or name: "
        self.prompt_db_file = "Enter the database file name or path (default: test.db): "
        self.prompt_query_options = "=== Query Input Options ==="
        self.prompt_query_default = "1. Use default query (if available)"
        self.prompt_query_manual = "2. Manually input username/query"
        self.prompt_query_predefined = "3. Select from a list of predefined queries"
        self.prompt_query_separator = "==========================="
        self.prompt_query_choice = "Enter your choice (1, 2, or 3): "
        self.prompt_username = "Enter the username/query to probe: "
        self.prompt_executing = "\nExecuting {}..."
        self.prompt_results = "\nAttack Results:"
        self.prompt_no_results = "\nNo results found or an error occurred."
        self.prompt_continue = "\nDo you want to perform another attack? (y/n): "
        self.prompt_exit = "Exiting the program. Goodbye!"

        # Predefined queries
        self.predefined_queries = [
            "'OR '1' = '1",
            "admin' --",
            "'; DROP TABLE users; --"
        ]

        # Query input options
        self.query_options = [
            self.prompt_query_options,
            self.prompt_query_default,
            self.prompt_query_manual,
            self.prompt_query_predefined,
            self.prompt_query_separator
        ]

    def manage_db_connection(self, attack_ID, query, db='test.db'):
        """
        Manages the database connection and executes the selected attack.
        """
        try:
            print(f"SQLite3: Attempting to connect to {db}...")  # Debug
            db_connection = sqlite3.connect(db)  # Attempt to connect to the database
            print(f"SQLite3: Established connection to {db}!")  # Debug

            print(f"\nSQLite3: Initializing cursor...")  # Debug
            db_cursor = db_connection.cursor()  # Create a cursor
            print(f"SQLite3: Cursor initialized!")  # Debug

            # Execute the selected attack
            result = self.execute_attack(attack_ID, query, db_connection, db_cursor)

            return result

        except sqlite3.Error as e:
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
        print(f"\nExecuting Query: {probe_query}")  # Debug

        db_cursor.execute(probe_query)

        # If successful, collect all user data
        probe_result = db_cursor.fetchall()  # Returns a list of tuples or an empty list
        if len(probe_result) > 0:
            print(f"Extraction Successful!\n")
            self.successful_attacks += 1  # Increment successful attacks counter
        else:
            print(f"Extraction Unsuccessful.\n")
            self.unsuccessful_attacks += 1  # Increment unsuccessful attacks counter

        return probe_result

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
        # Menu description
        description = [
            self.prompt_welcome,
            self.prompt_description,
            self.prompt_instructions,
            self.prompt_quit_instruction
        ]

        # Menu options
        menu_lines = [
            "=== SQL Injection Attack Menu ===",
            *[f"{attack_ID}. {attack_info['sqli_name']}" for attack_ID, attack_info in self.attacks.items()],
            "================================",
            f"Successful Attacks: {self.successful_attacks}",
            f"Unsuccessful Attacks: {self.unsuccessful_attacks}",
            "================================"
        ]

        # Combine description and menu lines
        full_menu = description + [""] + menu_lines

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
            if choice == 'q':
                return None  # Return to main menu
            # Check if the input is a valid attack number
            if choice.isdigit() and int(choice) in self.attacks:
                return int(choice)
            # Check if the input is a valid attack name
            for attack_ID, attack_info in self.attacks.items():
                if choice == attack_info["sqli_name"].lower():
                    return attack_ID
            print("Invalid choice. Please try again or press 'q' to return to the main menu.")

    def handle_default_query(self):
        """Handler for default query option."""
        if self.current_default_query:
            print(f"Using default query: {self.current_default_query}")
            return self.current_default_query
        else:
            print("No default query available for this attack. Please choose another option.")
            return None

    def handle_manual_input(self):
        """Handler for manual input option."""
        username = input(self.prompt_username).strip()
        if username.lower() == 'q':
            return None
        return username

    def handle_predefined_queries(self):
        """Handler for predefined queries option."""
        predefined_lines = [
            "=== Predefined Queries ===",
            *[f"{i}. {query}" for i, query in enumerate(self.predefined_queries, start=1)],
            "========================="
        ]
        for line in predefined_lines:
            print(line.center(self.max_length))
        query_choice = input("Select a query by number: ").strip().lower()
        if query_choice == 'q':
            return None
        if query_choice.isdigit() and 1 <= int(query_choice) <= len(self.predefined_queries):
            return self.predefined_queries[int(query_choice) - 1]
        else:
            print("Invalid choice. Please try again or press 'q' to return to the main menu.")
            return None

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
            if option == 'q':
                return None  # Return to main menu

            handler = self.handlers.get(option)
            if handler:
                result = handler()
                if result is not None:
                    return result
            else:
                print("Invalid option. Please try again or press 'q' to return to the main menu.")

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
            if db.lower() == 'q':
                continue  # Return to main menu
            if not db:
                db = 'test.db'

            # Get the query input
            query = self.get_query_input(attack_ID)
            if query is None:
                continue  # Return to main menu

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
            if continue_choice == 'q':
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