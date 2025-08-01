#!/usr/bin/env python3
import sys
import os
from termcolor import colored
from datetime import datetime
from lunchbot.config import URLS, URLS_VISUAL, MODEL_NAME, SYSTEM_PROMPT
from lunchbot.fetcher import get_domain_without_tld, get_html_with_playwright
from lunchbot.llm_client import build_extract_prompt, build_summary_prompt, \
     query_llm, chat_llm
from lunchbot.screentaker import read_screenshot
from lunchbot.fileutils import load_url_list, load_urls_visual
from lunchbot.dateutils import get_today, get_todays_summary


def week() -> None:
    print("Retrieving weekly menus...")
    url_list = load_url_list()
    url_visual = load_urls_visual(URLS_VISUAL)

    combined = {url: {'type': 'page'} for url in url_list}
    combined.update({url: {'type': 'visual', 'options': options}
                    for url, options in url_visual.items()})

    for url, m in combined.items():
        if m['type'] == 'page':
            print(f'Getting web source [{url[:80]}]...')
            html_source = get_html_with_playwright(url)
            prompt = build_extract_prompt(html_source)
            restaurant_name = get_domain_without_tld(url)
        else:
            print(f'Taking screenshot of: [{url[:80]}]...')
            ocr = read_screenshot(url, 'screen.png', m['options'])
            prompt = build_extract_prompt(ocr)
            if 'restaurant_name' in m['options']:
                restaurant_name = m['options']['restaurant_name']
            else:
                restaurant_name = get_domain_without_tld(url)

        print(f'Querying LLM: [{MODEL_NAME}]...')
        response = query_llm(prompt, think_in_response=False)

        os.makedirs('./menus', exist_ok=True)
        with open(f'./menus/{restaurant_name}.txt', 'w+',
                  encoding='utf-8') as f:
            f.write(response)


def day() -> None:
    print("Summarizing stored menus...")
    texts = []
    names = []
    for fi in os.listdir('./menus'):
        if fi.endswith('.txt'):
            path = os.path.join('./menus', fi)
            names.append(fi.rsplit('.', 1)[0])
            with open(path, 'r', encoding='utf-8') as f:
                texts.append(f.read())
                prompt = build_summary_prompt(texts, names)
    print(f'Querying LLM: {MODEL_NAME}...')
    response = query_llm(prompt, think_in_response=False)
    with open(f'./summaries/{get_today()}.txt', 'w+',
              encoding='utf-8') as f:
        f.write(response)


def chat() -> None:
    with open(SYSTEM_PROMPT, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    system_prompt = f"{system_prompt} You can retreive a today's lunch \
            menus by calling a function 'get_todays_summary' if needed."
    messages = [{"role": "system", "content": system_prompt}]
    while True:
        # Process user input
        user_input = input("You: ")
        if not user_input or user_input == 'q' or user_input == 'quit' or user_input == 'exit':
            print('Bye.')
            break  # exit loop on empty input or keyword TODO: exit keywords
        messages.append({"role": "user", "content": user_input})

        # Gen. reply message (or more if tools are called)
        self_conv = chat_llm(messages,
                             tools={"get_todays_summary": get_todays_summary},
                             think_in_response=False)  # TODO; IDK if include it or not
        print(f'Bot: {self_conv[-1]}\n')
        messages.append({"role": "assistant", "content": self_conv[-1]})


def screen() -> None:
    print(read_screenshot(
        'https://udrevaka.cz/pages/poledni-menu',
        'screen.png',
        options={'cookie_accept_text': 'Přijmout'}))


actions = {
    'week': week,
    'day': day,
    'chat': chat,
    # testing actions
    'screen': screen
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py 'your query here'")
        sys.exit(1)
    user_query = sys.argv[1]

    if user_query not in actions:
        print('Use one of these: {week, day, chat, screen}.')
        return

    actions[user_query]()


if __name__ == "__main__":
    main()
