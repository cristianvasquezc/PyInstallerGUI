import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading

class BuildWindow(tk.Toplevel):
    def __init__(self, parent, command, workdir, env=None):
        super().__init__(parent)
        self.workdir = workdir
        self.env = env
        
        self.title("Proceso PyInstaller")
        self.set_app_icon()
        self.resizable(False, False)
        self.center_window(720, 460)

        self.transient(parent)
        self.grab_set()

        ttk.Label(self, text="Comando generado").pack(anchor="w", padx=10, pady=(10, 2))
        self.txt_cmd = tk.Text(self, height=4)
        self.txt_cmd.pack(fill="x", padx=10)
        self.txt_cmd.insert("1.0", command)
        self.txt_cmd.config(state="disabled")

        ttk.Label(self, text="Logs de PyInstaller").pack(anchor="w", padx=10, pady=(10, 2))
        self.txt_logs = tk.Text(
            self,
            bg="#111",
            fg="#0f0",
            state="disabled"
        )
        self.txt_logs.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=5)

        threading.Thread(target=self.run_build, args=(command,), daemon=True).start()



    def log(self, text):
        self.txt_logs.config(state="normal")
        self.txt_logs.insert(tk.END, text)
        self.txt_logs.see(tk.END)
        self.txt_logs.config(state="disabled")

    def run_build(self, command):
        self.log("Ejecutando PyInstaller...\n\n")

        process = subprocess.Popen(
            command,
            shell=True,
            cwd=self.workdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=self.env
        )

        for line in process.stdout:
            self.log(line)

        process.wait()
        code = process.returncode

        if code == 0:
            self.log("\n✔ Proceso finalizado correctamente\n")
            self.after(
                0,
                lambda: messagebox.showinfo(
                    "Build finalizado",
                    "El proceso terminó correctamente.\n\nEl ejecutable ya fue generado.", parent=self
                )
            )
        else:
            self.log(f"\n❌ Proceso finalizado con errores (código {code})\n")
            self.after(
                0,
                lambda: messagebox.showerror(
                    "Build con errores",
                    "El proceso terminó, pero hubo errores.\nRevisa los logs.",
                    parent=self
                )
            )
