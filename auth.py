import sqlite3
import hashlib
from datetime import datetime

DB_FILE = "users.db"

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT,
            company TEXT,
            role TEXT DEFAULT 'Analyst',
            predictions_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            product_category TEXT,
            product_price REAL,
            prediction_result TEXT,
            probability REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password, full_name, company):
    """Register a new user"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute(
            """INSERT INTO users (username, email, password, full_name, company) 
               VALUES (?, ?, ?, ?, ?)""",
            (username, email, hashed_password, full_name, company)
        )
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already exists!"
        elif "email" in str(e):
            return False, "Email already registered!"
        return False, "Registration failed!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def login_user(username, password):
    """Authenticate user"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute(
            """SELECT id, username, email, full_name, company, role, predictions_count 
               FROM users WHERE username = ? AND password = ?""",
            (username, hashed_password)
        )
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute(
                "UPDATE users SET last_login = ? WHERE username = ?",
                (datetime.now(), username)
            )
            conn.commit()
            
            user_data = {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3],
                'company': user[4],
                'role': user[5],
                'predictions_count': user[6]
            }
            conn.close()
            return True, user_data
        
        conn.close()
        return False, "Invalid username or password!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def update_prediction_count(username):
    """Increment user's prediction count"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET predictions_count = predictions_count + 1 WHERE username = ?",
            (username,)
        )
        conn.commit()
        
        cursor.execute("SELECT predictions_count FROM users WHERE username = ?", (username,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Error updating prediction count: {e}")
        return None

def log_prediction(username, product_category, product_price, prediction_result, probability):
    """Log prediction to database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO predictions_log 
               (username, product_category, product_price, prediction_result, probability) 
               VALUES (?, ?, ?, ?, ?)""",
            (username, product_category, product_price, prediction_result, probability)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging prediction: {e}")

def get_user_info(username):
    """Get updated user information"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, email, full_name, company, role, predictions_count, last_login FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'username': user[0],
                'email': user[1],
                'full_name': user[2],
                'company': user[3],
                'role': user[4],
                'predictions_count': user[5],
                'last_login': user[6]
            }
        return None
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None

# Initialize database when module is imported
init_db()