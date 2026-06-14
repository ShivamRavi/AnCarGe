import os
import tkinter as tk
from PIL import Image, ImageTk

class DistractedPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF6F7")

        imgs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imgs'))
        bad_path = os.path.join(imgs_dir, 'cat-bad.png')
        try:
            img = Image.open(bad_path)
        except Exception:
            img = None

        if img is not None:
            tk_title_img = ImageTk.PhotoImage(img, master=parent)
            title_img = tk.Label(self, image=tk_title_img, borderwidth=0, highlightthickness=0, bg="#FFF6F7")
            title_img.image = tk_title_img  # type: ignore
            title_img.pack(side="top", pady=3)
        else:
            title_img = tk.Label(self, text="(distracted)", bg="#FFF6F7")
            title_img.pack(side="top", pady=3)

        title_txt = tk.Label(self, text="dIsTrAcTiOn", font=("Press Start 2P", 22), bg="#FFF6F7", fg="#000000")
        subtitle_txt = tk.Label(self, text="evil cat got you!", font=("Press Start 2P", 8), bg="#FFF6F7", fg="#000000")
        title_txt.pack(side="top")
        subtitle_txt.pack(side="top")




if __name__ == "__main__":
    root = tk.Tk()
    root.title("Arecarge - Distracted Page")
    root.geometry("400x300")
    page = DistractedPage(root)
    page.pack(fill="both", expand=True)
    root.mainloop()