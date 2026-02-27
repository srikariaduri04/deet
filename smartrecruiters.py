import requests


def scrape_smartrecruiters(slug):
    url = f"https://api.smartrecruiters.com/v1/companies/{slug}/postings"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []

        data = response.json()

    except:
        return []

    jobs = []

    for job in data.get("content", []):
        jobs.append({
            "company": slug,
            "title": job.get("name"),
            "location": job.get("location", {}).get("city"),
            "job_type": job.get("typeOfEmployment"),
            "department": job.get("department"),
            "posted_date": job.get("releasedDate"),
            "apply_url": job.get("ref"),
            "platform": "SmartRecruiters"
        })

    return jobs