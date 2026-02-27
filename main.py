import schedule
import time
import logging

from database import (
    create_tables,
    insert_company,
    get_active_companies,
    insert_job
)

from universal_scraper import scrape_company


# ==============================
# LOGGING (Internal Only)
# ==============================
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==============================
# SEED COMPANIES (RUN ONCE)
# ==============================
def seed_companies():
    greenhouse = [
        "postman", "stripe", "figma",
        "coinbase", "databricks",
        "airbnb", "dropbox"
    ]

    lever = [
        "plaid"
    ]

    smart = [
        "BoschGroup", "Visa"
    ]

    for slug in greenhouse:
        insert_company(slug, "greenhouse", slug)

    for slug in lever:
        insert_company(slug, "lever", slug)

    for slug in smart:
        insert_company(slug, "smartrecruiters", slug)


# ==============================
# SCRAPER FUNCTION
# ==============================
def run_scraper():
    print("\n🚀 Starting job scrape...\n")
    logging.info("Scraper started")

    companies = get_active_companies()
    total_jobs = 0

    for name, platform, slug in companies:
        try:
            jobs = scrape_company(name, platform, slug)
            job_count = len(jobs)

            # Only show successful companies
            if job_count > 0:
                print(f"{name} → {job_count} jobs")
                logging.info(f"{name} → {job_count} jobs")

                for job in jobs:
                    insert_job(job)

                total_jobs += job_count

        except Exception as e:
            logging.error(f"{name} failed: {e}")
            continue

    print(f"\n✅ Total jobs scraped: {total_jobs}\n")
    logging.info(f"Total jobs scraped: {total_jobs}")
    logging.info("Scraper finished\n")


# ==============================
# SCHEDULER
# ==============================
def start_scheduler():
    print("⏰ Scheduler started. Running every 6 hours...\n")
    logging.info("Scheduler initialized")

    # Run immediately once
    run_scraper()

    # Schedule every 6 hours
    schedule.every(6).hours.do(run_scraper)

    while True:
        schedule.run_pending()
        time.sleep(60)


# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    create_tables()
    seed_companies()
    start_scheduler()