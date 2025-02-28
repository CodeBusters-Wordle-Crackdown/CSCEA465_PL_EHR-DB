import sqlite3

class SQLInjectionAttacks:
    def __init__(self, attack_ID):
        """
        Initialize the class with an attack_ID to determine which function to call.
        """
        self.attack_ID = attack_ID

    def execute_attack(self, username, db='test.db'):
        """
        Executes the attack based on the attack_ID.
        """
        if self.attack_ID == 1:
            return self.get_user_credentials(username, db)
        else:
            raise ValueError(f"Invalid attack_ID: {self.attack_ID}")

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


# Example usage
if __name__ == "__main__":
    # Create an instance of the class with attack_ID = 1
    attack = SQLInjectionAttacks(attack_ID=1)

    # Test SQL injection with malicious input
    malicious_input = "'OR '1' = '1"
    print("Testing SQL injection with malicious input:")
    result = attack.execute_attack(malicious_input)
    print(result)

    # Test with normal input
    normal_input = "alice"  # Replace with a valid username in your database
    print("\nTesting with normal input:")
    result = attack.execute_attack(normal_input)
    print(result)