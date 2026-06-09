import tkinter as tk
import sys
sys.path.insert(0, "c:/Users/shiva/OneDrive/Desktop/AnCarGe v5")

from arecarge.ui.switcher import Switcher
from arecarge.ui.pages import gui_home

root = tk.Tk()
root.configure(bg="#FFF6F7")
root.title("GUI Test")
root.geometry("400x400")
root.attributes("-topmost", True)

switcher = Switcher(root)
switcher.pack(fill="both", expand=True)

print("Showing home page...")
switcher.show_page(gui_home.HomePage)
print("Home page shown!")
print(f"Current page: {switcher.current_page}")
print(f"Root window visible: {root.winfo_exists()}")

root.mainloop()
