import requests


def scrape_lever(slug):
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []

        data = response.json()
        if not isinstance(data, list):
            return []

    except:
        return []

    jobs = []

    for job in data:
        jobs.append({
            "company": slug,
            "title": job.get("text"),
            "location": job.get("categories", {}).get("location"),
            "job_type": job.get("categories", {}).get("commitment"),
            "department": job.get("categories", {}).get("team"),
            "posted_date": "Not Available",
            "apply_url": job.get("hostedUrl"),
            "platform": "Lever"
        })

    return jobs