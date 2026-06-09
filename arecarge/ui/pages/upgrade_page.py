import tkinter as tk
from PIL import Image, ImageTk
from arecarge.shared import sq

class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF6F7")

        img = Image.open("C:/Users/shiva/OneDrive/Desktop/AnCarGe v5/arecarge/ui/imgs/cards.webp")
        tk_title_img = ImageTk.PhotoImage(img)
        title_img = tk.Label(self, image=tk_title_img, borderwidth=0, highlightthickness=0, bg="#FFF6F7")
        title_img.image = tk_title_img  # type: ignore
        title_img.pack(side="top", pady=2)

        title_txt = tk.Label(self, text="ANCARGE", font=("Press Start 2P", 30), bg="#FFF6F7", fg="#000000")
        subtitle_txt = tk.Label(self, text="Type start in console to begin", font=("Press Start 2P", 8), bg="#FFF6F7", fg="#000000")
        title_txt.pack(side="top")
        subtitle_txt.pack(side="top")
        
        # Start button
        start_btn = tk.Button(self, text="START GAME", font=("Press Start 2P", 12), bg="#000000", fg="#FFFFFF", command=self.start_game, padx=20, pady=10)
        start_btn.pack(side="top", pady=30)
    
    def start_game(self):
        sq.put("start")
