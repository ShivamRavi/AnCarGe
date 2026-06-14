import tkinter as tk
from PIL import Image, ImageTk
from arecarge.shared import sq
from arecarge.data.constants import upgrades

class UpgradePage(tk.Frame):
    def __init__(self, parent, player=None):
        super().__init__(parent, bg="#FFF6F7")

        header = tk.Frame(self, bg="#FFF6F7")
        header.pack(fill="x", pady=6)
        tk.Label(header, text="UPGRADES", font=("Press Start 2P", 18), bg="#FFF6F7", fg="#000000").pack()

        body = tk.Frame(self, bg="#FFF6F7")
        body.pack(fill="both", expand=True, padx=12, pady=6)

        if not upgrades:
            tk.Label(body, text="No upgrades available.", bg="#FFF6F7").pack()
            return

        for up in upgrades:
            frame = tk.Frame(body, bg="#F7F7F7", bd=1, relief="ridge")
            frame.pack(fill="x", pady=6)
            tk.Label(frame, text=up.name, font=("Press Start 2P", 10), bg="#F7F7F7").pack(side="left", padx=8)
            tk.Label(frame, text=f"Cost: {up.coins_required}", font=("Press Start 2P", 8), bg="#F7F7F7").pack(side="left", padx=8)

            req_text = ", ".join(up.required_items) if up.required_items else "None"
            tk.Label(frame, text=f"Requires: {req_text}", font=("Press Start 2P", 8), bg="#F7F7F7").pack(side="left", padx=8)

            btn_state = "normal"
            missing = []
            if player is None:
                btn_state = "disabled"
                missing = up.required_items
            else:
                if up.name in player.abilities:
                    btn_state = "disabled"
                elif up.prev not in player.abilities:
                    btn_state = "disabled"
                    missing = [up.prev]
                else:
                    for item in up.required_items:
                        if item not in player.stash:
                            missing.append(item)
                    if player.coins < up.coins_required:
                        missing.append("coins")
                    if missing:
                        btn_state = "disabled"

            status_lbl = tk.Label(frame, text=("Locked" if btn_state=="disabled" else "Ready"), font=("Press Start 2P", 8), bg="#F7F7F7")
            status_lbl.pack(side="right", padx=8)

            def make_upgrade(u=up, st=status_lbl, fr=frame, pl=player):
                if pl is None:
                    return
                for itm in u.required_items:
                    if itm in pl.stash:
                        pl.stash.remove(itm)
                pl.coins -= u.coins_required
                pl.abilities.append(u.name)
                pl.ability_levels[u.name] = 1
                if u.prev in pl.abilities:
                    try:
                        pl.abilities.remove(u.prev)
                    except Exception:
                        pass
                st.config(text="Upgraded")
                btn.config(state="disabled")

            btn = tk.Button(frame, text="Upgrade", command=lambda u=up: make_upgrade(u), bg="#000000", fg="#FFFFFF", state=btn_state)
            btn.pack(side="right", padx=8, pady=6)
