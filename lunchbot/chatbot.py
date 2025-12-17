import sys
import os
from datetime import datetime
from termcolor import colored
from lunchbot.config import URLS, URLS_VISUAL, MODEL_NAME, SYSTEM_PROMPT, \
     FUNC_DESC, FORMAT_PROMPT
from lunchbot.fetcher import get_domain_without_tld, get_html_with_playwright
from lunchbot.llm_client import build_extract_prompt, build_summary_prompt, \
     query_llm, chat_llm
from lunchbot.screentaker import read_screenshot
from lunchbot.fileutils import load_url_list, load_urls_visual
from lunchbot.dateutils import get_today, get_todays_summary
from lunchbot.users import load_user_profile


def chat(username, message) -> str:
    with open(SYSTEM_PROMPT, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    with open(FUNC_DESC, 'r', encoding='utf-8') as f:
        func_descriptions = f.read()
    with open(FORMAT_PROMPT, 'r', encoding='utf-8') as f:
        format_prompt = f.read()
    system_prompt = f"{system_prompt}\n{func_descriptions}\n{format_prompt}"
    messages = [{"role": "system", "content": system_prompt}]
    
    profile = load_user_profile(username)
    
    # messages.append({"role": "user", "content": user_input})
    # self_conv = chat_llm(messages,
    #                      tools={"get_todays_summary": get_todays_summary},
    #                      think_in_response=False)  # TODO; IDK if include it or not
    # messages.append({"role": "assistant", "content": self_conv[-1]})
    return f"Hello {username}"
