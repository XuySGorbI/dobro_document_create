import customtkinter as ctk
from tkinter import ttk

class EventExcelUpdaterApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("800x600")
        self.app.title("Event Excel Updater")
        
        # Setup the main UI
        self.setup_gui()

    def setup_gui(self):
        # Frame for the upper section (two columns for inputs and buttons)
        upper_frame = ctk.CTkFrame(self.app)
        upper_frame.pack(fill="x", pady=10, padx=10)

        # Left column frame
        left_frame = ctk.CTkFrame(upper_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=10)

        # Label for "Интерфейс 1" above the left column
        left_label = ctk.CTkLabel(left_frame, text="Интерфейс 1")
        left_label.pack(pady=10)

        # Entry field in the left column
        self.left_entry = ctk.CTkEntry(left_frame, width=300)
        self.left_entry.pack(pady=10)

        # Button in the left column
        left_button = ctk.CTkButton(left_frame, text="Кнопка")
        left_button.pack(pady=10)

        # Right column frame
        right_frame = ctk.CTkFrame(upper_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=10)

        # Label for "Интерфейс 2" above the right column
        right_label = ctk.CTkLabel(right_frame, text="Интерфейс 2")
        right_label.pack(pady=10)

        # Entry field in the right column
        self.right_entry = ctk.CTkEntry(right_frame, width=300)
        self.right_entry.pack(pady=10)

        # Frame for two buttons in the right column
        right_buttons_frame = ctk.CTkFrame(right_frame)
        right_buttons_frame.pack(pady=10)

        # Two buttons side by side in the right column
        right_button_1 = ctk.CTkButton(right_buttons_frame, text="Кнопка 1")
        right_button_1.grid(row=0, column=0, padx=5)

        right_button_2 = ctk.CTkButton(right_buttons_frame, text="Кнопка 2")
        right_button_2.grid(row=0, column=1, padx=5)

        # Frame for the table (Treeview)
        table_frame = ctk.CTkFrame(self.app)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Table to display data
        columns = [
            'Полугодие', 'квартал', 'месяц', 'дата', 'часы мероприятия', 
            'мероприятие', 'Проект', 'количество волонтеров', 'количество благополучателей', 
            'место проведения', 'краткое описание', 'Ссылка', 'время проведения', 
            'общее количество часов волонтёров'
        ]
        
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(side="left", fill="both", expand=True)

        # Horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(self.app, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=x_scrollbar.set)
        x_scrollbar.pack(side="bottom", fill="x")

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = EventExcelUpdaterApp()
    app.run()