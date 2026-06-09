
import tkinter as tk
from turtle import done
from PIL import Image, ImageTk

class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFF6F7")

        title_label = tk.Label(
            self,
            text="MAIN MENU",
            font=("Press Start 2P", 20),
            bg="#FFF6F7",
            fg="#000000"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=15)

        self.grid_columnconfigure(0, weight=1)   
        self.grid_columnconfigure(1, weight=1)


        self.done_label = tk.Label(self, text="DONE", font=("Press Start 2P", 10),
                              bg="#FFF6F7", fg="#000000")
        self.done_label.grid(row=1, column=1, sticky="e", padx=23, pady=10)

        self.distracted_label = tk.Label(self, text="DISTRACT", font=("Press Start 2P", 10),
                                    bg="#FFF6F7", fg="#000000")
        self.distracted_label.grid(row=2, column=1, sticky="e", padx=23, pady=2)

        self.help_label = tk.Label(self, text="HELP", font=("Press Start 2P", 10),
                              bg="#FFF6F7", fg="#000000")
        self.help_label.grid(row=3, column=1, sticky="e", padx=23, pady=2)

        self.use_label = tk.Label(self, text="USE", font=("Press Start 2P", 10),
                             bg="#FFF6F7", fg="#000000")
        self.use_label.grid(row=4, column=1, sticky="e", padx=23, pady=2)


        for label in [self.done_label, self.distracted_label, self.help_label, self.use_label]:
            label.bind("<Button-1>", self.show_arrow)

        cat_img = Image.open("C:/Users/shiva/OneDrive/Desktop/AnCarGe v5/arecarge/ui/imgs/kittycat2.png")
        tk_cat_img = ImageTk.PhotoImage(cat_img, master=parent)

        cat_label = tk.Label(self, image=tk_cat_img, borderwidth=0,
                             highlightthickness=0, bg="#FFF6F7")
        cat_label.image = tk_cat_img  #type: ignore
        cat_label.grid(row=1, column=0, rowspan=4, pady=20, sticky="e")


        menu_labels = [self.done_label, self.distracted_label, self.help_label, self.use_label]
        self.menu_labels = menu_labels

    def show_arrow(self, event):
        for lbl in self.menu_labels:
            lbl.config(text=lbl.cget("text").replace("-> ", ""))

        original_text = event.widget.cget("text")
        event.widget.config(text="-> " + original_text)

        self.after(2000, lambda w=event.widget, t=original_text: w.config(text=t))


        


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Arecarge - Home Page")
    root.geometry("350x250")
    root.configure(bg="#FFF6F7")

    page = HomePage(root)
    page.pack(fill="both", expand=True)

    root.mainloop()

