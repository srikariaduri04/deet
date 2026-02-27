import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_jobs(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    job_cards = soup.find_all("div", class_="card-content")

    for job in job_cards:
        title = job.find("h2", class_="title").text.strip()
        company = job.find("h3", class_="company").text.strip()
        location = job.find("p", class_="location").text.strip()

        # Extract link
        link_tag = job.find("a")
        job_url = urljoin(base_url, link_tag["href"]) if link_tag else None

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "url": job_url
        })

    return jobs