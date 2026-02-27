from greenhouse import scrape_greenhouse
from lever import scrape_lever
from smartrecruiters import scrape_smartrecruiters


def scrape_company(name, platform, slug):

    if platform == "greenhouse":
        return scrape_greenhouse(slug)

    elif platform == "lever":
        return scrape_lever(slug)

    elif platform == "smartrecruiters":
        return scrape_smartrecruiters(slug)

    else:
        print(f"Platform not supported: {platform}")
        return []