"""
Part 1: Basic Flask with SQLite Database
=========================================
Your first step into databases! Moving from hardcoded lists to real database.

What You'll Learn:
- Connecting Flask to SQLite database
- Creating a table
- Inserting data (Create)
- Reading data (Read)

Prerequisites: You should know Flask basics (routes, templates, render_template)
"""

from flask import Flask, render_template
import sqlite3  # Built-in Python library for SQLite database

app = Flask(__name__)

DATABASE = 'students.db'  # Database file name (auto-created)


# =============================================================================
# DATABASE HELPER FUNCTIONS
# =============================================================================

def get_db_connection():
    """Create a connection to the database"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def init_db():
    """Create students table if it doesn't exist"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    """Home page - Display all students"""
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)


@app.route('/add')
def add_sample_student():
    """
    Add sample students to database
    (Exercise solution: adding different students)
    """
    conn = get_db_connection()

    conn.executemany(
        'INSERT INTO students (name, email, course) VALUES (?, ?, ?)',
        [
            ('Mayuri Mahajan', 'mayuri@gmail.com', 'Data Science'),
            ('Amit Sharma', 'amit@gmail.com', 'Web Development'),
            ('Sneha Patil', 'sneha@gmail.com', 'Machine Learning')
        ]
    )

    conn.commit()
    conn.close()

    return 'Sample students added! <a href="/">Go back to home</a>'


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    init_db()  # Create table when app starts
    app.run(debug=True)



# =============================================================================
# KEY CONCEPTS EXPLAINED:
# =============================================================================
#
# 1. SQLite: A lightweight database stored in a single file (.db)
#    - No server needed (unlike MySQL/PostgreSQL)
#    - Perfect for learning and small projects
#
# 2. Connection Flow:
#    connect → execute SQL → commit (if changing data) → close
#
# 3. SQL Commands Used:
#    - CREATE TABLE: Define table structure
#    - SELECT * FROM: Get all data
#    - INSERT INTO: Add new data
#
# 4. row_factory = sqlite3.Row:
#    - Without this: row[0], row[1] (access by index)
#    - With this: row['name'], row['email'] (access by column name)
#
# =============================================================================


# =============================================================================
# EXERCISE:
# =============================================================================
#
# Try modifying `add_sample_student()` to add different students with
# different names!
#
# =============================================================================
