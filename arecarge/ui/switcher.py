

from arecarge.ui.pages import gui_home, inventory_page, upgrade_page, boss_page, distracted_page as disp, done_page as dope
import tkinter as tk


class Switcher(tk.Frame):
    def __init__(self, parent, bg="#FFF6F7"):
        super().__init__(parent, bg=bg)
        self.parent = parent
        self.current_page = None
        self.current_bg = bg

    def show_page(self, page_class, bg=None, transition="fade", **kwargs):
        if bg:
            self.current_bg = bg
            self.configure(bg=bg)
            try:
                self.parent.configure(bg=bg)
            except Exception:
                pass

        new_page = page_class(self, **kwargs)
        self.show_page_frfr(new_page)
    def show_page_frfr(self, new_page):
        if self.current_page:
            self.current_page.destroy()
        screen_w = self.parent.winfo_screenwidth()
        screen_h = self.parent.winfo_screenheight()
        full_w = max(400, int(screen_w * 0.45))
        full_h = max(400, int(screen_h * 0.55))
        inventory_h = max(520, int(screen_h * 0.65))
        small_w = max(400, int(screen_w * 0.35))
        small_h = max(300, int(screen_h * 0.35))

        if isinstance(new_page, (gui_home.HomePage, boss_page.BossPage, inventory_page.InventoryPage)):
            if isinstance(new_page, inventory_page.InventoryPage):
                self.parent.geometry(f"{full_w}x{inventory_h}")
            else:
                self.parent.geometry(f"{full_w}x{full_h}")
            new_page.pack(fill="both", expand=True)
            self.current_page = new_page
        else:
            self.parent.geometry(f"{small_w}x{small_h}")
            self.parent.update_idletasks()
            width = self.parent.winfo_width() or small_w
            height = self.parent.winfo_height() or small_h
            new_page.place(x=0, y=0, width=width, height=height)
            self.current_page = new_page


    

if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    root.title("Arecarge - Switcher Test")
    root.geometry("400x300")
    root.configure(bg="#FFF6F7")

    switcher = Switcher(root)
    switcher.show_page(gui_home.HomePage)
    

    root.mainloop()