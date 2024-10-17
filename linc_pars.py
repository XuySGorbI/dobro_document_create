from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import asyncio 



class Lincs_parser:
    """класс для извлечения ссылок на добрые дела при инициализации __init__ ссылка на организацию, ранняя дата, позднейшая дата)"""
    
    # Целевые даты для сравнения
    start_date = datetime(2023, 11, 17)
    end_date = datetime(2024, 9, 12)
    
    page_org = None

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
    
        
    def __init__(self, html = 0, start = str, end = str):
        """Вводит в переменные (html stsrt=str end=str)"""               
        self.page_org = html
        
        self.start_date = datetime.strptime(start, "%m/%d/%y")
        
        self.end_date = datetime.strptime(end, "%m/%d/%y")
    
    
    
    def translate_date(self, date_str):
        """Переводит строковую дату с русскими месяцами в формат 'день месяц год' с числовыми месяцами."""
        parts = date_str.split()
        if len(parts) == 3:
            day, month, year = parts
            # Заменяем русские месяцы на числовые
            month = self.months.get(month, month)
            return f"{day} {month} {year}"
        return None

    def parse_events(self, page_org):
        """Парсит страницу с событиями и сохраняет ссылки на события, которые попадают в заданный диапазон дат."""
        soup = BeautifulSoup(page_org, 'html.parser')
        events = soup.find_all('div', class_='OrganizationEventsPage_events__item__NULCJ')

        for event in events:
            # Извлекаем текстовую строку с датой из события
            date_element = event.find('span', class_="CardTypes_card-date__title__zS1Lv")
            
            if date_element is not None:
                date_str = date_element.text.strip()  # Например, "12 сентября 2024"
                
                # Переводим русскую дату в формат с числовыми месяцами
                translated_date_str = self.translate_date(date_str)

                if translated_date_str:
                    # Преобразуем строку даты в объект datetime для корректного сравнения
                    try:
                        event_date = datetime.strptime(translated_date_str, "%d %m %Y")
                        
                        # Проверяем, попадает ли дата события в диапазон
                        if self.start_date <= event_date <= self.end_date:
                            # Извлекаем ссылку на мероприятие
                            event_link = event.find('a', href=True)['href']
                            self.event_links.append(event_link)
                    except ValueError:
                        # Пропускаем, если не удалось преобразовать дату
                        print(f"Ошибка преобразования даты: {translated_date_str}")
                        continue

    async def fetch_events(self):
        """Асинхронная функция для работы с браузером и загрузки всех событий."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)  # Можно использовать и Firefox: p.firefox.launch(headless=True)
            page = await browser.new_page()

            # Переходим на страницу
            await page.goto(f'https://dobro.ru/organizations/{self.page_org}/events')

            # Продолжаем нажимать кнопку "Показать еще" до тех пор, пока она не исчезнет
            while True:
                try:
                    # Нажимаем кнопку "Показать еще"
                    await page.click("button:has-text('Показать еще')")

                    # Ждем некоторое время для загрузки новых данных
                    await asyncio.sleep(0.4)
                except:                    
                    break

            # После того, как все данные загружены, начинаем парсить страницу
            content = await page.content()
            self.parse_events(content)

            # Закрываем браузер
            await browser.close()

    # Запуск асинхронного кода
    async def pars_linc(self, number_org):
        self.page_org = number_org
        await self.fetch_events()
        # Выводим собранные ссылки
        return self.event_links
        

