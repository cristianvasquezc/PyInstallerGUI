import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.utils import resource_path, set_app_icon, center_window

class DependencyWindow(tk.Toplevel):
    def __init__(self, parent, python_ok, pyinstaller_ok):
        super().__init__(parent)

        self.title("Dependencias requeridas")
        self.resizable(False, False)
        set_app_icon(self)
        self.transient(parent)
        self.grab_set()

        center_window(self, 460, 200)

        ttk.Label(
            self,
            text="Faltan dependencias necesarias para ejecutar esta aplicación",
            font=("Segoe UI", 10, "bold"),
            wraplength=430,
            justify="center"
        ).pack(pady=(15, 10))

        frame = ttk.Frame(self)
        frame.pack(pady=10, padx=20, fill="x")

        py_status = "✓ Python instalado" if python_ok else "❌ Python no está instalado"
        lbl_python = ttk.Label(frame, text=py_status)
        lbl_python.grid(row=0, column=0, sticky="w", pady=4)
        
        btn_python = ttk.Button(frame, text="Descargar Python",
                                command=lambda: webbrowser.open("https://www.python.org/downloads/"))
        btn_python.grid(row=0, column=1, sticky="e")
        if python_ok:
            btn_python.state(["disabled"])

        frame.columnconfigure(0, weight=1)

        pi_status = "✓ PyInstaller instalado" if pyinstaller_ok else "❌ PyInstaller no está instalado"
        lbl_pyinstaller = ttk.Label(frame, text=pi_status)
        lbl_pyinstaller.grid(row=1, column=0, sticky="w", pady=4)
        
        btn_pyinstaller = ttk.Button(frame, text="Instalar PyInstaller",
                                     command=lambda: webbrowser.open("https://pyinstaller.org/en/stable/installation.html"))
        btn_pyinstaller.grid(row=1, column=1, sticky="e")
        if pyinstaller_ok:
            btn_pyinstaller.state(["disabled"])
