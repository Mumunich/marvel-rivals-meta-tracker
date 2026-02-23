import sys
import time
from playwright.sync_api import sync_playwright

def take_full_shot(url, filename):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(3) # Даем прогрузиться всему
            page.screenshot(path=filename, full_page=True)
            print("SUCCESS")
        finally:
            browser.close()

if __name__ == "__main__":
    # Вызываем: python screenshoter.py URL FILENAME
    if len(sys.argv) > 2:
        take_full_shot(sys.argv[1], sys.argv[2])