from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time


def load_all_events(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()  # или p.firefox.launch() или p.webkit.launch()
        page = browser.new_page()
        page.goto(url)

        try:
            while True:
                try:
                    button = page.locator('div.sc-4d3122e0-0 > button:text("Показать еще")')
                    button.click()
                    time.sleep(1)  # даем время странице подгрузиться
                except Exception:
                    # Если кнопка не найдена (больше нет событий), выходим из цикла
                    break
        except Exception as e:
            return(f"Произошла ошибка: {e}")
        finally:
            html = page.content()
            browser.close()
            
        return html




if __name__ == "__main__":
    load_all_events(URL, OUTPUT_FILE)