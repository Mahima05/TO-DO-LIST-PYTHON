import sqlite3

def create_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE,
                        age INTEGER,
                        role TEXT,
                        mobile TEXT,
                        password TEXT NOT NULL
                      )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
