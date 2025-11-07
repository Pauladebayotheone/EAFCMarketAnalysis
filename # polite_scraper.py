# polite_scraper.py
import requests
import time
import urllib.robotparser
from bs4 import BeautifulSoup

BASE = "https://www.example-site-with-listings.com"  # replace with the public page URL you may legally scrape

def can_fetch(url, user_agent="my-scraper"):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(BASE + "/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, url)

def fetch_listing_page(url):
    if not can_fetch(url):
        raise SystemExit("robots.txt disallows scraping this URL.")
    headers = {"User-Agent": "MyMarketAnalyticsBot/1.0 (+email@example.com)"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    time.sleep(1.5)   # polite rate limiting (adjust upward if needed)
    return resp.text

def parse_listings(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for item in soup.select(".listing-row"):  # change selector to match target site
        name = item.select_one(".player-name").get_text(strip=True)
        price = item.select_one(".price").get_text(strip=True).replace(",", "")
        rows.append({"name": name, "price": int(price)})
    return rows

if __name__ == "__main__":
    url = BASE + "/market/listings?page=1"
    html = fetch_listing_page(url)
    data = parse_listings(html)
    print(data)
