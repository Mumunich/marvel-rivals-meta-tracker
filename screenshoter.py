from playwright.sync_api import sync_playwright

def take_shot():
    with sync_playwright() as p:
        # Запускаем браузер
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # Заходим на сайт по ссылке
            page.goto("https://rivalsmeta.com/tier-list", wait_until="domcontentloaded")
            # Небольшая пауза в 3 секунды, чтобы карточки героев "проявились"
            page.wait_for_timeout(3000)
            # Делаем скриншот всей страницы
            page.screenshot(path="tierlist_final.png", full_page=True)
            print("SUCCESS") # Чтобы app.py понял, что всё ок
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    take_shot()