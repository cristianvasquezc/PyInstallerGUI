import subprocess
import shutil
import sys
import os

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
    except AttributeError:
        base = os.path.abspath(os.path.dirname(__file__)) 
    return os.path.join(base, rel_path)

def set_app_icon(window, icon_name="assets/icon.ico"):
    from tkinter import TclError
    icon_path = resource_path(icon_name)
    if os.path.exists(icon_path):
        try:
            window.iconbitmap(icon_path)
        except TclError:
            pass

def is_python_installed():
    try:
        subprocess.run(
            ["python", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except Exception:
        return False

def is_pyinstaller_installed():
    return shutil.which("pyinstaller") is not None

def check_env(*buttons):
    python_ok = is_python_installed()
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
