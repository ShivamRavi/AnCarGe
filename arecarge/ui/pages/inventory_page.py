import tkinter as tk
from tkinter import font
from PIL import Image, ImageDraw, ImageTk

class InventoryPage(tk.Frame):
    def __init__(self, parent, player=None):
        super().__init__(parent, bg="#0F1425")
        self.player = player

        header = tk.Frame(self, bg="#1F2A44")
        header.pack(fill="x")
        tk.Label(header, text="INVENTORY", font=("Press Start 2P", 14), bg="#1F2A44", fg="#F8F8F2").pack(pady=12)

        board = tk.Frame(self, bg="#141B2D")
        board.place(relx=0.5, rely=0.5, anchor="center", width=360, height=360)
        # ensure cards scale slightly when container is larger
        self.bind("<Configure>", lambda e: self._on_resize(e, board))

    def _on_resize(self, event, board):
        w = max(300, int(event.width * 0.85))
        h = max(320, int(event.height * 0.75))
        board.place_configure(width=w, height=h)

        stats_card = self._card(board, "PLAYER STATS", "#2F3B58", 20, 20, 160, 320)
        self._populate_stats(stats_card)

        right_card = self._card(board, "EQUIPMENT", "#27354E", 200, 20, 150, 320)
        self._populate_right(right_card)

    def _card(self, parent, title, bg, x, y, width, height):
        card = tk.Frame(parent, bg=bg, bd=0)
        card.place(x=x, y=y, width=width, height=height)
        tk.Label(card, text=title, font=("Press Start 2P", 8), bg=bg, fg="#F8F8F2").pack(pady=8)
        return card

    def _populate_stats(self, frame):
        if not self.player:
            return
        text_style = ("Press Start 2P", 8)
        values = [
            ("HP", self.player.hp, "#E53E3E"),
            ("LVL", self.player.level, "#F6AD55"),
            ("XP", self.player.xp, "#63B3ED"),
            ("COINS", self.player.coins, "#F6E05E"),
            ("CHESTS", self.player.chests, "#9F7AEA"),
            ("TYPE", self.player.type or "NONE", "#A0AEC0"),
        ]
        for label, value, color in values:
            row = tk.Frame(frame, bg=frame["bg"])
            row.pack(fill="x", padx=12, pady=3)
            tk.Label(row, text=f"{label}", font=text_style, bg=frame["bg"], fg="#CBD5E0").pack(side="left")
            tk.Label(row, text=str(value), font=text_style, bg=frame["bg"], fg=color).pack(side="right")

        bar_frame = tk.Frame(frame, bg=frame["bg"])
        bar_frame.pack(fill="x", padx=12, pady=10)
        self._progress_bar(bar_frame, self.player.hp, 120, "#E53E3E")
        tk.Label(bar_frame, text="HP", font=("Press Start 2P", 6), bg=frame["bg"], fg="#E2E8F0").pack(anchor="w")

    def _populate_right(self, frame):
        if not self.player:
            return
        section_height = 96
        self._item_section(frame, "Stash", self.player.stash, 0, section_height)
        self._item_section(frame, "Backpack", self.player.backpack, section_height + 5, section_height)
        self._item_section(frame, "Abilities", [f"{a} [Lv {self.player.ability_levels.get(a,1)}]" for a in self.player.abilities], 2 * (section_height + 5), section_height)

    def _item_section(self, frame, title, items, y, height):
        section = tk.Frame(frame, bg="#1C2538")
        section.place(x=10, y=y + 30, width=130, height=height)
        tk.Label(section, text=title, font=("Press Start 2P", 7), bg="#1C2538", fg="#F8F8F2").pack(pady=5)
        if items:
            for item in items[:4]:
                tk.Label(section, text=str(item), font=("Press Start 2P", 6), bg="#1C2538", fg="#A0AEC0", wraplength=110, justify="left").pack(anchor="w", padx=8, pady=1)
            if len(items) > 4:
                tk.Label(section, text=f"+{len(items)-4} more", font=("Press Start 2P", 6), bg="#1C2538", fg="#718096").pack(anchor="w", padx=8, pady=2)
        else:
            tk.Label(section, text="empty", font=("Press Start 2P", 6), bg="#1C2538", fg="#718096").pack(pady=20)

    def _progress_bar(self, parent, value, width, color):
        bar = tk.Canvas(parent, width=width, height=10, bg="#2D3748", highlightthickness=0)
        bar.pack()
        fill = min(max(value, 0), width)
        bar.create_rectangle(0, 0, fill, 10, fill=color, width=0)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Arecarge - Inventory")
    root.geometry("400x520")
    
    class DummyPlayer:
        def __init__(self):
            self.hp = 80
            self.level = 6
            self.xp = 1325
            self.coins = 345
            self.chests = 2
            self.type = "Lust"
            self.stash = ["Potion of Healing", "Fire Gem", "Mystic Scroll", "Bag of Coins", "Lucky Clover"]
            self.backpack = ["Iron Sword", "Shield of Light", "Herb Pouch"]
            self.abilities = ["Heal", "Shield", "Greed"]
            self.ability_levels = {"Heal": 3, "Shield": 2, "Greed": 1}
    
    page = InventoryPage(root, DummyPlayer())
    page.pack(fill="both", expand=True)
    root.mainloop()