from .data.constants import BOSS_UNLOCK_LEVEL, bosses, lookup, all_abilities
from .data import constants
import random
from .io import ConsoleIO
import time

console = ConsoleIO()

def get_boss(boss=None) -> constants.Boss | None:
    if boss:
        boss_info = lookup(boss)
        if boss_info:
            return boss_info if isinstance(boss_info, constants.Boss) else None
        else:
            console.display("Boss not found.")
            pass
    else:
        random_boss = random.choice(bosses)
        boss_info = lookup(random_boss.name)
        return boss_info if isinstance(boss_info, constants.Boss) else None

def get_boss_challenge(boss):
    boss_info = lookup(boss)
    if not isinstance(boss_info, constants.Boss):
        raise ValueError("Expected a Boss object, got something else.")
    if not boss_info:
        console.display("Boss not found.")
        return None
    challenge_time = random.choices(
        list(boss_info.challenges.keys()),
        weights=list(boss_info.challenges.values()),
        k=1
    )[0]
    return challenge_time

def complete_challenge(boss: constants.Boss, challenge_time):
    if not isinstance(boss, constants.Boss):
        raise ValueError("wut. wrong obj")
    items_got = []
    #eg: 20min focus -> 20*60 seconds
    challenge_time = int(challenge_time.split("min")[0]) * 60
    curr_timee = time.time()
    while time.time() - curr_timee < challenge_time * 60:
        time_left = challenge_time * 60 - (time.time() - curr_timee)
        mins = int(time_left // 60)
        secs = int(time_left % 60)
        console.display(f"Time left: {mins}m {secs}s", end="\r", flush=True)
        time.sleep(1)
    console.display("\nChallenge completed! You defeated the boss!")
    for item, chance in boss.drop_table.items():
        if random.random() < chance:
            console.display(f"You received: {item}")
            items_got.append(item)
    return items_got


if __name__ == "__main__":
    boss = get_boss()
    if boss:
        challenge_time = get_boss_challenge(boss)
        if challenge_time:
            rewards = complete_challenge(boss, challenge_time)