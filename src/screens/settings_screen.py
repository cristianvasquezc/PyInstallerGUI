import tkinter as tk
from tkinter import ttk, filedialog
from src.utils import get_python_path, get_pyinstaller_path

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, current_python, current_pyinstaller, callback):
        super().__init__(parent)
        self.withdraw()
        self.callback = callback
        
        self.title("Configuración")
        self.set_app_icon()
        self.resizable(False, False)
        self.center_window(500, 150)
        self.deiconify()
        self.transient(parent)
        self.grab_set()

        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        main_frame.columnconfigure(1, weight=1)

        # ===== PYTHON =====
        ttk.Label(main_frame, text="Ruta Python:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_python = ttk.Entry(main_frame)
        self.entry_python.grid(row=0, column=1, sticky="ew", padx=5)
        self.entry_python.insert(0, current_python)
        ttk.Button(main_frame, text="...", width=3, command=self.browse_python).grid(row=0, column=2)

        # ===== PYINSTALLER =====
        ttk.Label(main_frame, text="Ruta PyInstaller:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_pi = ttk.Entry(main_frame)
        self.entry_pi.grid(row=1, column=1, sticky="ew", padx=5)
        self.entry_pi.insert(0, current_pyinstaller)
        ttk.Button(main_frame, text="...", width=3, command=self.browse_pyinstaller).grid(row=1, column=2)

        # ===== BOTONES =====
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=(20, 0), sticky="ew")

        ttk.Button(btn_frame, text="Restaurar valores por defecto", command=self.restore_defaults).pack(side="left")
        
        ttk.Button(btn_frame, text="Guardar", command=self.save).pack(side="right")
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side="right", padx=5)

    def browse_python(self):
        f = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
        if f:
            self.entry_python.delete(0, tk.END)
            self.entry_python.insert(0, f)

    def browse_pyinstaller(self):
        f = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
        if f:
            self.entry_pi.delete(0, tk.END)
            self.entry_pi.insert(0, f)

    def restore_defaults(self):
        self.entry_python.delete(0, tk.END)
        self.entry_python.insert(0, get_python_path())
        
        self.entry_pi.delete(0, tk.END)
        self.entry_pi.insert(0, get_pyinstaller_path())

    def save(self):
        py = self.entry_python.get().strip()
        pi = self.entry_pi.get().strip()
        self.callback(py, pi)
        self.destroy()
