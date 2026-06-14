import tkinter as tk
from tkinter import font
import time
from PIL import Image, ImageTk, ImageDraw

BOSS_DEFS = {
    "ember": {"bg":"#2D0808","accent":"#FF7A18","icon":"//","subtitle":"Scorching sigma"},
    "blood": {"bg":"#290505","accent":"#C1121F","icon":"*()*","subtitle":"The Crimson rizller"},
    "xyolem": {"bg":"#08270F","accent":"#7DE68E","icon":"/*","subtitle":"The Verdant macaw (gag scarlet macaw)"},
    "default": {"bg":"#0F1425","accent":"#5E82F7","icon":"|","subtitle":"Ancient skibidi"},
}


def get_boss_style(name: str) -> dict:
    if not name:
        return BOSS_DEFS["default"]
    key = name.lower()
    for token, style in BOSS_DEFS.items():
        if token in key:
            return style
    return BOSS_DEFS["default"]


class BossPage(tk.Frame):
    def __init__(self, parent, boss=None, challenge_time=120):
        super().__init__(parent, bg="#0F1425")
        self.boss = boss
        self.challenge_time = challenge_time
        self.start_time = None
        self.timer_running = False

        if not boss:
            raise ValueError("BossPage requires a boss object")
        style = get_boss_style(boss.name)

        header = tk.Frame(self, bg=style["bg"], height=70)
        header.pack(fill="x")
        title = tk.Label(header, text="BOSS CHAMBER", font=("Press Start 2P", 14), bg=style["bg"], fg="#F8F8F2")
        title.pack(pady=12)

        card = tk.Frame(self, bg="#141A2B", bd=0)
        card.place(relx=0.5, y=60, anchor="n", width=360, height=320)

        image_frame = tk.Frame(card, bg="#101420")
        image_frame.place(x=15, y=15, width=140, height=160)
        img = self._create_placeholder(140, 140, style["icon"], style["accent"], boss.name)
        boss_img = ImageTk.PhotoImage(img)
        pic = tk.Label(image_frame, image=boss_img, bg="#101420")
        pic.image = boss_img #type: ignore
        pic.place(relx=0.5, rely=0.5, anchor="center")

        name_label = tk.Label(card, text=boss.name, font=("Press Start 2P", 12), bg="#141A2B", fg="#F8F8F2")
        name_label.place(x=170, y=20)
        subtitle_label = tk.Label(card, text=style["subtitle"], font=("Press Start 2P", 7), bg="#141A2B", fg=style["accent"])
        subtitle_label.place(x=170, y=44)

        hp_bar = tk.Frame(card, bg="#333645", bd=2, relief="ridge")
        hp_bar.place(x=170, y=75, width=170, height=26)
        try:
            hp_val = int(getattr(boss, 'hp', 0) or 0)
        except Exception:
            hp_val = 0
        max_hp = max(hp_val, 100)
        fill_calc = int(160 * (hp_val / max_hp)) if max_hp > 0 else 10
        fill_width = min(160, max(10, fill_calc))
        hp_fill = tk.Frame(hp_bar, bg=style["accent"], width=fill_width, height=18)
        hp_fill.place(x=5, y=4)
        hp_label = tk.Label(card, text=f"HP: {hp_val}", font=("Press Start 2P", 7), bg="#141A2B", fg="#F8F8F2")
        hp_label.place(x=170, y=80)

        self.timer_label = tk.Label(card, text=f"Time Left: {int(challenge_time)// 60}:{int(challenge_time % 60):02d}", font=("Press Start 2P", 8), bg="#141A2B", fg="#FFB86C")
        self.timer_label.place(x=170, y=110)

        drop_frame = tk.Frame(card, bg="#0F1425")
        drop_frame.place(x=15, y=185, width=330, height=100)
        drop_title = tk.Label(drop_frame, text="Drop Chances", font=("Press Start 2P", 8), bg="#0F1425", fg="#F8F8F2")
        drop_title.pack(anchor="nw", padx=10, pady=(8, 0))

        for item, chance in list(boss.drop_table.items())[:4]:
            drop_text = f"{item}: {int(chance * 100)}%"
            tk.Label(drop_frame, text=drop_text, font=("Press Start 2P", 7), bg="#0F1425", fg="#D8DEE9").pack(anchor="w", padx=12, pady=2)

        self.start_button = tk.Button(card, text="BEGIN", font=("Press Start 2P", 10), bg=style["accent"], fg="#0F1425", activebackground="#FFFFFF", activeforeground="#000000", bd=0, command=self.start_challenge)
        self.start_button.place(x=190, y=250, width=140, height=35)

    def _create_placeholder(self, width, height, icon, accent, title):
        img = Image.new("RGB", (width, height), "#101420")
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (width - 1, height - 1)], outline=accent, width=3)
        draw.ellipse([(10, 10), (width - 10, height - 10)], outline=accent, width=3)
        text_x = int(width // 2 - 18)
        text_y = int(height // 2 - 15)
        draw.text((text_x, text_y), str(icon), fill=accent)
        return img

    def start_challenge(self):
        self.start_button.config(state="disabled", text="FIGHTING...")
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        elapsed = time.time() - self.start_time # type: ignore
        remaining = max(0, self.challenge_time - elapsed)
        mins = int(remaining // 60)
        secs = int(remaining % 60)
        self.timer_label.config(text=f"Time Left: {mins}:{secs:02d}")
        if remaining <= 0:
            self.timer_running = False
            self.start_button.config(state="normal", text="VICTORY")
        else:
            self.after(250, self.update_timer)


class BossSuccessPage(tk.Frame):
    def __init__(self, parent, boss=None, drops=None):
        super().__init__(parent, bg="#0A3D62")
        title = tk.Label(self, text="VICTORY", font=("Press Start 2P", 18), bg="#0A3D62", fg="#F7F1E3")
        title.pack(pady=(30, 10))
        if boss:
            name = tk.Label(self, text=boss.name, font=("Press Start 2P", 12), bg="#0A3D62", fg="#A5D6A7")
            name.pack(pady=4)
        if drops:
            drop_label = tk.Label(self, text="Loot Obtained", font=("Press Start 2P", 8), bg="#0A3D62", fg="#F7F1E3")
            drop_label.pack(pady=8)
            for drop in drops[:4]:
                tk.Label(self, text=f"• {drop}", font=("Press Start 2P", 7), bg="#0A3D62", fg="#DFF9FB").pack(anchor="w", padx=40)
        note = tk.Label(self, text="Good job! Return to the home page.", font=("Press Start 2P", 7), bg="#0A3D62", fg="#CAD3C8")
        note.pack(pady=16)


class BossFailurePage(tk.Frame):
    def __init__(self, parent, boss=None):
        super().__init__(parent, bg="#581845")
        title = tk.Label(self, text="DEFEAT", font=("Press Start 2P", 18), bg="#581845", fg="#F9EBEA")
        title.pack(pady=(30, 8))
        if boss:
            name = tk.Label(self, text=boss.name, font=("Press Start 2P", 12), bg="#581845", fg="#F8C291")
            name.pack(pady=4)
        note = tk.Label(self, text="Better luck next time. Keep trying!", font=("Press Start 2P", 7), bg="#581845", fg="#F8EFBA")
        note.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Arecarge - Boss Challenge")
    root.geometry("400x400")

    class DummyBoss:
        def __init__(self):
            self.name = "Xyolem"
            self.hp = 150
            self.drop_table = {"Flame Shard": 0.5, "Burning Essence": 0.3, "Charred Bone": 0.2}

    boss_page = BossPage(root, boss=DummyBoss(), challenge_time=30)
    boss_page.pack(fill="both", expand=True)

    root.mainloop()