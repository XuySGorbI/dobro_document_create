from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

# Целевая ссылка
URL = "https://dobro.ru/organizations/10045181/events?order%5Bid%5D=asc"

# Имя файла для сохранения
OUTPUT_FILE = "dobro_events.html"


def load_all_events(url, output_file):
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
            print(f"Произошла ошибка: {e}")
        finally:
            html = page.content()
            browser.close()

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html)

        print(f"Страница сохранена в {output_file}")


if __name__ == "__main__":
    load_all_events(URL, OUTPUT_FILE)