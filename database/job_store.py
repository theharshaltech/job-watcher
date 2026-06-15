import sqlite3

def save_job(job):

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO jobs(company, role, link)
            VALUES (?, ?, ?)
            """,
            (
                job["company"],
                job["role"],
                job["link"]
            )
        )

        conn.commit()
        conn.close()

        return True

    except:

        conn.close()
        return False