import requests


def scrape_lever(company_slug):
    """
    Scrapes jobs from Lever-based career boards.
    Example: razorpay
    """

    url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[ERROR] Lever ({company_slug}):", e)
        return []

    jobs = []

    for job in data:
        jobs.append({
            "company": company_slug,
            "title": job.get("text"),
            "location": job.get("categories", {}).get("location"),
            "job_id": job.get("id"),
            "url": job.get("hostedUrl"),
            "platform": "Lever"
        })

    return jobs