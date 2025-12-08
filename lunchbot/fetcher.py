import requests
from playwright.sync_api import sync_playwright
import re
import json
from datetime import date


def fetch_urls(url_list):
    '''Fetches the source of given url list
    param: url_list

    '''
    html_sources = {}
    for url in url_list:
        try:
            # response = requests.get(url, timeout=5)
            # response.raise_for_status()
            # html_sources[url] = response.text
            html_sources[url] = get_html_with_playwright(url)
        except Exception as e:
            html_sources[url] = f"[ERROR] Could not fetch: {e}"
    return html_sources


def get_html_with_playwright(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ))
        page = context.new_page()
        try:
            page.goto(url, timeout=15000)  # 15 seconds
            try:
                page.wait_for_selector("body", timeout=10000)
            except:
                print("Selector #body not found within 10 seconds")
            html = page.content()
        finally:
            browser.close()
    return html


def get_domain_without_tld(url: str) -> str:
    # Extract hostname part
    match = re.search(r'^(?:https?://)?(?:www\.)?([^/:]+)', url)
    if not match:
        return ''
    host = match.group(1)

    # Split domain by dot
    parts = host.split('.')
    if len(parts) >= 2:
        return parts[-2]  # second-to-last part
    return parts[0]


def fetch_lepsimenu():
    url = "https://www.lepsimenu.cz/api/menus"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.lepsimenu.cz/",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
        "TE": "trailers",
    }

    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    params = {"date": formatted_date}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    with open(f"data/lepsimenu_{formatted_date}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
