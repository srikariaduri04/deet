import sqlite3
from datetime import datetime

DB_NAME = "jobs.db"


# ==============================
# DATABASE CONNECTION
# ==============================
def create_connection():
    return sqlite3.connect(DB_NAME)


# ==============================
# CREATE TABLES
# ==============================
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Jobs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        title TEXT,
        location TEXT,
        job_type TEXT,
        department TEXT,
        posted_date TEXT,
        apply_url TEXT UNIQUE,
        platform TEXT,
        scraped_at TEXT
    )
    """)

    # Companies Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        platform TEXT,
        slug TEXT,
        active INTEGER DEFAULT 1
    )
    """)

    conn.commit()
    conn.close()


# ==============================
# VALUE CLEANING (CRITICAL FIX)
# ==============================
def clean_value(value):
    """
    Ensures SQLite only receives safe data types.
    Converts dict/list to string.
    Converts None to empty string.
    """
    if isinstance(value, (dict, list)):
        return str(value)

    if value is None:
        return ""

    return str(value)


# ==============================
# INSERT COMPANY
# ==============================
def insert_company(name, platform, slug):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO companies (name, platform, slug)
        VALUES (?, ?, ?)
        """, (name, platform, slug))

        conn.commit()
        print(f"Inserted company: {name}")

    except sqlite3.IntegrityError:
        # Company already exists
        pass

    except Exception as e:
        print("Company Insert Error:", e)

    conn.close()


# ==============================
# GET ACTIVE COMPANIES
# ==============================
def get_active_companies():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, platform, slug
    FROM companies
    WHERE active = 1
    """)

    companies = cursor.fetchall()
    conn.close()

    return companies


# ==============================
# INSERT SINGLE JOB
# ==============================
def insert_job(job):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO jobs (
            company,
            title,
            location,
            job_type,
            department,
            posted_date,
            apply_url,
            platform,
            scraped_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            clean_value(job.get("company")),
            clean_value(job.get("title")),
            clean_value(job.get("location")),
            clean_value(job.get("job_type")),
            clean_value(job.get("department")),
            clean_value(job.get("posted_date")),
            clean_value(job.get("apply_url")),
            clean_value(job.get("platform")),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

    except sqlite3.IntegrityError:
        # Duplicate job (same apply_url)
        pass

    except Exception as e:
        print("Job Insert Error:", e)

    conn.close()


# ==============================
# INSERT MULTIPLE JOBS
# ==============================
def insert_multiple_jobs(job_list):
    for job in job_list:
        insert_job(job)


# ==============================
# OPTIONAL: FETCH ALL JOBS
# ==============================
def fetch_all_jobs():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    conn.close()
    return jobs


# ==============================
# OPTIONAL: CLEAR JOBS TABLE
# ==============================
def clear_jobs():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs")

    conn.commit()
    conn.close()

    print("Jobs table cleared.")