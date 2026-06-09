import tkinter as tk
from PIL import Image, ImageTk

class DonePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF6F7")

        # Load image
        img = Image.open("C:/Users/shiva/OneDrive/Desktop/AnCarGe v5/arecarge/ui/imgs/cat-good-2.png")
        tk_title_img = ImageTk.PhotoImage(img)

        # Image label
        title_img = tk.Label(self, image=tk_title_img, borderwidth=0, highlightthickness=0, bg="#FFF6F7")
        title_img.image = tk_title_img  # type: ignore
        title_img.pack(pady=2, expand=True, anchor="center", padx=40)

        # Text labels
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
    root.geometry("400x300")
    page = DonePage(root)
    page.pack(fill="both", expand=True)
    root.mainloop()
