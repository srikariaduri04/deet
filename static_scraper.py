import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_static(company_name, url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        return []

    jobs = []

    for link in soup.find_all("a", href=True):
        text = link.get_text(strip=True)

        if any(keyword in text.lower() for keyword in
               ["engineer", "developer", "manager", "intern", "analyst"]):

            jobs.append({
                "company": company_name,
                "title": text,
                "location": "Not Specified",
                "job_id": None,
                "url": urljoin(url, link["href"]),
                "platform": "Static"
            })

    return jobs