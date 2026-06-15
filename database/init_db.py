import sqlite3

def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    # Drop table if exists to ensure clean schema update
    cursor.execute("DROP TABLE IF EXISTS jobs")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        role TEXT,
        location TEXT,
        link TEXT UNIQUE,
        date_posted TEXT,
        date_scraped DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("Database Initialized with new schema")

if __name__ == "__main__":
    init_db()