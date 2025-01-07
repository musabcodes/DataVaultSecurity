import tkinter as tk
from gui import SecurityScannerGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityScannerGUI(root)
    root.mainloop()
