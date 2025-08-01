#!/usr/bin/env python3
from datetime import datetime
from termcolor import colored


def get_today() -> str:
    today = datetime.today()
    return f"{today.strftime('%d-%m')}"


def get_todays_summary() -> str:
    """
    Returns today's lunch summary from file, or error message if not found.
    """
    print(colored('Called tool: get_todays_summary.', 'grey'))
    fn = f'./summaries/{get_today()}.txt'
    try:
        with open(fn, 'r', encoding='utf-8') as f:
            summary = f.read()
            print(colored('Summary retrieved: '
                          + summary[:20].replace('\n', ' ') + '...', 'grey'))
    except FileNotFoundError:
        print(f'Summary for today not found at: {fn}')
        return f'Summary for today not found at: {fn}'
    return summary
