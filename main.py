import customtkinter as ctk  # Для пользовательского интерфейса
from tkinter import ttk  # Виджеты интерфейса
from dobro_pars import dobro_parser  # Для работы с парсингом данных по ссылкам
from linc_pars import Lincs_parser  # Для извлечения ссылок на мероприятия
from tkcalendar import DateEntry  # Виджет для выбора даты
import tkinter as tk  # Для работы с буфером обмена
import asyncio
import webbrowser
import sqlite3

class_one_pars = dobro_parser()  # Экземпляр класса `dobro_parser`

class EventExcelUpdaterApp:
    """
    Класс приложения для парсинга событий и записи данных в Excel.
    """
    
    def __init__(self):
        """
        Инициализация приложения.
        """
        self.app = ctk.CTk()  # Создаём основное окно приложения
        self.app.geometry("800x600")  # Устанавливаем размеры окна
        self.app.title("Event Excel Updater")  # Устанавливаем заголовок окна
        
        # Настраиваем графический интерфейс
        self.setup_gui()
        self.app.bind("<Control-KeyPress>", self.keypress)
        
    @staticmethod
    def keypress(event):
        if event.keysym == "v":
            pass
        elif event.keycode == 86:
            event.widget.event_generate('<<Paste>>')
        elif event.keycode == 67:
            event.widget.event_generate('<<Copy>>')
        elif event.keycode == 88:
            event.widget.event_generate('<<Cut>>')

    def setup_gui(self):
        """
        Создаёт элементы пользовательского интерфейса и размещает их.
        """
        self.link1 = ctk.CTkLabel(self.app, text="руководство", text_color="blue", cursor="hand2")
        self.link1.pack(pady=10)
        self.link1.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/XuySGorbI/dobro_document_create/blob/main/README.md"))
        # Метка для отображения сообщений об ошибках и результатах
        self.err_label = ctk.CTkLabel(self.app, text="Вывод процесса")
        self.err_label.pack(pady=10)
        
        # Верхняя секция интерфейса с двумя колонками
        upper_frame = ctk.CTkFrame(self.app)
        upper_frame.pack(fill="x", pady=10, padx=10)

        # Левая колонка
        left_frame = ctk.CTkFrame(upper_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=10)

        # Поле для ввода произвольного текста (не используется в текущей логике)
        self.left_label = ctk.CTkLabel(left_frame, text="По ссылке")
        self.left_label.pack(pady=10)

        self.left_entry = ctk.CTkEntry(left_frame, width=300, placeholder_text = "Введите ссылку на доброе дело")
        self.left_entry.pack(pady=10)

        self.left_button_1 = ctk.CTkButton(left_frame, text="Открыть файл", command=lambda: class_one_pars.open_file(self.table_frame)) # Без функционала
        self.left_button_1.pack(pady=10)
        
        self.left_button_2 = ctk.CTkButton(left_frame, text="добавить", command=lambda: class_one_pars.for_button_pars(self.left_entry, self.err_label, self.table_frame))  # Без функционала
        self.left_button_2.pack(pady=10)
     
        
        # Правая колонка
        right_frame = ctk.CTkFrame(upper_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=10)

        # Метки и поля для выбора дат
        self.right_label = ctk.CTkLabel(right_frame, text="По дате")
        self.right_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        self.start_date_label = ctk.CTkLabel(right_frame, text="От:")
        self.start_date_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.start_date_entry = DateEntry(right_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.end_date_label = ctk.CTkLabel(right_frame, text="До:")
        self.end_date_label.grid(row=2, column=0, padx=5, pady=5)
        
        self.end_date_entry = DateEntry(right_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Поле для ввода индекса организации
        self.org_index_label = ctk.CTkLabel(right_frame, text="Индекс организации")
        self.org_index_label.grid(row=3, column=0, padx=5, pady=10, columnspan=2)

        self.org_index_entry = ctk.CTkEntry(right_frame, width=300, placeholder_text = "индекс ищите в ссылке организаци цыфрами")
        self.org_index_entry.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        # Кнопки в правой колонке
        right_buttons_frame = ctk.CTkFrame(right_frame)
        right_buttons_frame.grid(row=5, column=0, pady=10, columnspan=2)

        # Кнопка для открытия файла
        right_button_1 = ctk.CTkButton(
            right_buttons_frame,
            text="Открыть файл",
            command=lambda: class_one_pars.open_file(self.table_frame)  # Передаём таблицу
        )
        right_button_1.grid(row=0, column=0, padx=5)

        # Кнопка для парсинга событий и создания отчёта
        right_button_2 = ctk.CTkButton(right_buttons_frame, text="Создать отчёт", command=self.fetch_and_parse)
        right_button_2.grid(row=0, column=1, padx=5)

        # Таблица для отображения данных
        self.table_frame = ttk.Treeview(self.app, columns=("Дата", "Время", "Название", "Проект", "Место", "Ссылка"), show="headings")
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Настраиваем заголовки таблицы
        for col in ("Дата", "Время", "Название", "Проект", "Место", "Ссылка"):
            self.table_frame.heading(col, text=col)
        
    def create_db(self, id_org):
        """
        Метод для создания базы данных и создания таблиц организаций
        """
        connection = sqlite3.connect('shem.db')
        cursor = connection.cursor()
        
        cuesor.execute(f'''
        CREATE TABLE IF NOT EXISTS ? (
        id INTEGER PRIMARY KEY,
        event_title TEXT NOT NULL,
        project_name TEXT,
        location TEXT NOT NULL,
        url TEXT NOT NULL,
        date TEXT NOT NULL,
        time_range TEXT NOT NULL,
        volunteers INTEGER NOT NULL,
        beneficiaries INTEGER
        )
        ''', (id_org))
        
        cursor.execute('''
        CREATE TABLE IF NOT EXIST end_date_pars(
        id_org INTEGER NOT NULL,
        last_date_pars INTEGER NOT NULL
        )
        ''')
        
        connection.close()


    def fetch_and_parse(self):
        """
        Асинхронная функция для извлечения ссылок на мероприятия и обработки каждой ссылки.
        """
        try:
            #Извлечение id организаци
            org_id_get = self.org_index_entry.get()
            #Создаёт базу данных таблицы индекс id и дату 
            self.create_db(org_id_get)
            
            ## СОЗДАТЬ Проверку на наличии даты и добавить таблицу для последней даты обновления
            
            connection = sqlite3.connecr('shem.db')
            cursor = connection.cursor()
            
            cursor.execute(f'''
            SELECT last_date_pars from end_date_pars where id_org = ?
            ''', (org_id_get))
            
            end_date_pars = cursor.fetchall().strftime('%d/%m/%y')
            
            
            
            # Создаём объект Lincs_parser с данными из интерфейса
            lincs_parser = Lincs_parser(
                html=f"https://dobro.ru/organizations/{org_id_get}/events?order%5Bid%5D=desc",
                start=self.start_date_entry.get_date().strftime('%d/%m/%y'),
                end=self.end_date_entry.get_date().strftime('%d/%m/%y')
            )
            
            event_links = lincs_parser.pars_all_lincs()
                        
            # Парсим каждую ссылку и добавляем данные в Excel
            for link in event_links:
                class_one_pars.for_button_pars(link, self.err_label, self.table_frame)
                
            
            self.err_label.configure(text="Обработка завершена успешно!")
        
        except Exception as e:
            self.err_label.configure(text=f"Ошибка: {e}")



    def run(self):
        """
        Запускает приложение.
        """
        self.app.mainloop()


if __name__ == "__main__":
    # Создаём экземпляр приложения и запускаем его
    app = EventExcelUpdaterApp()
    app.run()
