from .data.constants import all_abilities

def healHandler(player,io, rng, **ctx):
    lvl = player.ability_levels.get("Heal", 1)
    if lvl == 1:
        player.hp += 15
        io.display("You used Heal! +15 HP")
        player.cooldown = 1
    elif lvl == 2:
        player.hp += 50
        io.display("You used Medic! +50 HP")
        player.cooldown = 2
    else:
        player.hp += 70
        gained = rng.randint(1, 2)
        player.chests += gained
        io.display(f"You used Bloodsteal! +70 HP and gained {gained} chests!")
        player.cooldown = 3

    return


def greedHandler(player, io, rng, **ctx):
    lvl = player.ability_levels.get("Greed", 1)
    if lvl == 1:
        if rng.random() < 0.5:
            player.chests += 1
            io.display("Double or Nothing succeeded! +1 Chest")
        else:
            player.chests = max(0, player.chests - 1)
            io.display("Double or Nothing failed! -1 Chest")
    else:
        if rng.random() < 0.6:
            player.chests += 2
            io.display("Bloodlust succeeded! +2 Chests")
        else:
            player.chests += 1
            io.display("Bloodlust gave 1 chest")
    player.cooldown = 2
    return


def bloodlustHandler(player, io, rng, **ctx):
    if rng.random() < 0.6:
        gained = rng.randint(1, 3)
        player.chests += gained
        coins = rng.randint(5, 30)
        player.coins += coins
        io.display(f"Bloodlust surges! +{gained} chests and +{coins} coins")
    else:
        player.chests = max(0, player.chests - 1)
        io.display("Bloodlust backfired! -1 chest")
    player.cooldown = 3
    return


def greed_v3Handler(player, io, rng, **ctx):
    sacrifice_type = rng.random()
    if sacrifice_type > 0.5:
        sacrifice = rng.randint(30, 50)
    else:
        sacrifice = "random item from stash"
    confirm = io.prompt(f"Awaken the Blood Maw? Sacrifice {sacrifice} for massive gain (yes/no): ").lower()
    if confirm not in ("yes", "y"):
        io.display("You resisted the Maw.")
        return
    if sacrifice == "random item from stash":
        if player.stash:
            sacrificed_item = rng.choice(player.stash)
            player.stash.remove(sacrificed_item)
            io.display(f"You sacrificed {sacrificed_item} from your stash to awaken the Blood Maw!")
        else:
            io.display("No items in stash to sacrifice!")
            return
    elif isinstance(sacrifice, int) and sacrifice > player.hp - 1:
        io.display("Sacrifice would be lethal! You resist to avoid death...")
        return
    elif isinstance(sacrifice, int):
        player.hp -= sacrifice
        io.display(f"You sacrificed {sacrifice} HP to awaken the Blood Maw!")
    immediate_chests = rng.randint(1, 5)
    immediate_coins = rng.randint(100, 400)
    player.chests += immediate_chests
    player.coins += immediate_coins
    player.greed_maw_turns = 2
    player.cooldown = 5
    io.display(
    f"The Blood Maw awakens! "
    f"Sacrifice: {sacrifice if isinstance(sacrifice, int) else str(sacrifice)} | "
    f"Reward: +{immediate_chests} chests, +{immediate_coins} coins | "
    f"Duration: devours for {player.greed_maw_turns} tasks."
)

    return


def blockahHandler(player, io, rng, **ctx):
    if player.cooldown > 0:
        io.display("Blockah' is on cooldown.")
        return
    player.block = True
    player.block_count = max(getattr(player, 'block_count', 0), 1)
    player.cooldown = 2
    io.display("You used Blockah' - will block the next distraction.")
    return


def shieldOfLightHandler(player, io, rng, **ctx):
    if player.cooldown > 0:
        io.display("Shield of Light is on cooldown.")
        return
    player.block = True
    player.block_count = max(getattr(player, 'block_count', 0), 2)
    player.hp += 40
    player.coins += rng.randint(1, 6)
    player.cooldown = 3
    io.display("Shield of Light activated! Block next 2 distractions and +40 HP")
    return


def instinctHandler(player, io, rng, **ctx):
    if player.cooldown > 0:
        io.display("Instinct is on cooldown.")
        return
    player.block = True
    player.block_count = max(getattr(player, 'block_count', 0), 3)
    player.instinct_reflect_turns = 3
    player.hp = min(200, player.hp + 50)
    bonus = rng.randint(1, 3)
    player.chests += bonus
    player.cooldown = 5
    io.display(f"Instinct awakened! For the next 3 blocks distractions will be reflected: +50 HP and +{bonus} chests immediately.")
    return


def emberSurgeHandler(player, io, rng, **ctx):
    if player.cooldown > 0:
        io.display("Ember Surge is on cooldown.")
        return
    player.ember_aura_turns = 2
    coins_to_burn = min(player.coins, 100)
    if coins_to_burn >= 10:
        burn_choice = io.prompt(f"Ember Surge can convert up to 100 coins into chests at a rate of 10 coins per chest. Burn {coins_to_burn} coins for {coins_to_burn // 10} chests? (yes/no): ").lower()
        if burn_choice in ("yes", "y"):
            converted = coins_to_burn // 10
            player.coins -= coins_to_burn
            player.chests += converted
            io.display(f"Ember Surge consumed {coins_to_burn} coins to create {converted} extra chests.")
    player.block = True
    player.block_count = max(getattr(player, 'block_count', 0), 2)
    player.cooldown = 6
    player.hp += 50
    io.display("Ember Surge erupted! +50 HP, ember aura for 2 blocked distractions, and consumed coins -> chests if available.")
    try:
        player.abilities.remove("Ember Surge")
    except Exception:
        pass
    return


def darkRainbowHandler(player, io, rng, **ctx):
    if player.cooldown > 0:
        io.display("Dark Rainbow is on cooldown.")
        return
    outcome = rng.random()
    if outcome < 0.5:
        chests = rng.randint(1, 3)
        coins = rng.randint(20, 50)
        xp = rng.randint(5, 20)
        player.chests += chests
        player.coins += coins
        player.xp += xp
        io.display(f"Dark Rainbow granted {chests} chests, {coins} coins, and {xp} XP!")
    else:
        loss_hp = rng.randint(10, 25)
        loss_coins = rng.randint(5, 15)
        player.hp -= loss_hp
        player.coins = max(0, player.coins - loss_coins)
        io.display(f"The Dark Rainbow backfired! Lost {loss_hp} HP and {loss_coins} coins.")
    player.cooldown = 4
    return


def fertilityHandler(player, io, rng, **ctx):
    if player.cooldown > 0:
        io.display("Fertility is on cooldown.")
        return
    player.xp_boost_turns = 3
    player.cooldown = 5
    io.display("Fertility activated! Tasks grant extra XP for the next 3 completions.")
    return

def blueFlameHandler(player, io, rng, **ctx):
    if player.cooldown > 0:
        io.display(f"Blue Flame is on cooldown! {player.cooldown} turns remaining.")
        return

    # Exclude abilities Blue Flame should not copy
    excluded = {"Blue Flame", "Ember Surge", "Dark Rainbow", "Fertility", "Heal", "Medic", "Blockah'", "Shield of Light", "Greed", "Bloodsteal"}
    possible = [a for a in all_abilities if a not in excluded]

    if not possible:
        io.display("Nothing for Blue Flame to copy right now.")
        return

    ability_to_copy = rng.choice(possible).lower()

    
    handler = ABILITY_HANDLERS.get(ability_to_copy)
    if callable(handler):
        io.display(f"Blue Flame echoes {ability_to_copy}!")
        handler(player, io, rng) 
    else:
        io.display("Blue Flame flickers, but fails to copy anything...")

    
    if "Blue Flame" in player.abilities:
        player.abilities.remove("Blue Flame")
    player.cooldown = 3




ABILITY_HANDLERS = {
    "heal": healHandler,
    "medic": healHandler,
    "bloodsteal": healHandler,
    "greed": greedHandler,
    "bloodlust": bloodlustHandler,
    "blood maw": greed_v3Handler,
    "blockah'": blockahHandler,
    "shield of light": shieldOfLightHandler,
    "instinct": instinctHandler,
    "ember surge": emberSurgeHandler,
    "dark rainbow": darkRainbowHandler,
    "fertility": fertilityHandler,
    "blue flame": blueFlameHandler,
}