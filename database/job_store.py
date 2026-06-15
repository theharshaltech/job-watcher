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

        print("NEW JOB:", job["company"], "-", job["role"])

        conn.close()

        return True

    except Exception as e:

        print("DATABASE ERROR:", e)

        conn.close()

        return False