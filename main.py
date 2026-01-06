import tkinter as tk
from src.screens.main_screen import MainScreen
from src.utils import check_env
from src.screens.dependency_screen import DependencyWindow

# =========================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    env = check_env()

    MainScreen(root)
    root.deiconify()   

    if not env["ok"]:
        DependencyWindow(root, env["python"], env["pyinstaller"])

    root.mainloop()
