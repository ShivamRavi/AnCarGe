import os
import tkinter as tk
from PIL import Image, ImageTk
from arecarge.shared import sq

class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF6F7")

        imgs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imgs'))
        cards_path = os.path.join(imgs_dir, 'cards.webp')
        placeholder_path = os.path.join(imgs_dir, 'home_placeholder.svg')

        try:
            img = Image.open(cards_path)
        except Exception:
            try:
                img = Image.open(placeholder_path)
            except Exception:
                img = None

        if img is not None:
            tk_title_img = ImageTk.PhotoImage(img, master=parent)
            title_img = tk.Label(self, image=tk_title_img, borderwidth=0, highlightthickness=0, bg="#FFF6F7")
            title_img.image = tk_title_img  # type: ignore
            title_img.pack(side="top", pady=2)

        title_txt = tk.Label(self, text="ANCARGE", font=("Press Start 2P", 30), bg="#FFF6F7", fg="#000000")
        subtitle_txt = tk.Label(self, text="Type start in console to begin", font=("Press Start 2P", 8), bg="#FFF6F7", fg="#000000")
        title_txt.pack(side="top")
        subtitle_txt.pack(side="top")
