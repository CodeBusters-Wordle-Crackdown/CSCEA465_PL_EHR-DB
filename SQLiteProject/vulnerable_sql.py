import sqlite3

class SQLInjectionAttacks:
    def __init__(self):
        """
        Initialize the class with a dictionary of available attacks.
        """
        self.attacks = {
            1: {
                "function": self.get_user_credentials,
                "sqli_name": "Extract User Credentials"
            }
            # Add more attacks here as needed
        }

    def execute_attack(self, attack_ID, username, db='test.db'):
        """
        Executes the attack based on the attack_ID.
        """
        if attack_ID in self.attacks:
            return self.attacks[attack_ID]["function"](username, db)
        else:
            raise ValueError(f"Invalid attack_ID: {attack_ID}")

    def get_user_credentials(self, username, db='test.db'):
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

            # Check for vulnerable query in the database
            probe_query = f"SELECT * FROM users WHERE username = '{username}'"
            print(f"\nExecuting Query: {probe_query}")  # Debug

            db_cursor.execute(probe_query)

            # If successful, collect all user data
            probe_result = db_cursor.fetchall()  # Returns a list of tuples or an empty list
            if len(probe_result) > 0:
                print(f"Extraction Successful!\n")

            return probe_result

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

        finally:
            # Close the connection
            if db_connection:
                db_connection.close()

    def display_menu(self):
        """
        Displays a formatted menu of available SQL injection methods.
        """
        print("\n=== SQL Injection Attack Menu ===")
        for attack_ID, attack_info in self.attacks.items():
            print(f"{attack_ID}. {attack_info['sqli_name']}")
        print("================================")

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

    def main_menu(self):
        """
        Main menu function to interact with the user.
        """
        # Display the menu
        self.display_menu()

        # Get the user's choice
        attack_ID = self.get_user_choice()

        # Get the database file name or path
        db = input("Enter the database file name or path (default: test.db): ").strip()
        if not db:
            db = 'test.db'

        # Get the username input for the attack
        username = input("Enter the username to probe: ").strip()

        # Execute the selected attack
        print(f"\nExecuting {self.attacks[attack_ID]['sqli_name']}...")
        result = self.execute_attack(attack_ID, username, db)

        # Display the results
        if result:
            print("\nAttack Results:")
            for row in result:
                print(row)
        else:
            print("\nNo results found or an error occurred.")


# Example usage
if __name__ == "__main__":
    # Create an instance of the class
    sql_attacks = SQLInjectionAttacks()

    # Run the main menu
    sql_attacks.main_menu()