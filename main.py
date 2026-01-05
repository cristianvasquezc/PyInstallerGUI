import tkinter as tk
from src.screens.main_screen import MainScreen
from src.utils import resource_path, center_window, is_python_installed, is_pyinstaller_installed
from src.screens.dependency_screen import DependencyWindow

# =========================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    python_ok = is_python_installed()
    pyinstaller_ok = is_pyinstaller_installed()

    if not (python_ok and pyinstaller_ok):
        DependencyWindow(root, python_ok, pyinstaller_ok)

    MainScreen(root)
    center_window(root, 780, 420)
    root.deiconify()   
    root.mainloop()
