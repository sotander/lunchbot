#!/usr/bin/env python3
import sys
import os
from lunchbot.config import URLS, URLS_VISUAL, MODEL_NAME
from lunchbot.fetcher import get_domain_without_tld, get_html_with_playwright
from lunchbot.llm_client import build_extract_prompt, build_summary_prompt, query_llm
from lunchbot.screentaker import take_screenshot

def load_url_list(file_path=URLS):
    with open(file_path, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
        print(urls)
        return urls


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py 'your query here'")
        sys.exit(1)

    user_query = sys.argv[1]
    if user_query == 'reload':
        url_list = load_url_list()
        url_visual = load_url_list(URLS_VISUAL)

        combined = { url: {'type': 'page'} for url in url_list }
        combined.update({url: {'type': 'visual'} for url in url_visual})

        for url, m in combined.items():
            if m['type'] == 'page':
                print(f'Getting web source [{url[:80]}]...')
                html_source = get_html_with_playwright(url)
                print(html_source)
                prompt = build_extract_prompt(html_source)
            else:
                print(f'Taking screenshot of: [{url[:80]}]...')
                TODO
            print(f'Querying LLM: [{MODEL_NAME}]...')
            response = query_llm(prompt, think_in_response=False)
            with open(f'./menus/{get_domain_without_tld(url)}.txt', 'w+',
                      encoding='utf-8') as f:
                f.write(response)
    elif user_query == 'screen':
        take_screenshot('https://udrevaka.cz/pages/poledni-menu', 'screen.png')
    else:
        texts = []
        names = []
        for fi in os.listdir('./menus'):
            if fi.endswith('.txt'):
                path = os.path.join('./menus', fi)
                names.append(fi.rsplit('.', 1)[0])
                with open(path, 'r', encoding='utf-8') as f:
                    texts.append(f.read())
                    # print(f'Loaded: {texts[-1]}')
        prompt = build_summary_prompt(texts, names, user_query)
        print(f'Querying LLM: {MODEL_NAME}...')
        response = query_llm(prompt, think_in_response=False)
        print(response)


if __name__ == "__main__":
    main()
