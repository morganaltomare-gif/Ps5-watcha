#!/usr/bin/env python3
"""Single-run PS5 Pro stock check for GitHub Actions. Notifies via ntfy.sh."""
import os
import random
import time

import requests

NTFY_TOPIC = os.environ["NTFY_TOPIC"]  # set as a GitHub secret

# Paste real PS5 Pro product URLs, plus wording found in each page's source.
SITES = [
    {
        "name": "EB Digital",
        "url": "https://www.ebgames.com.au/product/ps5/325647-playstation-5-pro-digital-console-refurbished-by-eb-games-preowned",
        "in_stock": "Add to cart",
        "out_of_stock": "Out of stock",
    },
    {
        "name": "EB Disc",
        "url": "https://www.ebgames.com.au/product/ps5/325648-playstation-5-pro-disc-console-refurbished-by-eb-games-preowned",
        "in_stock": "Add to Cart",
        "out_of_stock": "Out of Stock",
    },
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) "
        "Gecko/20100101 Firefox/128.0"
    ),
    "Accept-Language": "en-AU,en;q=0.9",
}


def notify(title, message, url):
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers={"Title": title, "Click": url, "Priority": "urgent"},
        timeout=10,
    )


def check(site):
    try:
        r = requests.get(site["url"], headers=HEADERS, timeout=20)
    except requests.RequestException as e:
        print(f"[{site['name']}] error: {e}")
        return None
    if r.status_code != 200:
        print(f"[{site['name']}] HTTP {r.status_code} (may be blocking bots)")
        return None
    html = r.text.lower()
    return site["in_stock"].lower() in html and site["out_of_stock"].lower() not in html


for site in SITES:
    in_stock = check(site)
    print(f"{site['name']}: {in_stock}")
    if in_stock:
        notify(f"PS5 Pro IN STOCK: {site['name']}", "Go go go!", site["url"])
    time.sleep(random.uniform(2, 5))
