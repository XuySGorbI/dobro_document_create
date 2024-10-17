import customtkinter as ctk
from tkinter import ttk
from dobro_pars import dobro_parser
# from linc_pars import Lincs_parser
from tkcalendar import DateEntry

file_path=None
class_one_pars = dobro_parser()

class EventExcelUpdaterApp:
    
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("800x600")
        self.app.title("Event Excel Updater")
        
        # Setup the main UI
        self.setup_gui()

    
    def setup_gui(self):
        # Error label for errors and outputs for the user
        err_label = ctk.CTkLabel(self.app, text="Вывод процесса")
        err_label.pack(pady=10)
        
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

        # Label for the right column
        right_label = ctk.CTkLabel(right_frame, text="Даты")
        right_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        # "Дата от" field
        start_date_label = ctk.CTkLabel(right_frame, text="От:")
        start_date_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.start_date_entry = DateEntry(right_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        # "Дата до" field
        end_date_label = ctk.CTkLabel(right_frame, text="До:")
        end_date_label.grid(row=2, column=0, padx=5, pady=5)
        
        self.end_date_entry = DateEntry(right_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Label for "Индекс организации"
        org_index_label = ctk.CTkLabel(right_frame, text="Индекс организации")
        org_index_label.grid(row=3, column=0, padx=5, pady=10, columnspan=2)

        # Entry field for organization index
        self.org_index_entry = ctk.CTkEntry(right_frame, width=300)
        self.org_index_entry.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        # Frame for two buttons in the right column
        right_buttons_frame = ctk.CTkFrame(right_frame)
        right_buttons_frame.grid(row=5, column=0, pady=10, columnspan=2)

        # Two buttons side by side in the right column
        right_button_1 = ctk.CTkButton(right_buttons_frame, text="Открыть файл", command=class_one_pars.open_file)
        right_button_1.grid(row=0, column=0, padx=5)

        right_button_2 = ctk.CTkButton(right_buttons_frame, text="Создать отчёт")
        right_button_2.grid(row=0, column=1, padx=5)

        # Frame for the table (Treeview)
        table_frame = ctk.CTkFrame(self.app)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def pars_all(self):
        
        # lincs = Lincs_parser()        
        
        class_one_pars.for_button_pars()
    
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = EventExcelUpdaterApp()
    app.run()