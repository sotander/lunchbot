import time
from PIL import Image
import pytesseract
from playwright.sync_api import sync_playwright


def read_screenshot(url, screenshot_path, options):
    '''
    Take screenshot, OCR, and return text content.

    url -- the url
    screenshot_path -- temp location of the screenshot (overwritten every time)
    option -- dict with per url options:
        cookie_accept_text -- clicks on el. with the text
        image_id -- clicks on element with id
    '''
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1200, "height": 2540})
        page.goto(url)
        page.wait_for_load_state("networkidle")

        # special options per url
        if options.get('cookie_accept_text'):
            loc = options['cookie_accept_text']  # wnd_ImageBlock_57548_img
            element = page \
                .locator(f"xpath=//*[normalize-space(text())='{loc}']") \
                .element_handle()
            page.evaluate("(el) => el.style.border = '3px solid red'", element)
            # page.wait_for(state="attached")
            element.click(force=True)
            time.sleep(1)
        elif options.get('image_id'):
            loc = options['image_id']  # wnd_ImageBlock_57548_img
            print(loc)
            element = page \
                .locator(f"#{loc}") \
                .element_handle()
            page.evaluate("(el) => el.style.border = '3px solid red'", element)
            element.click()
            time.sleep(1)
        page.screenshot(path=screenshot_path)
        browser.close()

    # Wait just in case
    time.sleep(1)

    # Run OCR on the screenshot
    image = Image.open(screenshot_path)
    text = pytesseract.image_to_string(image, lang='ces', config='--psm 6')
    return text
