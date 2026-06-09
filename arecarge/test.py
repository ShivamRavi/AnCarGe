import curses
import time

class Player:
    def __init__(self):
        self.hp = 100
        self.xp = 50
        self.level = 3
        self.cooldown = 0
        self.cooldown_max = 3
        self.abilities = {
            "h": "Heal",
            "b": "Blood Maw",
            "f": "Blue Flame"
        }

def draw_ui(stdscr, player, event_log):
    stdscr.clear()

    # Title
    stdscr.addstr(0, 2, "=== Game Dashboard ===", curses.A_BOLD)

    # Player stats
    stats = [
        f"HP: {player.hp}",
        f"XP: {player.xp}",
        f"Level: {player.level}",
        f"Cooldown: {player.cooldown} turns"
    ]
    for i, line in enumerate(stats, start=2):
        stdscr.addstr(i, 2, line)

    # Abilities
    stdscr.addstr(7, 2, "Abilities (press key):", curses.A_UNDERLINE)
    for idx, (key, ability) in enumerate(player.abilities.items(), start=8):
        status = "Locked" if player.cooldown > 0 else "Ready"
        color = curses.color_pair(1) if status == "Ready" else curses.color_pair(2)
        stdscr.addstr(idx, 4, f"[{key}] {ability} - {status}", color)

    # Event log
    stdscr.addstr(14, 2, "Event Log:", curses.A_UNDERLINE)
    for i, event in enumerate(event_log[-5:], start=15):
        stdscr.addstr(i, 4, event)

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Ready
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Locked

    player = Player()
    event_log = []

    while True:
        draw_ui(stdscr, player, event_log)

        # Wait for input
        key = stdscr.getch()

        if key == ord("q"):  # quit
            break

        # Ability usage
        if chr(key) in player.abilities:
            ability = player.abilities[chr(key)]
            if player.cooldown == 0:
                event_log.append(f"Used {ability}!")
                player.cooldown = player.cooldown_max
                if ability == "Heal":
                    player.hp += 10
                elif ability == "Blood Maw":
                    event_log.append("Blood Maw dealt 30 damage!")
                elif ability == "Blue Flame":
                    event_log.append("Blue Flame echoes Bloodlust!")
            else:
                event_log.append(f"{ability} is on cooldown!")

        # Tick cooldown down each loop
        if player.cooldown > 0:
            player.cooldown -= 1

        time.sleep(1)

curses.wrapper(main)
