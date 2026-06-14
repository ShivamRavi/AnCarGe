import os
import tkinter as tk
from PIL import Image, ImageTk

class DonePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF6F7")

        # try package-relative image path, fall back to simple label if missing
        imgs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imgs'))
        img_path = os.path.join(imgs_dir, 'cat-good-2.png')
        tk_title_img = None
        try:
            img = Image.open(img_path)
            tk_title_img = ImageTk.PhotoImage(img)
        except Exception:
            try:
                # try a generic placeholder
                placeholder = os.path.join(imgs_dir, 'home_placeholder.svg')
                img = Image.open(placeholder)
                tk_title_img = ImageTk.PhotoImage(img)
            except Exception:
                tk_title_img = None

        if tk_title_img:
            title_img = tk.Label(self, image=tk_title_img, borderwidth=0, highlightthickness=0, bg="#FFF6F7")
            title_img.image = tk_title_img  # type: ignore
            title_img.pack(pady=2, expand=True, anchor="center", padx=40)
        else:
            title_img = tk.Label(self, text="(Done Image)", bg="#FFF6F7", fg="#000000")
            title_img.pack(pady=8)

        title_txt = tk.Label(self, text=" Done!", font=("Press Start 2P", 30), bg="#FFF6F7", fg="#000000")
        subtitle_txt = tk.Label(self, text="good kitty", font=("Press Start 2P", 12), bg="#FFF6F7", fg="#000000")

        title_txt.pack(pady=0, expand=True, anchor="center")
        subtitle_txt.pack(pady=0, expand=True, anchor="center")

    def clear_all(self):
        for widget in self.winfo_children():
            widget.destroy()

    def wait_clear_all(self):
        self.after(2000, self.clear_all)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Arecarge - Done Page")
    root.geometry("350x300")
    page = DonePage(root)
    page.pack(fill="both", expand=True)
    root.mainloop()
