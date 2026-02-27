import requests


def scrape_greenhouse(slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []

        data = response.json()
        if "jobs" not in data:
            return []

    except:
        return []

    jobs = []

    for job in data.get("jobs", []):
        jobs.append({
            "company": slug,
            "title": job.get("title"),
            "location": job.get("location", {}).get("name"),
            "job_type": "Not Specified",
            "department": "Not Specified",
            "posted_date": "Not Available",
            "apply_url": job.get("absolute_url"),
            "platform": "Greenhouse"
        })

    return jobs