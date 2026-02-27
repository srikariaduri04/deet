import requests


def scrape_workday(company_name, base_url):
    # Attempt common Workday API pattern
    api_url = base_url.rstrip("/") + "/wday/cxs/" + company_name + "/jobs"

    try:
        response = requests.post(api_url, json={"limit": 50, "offset": 0})
        data = response.json()
    except:
        return []

    jobs = []

    for job in data.get("jobPostings", []):
        jobs.append({
            "company": company_name,
            "title": job.get("title"),
            "location": job.get("locationsText"),
            "job_id": job.get("externalPath"),
            "url": base_url + job.get("externalPath", ""),
            "platform": "Workday"
        })

    return jobs