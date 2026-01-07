import tkinter as tk
from src.screens.settings_screen import SettingsWindow
from src.screens.about_screen import AboutWindow
from src.screens.update_screen import UpdateWindow

class MenuBar(tk.Menu):
    def __init__(self, main_screen):
        super().__init__(main_screen.root)
        self.main_screen = main_screen
        self.create_menu()
        self.bind_keys()

    def create_menu(self):
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Configuración", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.main_screen.root.quit)
        self.add_cascade(label="Archivo", menu=file_menu)

        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="Buscar actualizaciones", command=self.check_updates)
        help_menu.add_separator()
        help_menu.add_command(label="Acerca de", command=self.show_about)
        self.add_cascade(label="Ayuda", menu=help_menu)

    def bind_keys(self):
        self.main_screen.root.bind("<F1>", self.show_about)

    def open_settings(self, event=None):
        def save_callback(py, pi):
            self.main_screen.python_path = py
            self.main_screen.pyinstaller_path = pi
            
        SettingsWindow(self.main_screen.root, self.main_screen.python_path, self.main_screen.pyinstaller_path, save_callback)

    def show_about(self, event=None):
        AboutWindow(self.main_screen.root)

    def check_updates(self, event=None):
        UpdateWindow(self.main_screen.root)
