import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    """
    Получить HTML-код страницы по URL.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_data(html, class_names):
    """
    Извлечь данные из HTML-кода по массиву имен классов.
    
    :param html: HTML-код страницы.
    :param class_names: Массив имен классов для извлечения данных.
    :return: Словарь с именами классов и извлеченными данными.
    """
    soup = BeautifulSoup(html, 'html.parser')
    extracted_data = {}
    
    for class_name in class_names:
        elements = soup.find_all(class_=class_name)
        extracted_data[class_name] = [element.get_text(strip=True) for element in elements]
    
    return extracted_data

#вывод
def pars_dob(url):    
    class_names = ["EventInfo_event-title__k6Fsy d-none d-md-block",
                   "EventInfo_event-partner__mHSXd d-none d-md-block",
                   "CardTypes_card-location__title__uqLH2",
                   "CardTypes_card-time__title__b3zsJ",
                   "EventVacanciesTab_tab__ePxnH"]
    html = fetch_html(url)
    data = extract_data(html, class_names)
    out_data = {}
    for class_name, texts in data.items():
       
        texts = list(set(texts))
        for text in texts:
            try:
                out_data[class_name] = str(out_data[class_name]) + str(text) + "$"                
            except:
                out_data[class_name] = text
                
    out_data["url"] = url
    return out_data