import shutil
import sys
import os
import tkinter as tk

def center_window(self, width, height):
    self.update_idletasks()
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    self.geometry(f"{width}x{height}+{x}+{y}")

def resource_path(rel_path):
    try:
        base = sys._MEIPASS 
    except AttributeError:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    return os.path.join(base, rel_path)

def set_app_icon(self, icon_name="assets/icon.ico"):
    from tkinter import TclError
    icon_path = resource_path(icon_name)
    if os.path.exists(icon_path):
        try:
            self.iconbitmap(icon_path)
        except TclError:
            pass

# Monkey-patching
tk.Tk.center_window = center_window
tk.Toplevel.center_window = center_window
tk.Tk.set_app_icon = set_app_icon
tk.Toplevel.set_app_icon = set_app_icon

def is_python_installed():
    return True

def get_python_path():
    if getattr(sys, 'frozen', False):
        path = shutil.which("python")
        return path if path else sys.executable
    else:
        return sys.executable

def get_pyinstaller_path():
    path = shutil.which("pyinstaller")
    return path if path else ""

def is_pyinstaller_installed():
    return get_pyinstaller_path() != ""

def check_env(*buttons, python_path=None, pyinstaller_path=None):
    if python_path and os.path.isfile(python_path):
        python_ok = True
    else:
        python_ok = is_python_installed()
    
    if pyinstaller_path and os.path.isfile(pyinstaller_path):
        pyinstaller_ok = True
    else:
        pyinstaller_ok = is_pyinstaller_installed()
    
    ok = python_ok and pyinstaller_ok

    for btn in buttons:
        try:
            if not ok:
                btn.state(["disabled"])
            else:
                btn.state(["!disabled"])
        except Exception:
            pass

    return {"python": python_ok, "pyinstaller": pyinstaller_ok, "ok": ok}
