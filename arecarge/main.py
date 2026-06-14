# main.py
# making dis pythonic
import os
import random
import threading
import time
import tkinter as tk
import queue

from arecarge.shared import sq
from arecarge.player import Player
from arecarge.io import IO, ConsoleIO
from arecarge.abilities import ABILITY_HANDLERS
from arecarge.bosses import BOSS_UNLOCK_LEVEL
from arecarge.data.constants import all_abilities
from arecarge.ui.switcher import Switcher
from arecarge.ui.pages import gui_home, home_main, done_page as dope, boss_page, inventory_page, distracted_page as disp, ability_page, upgrade_page

io = ConsoleIO()
rng = random.Random()
stdin_queue = queue.Queue()

def get_input(prompt="", timeout=None):
    print(prompt, end="", flush=True)
    try:
        val = stdin_queue.get(timeout=timeout)
        if val is None:
            return ""
        return val
    except queue.Empty:
        return ""

def start_input_thread():
    def read_input():
        while True:
            try:
                line = input()
                stdin_queue.put(line)
            except EOFError:
                stdin_queue.put(None)
                break
    t = threading.Thread(target=read_input, daemon=True)
    t.start()


def set_attr(player, attr, prompt, cast=int):
    """Helper to set player attributes with user input."""
    value = cast(get_input(prompt))
    setattr(player, attr, value)
    print(f"{attr.capitalize()} set to {value}")

def add_item(player):
    """I mean, testiii neeeds items"""
    items = [
        "Potion of Healing", "Potion of Vitality", "Potion of Luck",
        "Potion of Shielding", "Crystal of Revisal", "Aegis",
        "Clove of Fortune", "BloodHeart", "XyolemHeart",
        "EmberHeart", "Bag of Coins"
    ]
    print("Items you can add:", ", ".join(items))
    item_to_add = get_input("Enter item to add to stash: ")
    player.stash.append(item_to_add)

def spawn_boss(player):
    """duh. boss. spawn. battle."""
    if player.level < BOSS_UNLOCK_LEVEL:
        print("hacker")
        return
    print("Spawning a boss battle...")
    player.boss_battle()

def add_ability(player):
    """Add an ability to the player. read da name of the function. it adds an ability."""
    print("Available abilities:", ", ".join(all_abilities))
    ability_to_add = get_input("Enter ability to add: ")
    if ability_to_add in all_abilities and ability_to_add not in player.abilities:
        player.abilities.append(ability_to_add)
        player.ability_levels[ability_to_add] = 1
        print(f"Added ability: {ability_to_add}")
    else:
        print("Invalid or duplicate ability.")

def use_ability(player):
    """are u jobbless.  use ability..."""
    print("Available abilities:")
    for ability in player.abilities:
        level = player.ability_levels.get(ability, 1)
        print(f"{ability} (Level {level})")
    ability = get_input("Enter ability: ").lower()
    if player.cooldown > 0:
        print(f"{ability} is on cooldown for {player.cooldown} more turns. (global cooldown)")
        return
    player.use_ability(ability, io, rng)


def use_ask(player):
    """use item from stash or backpack. ask which one. LIKE IT SAYS USE ASKK"""
    choice = get_input("Use from stash or backpack? (stash/backpack/ability): ").strip().lower()
    if choice == "stash":
        player.use_item()
    elif choice == "backpack":
        player.use_backpack()
    elif choice == "ability":
        use_ability(player)
    else:
        print("Invalid choice.")

COMMANDS = {
    "add item": add_item,
    "spawn boss": spawn_boss,
    "upgrade ability": lambda p: p.upgrade_ability(),
    "redeem reward": lambda p: p.redeem_reward(),
    "reset cooldown": lambda p: setattr(p, "cooldown", 0),
    "get reward": lambda p: print(f"Random reward: {p.get_random_reward()}"),
    "print stats": lambda p: p.print_stats(),
    "task": lambda p: p.task_completed(),
    "add ability": add_ability,
    "set coins": lambda p: set_attr(p, "coins", "Enter coins: "),
    "add xp": lambda p: set_attr(p, "xp", "Enter XP: "),
    "level up": lambda p: (p.task_completed(), p.level_up()),
    "ability": use_ability,
    "open": lambda p: p.open_chest(),
    "list stash": lambda p: p.list_stash(),
    "list backpack": lambda p: p.list_backpack(),
    "use stash": lambda p: p.use_item(),
    "use backpack": lambda p: p.use_backpack(),
    "use ability": lambda p: p.use_ability(),
    "distraction": lambda p: p.distraction(),
    "set level": lambda p: set_attr(p, "level", "Enter level: "),
    "set hp": lambda p: set_attr(p, "hp", "Enter HP: "),
    "set xp": lambda p: set_attr(p, "xp", "Enter XP: "),
    "set chests": lambda p: set_attr(p, "chests", "Enter chests: "),
}

PLAYER_COMMANDS = {
    "upgrade": lambda p: sq.put("upgrade"),
    "redeem": lambda p: p.redeem_reward(),
    "done": lambda p: p.task_completed(),
    "distraction": lambda p: p.distraction(),
    "ability": use_ability,
    "use": lambda p: sq.put("inventory"),
    "open": lambda p: p.open_chest(),
    "stats": lambda p: p.print_stats(),
    "save": lambda p: p.save_progress(),
    "inventory": lambda p: sq.put("inventory"),
    "use stash": lambda p: sq.put("inventory"),
    "use backpack": lambda p: sq.put("inventory"),
    "home": lambda p: sq.put("home"),
}


def phonk(phonkname ="ay mi gattito"):
    "pabre mi gattito maja mojo mojo mito"
    print(f"Playing phonk track: {phonkname}")
    print("Phonk vibes intensify...")
    print("Phonk track ended.")

def cli_input_loop():
    global current_player

    # Print prompt and wait for either "start" from GUI or name input
    print("Enter your name (or press START button): ", end="", flush=True)

    player_name = None
    start_time = time.time()
    timeout = 120  # 2 minute timeout

    while not player_name and (time.time() - start_time) < timeout:
        # Check for GUI START button
        try:
            msg = sq.get_nowait()
            if msg == "start":
                player_name = "Player"
                print("\nGame started!")
                break
        except queue.Empty:
            pass

        # Check for name input
        try:
            name = stdin_queue.get_nowait()
            if name:
                player_name = name
        except queue.Empty:
            pass

        time.sleep(0.05)

    if not player_name:
        player_name = "Player"

    player = Player(player_name)
    current_player = player

    tester_mode = player_name.strip() == "Tester"
    if tester_mode:
        print("Tester mode onini bananini!")

    if os.path.exists(f"{player_name}_progress.json"):
        resp = get_input("Save file found. Load it? (yes/no): ")
        if resp.lower() in ("yes", "y", "yea", "yuppi duppi", "oki") and not tester_mode:
            player.load_progress()

    while True:
        player.print_stats()
        if player.needs_type_choice:
            choice = get_input("Choose your type: Lust (DOUBLER) or Dismissal (BLOCKER): ")
            player.choose_type(choice)

        command = get_input("Enter command (or 'help'/'exit'/'use'): ").strip().lower()

        if command == "exit" or command == "quit":
            player.save_progress()
            print("Goodbye!")
            break
        elif command == "help":
            print("Available commands:", ", ".join(COMMANDS.keys())) if tester_mode else print("Available commands:", ", ".join(PLAYER_COMMANDS.keys()))
        elif command in PLAYER_COMMANDS and not tester_mode:
            PLAYER_COMMANDS[command](player)
        elif command in COMMANDS and tester_mode:
            COMMANDS[command](player)
        elif command == "done":
            player.task_completed()
            player.level_up()
            if random.random() >= 0.8 and player.level >= 3:
                player.boss_battle()
        else:
            print("Unknown command.")
        if player.needs_type_choice:
            choice = get_input("Choose your type: Lust (DOUBLER) or Dismissal (BLOCKER): ")
            player.choose_type(choice)

def main():
    global current_player
    current_player = None
    
    root = tk.Tk()
    root.configure(bg="#FFF6F7")
    root.title("Main UI Window")
    root.geometry("350x400")
    root.attributes("-topmost", True)
    switcher = Switcher(root)
    switcher.pack(fill="both", expand=True)
    switcher.show_page(home_main.HomePage)

    def poll_queue():
        try:
            while True:
                msg = sq.get_nowait()
                if not isinstance(switcher.current_page, (gui_home.HomePage, boss_page.BossPage, inventory_page.InventoryPage)):
                    root.geometry("400x300")
                if msg == "task_completed":
                    switcher.show_page(dope.DonePage)
                    root.after(2000, lambda: switcher.show_page(gui_home.HomePage))
                elif msg == "distraction":
                    switcher.show_page(disp.DistractedPage)
                    root.after(2000, lambda: switcher.show_page(gui_home.HomePage))
                elif msg == "start":
                    # brief celebratory/home splash, then return to main home
                    switcher.show_page(gui_home.HomePage)
                    root.after(1500, lambda: switcher.show_page(home_main.HomePage))
                elif msg == "inventory" or (isinstance(msg, dict) and msg.get("type") == "inventory"):
                    root.geometry("{}x{}".format(root.winfo_width(), max(root.winfo_height(), 520)))
                    switcher.show_page(inventory_page.InventoryPage, player=current_player)
                elif msg == "upgrade":
                    root.geometry("350x400")
                    switcher.show_page(upgrade_page.UpgradePage, player=current_player)
                elif isinstance(msg, dict) and msg.get("type") == "boss":
                    root.geometry("{}x{}".format(root.winfo_width(), max(root.winfo_height(), 400)))
                    switcher.show_page(boss_page.BossPage, boss=msg.get("boss"), challenge_time=msg.get("time", 5))
                elif isinstance(msg, dict) and msg.get("type") == "boss_success":
                    switcher.show_page(boss_page.BossSuccessPage, boss=msg.get("boss"), drops=msg.get("drops"))
                    root.after(3000, lambda: switcher.show_page(gui_home.HomePage))
                elif isinstance(msg, dict) and msg.get("type") == "boss_failure":
                    switcher.show_page(boss_page.BossFailurePage, boss=msg.get("boss"))
                    root.after(3000, lambda: switcher.show_page(gui_home.HomePage))
        except queue.Empty:
            pass
        root.after(200, poll_queue)

    start_input_thread()
    threading.Thread(target=cli_input_loop, daemon=True).start()
    poll_queue()
    root.mainloop()

if __name__ == "__main__":
    main()
