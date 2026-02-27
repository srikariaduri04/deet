from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape_selenium(company_name, url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)
    time.sleep(5)

    jobs = []

    elements = driver.find_elements(By.TAG_NAME, "a")

    for element in elements:
        text = element.text.strip()

        if any(keyword in text.lower() for keyword in
               ["engineer", "developer", "manager", "intern", "analyst"]):

            jobs.append({
                "company": company_name,
                "title": text,
                "location": "Not Specified",
                "job_id": None,
                "url": element.get_attribute("href"),
                "platform": "Selenium"
            })

    driver.quit()

    return jobs