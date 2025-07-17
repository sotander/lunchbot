from datetime import datetime
from ollama import Client
from .config import MODEL_NAME, OLLAMA_PORT, PROMPT_BASE, PROMPT_BASE_SUMMARY

client = Client(host=f"http://localhost:{OLLAMA_PORT}")
day_en_cs = {
    "Monday": "pondělí",
    "Tuesday": "úterý",
    "Wednesday": "středa",
    "Thursday": "čtvrtek",
    "Friday": "pátek",
    "Saturday": "sobota",
    "Sunday": "neděle"
}


def build_extract_prompt(html_source):
    '''Prompt for extracting menu from single HTML page.'''
    with open(PROMPT_BASE, 'r', encoding='utf-8') as f:
        pb = f.read()
        p = pb.format(joined_sources=html_source)
    return p


def build_summary_prompt(list_menus, list_names, user_query):
    '''Prompt for summarizing menus saved as jsons.'''
    joined_menus = "\n\n".join(
        f"---\nRestaurant: {name}\nHTML:\n{menu}\n" for name, menu
        in dict(zip(list_names, list_menus)).items())

    with open('./lunchbot/alergens.txt', 'r', encoding='utf-8') as f:
        alergens = f.read()

    today_cs = day_en_cs[datetime.now().strftime('%A')]
    date_cs = datetime.today().strftime('%d.%m.%Y %H:%M:%S')

    with open(PROMPT_BASE_SUMMARY, 'r', encoding='utf-8') as f:
        pb = f.read()
        p = pb.format(today=today_cs, date=date_cs, alergens=alergens,
                      user_query=user_query, joined_sources=joined_menus)
    return p


def query_llm(prompt, think_in_response=True):
    '''Send request to local ollama server'''
    response = client.generate(model=MODEL_NAME, prompt=prompt,
                               options={'num_ctx': 40960})
                               #options={'num_ctx': 65536})
    result = response.response
    if not think_in_response:
        parts = result.split('</think>', 1)
        result = parts[1].strip() if len(parts) > 1 else result
    return result


def chat_llm(messages, think_in_response=True):
    '''Chat with local ollama server'''
    response = client.chat(model=MODEL_NAME, messages=messages)
    result = response.message.content
    if not think_in_response:
        parts = result.split('</think>', 1)
        result = parts[1].strip() if len(parts) > 1 else result
    return result
