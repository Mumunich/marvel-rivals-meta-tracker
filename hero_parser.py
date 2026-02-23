import sys
import json
import time
from playwright.sync_api import sync_playwright

def get_meta():
    """Собираем иконки и имена в JSON (вывод в консоль)"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("https://rivalsmeta.com/skins", wait_until="domcontentloaded")
            hero_elements = page.locator("div.hero-skins")
            data = []
            for i in range(hero_elements.count() - 1):
                block = hero_elements.nth(i)
                name = block.locator("h2").inner_text().replace(" Skins", "").strip()
                icon = block.locator("img").first.get_attribute("src")
                if icon.startswith("/"):
                    icon = f"https://rivalsmeta.com{icon}".replace("s_32x32", "s_64x64")
                data.append({"name": name, "icon": icon})
            print(json.dumps(data))
        finally:
            browser.close()

def take_hero_shot(hero_name, filename):
    """Скриншот конкретного блока героя"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(device_scale_factor=2)
        page = context.new_page()
        try:
            page.goto("https://rivalsmeta.com/skins", wait_until="domcontentloaded")
            # Находим блок через текст в h2
            target = page.locator(f"div.hero-skins:has(h2:has-text('{hero_name}'))")
            target.scroll_into_view_if_needed()
            time.sleep(3) # Ждем прогрузки картинок скинов
            target.screenshot(path=filename)
            print("SUCCESS")
        finally:
            browser.close()

if __name__ == "__main__":
    if sys.argv[1] == "--meta":
        get_meta()
    elif len(sys.argv) > 2:
        take_hero_shot(sys.argv[1], sys.argv[2])