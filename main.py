#!/usr/bin/env python3
import sys
import os
from lunchbot.config import URLS, URLS_VISUAL, MODEL_NAME
from lunchbot.fetcher import get_domain_without_tld, get_html_with_playwright
from lunchbot.llm_client import build_extract_prompt, build_summary_prompt, query_llm
from lunchbot.screentaker import read_screenshot


def load_url_list(file_path=URLS) -> list[str]:
    '''Parse file, return lines as urls.'''
    with open(file_path, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
        print(urls)
        return urls


def load_urls_visual(file_path=URLS_VISUAL) -> dict:
    '''Parse: url, option1=value1, option2=value2, ...'''
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
        u_opt = {}
        for line in lines:
            parts = [part.strip() for part in line.split(",")]
            url = parts[0]
            if len(parts) > 1:
                options = dict(part.split("=", 1) for part in parts[1:])
            else:
                options = {}
            u_opt[url] = options
    return u_opt


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py 'your query here'")
        sys.exit(1)

    user_query = sys.argv[1]
    if user_query == 'reload':
        url_list = load_url_list()
        url_visual = load_urls_visual(URLS_VISUAL)

        import ipdb; ipdb.set_trace()
        combined = {url: {'type': 'page'} for url in url_list}
        combined.update({url: {'type': 'visual', 'options': options}
                        for url, options in url_visual.items()})

        for url, m in combined.items():
            if m['type'] == 'page':
                print(f'Getting web source [{url[:80]}]...')
                html_source = get_html_with_playwright(url)
                prompt = build_extract_prompt(html_source)
            else:
                print(f'Taking screenshot of: [{url[:80]}]...')
                ocr = read_screenshot(url, 'screen.png', m['options'])
                prompt = build_extract_prompt(ocr)
 
            print(f'Querying LLM: [{MODEL_NAME}]...')
            response = query_llm(prompt, think_in_response=False)
            with open(f'./menus/{get_domain_without_tld(url)}.txt', 'w+',
                      encoding='utf-8') as f:
                f.write(response)
    elif user_query == 'screen':  # for testing screens
        print(read_screenshot(
            'https://udrevaka.cz/pages/poledni-menu',
            'screen.png',
            options={'cookie_accept_text': 'Přijmout'}))
        # print(read_screenshot(
        #     'https://www.naruzkubrno.cz/tydenni-menu/',
        #     'screen.png',
        #     options={'image_id': 'wnd_ImageBlock_57548_img'}))
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
