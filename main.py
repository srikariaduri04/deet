from greenhouse import scrape_greenhouse
from lever import scrape_lever
from database import create_table, insert_multiple_jobs


def main():
    create_table()

    all_jobs = []

    # Greenhouse companies
    greenhouse_companies = [
        "postman",
        "stripe"
    ]

    # Lever companies (optional)
    lever_companies = []

    print("\n🔍 Scraping Greenhouse Companies...\n")

    for company in greenhouse_companies:
        jobs = scrape_greenhouse(company)
        print(f"{company.upper()} → {len(jobs)} jobs found")
        all_jobs.extend(jobs)

    print("\n🔍 Scraping Lever Companies...\n")

    for company in lever_companies:
        jobs = scrape_lever(company)
        print(f"{company.upper()} → {len(jobs)} jobs found")
        all_jobs.extend(jobs)

    print(f"\n💾 Saving {len(all_jobs)} jobs to database...\n")

    insert_multiple_jobs(all_jobs)

    print("\n✅ Process Completed Successfully")


if __name__ == "__main__":
    main()