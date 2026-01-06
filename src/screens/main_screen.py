import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from src.screens.build_screen import BuildWindow
from src.utils import check_env
import os

class MainScreen:

    def __init__(self, root):
        self.root = root
        root.title("PyInstaller GUI Builder")
        root.set_app_icon()
        root.resizable(False, False)
        root.center_window(780, 380)

        self.data_files = []
        self.binaries = []
        self.hidden_imports = []
        self.collect_all_list = []
        self.icon_path = None
        self.icon_img = None

        self.placeholder_img = ImageTk.PhotoImage(
            Image.new("RGBA", (100, 100))
        )

        self.build_ui()

        self.default_icon = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets/installer-icon.ico"
        )

    # ================= UI =================
    def build_ui(self):

        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        main.columnconfigure(2, weight=1)

        # ===== ICONO =====
        self.icon_label = tk.Label(
            main,
            width=100,
            height=100,
            image=self.placeholder_img,
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

        ttk.Checkbutton(options, text="Windowed (Sin consola)", variable=self.windowed).grid(row=0, column=0, padx=6)
        ttk.Checkbutton(options, text="Onefile", variable=self.onefile).grid(row=0, column=1, padx=6)
        ttk.Checkbutton(options, text="Clean build", variable=self.clean).grid(row=0, column=2, padx=6)
        ttk.Checkbutton(options, text="Strip", variable=self.strip).grid(row=0, column=3, padx=6)
        ttk.Checkbutton(options, text="Un UPX", variable=self.noupx).grid(row=0, column=4, padx=6)

        # ===== NOTEBOOK =====
        notebook = ttk.Notebook(main)
        notebook.grid(row=4, column=0, columnspan=4, sticky="nsew", pady=10)

        self.tab_data(notebook)
        self.tab_binaries(notebook) 
        self.tab_imports(notebook)
        self.tab_collect_all(notebook)
        self.tab_advanced(notebook)

        # ===== PROCESAR =====
        button_frame = tk.Frame(main)
        button_frame.grid(row=5, column=0, columnspan=4, sticky="e", pady=(0, 8))
        
        style = ttk.Style()
        style.configure("Big.TButton", font=("", 14, "bold"))

        self.btn_process = ttk.Button(
            button_frame, 
            text="Procesar", 
            command=self.process,
            padding=(10, 10),
            style="Big.TButton" 
        )
        self.btn_process.pack(side="right")

        check_env(self.btn_process)

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
        btns.pack(side="left", fill="y", padx=(10, 0))

        ttk.Button(btns, text="Añadir Archivo", command=self.add_data_file).pack(fill="x", pady=(0, 5))
        ttk.Button(btns, text="Añadir Carpeta", command=self.add_data_folder).pack(fill="x", pady=(0, 5))

        self.btn_remove_data = ttk.Button(btns, text="Eliminar", command=self.remove_data)
        self.btn_remove_data.pack(fill="x")
        self.btn_remove_data.state(["disabled"])

        self.list_data.bind("<<ListboxSelect>>", lambda e: self.on_select(self.list_data, self.btn_remove_data))

    def tab_binaries(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="Binarios")
    
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(side="left", fill="both", expand=True)
    
        self.list_binaries = tk.Listbox(list_frame, height=6)
        self.list_binaries.pack(fill="both", expand=True)
    
        btns = ttk.Frame(main_frame)
        btns.pack(side="left", fill="y", padx=(10, 0))
    
        ttk.Button(btns, text="Añadir Archivo", command=self.add_binary_file).pack(fill="x", pady=(0, 5))
    
        self.btn_remove_bin = ttk.Button(btns, text="Eliminar", command=self.remove_binary)
        self.btn_remove_bin.pack(fill="x")
        self.btn_remove_bin.state(["disabled"])

        self.list_binaries.bind("<<ListboxSelect>>", lambda e: self.on_select(self.list_binaries, self.btn_remove_bin))

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
        btns.pack(side="left", fill="y", padx=(10, 0))

        ttk.Button(btns, text="Añadir", command=self.add_import).pack(fill="x", pady=(0, 5))
        
        self.btn_remove_imp = ttk.Button(btns, text="Eliminar", command=self.remove_import)
        self.btn_remove_imp.pack(fill="x")
        self.btn_remove_imp.state(["disabled"])

        self.list_imports.bind("<<ListboxSelect>>", lambda e: self.on_select(self.list_imports, self.btn_remove_imp))

    def tab_collect_all(self, nb):
        tab = ttk.Frame(nb)
        nb.add(tab, text="Collect All")

        main_frame = ttk.Frame(tab)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        list_frame = ttk.Frame(main_frame)
        list_frame.pack(side="left", fill="both", expand=True)

        self.list_collect = tk.Listbox(list_frame, height=6)
        self.list_collect.pack(fill="both", expand=True)

        btns = ttk.Frame(main_frame)
        btns.pack(side="left", fill="y", padx=(10, 0))

        ttk.Button(btns, text="Añadir", command=self.add_collect).pack(fill="x", pady=(0, 5))
        
        self.btn_remove_collect = ttk.Button(btns, text="Eliminar", command=self.remove_collect)
        self.btn_remove_collect.pack(fill="x")
        self.btn_remove_collect.state(["disabled"])

        self.list_collect.bind("<<ListboxSelect>>", lambda e: self.on_select(self.list_collect, self.btn_remove_collect))

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
            img = Image.open(f).resize((100, 100), Image.Resampling.LANCZOS)
            self.icon_img = ImageTk.PhotoImage(img)
            self.icon_label.config(image=self.icon_img)

    def on_select(self, listbox, btn):
        if listbox.curselection():
            btn.state(["!disabled"])
        else:
            btn.state(["disabled"])

    def add_data_file(self):
        files = filedialog.askopenfilenames(title="Seleccionar archivos")
        for f in files:
            if f and f not in self.data_files:
                self.data_files.append(f)
                self.list_data.insert(tk.END, f"{f} (Archivo)")
    
    def add_data_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta")
        if folder and folder not in self.data_files:
            self.data_files.append(folder)
            self.list_data.insert(tk.END, f"{folder} (Carpeta)")

    def remove_data(self):
        sel = self.list_data.curselection()
        if sel:
            self.data_files.pop(sel[0])
            self.list_data.delete(sel)
            self.btn_remove_data.state(["disabled"])

    def add_binary_file(self):
        files = filedialog.askopenfilenames(title="Seleccionar binarios")
        for f in files:
            if f and f not in self.binaries:
                self.binaries.append(f)
                self.list_binaries.insert(tk.END, f)

    def remove_binary(self):
        sel = self.list_binaries.curselection()
        if sel:
            self.binaries.pop(sel[0])
            self.list_binaries.delete(sel)
            self.btn_remove_bin.state(["disabled"])
    
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
            self.btn_remove_imp.state(["disabled"])

    def add_collect(self):
        name = simple_input(self.root)
        if name:
            self.collect_all_list.append(name)
            self.list_collect.insert(tk.END, name)

    def remove_collect(self):
        sel = self.list_collect.curselection()
        if sel:
            self.collect_all_list.pop(sel[0])
            self.list_collect.delete(sel)
            self.btn_remove_collect.state(["disabled"])

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
    
        # Helper para calcular destino
        def get_dest(path, base_dir):
            try:
                abs_path = os.path.abspath(path)
                abs_base = os.path.abspath(base_dir)
                
                if os.path.splitdrive(abs_path)[0].lower() != os.path.splitdrive(abs_base)[0].lower():
                    return os.path.basename(abs_path) if os.path.isdir(abs_path) else "."

                rel = os.path.relpath(abs_path, abs_base)
                
                if rel.startswith(".."):
                    return os.path.basename(abs_path) if os.path.isdir(abs_path) else "."
                
                if os.path.isfile(abs_path):
                    d = os.path.dirname(rel)
                    return d if d else "."
                else:
                    return rel
            except Exception:
                return "."

        workdir = os.path.dirname(os.path.abspath(script))

        for f in self.data_files:
            dest = get_dest(f, workdir)
            cmd.append(f'--add-data "{f};{dest}"')

        for b in self.binaries:
            dest = get_dest(b, workdir)
            cmd.append(f'--add-binary "{b};{dest}"')
    
        for h in self.hidden_imports:
            cmd.append(f'--hidden-import {h}')

        for c in self.collect_all_list:
            cmd.append(f'--collect-all "{c}"')
    
        if self.debug.get():
            cmd.append(f'--debug {self.debug.get()}')
    
        if self.loglevel.get():
            cmd.append(f'--log-level {self.loglevel.get()}')
            
        cmd.append(f'"{script}"')
    
        workdir = os.path.abspath(os.path.dirname(script))
        BuildWindow(self.root, " ".join(cmd), workdir)

# =========================
def simple_input(parent):
    w = tk.Toplevel(parent)
    w.withdraw()
    w.title("Agregar módulo")
    w.set_app_icon()
    w.resizable(False, False)
    w.center_window(300, 100)
    w.deiconify()
    w.grab_set()

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
