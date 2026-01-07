import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import json
import webbrowser
import threading
import re
from version import VERSION

class UpdateWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.withdraw()
        self.title("Buscar Actualizaciones")
        self.resizable(False, False)
        self.center_window(300, 190)
        self.set_app_icon()
        self.transient(parent)
        self.grab_set()
        
        self.repo_url = "https://api.github.com/repos/cristianvasquezc/PyInstallerGUI/releases/latest"
        self.download_url = "https://github.com/cristianvasquezc/PyInstallerGUI/releases/latest"
        
        self.build_ui()
        self.deiconify()
        
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def build_ui(self):
        main = tk.Frame(self)
        main.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(main, text="Buscador de Actualizaciones", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        info_frame = tk.Frame(main)
        info_frame.pack(fill="x", pady=5)
        
        tk.Label(info_frame, text=f"Versión actual:").grid(row=0, column=0, sticky="w")
        tk.Label(info_frame, text=VERSION, font=("Arial", 10, "bold")).grid(row=0, column=1, sticky="w", padx=5)
        
        tk.Label(info_frame, text=f"Última versión:").grid(row=1, column=0, sticky="w")
        self.latest_version_label = tk.Label(info_frame, text="Buscando...", font=("Arial", 10, "bold"))
        self.latest_version_label.grid(row=1, column=1, sticky="w", padx=5)
        
        self.status_label = tk.Label(main, text="Comprobando disponibilidad...", fg="gray")
        self.status_label.pack(pady=10)
        
        self.update_btn = ttk.Button(main, text="Actualizar ahora", state="disabled", command=self.open_release_page)
        self.update_btn.pack(pady=5)
        
    def check_for_updates(self):
        try:
            req = urllib.request.Request(self.repo_url)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                tag = data.get("tag_name", "0.0.0")
                latest_v = tag.lstrip('vV')
                self.download_url = data.get("html_url", self.download_url)
                
                self.after(0, lambda: self.update_status(latest_v))
        except Exception as e:
            self.after(0, lambda: self.status_label.config(text=f"Error al buscar: {str(e)}", fg="red"))
            self.after(0, lambda: self.latest_version_label.config(text="Error"))

    def update_status(self, latest_v):
        self.latest_version_label.config(text=latest_v)
        
        def to_ints(v):
            return [int(p) for p in re.findall(r'\d+', v)]

        current = to_ints(VERSION)
        latest = to_ints(latest_v)
        
        if latest > current:
            self.status_label.config(text="¡Hay una nueva versión disponible!", fg="green")
            self.update_btn.state(["!disabled"])
        else:
            self.status_label.config(text="Ya tienes la última versión instalada.", fg="blue")

    def open_release_page(self):
        webbrowser.open(self.download_url)
        self.destroy()
