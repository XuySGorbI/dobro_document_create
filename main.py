import customtkinter as ctk  # Для пользовательского интерфейса
from tkinter import ttk  # Виджеты интерфейса
from dobro_pars import dobro_parser  # Для работы с парсингом данных по ссылкам
from linc_pars import Lincs_parser  # Для извлечения ссылок на мероприятия
from tkcalendar import DateEntry  # Виджет для выбора даты
import asyncio
import tkinter as tk  # Для работы с буфером обмена

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

    def setup_gui(self):
        """
        Создаёт элементы пользовательского интерфейса и размещает их.
        """
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

        self.left_entry = ctk.CTkEntry(left_frame, width=300)
        self.left_entry.pack(pady=10)

        self.left_button = ctk.CTkButton(left_frame, text="добавить")  # Без функционала
        self.left_button.pack(pady=10)
        
        # Добавляем поддержку Ctrl+V в поле ввода
        self.left_entry.bind("<Control-v>", self.paste_clipboard)
        self.left_entry.bind("<Control-V>", self.paste_clipboard)
        
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

        self.org_index_entry = ctk.CTkEntry(right_frame, width=300)
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
        right_button_2 = ctk.CTkButton(right_buttons_frame, text="Создать отчёт", command=self.pars_and_create_rows)
        right_button_2.grid(row=0, column=1, padx=5)

        # Таблица для отображения данных
        self.table_frame = ttk.Treeview(self.app, columns=("Дата", "Время", "Название", "Проект", "Место", "Ссылка"), show="headings")
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Настраиваем заголовки таблицы
        for col in ("Дата", "Время", "Название", "Проект", "Место", "Ссылка"):
            self.table_frame.heading(col, text=col)

    def paste_clipboard(self, event=None):
        """
        Обработчик вставки из буфера обмена в CTkEntry.
        """
        try:
            clipboard_text = self.app.clipboard_get()
            event.widget.insert("insert", clipboard_text)
        except tk.TclError:
            pass

    async def fetch_and_parse(self):
        """
        Асинхронная функция для извлечения ссылок на мероприятия и обработки каждой ссылки.
        """
        try:
            # Создаём объект Lincs_parser с данными из интерфейса
            lincs_parser = Lincs_parser(
                html=self.org_index_entry.get(),
                start=self.start_date_entry.get_date().strftime('%d/%m/%y'),
                end=self.end_date_entry.get_date().strftime('%d/%m/%y')
            )
            
                        
            # Парсим каждую ссылку и добавляем данные в Excel
            for link in event_links:
                data = class_one_pars.for_button_pars(link, self.err_label, self.table_frame)
                self.add_to_table(data)
            
            self.err_label.configure(text="Обработка завершена успешно!")
        
        except Exception as e:
            self.err_label.configure(text=f"Ошибка: {e}")

    def add_to_table(self, data):
        """
        Добавляет данные в таблицу (Treeview).
        """
        self.table_frame.insert("", "end", values=(
            data.get('date'),
            data.get('time_range'),
            data.get('event_title'),
            data.get('project_name'),
            data.get('location'),
            data.get('url')
        ))

    def pars_and_create_rows(self):
        """
        Запускает асинхронный процесс парсинга и обработки ссылок.
        """
        asyncio.run(self.fetch_and_parse())

    def run(self):
        """
        Запускает приложение.
        """
        self.app.mainloop()


if __name__ == "__main__":
    # Создаём экземпляр приложения и запускаем его
    app = EventExcelUpdaterApp()
    app.run()
