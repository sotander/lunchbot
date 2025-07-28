# Lunchbot

Lunchbot is a Python-based application that uses local language models to extract lunch menus from websites and run a chatbot over the retrieved data. It supports both traditional web scraping and OCR for visual menus.

## Prerequisites

### 1. Ollama Setup

- Ollama version 0.10.0 or newer
- Ollama must be running on the port defined in `./lunchbot/config.py`
- Set the context length to at least 40960:
  export OLLAMA_CONTEXT_LENGTH=40960
- Pull the model defined in `./lunchbot/config.py`. The model must have the `tool` label in Ollama.

### 2. Python Environment

- Python 3.9 or newer
- Install required packages:
  pip install ollama playwright
  playwright install chromium

### 3. Tesseract OCR

- Install `tesseract-ocr` (e.g., via apt):
  sudo apt install tesseract-ocr
- Install languages for tesseract:
  sudo apt-get install tesseract-ocr-ces
- Install `pytesseract`:
  pip install pytesseract

## Running Lunchbot

### Retrieve Menus for the Week

  python main.py week

Fetches lunch menus from `./lunchbot/urls.txt` and `./lunchbot/urls_visual.txt`.

### Summarize Menus for the Day

  python main.py day

Summarizes menus from `./lunchbot/menus/*` and saves output to `./lunchbot/summaries`.

### Start Chatbot

  python main.py chat

Starts an interactive chat session.

- To give the bot access to today's menu, ask something about the daily menus. This triggers a tool call to load the current day's summary from disk.
- To quit, use: `q`, `quit`, or `exit`

## URL Formats

In `urls_visual.txt`, each line can include additional options after the URL (comma-separated):

- `image_id`: ID of the HTML element containing the menu image
- `cookie_accept_test`: CSS locator for the consent form's "Accept" button

