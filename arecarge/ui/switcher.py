

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
        STANDARD_W = 350
        STANDARD_H = 400
        INVENTORY_W = 400
        INVENTORY_H = 520
        BOSS_W = 400
        BOSS_H = 400

        # Respect screen size but clamp to sensible defaults
        max_w = min(int(screen_w * 0.6), 800)
        max_h = min(int(screen_h * 0.7), 800)

        std_w = min(max(STANDARD_W, int(screen_w * 0.4)), max_w)
        std_h = min(max(STANDARD_H, int(screen_h * 0.45)), max_h)
        inv_h = min(max(INVENTORY_H, int(screen_h * 0.55)), max_h)
        boss_h = min(max(BOSS_H, int(screen_h * 0.45)), max_h)
        small_w = max(300, int(screen_w * 0.35))
        small_h = max(250, int(screen_h * 0.3))

        if isinstance(new_page, (gui_home.HomePage, boss_page.BossPage, inventory_page.InventoryPage)):
            if isinstance(new_page, inventory_page.InventoryPage):
                self.parent.geometry(f"{INVENTORY_W}x{inv_h}")
            elif isinstance(new_page, boss_page.BossPage):
                self.parent.geometry(f"{BOSS_W}x{boss_h}")
            else:
                self.parent.geometry(f"{std_w}x{std_h}")
            new_page.pack(fill="both", expand=True)
            self.current_page = new_page
        else:
            # small dialog-style pages use place and animate from 0 to full size
            self.parent.geometry(f"{STANDARD_W}x{STANDARD_H}")
            self.parent.update_idletasks()
            target_w = self.parent.winfo_width() or STANDARD_W
            target_h = self.parent.winfo_height() or STANDARD_H
            # start small
            new_page.place(x=0, y=0, width=1, height=1)
            self.current_page = new_page

            steps = 6
            def animate(step=1):
                if step > steps:
                    new_page.place(x=0, y=0, width=target_w, height=target_h)
                    return
                w = int(target_w * (step / steps))
                h = int(target_h * (step / steps))
                new_page.place(x=0, y=0, width=w, height=h)
                self.after(25, lambda: animate(step + 1))
            animate()


    

if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    root.title("Arecarge - Switcher Test")
    root.geometry("400x300")
    root.configure(bg="#FFF6F7")

    switcher = Switcher(root)
    switcher.show_page(gui_home.HomePage)
    

    root.mainloop()