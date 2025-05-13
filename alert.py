import requests
from bs4 import BeautifulSoup
import os

URL = os.environ.get("PAGE_URL")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Discord 또는 Slack Webhook URL

def scrape():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    lectures = []
    for row in soup.select("table tbody tr"):
        cols = row.find_all("td")
        if len(cols) < 7:
            continue
        no = cols[0].get_text(strip=True)
        title = cols[1].get_text(strip=True)
        status = cols[6].get_text(strip=True)
        link = "https://www.swmaestro.org" + row.find("a")["href"]
        lectures.append((no, title, status, link))
    return lectures

def send_alert(title, link):
    data = {
        "content": f"🆕 신규 강의 또는 재오픈!\n**{title}**\n👉 [신청하기]({link})"
    }
    requests.post(WEBHOOK_URL, json=data)

def main():
    lectures = scrape()
    for no, title, status, link in lectures:
        if status == "접수중" and "자유 멘토링" in title:
            send_alert(title, link)

if __name__ == "__main__":
    main()
