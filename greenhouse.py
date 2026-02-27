import requests


def scrape_greenhouse(company_slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 404:
            print(f"[SKIPPED] {company_slug} not found on Greenhouse")
            return []

        response.raise_for_status()
        data = response.json()

    except Exception as e:
        print(f"[ERROR] Greenhouse ({company_slug}):", e)
        return []

    jobs = []

    for job in data.get("jobs", []):
        jobs.append({
            "company": company_slug,
            "title": job.get("title"),
            "location": job.get("location", {}).get("name"),
            "job_id": job.get("id"),
            "url": job.get("absolute_url"),
            "platform": "Greenhouse"
        })

    return jobs