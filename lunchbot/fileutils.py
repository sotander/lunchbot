#!/usr/bin/env python3
from lunchbot.config import URLS, URLS_VISUAL


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
