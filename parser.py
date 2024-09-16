from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime

# Целевые даты для сравнения
start_date = datetime(2023, 11, 17)
end_date = datetime(2024, 9, 12)

# Массив для хранения ссылок на мероприятия
event_links = []

# Словарь для перевода русских месяцев на числовые значения
months = {
    'января': '1',
    'февраля': '2',
    'марта': '3',
    'апреля': '4',
    'мая': '5',
    'июня': '6',
    'июля': '7',
    'августа': '8',
    'сентября': '9',
    'октября': '10',
    'ноября': '11',
    'декабря': '12'
}

def translate_date(date_str):
    """Переводит строковую дату с русскими месяцами в формат 'день месяц год' с числовыми месяцами."""
    parts = date_str.split()
    if len(parts) == 3:
        day, month, year = parts
        # Заменяем русские месяцы на числовые
        month = months.get(month, month)
        return f"{day} {month} {year}"
    return None

def parse_events(page_html):
    """Парсит страницу с событиями и сохраняет ссылки на события, которые попадают в заданный диапазон дат."""
    soup = BeautifulSoup(page_html, 'html.parser')
    events = soup.find_all('div', class_='EventCard_card-wrapper__xn0uf')

    for event in events:
        # Извлекаем текстовую строку с датой из события
        date_element = event.find('span', class_='CardTypes_card-date__title__zS1Lv')
        
        if date_element is not None:
            date_str = date_element.text.strip()  # Например, "9 июня 2024"
            
            # Переводим русскую дату в формат с числовыми месяцами
            translated_date_str = translate_date(date_str)

            if translated_date_str:
                # Преобразуем строку даты в объект datetime для корректного сравнения
                try:
                    event_date = datetime.strptime(translated_date_str, "%d %m %Y")
                    
                    # Проверяем, попадает ли дата события в диапазон
                    if start_date <= event_date <= end_date:
                        # Извлекаем ссылку на мероприятие
                        print("Дата найдена")
                        event_link = event.find('a', href=True)['href']
                        event_links.append(event_link)
                except ValueError:
                    # Пропускаем, если не удалось преобразовать дату
                    print(f"Ошибка преобразования даты: {translated_date_str}")
                    continue
        
# Используем Playwright для работы с браузером
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Можно использовать и Firefox: p.firefox.launch(headless=True)
    page = browser.new_page()

    # Переходим на страницу
    page.goto('https://dobro.ru/organizations/10045181/events?order%5Bid%5D=desc')

    # Продолжаем нажимать кнопку "Показать еще" до тех пор, пока она не исчезнет
    while True:
        try:
            # Нажимаем кнопку "Показать еще"
            page.click("button:has-text('Показать еще')")

            # Ждем некоторое время для загрузки новых данных
            page.wait_for_timeout(2000)
        except:
            print("Кнопка 'Показать еще' не найдена или больше нет данных.")
            break

    # После того, как все данные загружены, начинаем парсить страницу
    parse_events(page.content())

    # Закрываем браузер
    browser.close()

# Выводим собранные ссылки
print("Ссылки на мероприятия в диапазоне дат:")
for link in event_links:
    print(link)
