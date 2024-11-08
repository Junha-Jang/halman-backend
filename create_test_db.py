import sqlite3

def create_test_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Drop the existing task table if it exists
    cursor.execute('DROP TABLE IF EXISTS task')
    
    # Create the user table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            profile_url TEXT NOT NULL UNIQUE
        )
    ''')
    
    # Create the task table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TIMESTAMP NOT NULL,
            assigned_user INTEGER,
            status BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (assigned_user) REFERENCES user (id)
        )
    ''')
    
    # Insert sample data into user table
    cursor.execute('INSERT INTO user (name, profile_url) VALUES (?, ?)', ("Alice", "http://example.com/alice"))
    cursor.execute('INSERT INTO user (name, profile_url) VALUES (?, ?)', ("Bob", "http://example.com/bob"))
    
    # Insert sample data into task table
    cursor.execute('INSERT INTO task (name, due_date, assigned_user, status) VALUES (?, ?, ?, ?)', ("Task 1", "2023-12-31 12:00:00", 1, False))
    cursor.execute('INSERT INTO task (name, due_date, assigned_user, status) VALUES (?, ?, ?, ?)', ("Task 2", "2023-12-31 12:00:00", 2, False))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_test_db()
    print("test.db created and populated with sample data.")