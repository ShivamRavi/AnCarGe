import tkinter as tk
from tkinter import font

class AbilityPage(tk.Frame):
    def __init__(self, parent, ability_name="Focus Burst"):
        super().__init__(parent, bg="#FFF6F7")
        self.ability_name = ability_name
        self.canvas = tk.Canvas(self, bg="#FFF6F7", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.animation_step = 0
        self._draw_ui()
        self.after(60, self._animate)

    def _draw_ui(self):
        self.canvas.delete("all")
        width = self.winfo_width() or 400
        height = self.winfo_height() or 400
        cx = width // 2
        cy = height // 2
        radius = 80
        glow = (self.animation_step % 40) / 40.0

        for ring_index in range(3):
            ring_radius = radius + ring_index * 28 + glow * 8
            color = "#F4C2C2" if ring_index == 0 else "#E4A8A8" if ring_index == 1 else "#D48888"
            self.canvas.create_oval(
                cx - ring_radius,
                cy - ring_radius,
                cx + ring_radius,
                cy + ring_radius,
                outline=color,
                width=4,
            )

        self.canvas.create_text(cx, cy - 8, text="⚡", font=("Arial", 40), fill="#C1121F")
        self.canvas.create_text(cx, cy + 40, text=self.ability_name, font=("Press Start 2P", 10), fill="#14213D")
        self.canvas.create_text(cx, cy + 70, text="Ability ready. Use to supercharge your next move.", font=("Arial", 8), fill="#4A4A4A")

    def _animate(self):
        self.animation_step = (self.animation_step + 1) % 120
        self._draw_ui()
        self.after(80, self._animate)
