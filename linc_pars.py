from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s",filename='log.log', encoding='utf-8')

class Lincs_parser:
    """
    Класс для извлечения ссылок на мероприятия с сайта dobro.ru.
    Предназначен для парсинга событий, которые попадают в указанный диапазон дат.
    """

    # Целевые даты для фильтрации событий
    start_date = datetime(2023, 11, 17)  # Начальная дата
    end_date = datetime(2024, 9, 12)     # Конечная дата
    
    # Переменная для хранения идентификатора организации
    page_org = None

    # Список для хранения ссылок на мероприятия
    event_links = None

    # Словарь для перевода названий месяцев с русского на числовое представление
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
    
    def __init__(self, html=0, start=str, end=str):
        """
        Инициализация объекта класса.
        
        :param html: HTML-код страницы (по умолчанию 0).
        :param start: Начальная дата в формате строки (дд/мм/гг).
        :param end: Конечная дата в формате строки (дд/мм/гг).
        """
        self.page_org = html  # Сохраняем HTML страницы
        self.start_date = datetime.strptime(start, "%d/%m/%y")  # Преобразуем строку в объект даты
        self.end_date = datetime.strptime(end, "%d/%m/%y")      # Преобразуем строку в объект даты
    
    def translate_date(self, date_str):
        """
        Переводит строку с русскими месяцами в формат 'день месяц год' с числовыми месяцами.
        
        :param date_str: Строка с датой (например, "12 сентября 2024").
        :return: Строка с датой в формате '12 9 2024'.
        """
        parts = date_str.split()
        if len(parts) == 3:  # Ожидаем три части: день, месяц, год
            day, month, year = parts
            # Заменяем название месяца на числовое значение
            month = self.months.get(month, month)
            return f"{day} {month} {year}"
        return None


    def parse_events(self, page):
        """Парсит страницу с событиями и сохраняет ссылки на события, которые попадают в заданный диапазон дат."""
        soup = BeautifulSoup(page, 'html.parser')
        events = soup.find_all('div', class_='OrganizationEventsPage_events__item__NULCJ col-12 col-sm-6 col-md-4 col-lg-3') ###функция не работает

        list_links = []
        
        for event in events:
            # Извлекаем текстовую строку с датой из события
            date_element = event.find('span', class_="CardTypes_card-date__title__zS1Lv")
            
            if date_element is not None:
                date_str = date_element.text.strip()  # Например, "12 сентября 2024"
                
                # Логируем исходную дату
                logging.info(f"Исходная дата: {date_str}")
                
                # Переводим русскую дату в формат с числовыми месяцами
                translated_date_str = self.translate_date(date_str)
                logging.info(f"Переведенная дата: {translated_date_str}")

                if translated_date_str:
                    try:
                        event_date = datetime.strptime(translated_date_str, "%d %m %Y")
                                                
                        # Проверяем, попадает ли дата события в диапазон
                        if self.start_date <= event_date <= self.end_date:
                            logging.info(f"Событие в диапазоне: {event_date}")
                            
                            # Извлекаем ссылку на мероприятие
                            event_link = event.find('a', href=True)['href']
                            logging.info(f"Добавлена ссылка: {type(event_link)}")
                            list_links.append(str(event_link))                            
                        else:
                            logging.info(f"Событие не в диапазоне: {event_date}")
                            
                    except Exception as e:
                        logging.error(f"Ошибка преобразования даты: {translated_date_str}, ошибка: {e}")
                        continue
                    
        self.event_links = list_links

    def load_all_events(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # p.firefox.launch() или p.chromium.launch()  или p.webkit.launch()
            page = browser.new_page()
            page.goto(self.page_org)

            try:                  
                
                while True:                    
                    try:
                        page.get_by_role("button", name="Показать еще").click() # Поиск по видимому тексту и кнопуе                        


                    except Exception as e:
                        logging.error(f"Предупреждение кнопки: {e}")
                        # Если кнопка не найдена (больше нет событий), выходим из цикла
                        break
            except Exception as e:
                return(f"Произошла ошибка: {e}")
            finally:
                content = page.content()
                browser.close()           
                self.parse_events(content)

            
    def pars_all_lincs(self):
        """
        Основной метод для извлечения ссылок на мероприятия.
        
        :param number_org: Идентификатор организации.
        :return: Список ссылок на мероприятия.
        """
        self.load_all_events()  # Загружаем и парсим события
        return self.event_links  # Возвращаем собранные ссылки
