import tkinter as tk
from tkinter import ttk
import webbrowser
from src.utils import resource_path
from version import VERSION

class AboutWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.withdraw()
        
        self.title("Acerca de")
        self.set_app_icon()
        self.resizable(False, False)
        self.center_window(400, 280)
        self.transient(parent)
        self.grab_set()
        
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ttk.Label(
            main, 
            text="PyInstaller GUI Builder", 
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(10, 5))

        # Version
        ttk.Label(main, text=f"v{VERSION}", foreground="#666").pack()

        # Description
        ttk.Label(
            main, 
            text="Herramienta gráfica para simplificar\nel uso de PyInstaller.",
            justify="center"
        ).pack(pady=20)

        # Link
        link = ttk.Label(
            main, 
            text="Creado por Cristian Vásquez", 
            foreground="#0066cc", 
            cursor="hand2",
            font=("Segoe UI", 9, "underline")
        )
        link.pack()
        link.bind("<Button-1>", lambda e: webbrowser.open("https://mislinks.netlify.app/"))

        # Button
        ttk.Button(main, text="Cerrar", command=self.destroy).pack(pady=(25, 0))
        
        self.deiconify()
        self.bind("<Escape>", lambda e: self.destroy())
