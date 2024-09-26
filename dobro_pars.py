import customtkinter as ctk
from tkinter import ttk, filedialog
from openpyxl import load_workbook, Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
from myparser import pars_dob
import re
from datetime import datetime

# Словарь для преобразования русских месяцев в английские
months = {
    'января': 'January',
    'февраля': 'February',
    'марта': 'March',
    'апреля': 'April',
    'мая': 'May',
    'июня': 'June',
    'июля': 'July',
    'августа': 'August',
    'сентября': 'September',
    'октября': 'October',
    'ноября': 'November',
    'декабря': 'December'
}

# Функция для извлечения данных из словаря и генерации данных строки Excel
def extract_data(data):
    event_title = data['EventInfo_event-title__k6Fsy d-none d-md-block']
    project = data['EventInfo_event-partner__mHSXd d-none d-md-block']
    location = data['CardTypes_card-location__title__uqLH2']
    time_info = data['CardTypes_card-time__title__b3zsJ']
    vacancies = data['EventVacanciesTab_tab__ePxnH']
    url = data['url']

    # Извлечение даты и времени
    date_part, time_part = time_info.split(',')
    day, month_rus, year = date_part.strip().split()
    month = months[month_rus]
    date = datetime.strptime(f"{day} {month} {year}", '%d %B %Y').strftime('%d.%m.%Y')
    time_range = time_part.strip()

    # Обработка вакансий
    volunteers = 0
    beneficiaries = 0
    for vacancy in vacancies.split('$'):
        try:
            matches = re.findall(r'(\d+)из\d+', vacancy)
            for match in matches:
                number = int(match)
                if 'участник' not in vacancy:
                    volunteers += number
                else:
                    beneficiaries += number
        except ValueError:
            continue

    # Извлечение названия проекта
    project_name = project.split('#')[-1]

    return {
        'date': date,
        'time_range': time_range,
        'event_title': event_title,
        'project_name': project_name,
        'location': location,
        'volunteers': volunteers,
        'beneficiaries': beneficiaries,
        'url': url
    }

# Функция для создания новой строки в Excel
def create_excel_row(data, file_path):
    extracted_data = extract_data(data)
    date = extracted_data['date']
    time_range = extracted_data['time_range']
    event_title = extracted_data['event_title']
    project_name = extracted_data['project_name']
    location = extracted_data['location']
    volunteers = extracted_data['volunteers']
    beneficiaries = extracted_data['beneficiaries']
    url = extracted_data['url']

    # Открыть или создать книгу
    try:
        wb = load_workbook(file_path)
        ws = wb.active
    except FileNotFoundError:
        wb = Workbook()
        ws = wb.active
        # Запись заголовков
        headers = ['Полугодие', 'квартал', 'месяц', 'дата', 'часы мероприятия', 'мероприятие', 'Проект', 'количество волонтеров', 'количество благополучателей', 'место проведения', 'краткое описание', 'Ссылка', 'время проведения', 'общее количество часов волонтёров']
        ws.append(headers)

    # Найти последнюю строку
    last_row = ws.max_row + 1

    # Запись данных
    ws[f'D{last_row}'] = date
    ws[f'E{last_row}'] = f'=ТЕКСТ((ВРЕМЗНАЧ(ПСТР(M{last_row}, НАЙТИ("-", M{last_row}) + 2, 5)) - ВРЕМЗНАЧ(ЛЕВСИМВ(M{last_row}, НАЙТИ("-", M{last_row}) - 2))), "ч")'
    ws[f'F{last_row}'] = event_title
    ws[f'G{last_row}'] = project_name
    ws[f'H{last_row}'] = volunteers
    ws[f'I{last_row}'] = beneficiaries
    ws[f'J{last_row}'] = location
    ws[f'L{last_row}'] = url
    ws[f'M{last_row}'] = time_range
    ws[f'N{last_row}'] = f'=H{last_row} * E{last_row}'

    # Формулы
    ws[f'A{last_row}'] = f'=ЕСЛИ(МЕСЯЦ(D{last_row}) <= 6, 1, 2)'
    ws[f'B{last_row}'] = f'=ОКРУГЛВВЕРХ(МЕСЯЦ(D{last_row})/3, 0)'
    ws[f'C{last_row}'] = f'=ПРОПИСН(ТЕКСТ(D{last_row}, "ММММ"))'

    # Сохранение книги
    wb.save(file_path)

# Функция для обработки нажатия кнопки
def on_button_click(url_entry, error_label, tree, file_path):
    url = url_entry.get()
    if not url:
        error_label.configure(text="Ошибка: URL не может быть пустым")
        return

    error_label.configure(text=f"Получен URL: {url}")

    data = pars_dob(url)
    
   
    error_label.configure(text=f"Получены данные: {data}")

    create_excel_row(data, file_path)
    error_label.configure(text="Строка успешно добавлена")
    load_excel_data(tree, file_path)

# Функция для открытия файла Excel
def open_file(tree, set_file_path, file_label):
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if filepath:
        set_file_path(filepath, file_label)
        load_excel_data(tree, filepath)

# Функция для загрузки и отображения данных Excel
def load_excel_data(tree, filepath='events.xlsx'):
    for row in tree.get_children():
        tree.delete(row)

    try:
        wb = load_workbook(filepath)
        ws = wb.active
        rows = ws.iter_rows(values_only=True)
        for row in rows:
            tree.insert("", "end", values=row)
    except FileNotFoundError:
        pass