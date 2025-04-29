import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    """
    Получить HTML-код страницы по URL.
    
    :param url: Строка с URL страницы, которую нужно загрузить.
    :return: Строка с HTML-кодом загруженной страницы.
    """
    response = requests.get(url)  # Выполняем HTTP-запрос по указанному URL.
    response.raise_for_status()  # Если сервер вернул ошибку (например, 404 или 500), выбрасывается исключение.
    return response.text  # Возвращаем текст HTML-кода страницы.

def extract_data(html, class_names):
    """
    Извлечь данные из HTML-кода по массиву имен классов.
    
    :param html: HTML-код страницы (строка).
    :param class_names: Список (массив) с именами классов, по которым нужно найти данные на странице.
    :return: Словарь, где ключ — имя класса, а значение — список текста элементов с этим классом.
    """
    soup = BeautifulSoup(html, 'html.parser')  # Парсим HTML-код с помощью BeautifulSoup.
    extracted_data = {}  # Здесь будут храниться извлеченные данные.

    # Проходим по всем указанным именам классов.
    for class_name in class_names:
        # Находим все элементы с текущим именем класса.
        elements = soup.find_all(class_=class_name)
        # Сохраняем текст каждого элемента в виде списка, убирая лишние пробелы.
        extracted_data[class_name] = [element.get_text(strip=True) for element in elements]
    
    return extracted_data  # Возвращаем словарь с извлеченными данными.

#вывод
def pars_dob(url):    
    """
    Основная функция парсинга данных с веб-страницы.
    
    :param url: URL страницы для обработки.
    :return: Словарь с извлеченными данными и URL страницы.
    """
    # Определяем список классов, данные из которых нужно извлечь.
    class_names = ["EventInfo_event-title__k6Fsy d-none d-md-block",
                   "EventInfo_event-partner__mHSXd d-none d-md-block",
                   "CardTypes_card-location__title__uqLH2",
                   "CardTypes_card-time__title__b3zsJ",
                   "EventVacanciesTab_tab__ePxnH"]
    
    # Получаем HTML-код страницы.
    html = fetch_html(url)
    # Извлекаем данные по указанным классам.
    data = extract_data(html, class_names)
    
    # Создаем итоговый словарь для результатов.
    out_data = {}
    
    # Обрабатываем извлеченные данные.
    for class_name, texts in data.items():
        # Убираем дубликаты в тексте, используя set.
        texts = list(set(texts))
        for text in texts:
            try:
                # Если ключ уже существует, добавляем данные с разделителем "$".
                out_data[class_name] = str(out_data[class_name]) + str(text) + "$"                
            except:
                # Если ключа ещё нет, просто добавляем значение.
                out_data[class_name] = text
    
    # Добавляем URL страницы к итоговым данным.
    out_data["url"] = url
    
    return out_data  # Возвращаем итоговый словарь с результатами.
