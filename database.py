import sqlite3
from datetime import datetime


DB_NAME = "jobs.db"


def create_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        title TEXT NOT NULL,
        location TEXT,
        job_id TEXT,
        url TEXT UNIQUE NOT NULL,
        platform TEXT,
        category TEXT DEFAULT 'Uncategorized',
        scraped_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_job(job):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO jobs (
            company,
            title,
            location,
            job_id,
            url,
            platform,
            category,
            scraped_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job.get("company"),
            job.get("title"),
            job.get("location"),
            str(job.get("job_id")),
            job.get("url"),
            job.get("platform"),
            "Uncategorized",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        print(f"Inserted: {job.get('title')}")

    except sqlite3.IntegrityError:
        print(f"Skipped duplicate: {job.get('title')}")

    conn.close()


def insert_multiple_jobs(jobs):
    for job in jobs:
        insert_job(job)