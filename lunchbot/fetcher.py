# import requests
from playwright.sync_api import sync_playwright
import re


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

