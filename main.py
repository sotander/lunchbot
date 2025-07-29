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


def get_today() -> str:
    today = datetime.today()
    return f"{today.strftime('%d-%m')}"


def load_url_list(file_path=URLS) -> list[str]:
    '''Parse file, return lines as urls.'''
    with open(file_path, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
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


def get_todays_summary() -> str:
    """
    Returns today's lunch summary from a file, or an error message if not found.
    """
    print(colored('Called tool: get_todays_summary.', 'grey'))
    fn = f'./summaries/{get_today()}.txt'
    try:
        with open(fn, 'r', encoding='utf-8') as f:
            summary = f.read()
            print(colored('Summary retrieved: ' + summary[:60].replace('\n', ' ') + '...',
                  'grey'))
    except FileNotFoundError:
        print(f'Summary for today not found at: {fn}')
        return f'Summary for today not found at: {fn}'
    return summary


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py 'your query here'")
        sys.exit(1)
    user_query = sys.argv[1]

    if user_query == 'week':
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

    elif user_query == 'screen':  # for testing screens
        print(read_screenshot(
            'https://udrevaka.cz/pages/poledni-menu',
            'screen.png',
            options={'cookie_accept_text': 'Přijmout'}))

    elif user_query == 'day':
        print("Summarizing stored menus...")
        texts = []
        names = []
        for fi in os.listdir('./menus'):
            if fi.endswith('.txt'):
                path = os.path.join('./menus', fi)
                names.append(fi.rsplit('.', 1)[0])
                with open(path, 'r', encoding='utf-8') as f:
                    texts.append(f.read())
        prompt = build_summary_prompt(texts, names, user_query)
        print(f'Querying LLM: {MODEL_NAME}...')
        response = query_llm(prompt, think_in_response=False)
        # print(response)
        with open(f'./summaries/{get_today()}.txt', 'w+',
                  encoding='utf-8') as f:
            f.write(response)

    elif user_query == 'chat':
        # https://www.cohorte.co/blog/using-ollama-with-python-step-by-step-guide
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

    else:
        print('Use one of these: {week, day, chat, screen}.')


if __name__ == "__main__":
    main()
