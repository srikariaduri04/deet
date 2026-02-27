import requests


def detect_platform(url):
    try:
        response = requests.get(url, timeout=10)
        html = response.text.lower()
    except:
        return "dynamic"

    if "greenhouse.io" in html:
        return "greenhouse"

    elif "lever.co" in html:
        return "lever"

    elif "workday" in html or "myworkdayjobs" in html:
        return "workday"

    elif "smartrecruiters" in html:
        return "smartrecruiters"

    elif len(html.strip()) < 1000:
        return "dynamic"

    else:
        return "static"