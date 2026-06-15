import sqlite3
import datetime

def save_job(job):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO jobs(company, role, location, link, date_posted)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                job["company"],
                job["role"],
                job["location"],
                job["link"],
                job.get("date_posted", "N/A")
            )
        )
        conn.commit()
        print("NEW JOB:", job["company"], "-", job["role"])
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Link already exists, so it's a duplicate
        conn.close()
        return False
    except Exception as e:
        print("DATABASE ERROR:", e)
        conn.close()
        return False

def get_all_jobs():
    conn = sqlite3.connect("jobs.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY date_scraped DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_stats():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    
    # Total jobs
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]
    
    # Jobs today
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE date_scraped LIKE ?", (f"{today_str}%",))
    jobs_today = cursor.fetchone()[0]
    
    # Unique companies active in DB
    cursor.execute("SELECT DISTINCT company FROM jobs")
    companies = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return {
        "total_jobs": total_jobs,
        "jobs_today": jobs_today,
        "companies": companies
    }