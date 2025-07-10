from PIL import Image
import pytesseract
import time
import tempfile
from playwright.sync_api import sync_playwright


def read_screenshot(url, screenshot_path):
    # Take screenshot, OCR, and return text content
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1200, "height": 1920})
        page.goto(url)
        page.wait_for_load_state("networkidle")
        # print(page.locator("xpath=//*[normalize-space(text())='Přijmout']").is_visible())

        # page.locator(
        #        "xpath=//*[normalize-space(text())='Přijmout']").wait_for()
        # print(page.locator("xpath=//*[normalize-space(text())='Přijmout']").is_visible())

        # locator = page.locator("xpath=//*[normalize-space(text())='Přijmout']")
        # locator.wait_for(state="attached")
        # locator.click(force=True)
        element = page.locator("xpath=//*[normalize-space(text())='Přijmout']") \
                      .element_handle()
        page.evaluate("(el) => el.style.border = '3px solid red'", element)
        page.locator("xpath=//*[normalize-space(text())='Přijmout']").click(force=True)
        page.screenshot(path=screenshot_path)
        browser.close()

    time.sleep(1)

    # Run OCR on the screenshot
    image = Image.open(screenshot_path)
    text = pytesseract.image_to_string(image, lang='ces')  # or 'ces' for Czech
    return text
