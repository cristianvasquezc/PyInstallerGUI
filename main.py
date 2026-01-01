import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import threading
import sys
import os

# =========================
# VENTANA DE LOGS
# =========================
class BuildWindow(tk.Toplevel):
    def __init__(self, parent, command):
        super().__init__(parent)
        self.title("Proceso PyInstaller")
        self.resizable(False, False)
        self.center_window(720, 460)

        self.transient(parent)
        self.grab_set()

        if os.path.exists(resource_path("icon.ico")):
            self.iconbitmap(resource_path("icon.ico"))

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

    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.geometry(f"{width}x{height}+{x}+{y}")

    # -------- helper para escribir logs --------
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
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
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

# =========================
# APP PRINCIPAL
# =========================
class PyInstallerUI:

    def __init__(self, root):
        self.root = root
        root.title("PyInstaller GUI Builder")
        root.resizable(False, False)
        root.configure(bg="#f0f0f0")

        self.data_files = []
        self.hidden_imports = []
        self.icon_path = None
        self.icon_img = None

        self.placeholder_img = ImageTk.PhotoImage(
            Image.new("RGBA", (140, 140), "#dcdcdc")
        )

        self.build_ui()

        self.default_icon = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "installer-icon.ico"
        )

    # ================= UI =================
    def build_ui(self):

        main = tk.Frame(self.root, bg="#f0f0f0")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        main.columnconfigure(2, weight=1)

        # ===== ICONO =====
        self.icon_label = tk.Label(
            main,
            image=self.placeholder_img,
            bg="#dcdcdc",
            relief="solid",
            borderwidth=1
        )
        self.icon_label.grid(row=0, column=0, rowspan=3, padx=(0, 12), pady=5)
        self.icon_label.bind("<Button-1>", lambda e: self.pick_icon())

        # ===== CAMPOS =====
        ttk.Label(main, text="Script Principal (.py)").grid(row=0, column=1, sticky="w", pady=4)
        self.entry_script = ttk.Entry(main)
        self.entry_script.grid(row=0, column=2, sticky="ew", padx=5)
        ttk.Button(main, text="Seleccionar", command=self.pick_script).grid(row=0, column=3, padx=5)

        ttk.Label(main, text="Nombre de archivo").grid(row=1, column=1, sticky="w", pady=4)
        self.entry_name = ttk.Entry(main)
        self.entry_name.grid(row=1, column=2, sticky="ew", padx=5)
        self.entry_name.insert(0, "setup") 

        ttk.Label(main, text="Carpeta de salida").grid(row=2, column=1, sticky="w", pady=4)
        self.entry_dist = ttk.Entry(main)
        self.entry_dist.grid(row=2, column=2, sticky="ew", padx=5)
        ttk.Button(main, text="Seleccionar", command=self.pick_dist).grid(row=2, column=3, padx=5)

        # ===== OPCIONES =====
        options = ttk.Frame(main)
        options.grid(row=3, column=0, columnspan=4, sticky="w", pady=10)

        self.onefile = tk.BooleanVar(value=True)
        self.clean = tk.BooleanVar(value=True)
        self.strip = tk.BooleanVar()
        self.noupx = tk.BooleanVar()
        self.windowed = tk.BooleanVar(value=True)

        ttk.Checkbutton(options, text="Onefile", variable=self.onefile).grid(row=0, column=0, padx=6)
        ttk.Checkbutton(options, text="Clean build", variable=self.clean).grid(row=0, column=1, padx=6)
        ttk.Checkbutton(options, text="Strip", variable=self.strip).grid(row=0, column=2, padx=6)
        ttk.Checkbutton(options, text="Un UPX", variable=self.noupx).grid(row=0, column=3, padx=6)
        ttk.Checkbutton(options, text="Windowed (Sin consola)", variable=self.windowed).grid(row=0, column=4, padx=6)

        # ===== NOTEBOOK =====
        notebook = ttk.Notebook(main)
        notebook.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=10)

        self.tab_data(notebook)
        self.tab_imports(notebook)
        self.tab_advanced(notebook)

        # ===== PROCESAR =====
        button_frame = tk.Frame(main)
        button_frame.grid(row=5, column=0, columnspan=4, sticky="e", pady=(0, 8))

        ttk.Button(
            button_frame, 
            text="Procesar", 
            command=self.process,
            width=15,
            padding=(30, 13)
        ).pack(side="right")

    # ================= TABS =================
    def tab_data(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="Datos")

        main_frame = ttk.Frame(tab)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        list_frame = ttk.Frame(main_frame)
        list_frame.pack(side="left", fill="both", expand=True)

        self.list_data = tk.Listbox(list_frame, height=6)
        self.list_data.pack(fill="both", expand=True)

        btns = ttk.Frame(main_frame)
        btns.pack(side="left", fill="y", padx=(5, 0))

        ttk.Button(btns, text="Añadir", command=self.add_data).pack(fill="x", pady=(0, 5))
        ttk.Button(btns, text="Eliminar", command=self.remove_data).pack(fill="x")

    def tab_imports(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="Imports")

        main_frame = ttk.Frame(tab)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        list_frame = ttk.Frame(main_frame)
        list_frame.pack(side="left", fill="both", expand=True)

        self.list_imports = tk.Listbox(list_frame, height=6)
        self.list_imports.pack(fill="both", expand=True)

        btns = ttk.Frame(main_frame)
        btns.pack(side="left", fill="y", padx=(5, 0))

        ttk.Button(btns, text="Añadir", command=self.add_import).pack(fill="x", pady=(0, 5))
        ttk.Button(btns, text="Eliminar", command=self.remove_import).pack(fill="x")

    def tab_advanced(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="Avanzado")

        ttk.Label(tab, text="Debug").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.debug = ttk.Combobox(tab, values=["", "all", "imports"], width=20, state="readonly")
        self.debug.grid(row=0, column=1, padx=5)

        ttk.Label(tab, text="Log level").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.loglevel = ttk.Combobox(tab, values=["", "DEBUG", "INFO", "WARN"], width=20, state="readonly")
        self.loglevel.grid(row=1, column=1, padx=5)

    # ================= LÓGICA =================
    def pick_script(self):
        f = filedialog.askopenfilename(filetypes=[("Python", "*.py")])
        if f:
            self.entry_script.delete(0, tk.END)
            self.entry_script.insert(0, f)

    def pick_dist(self):
        f = filedialog.askdirectory()
        if f:
            self.entry_dist.delete(0, tk.END)
            self.entry_dist.insert(0, f)

    def pick_icon(self):
        f = filedialog.askopenfilename(filetypes=[("Icon", "*.ico")])
        if f:
            self.icon_path = f
            img = Image.open(f).resize((140, 140))
            self.icon_img = ImageTk.PhotoImage(img)
            self.icon_label.config(image=self.icon_img)

    def add_data(self):
        f = filedialog.askopenfilename()
        if f:
            self.data_files.append(f)
            self.list_data.insert(tk.END, f)

    def remove_data(self):
        sel = self.list_data.curselection()
        if sel:
            self.data_files.pop(sel[0])
            self.list_data.delete(sel)

    def add_import(self):
        name = simple_input(self.root)
        if name:
            self.hidden_imports.append(name)
            self.list_imports.insert(tk.END, name)

    def remove_import(self):
        sel = self.list_imports.curselection()
        if sel:
            self.hidden_imports.pop(sel[0])
            self.list_imports.delete(sel)

    def process(self):
        script = self.entry_script.get().strip()
        name = self.entry_name.get().strip()
        dist = self.entry_dist.get().strip()
    
        # ===== VALIDACIONES OBLIGATORIAS =====
        if not script:
            messagebox.showerror(
                "Campo obligatorio",
                "Debe seleccionar el script principal (.py)"
            )
            return
    
        if not dist:
            messagebox.showerror(
                "Campo obligatorio",
                "Debe seleccionar la carpeta de salida"
            )
            return
    
        # ===== COMANDO BASE =====
        cmd = ["pyinstaller"]
    
        if self.onefile.get(): cmd.append("--onefile")
        if self.windowed.get(): cmd.append("--windowed")
        if self.clean.get(): cmd.append("--clean")
        if self.strip.get(): cmd.append("--strip")
        if self.noupx.get(): cmd.append("--noupx")
    
        # ===== OPCIONALES =====
        if self.icon_path:
            cmd.append(f'--icon "{self.icon_path}"')
        elif os.path.exists(self.default_icon):
            cmd.append(f'--icon "{self.default_icon}"')
            
        if name:
            cmd.append(f'--name "{name}"')
    
        cmd.append(f'--distpath "{dist}"')
    
        for f in self.data_files:
            cmd.append(f'--add-data "{f};."')
    
        for h in self.hidden_imports:
            cmd.append(f'--hidden-import {h}')
    
        if self.debug.get():
            cmd.append(f'--debug {self.debug.get()}')
    
        if self.loglevel.get():
            cmd.append(f'--log-level {self.loglevel.get()}')
            
        cmd.append(f'"{script}"')
    
        BuildWindow(self.root, " ".join(cmd))

# =========================
def simple_input(parent):
    w = tk.Toplevel(parent)
    w.title("Hidden import")
    width = 300
    height = 100
    w.geometry(f"{width}x{height}")
    w.resizable(False, False)
    w.grab_set()

    w.update_idletasks()
    screen_width = w.winfo_screenwidth()
    screen_height = w.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    w.geometry(f"{width}x{height}+{x}+{y}")

    icon_path = resource_path("icon.ico")
    if os.path.exists(icon_path):
        w.iconbitmap(icon_path)

    ttk.Label(w, text="Nombre del módulo").pack(pady=10)
    e = ttk.Entry(w,width=40)
    e.pack(padx=10)
    e.focus()

    result = []

    def ok():
        result.append(e.get())
        w.destroy()

    ttk.Button(w, text="OK", command=ok).pack(pady=5)
    w.wait_window()
    return result[0] if result else None

# =========================
def center_window(root, width, height):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    root.geometry(f"{width}x{height}+{x}+{y}")

def resource_path(rel_path):
    try:
        base = sys._MEIPASS
    except:
        base = os.path.abspath(".")
    return os.path.join(base, rel_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    root.iconbitmap(resource_path("icon.ico"))
    PyInstallerUI(root)
    center_window(root, 780, 420)
    root.deiconify()   
    root.mainloop()
