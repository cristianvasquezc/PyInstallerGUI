import tkinter as tk
from src.screens.main_screen import MainScreen
from src.utils import resource_path, center_window, check_env
from src.screens.dependency_screen import DependencyWindow

# =========================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    env = check_env()

    if not env["ok"]:
        DependencyWindow(root, env["python"], env["pyinstaller"])

    MainScreen(root)
    center_window(root, 780, 420)
    root.deiconify()   
    root.mainloop()
