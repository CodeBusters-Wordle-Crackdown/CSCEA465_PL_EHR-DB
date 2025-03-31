# test_sqli.py
import pytest
import requests
import sqlite3
import subprocess
import time

# Configuration
BASE_URL = "http://localhost:5000"
SECURE_BASE_URL = "http://localhost:5000"  # Change if using different port
TEST_USER = "test_user"
TEST_PASSWORD = "test_pass"
TEST_COLOR = "blue"

# Fixture to start/stop vulnerable app
@pytest.fixture(scope="module")
def vulnerable_app():
    # Start the vulnerable app
    proc = subprocess.Popen(["python", "app.py"])
    time.sleep(2)  # Allow server to start
    yield
    proc.terminate()

# Fixture to start/stop secure app
@pytest.fixture(scope="module")
def secure_app():
    # Start the secure app
    proc = subprocess.Popen(["python", "app_secure.py"])
    time.sleep(2)
    yield
    proc.terminate()

def register_user(base_url, username, password, color):
    """Register a test user"""
    requests.post(f"{base_url}/register", data={
        "username": username,
        "password": password,
        "color": color
    })

# Test cases for vulnerable app
class TestVulnerableApp:
    def test_sqli_authentication_bypass(self, vulnerable_app):
        # Test classic ' OR '1'='1 bypass
        register_user(BASE_URL, TEST_USER, TEST_PASSWORD, TEST_COLOR)
        
        payload = "' OR '1'='1"
        response = requests.post(f"{BASE_URL}/login", data={
            "username": payload,
            "password": "anything"
        })
        
        assert TEST_COLOR in response.text
        assert "favorite color" in response.text

    def test_union_based_injection(self, vulnerable_app):
        # UNION-based attack to get all users
        payload = f"test_user' UNION SELECT 1, username, password, favorite_color FROM users--"
        
        response = requests.post(f"{BASE_URL}/login", data={
            "username": payload,
            "password": "anything"
        })
        
        assert "test_user" in response.text
        assert TEST_PASSWORD in response.text

    def test_error_based_injection(self, vulnerable_app):
        # Attempt to cause SQL error
        payload = "'"
        response = requests.post(f"{BASE_URL}/login", data={
            "username": payload,
            "password": "anything"
        })
        
        assert "something went wrong" not in response.text
        assert "Error" in response.text

# Test cases for secure app
class TestSecureApp:
    def test_sqli_prevention(self, secure_app):
        register_user(SECURE_BASE_URL, TEST_USER, TEST_PASSWORD, TEST_COLOR)
        
        payload = "' OR '1'='1"
        response = requests.post(f"{SECURE_BASE_URL}/login", data={
            "username": payload,
            "password": "anything"
        })
        
        assert "Invalid username or password" in response.text
        assert TEST_COLOR not in response.text

    def test_parameterized_queries(self, secure_app):
        # Test valid login
        response = requests.post(f"{SECURE_BASE_URL}/login", data={
            "username": TEST_USER,
            "password": TEST_PASSWORD
        })
        
        assert TEST_COLOR in response.text
        assert "favorite color" in response.text

    def test_encrypted_data_storage(self):
        # Verify database encryption
        conn = sqlite3.connect("users_secure.db")
        cursor = conn.cursor()
        cursor.execute("SELECT favorite_color FROM users WHERE username = ?", (TEST_USER,))
        result = cursor.fetchone()[0]
        conn.close()
        
        assert TEST_COLOR not in result
        assert isinstance(result, str) and len(result) > 20

# Test database direct access
def test_direct_db_injection():
    # Test direct database access vulnerability
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    malicious_input = "test_user'; DROP TABLE users;--"
    try:
        cursor.execute(f"SELECT * FROM users WHERE username = '{malicious_input}'")
    except sqlite3.OperationalError:
        pytest.fail("DROP TABLE executed successfully - vulnerable to SQLi!")
    
    conn.close()

if __name__ == "__main__":
    pytest.main(["-v", "test_sqli.py"])