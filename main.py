import customtkinter as ctk
from tkinter import ttk, filedialog
from functions import on_button_click, open_file, load_excel_data

def main():
    global file_path
    file_path = None

    # Инициализация GUI
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Event Excel Updater")

    # Кадр для открытия файла и его названия
    file_frame = ctk.CTkFrame(app)
    file_frame.pack(pady=20)

    # Кнопка для открытия файла
    open_button = ctk.CTkButton(file_frame, text="Открыть файл", command=lambda: open_file(tree, set_file_path, file_label))
    open_button.pack(side="left", padx=10)

    # Метка для отображения названия открытого файла
    file_label = ctk.CTkLabel(file_frame, text="Файл не открыт")
    file_label.pack(side="left", padx=10)

    # Поле ввода URL
    url_entry = ctk.CTkEntry(app, width=400)
    url_entry.pack(pady=20)

    # Кнопка для добавления строки
    add_button = ctk.CTkButton(app, text="Добавить строку", command=lambda: on_button_click(url_entry, error_label, tree, file_path))
    add_button.pack(pady=20)

    # Метка для отображения ошибок
    error_label = ctk.CTkLabel(app, text="")
    error_label.pack(pady=20)

    # Кадр для таблицы и ползунков
    table_frame = ctk.CTkFrame(app)
    table_frame.pack(pady=20, fill="both", expand=True)

    # Создание treeview для отображения данных Excel
    columns = ['Полугодие', 'квартал', 'месяц', 'дата', 'часы мероприятия', 'мероприятие', 'Проект', 'количество волонтеров', 'количество благополучателей', 'место проведения', 'краткое описание', 'Ссылка', 'время проведения', 'общее количество часов волонтёров']
    tree = ttk.Treeview(table_frame, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)

    tree.pack(side="left", fill="both", expand=True)

 
    # Горизонтальный ползунок
    x_scrollbar = ttk.Scrollbar(app, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=x_scrollbar.set)
    x_scrollbar.pack(side="bottom", fill="x")
    x_scrollbar.pack_propagate(False)

    # Загрузка данных при запуске
    load_excel_data(tree)

    app.mainloop()

def set_file_path(path, file_label):
    global file_path
    file_path = path
    file_label.configure(text=f"Открыт файл: {file_path}")

if __name__ == "__main__":
    main()
