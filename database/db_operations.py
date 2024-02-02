import sqlite3
import bcrypt
import time

# Create a persistent database connection
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_users_table():
    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT,
                failed_attempts INTEGER DEFAULT 0,
                last_attempt TIMESTAMP
            )
        ''')
        conn.commit()
        print("Users table created successfully")
    except Exception as e:
        print(f"Error creating users table: {e}")

def register(username, password):
    try:
        # Validate the inputs
        if not username or not password:
            print("Username and password cannot be empty")
            return

        password = password.encode('utf-8') # Convert to bytes
        hashed = bcrypt.hashpw(password, bcrypt.gensalt()) # Hash and salt the password

        c.execute('''
            INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, hashed))

        conn.commit()

        print(f"Registered user: {username}")
    except Exception as e:
        print(f"Error registering user: {e}")

def login(username, password):
    c.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))

    user = c.fetchone()

    # If a user is found, check the password
    if user is not None:
        password = password.encode('utf-8') # Convert to bytes
        hashed_password = user[1] # The hashed password is already in bytes

        # Check if the account is locked
        if user[2] >= 3 and time.time() - user[3] < 60*60: # 3 failed attempts within the last hour
            print("This account has been locked. Please try again later.")
            return False
        elif bcrypt.checkpw(password, hashed_password): # Check the password against the hashed password
            # If the password is correct, reset the failed attempts counter
            c.execute('''
                UPDATE users SET failed_attempts = 0 WHERE username = ?
            ''', (username,))
            conn.commit()
            return True
        else:
            # If the password is incorrect, increment the failed attempts counter and update the last attempt time
            c.execute('''
                UPDATE users SET failed_attempts = failed_attempts + 1, last_attempt = ? WHERE username = ?
            ''', (time.time(), username,))
            conn.commit()
            return False
    else:
        return False

create_users_table()