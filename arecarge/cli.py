import random
import os
import json
import time

BOSS_UNLOCK_LEVEL = 5
rarities = ["Common", "Uncommon", "Rare", "Legendary", "Mythical"]
rewards = {
    "Common": ["DTOX 5 min", "Check memes 2 min"],
    "Uncommon": ["Rblox 5min", "DTOX 10 min", "Anything 7mins"],
    "Rare": ["Watch 10 min anime clip", "Play 15 min game", "YT 10 min (/no shorts)"],
    "Legendary": ["40min DTOX", "20min GD"],
    "Mythical": ["1hr BREAK", "45min GAME"]
}


bosses =  {
    "Pheonix of Procrastination": {"hp": 350,
                                   "drop_table": {"Potion of Healing": 1, "Pheonix Feather": 1, "Potion of Vitality": 0.6, "XyolemHeart": 0.09, "Bag of Coins": 0, "Potion of Luck": 0, "Clove of Fortune": 0, "BloodHeart": 0, "Potion of Shielding": 0, "Crystal of Revisal": 0, "Aegis": 0, "EmberHeart": 0},
                                   "challenges": {"20min Focus": 0.6, "30min Focus": 0.3, "45min Focus": 0.2}
                                   },
    "Bloodlust of Vampiric Deformity" : {"hp": 500,
                                   "drop_table": {"Potion of Healing": 0, "Pheonix Feather": 0, "Potion of Vitality": 0, "XyolemHeart": 0, "Bag of Coins": 1, "Potion of Luck": 0.6, "Clove of Fortune": 0.4, "BloodHeart": 0.06, "Potion of Shielding": 0, "Crystal of Revisal": 0, "Aegis": 0, "EmberHeart": 0},
                                   "challenges": {"25min Focus": 0.4, "45min Focus": 0.3, "60min Focus": 0.2}
                        },
    "Knight and Mage of Unmovable Will" : {"hp": 500,
                                   "drop_table": {"Potion of Healing": 0, "Pheonix Feather": 0, "Potion of Vitality": 0, "XyolemHeart": 0, "Bag of Coins": 0, "Potion of Luck": 0, "Clove of Fortune": 0, "BloodHeart": 0, "Potion of Shielding": 1, "Crystal of Revisal": 0.6, "Aegis": 0.35, "EmberHeart": 0.07},
                                   "challenges": {"25min Focus": 0.4, "45min Focus": 0.3, "60min Focus": 0.2}
    }

}
items_needed_for_upgrade = {
     "Heal": ["Potion of Healing", "Pheonix Feather" ],
     "Medic": ["Potion of Vitality", "XyolemHeart"] ,
     "Greed": ["Bag of Coins", "Potion of Luck"],
     "Bloodlust": ["Clove of Fortune", "BloodHeart"],
     "Blockah'": ["Potion of Shielding", "Crystal of Revisal"],
     "Shield of Light": ["Aegis", "EmberHeart"]
}

coins_for_upgrade = {
    "Heal": 20, 
    "Medic": 80,
    "Greed": 50,
    "Bloodlust": 100,
    "Blockah'": 50,
    "Shield of Light": 100,
    "Greed v3": 130
}

all_abilities = ["Heal", "Medic", "Bloodsteal", "Greed", "Bloodlust", "Greed v3", "Blockah'", "Shield of Light", "Instinct", "Ember Surge", "Dark Rainbow", "Fertility"]

class Player:
    def __init__(self, name):
        self.name = name
        self.rewards_earned = []
        self.hp = 100
        self.xp = 0
        self.level = 1
        self.stash = []
        self.backpack = []
        self.chests = 0
        self.abilities = ["Heal"]
        self.ability_levels = {a: 1 for a in self.abilities}
        self.type = None
        self.block = False
        self.block_count = 0
        self.cooldown = 0
        self.coins = 0
        self.greed_maw_turns = 0
        self.instinct_reflect_turns = 0
        self.ember_aura_turns = 0
        self.xp_boost_turns = 0
        self.needs_type_choice = False

    def reset_cooldown(self):
        """Clear the current ability cooldown.
        This helper keeps item effects consistent when they reset cooldown.
        """
        self.cooldown = 0
    def get_random_reward(self):
        rarity = random.choices(rarities, weights=[37, 32, 14, 9, 4], k=1)[0]
        reward = random.choice(rewards[rarity])
        return f"{reward} ({rarity})"
    
    def boss_battle(self, boss=None):
        if self.level < BOSS_UNLOCK_LEVEL:
            print(f"Boss battles are unlocked at Level {BOSS_UNLOCK_LEVEL}!")
            print("how dare thee hack ur own script...................")
            return
        if boss is None:
            boss = random.choice(list(bosses.keys()))
        print(f"You have encountered the {boss}!")
        boss_info = bosses[boss]
        print(f"Boss HP: {boss_info['hp']}")
        print("Boss Drop Table:")
        for item, chance in boss_info["drop_table"].items():
            if chance > 0:
                print(f"  {item}: {chance * 100}% chance")
        challenge = random.choices(list(boss_info["challenges"].keys()), weights=list(boss_info["challenges"].values()), k=1)[0]
        print(f"Boss Challenge: {challenge}")
        try:
            challenge_time = int(challenge.split("min")[0])
        except Exception:
            challenge_time = 0
        if commands_unlocked == True:
            challenge_time = 0.01
        print(f"You must focus for {challenge_time} minutes to defeat the boss!")
        input("Press Enter to start the challenge...")
        curr_timee = time.time()
        while time.time() - curr_timee < challenge_time * 60:
            time_left = challenge_time * 60 - (time.time() - curr_timee)
            mins = int(time_left // 60)
            secs = int(time_left % 60)
            print(f"Time left: {mins}m {secs}s", end="\r", flush=True)
            time.sleep(1)
        print("\nChallenge completed! You defeated the boss!")
        for item, chance in boss_info["drop_table"].items():
            if random.random() < chance:
                self.stash.append(item)
                print(f"You received: {item}")
                self.cooldown = 0
                if item == "EmberHeart":
                    self.abilities.append("Ember Surge")
                    self.ability_levels["Ember Surge"] = 1
                    print("The dragon in you Rages. dun dun dunnnnn")
                elif item == "BloodHeart":
                    self.abilities.append("Dark Rainbow")
                    self.ability_levels["Dark Rainbow"] = 1
                    print("Not every rainbow has a unicorn")
                elif item == "XyolemHeart":
                    self.abilities.append("Fertility")
                    self.ability_levels["Fertility"] = 1
                    print("The XyolemHear pulses with green aura")


    def use_item(self):
        if not self.stash:
            print("Your stash is empty! No items to use.")
            return
        print("Your stash items:")
        for idx, item in enumerate(self.stash, 1):
            print(f"{idx}. {item}")
        choice = int(input("Enter the number of the item you want to use: "))
        if 1 <= choice <= len(self.stash):
            used_item = self.stash.pop(choice - 1)
            print(f"You used: {used_item}")
            if used_item == "Potion of Healing":
                self.hp += 40
                print("You healed for 40 HP!")
            elif used_item == "Potion of Vitality":
                self.hp += 90
                print("You healed for 90 HP!")    
                self.reset_cooldown()
                print("Your abilities are no longer on cooldown!")
            elif used_item == "Potion of Luck":
                clf_choice = random.random()
                if clf_choice > 0.5:
                   self.chests+= 2
                   print("Potion of Luck was lucky! +2 Chests")
                else:
                    print("Potion of Luck was lucky! 1 chest gain :)")
                    self.chests+=1
            elif used_item == "Potion of Shielding":
                self.block = True
                self.block_count = max(self.block_count, 1)
                print("You are now blocking the next distraction!")
            elif used_item == "Crystal of Revisal":
                self.block = True
                self.hp += 30
                print("You are now blocking the next distraction and healed for 30 HP!")
            elif used_item == "Aegis":
                self.block = True
                self.hp += 22
                self.chests += 1
                self.reset_cooldown()
                print("You are now blocking the next distraction, healed for 22 HP, gained 1 chest, and your abilities are no longer on cooldown!")
                self.abilities.append("Blue Flame")
                self.ability_levels["Blue Flame"] = 1
            elif used_item == "Clove of Fortune":
                clf_choice = random.random()
                if clf_choice > 0.4:
                   self.chests+= 2
                   if clf_choice >= 0.7:
                       self.chests += 1
                       print("Clove of Fortune was lucky! +3 Chests")
                       if clf_choice >= 0.8:
                           self.chests += 2
                           print("LUCKYYYYY!!!!! FAIYOH!!! +5 Chests")
                           if clf_choice >= 0.9:
                               self.chests += 2
                               print("Clove of Fortune was extremely lucky! +7 Chests")
                else:
                    self.chests+=1
            elif used_item == "BloodHeart" or used_item == "XyolemHeart" or used_item == "EmberHeart":
                print("too op for u to use :)")
                self.stash.append(used_item)
            elif used_item == "Bag of Coins":
                coins_gained = random.randint(30, 100)
                self.coins += coins_gained
                print(f"You used Bag of Coins and gained {coins_gained} coins!")
                
        else:
            print("Invalid choice.")

    def list_stash(self):
        if not self.stash:
            print("Stash is empty.")
            return
        print("Stash items:")
        for idx, item in enumerate(self.stash, 1):
            print(f"{idx}. {item}")

    def list_backpack(self):
        if not self.backpack:
            print("Backpack is empty.")
            return
        print("Backpack items:")
        for idx, item in enumerate(self.backpack, 1):
            print(f"{idx}. {item}")

    def use_backpack(self):
        if not self.backpack:
            print("Backpack is empty. Nothing to use.")
            return
        print("Backpack items:")
        for idx, item in enumerate(self.backpack, 1):
            print(f"{idx}. {item}")
        try:
            choice = int(input("Enter the number of the backpack item you want to use: "))
        except Exception:
            print("Invalid input.")
            return
        if 1 <= choice <= len(self.backpack):
            used = self.backpack.pop(choice - 1)
            self.rewards_earned.append(used)
            print(f"You used backpack item and moved it to rewards: {used}")
        else:
            print("Invalid choice.")


    def open_chest(self):
        if self.chests > 0:
            self.chests -= 1
            reward = self.get_random_reward()
            self.rewards_earned.append(reward)
            print(f"You opened a chest and received: {reward}")
            save_choice = input("Do you want to add your reward to backpack (yes/no): ").lower()
            if save_choice == "yes":
                self.backpack.append(reward)
        else:
            print("No chests to open. Womp Womp")
    def redeem_reward(self):
        print("Your rewards:")
        for idx, reward in enumerate(self.rewards_earned, 1):
            print(f"{idx}. {reward}")
        choice = int(input("Enter the number of the reward you want to redeem: "))
        if 1 <= choice <= len(self.rewards_earned):
            redeemed_reward = self.rewards_earned.pop(choice - 1)
            print(f"You redeemed: {redeemed_reward}")
    def upgrade_ability(self):
        print("Your abilities:")
        for idx, ability in enumerate(self.abilities, 1):
            print(f"{idx}. {ability}")
        choice = int(input("Enter the number of the ability you want to upgrade: "))
        if 1 <= choice <= len(self.abilities):
            ability_to_upgrade = self.abilities[choice - 1]
            upgrade_paths = {
                "Heal": "Medic",
                "Medic": "Bloodsteal",
                "Greed": "Bloodlust",
                "Bloodlust": "Greed v3",
                "Blockah'": "Shield of Light",
                "Shield of Light": "Instinct",
            }
            next_tier = upgrade_paths.get(ability_to_upgrade)
            if not next_tier:
                print("This ability cannot be upgraded further.")
                return
            
            upgrade_requirements = {
                "Medic": (["Potion of Healing", "Pheonix Feather"], coins_for_upgrade.get("Heal", 0)),
                "Bloodsteal": (["BloodHeart", "Aegis"], 150),
                "Bloodlust": (["Clove of Fortune", "BloodHeart"], coins_for_upgrade.get("Greed", 0)),
                "Greed v3": (["Bag of Coins", "Clove of Fortune"], coins_for_upgrade.get("Greed v3", 0)),
                "Shield of Light": (["Potion of Shielding", "Crystal of Revisal"], coins_for_upgrade.get("Blockah'", 0)),
                "Instinct": (["Aegis", "EmberHeart"], 150),
            }
            req_items, req_coins = upgrade_requirements.get(next_tier, ([], 0))
            print(f"You need the following items to upgrade to {next_tier}: {', '.join(req_items)} and {req_coins} coins")
            for it in req_items:
                if it not in self.stash:
                    print("You don't have the required items to upgrade this ability!")
                    return
            if self.coins < req_coins:
                print("You don't have enough coins to upgrade this ability!")
                return
            for it in req_items:
                self.stash.remove(it)
            self.coins -= req_coins
            self.abilities.append(next_tier)
            self.ability_levels[next_tier] = 1
            self.abilities.remove(ability_to_upgrade)
            if ability_to_upgrade in self.ability_levels:
                del self.ability_levels[ability_to_upgrade]
            print(f"Upgraded {ability_to_upgrade} to {next_tier}!")
        else:
            print("Invalid choice.")
    def task_completed(self):
        xp_gain = 30
        if self.xp_boost_turns > 0:
            extra = random.randint(10, 20)
            xp_gain += extra
            self.xp_boost_turns -= 1
            print(f"Fertility bonus! +{extra} extra XP ({self.xp_boost_turns} turns left)")
        self.xp += xp_gain
        if random.random() > 0.1:
            self.chests += 1
            print("You found a chest for completing your task! YAY!")
        else:
            print("No chestu???")
            if random.random() > 0.5:
                self.chests += 1
            else:
                print("nooo nooo chestuuu")
        if random.random() > 0.3:
            coins_earned = random.randint(5, 25)
            self.coins += coins_earned
            print(f"You earned {coins_earned} coins for completing the task.")
        if self.cooldown >= 1:
            self.cooldown -= 1
        else:
            self.cooldown = 0

        if getattr(self, 'greed_maw_turns', 0) > 0:
            bonus_chests = random.randint(2, 5)
            bonus_coins = random.randint(50, 150)
            self.chests += bonus_chests
            self.coins += bonus_coins
            self.greed_maw_turns -= 1
            print(f"Greed Maw hungers! +{bonus_chests} chests and +{bonus_coins} coins (remaining {self.greed_maw_turns} turns)")
            if self.greed_maw_turns == 0:
                print("The Greed Maw has bcom quet... for now.")

    def level_up(self):
        if self.xp >= self.level * 100:
            self.level += 1
            self.hp += 20
            self.xp = 0
            print(f"LEVEL UP!! You leveled up to Level {self.level}!")
        if self.level >= 3 and self.type is None:
            self.needs_type_choice = True


    def distraction(self):
        if self.block or self.block_count > 0:
            if self.block_count > 0:
                self.block_count -= 1
            else:
                self.block = False

            if getattr(self, 'instinct_reflect_turns', 0) > 0:
                heal = random.randint(15, 35)
                gained_chests = random.randint(1, 3)
                gained_coins = random.randint(10, 60)
                self.hp = min(200, self.hp + heal)
                self.chests += gained_chests
                self.coins += gained_coins
                self.instinct_reflect_turns -= 1
                print(f"Instinct reflected the distraction! Healed {heal} HP, +{gained_chests} chests and +{gained_coins} coins (remaining {self.instinct_reflect_turns})")
                if self.instinct_reflect_turns == 0:
                    print("Your Instinct has cooled down.")
            if getattr(self, 'ember_aura_turns', 0) > 0:
                heal = random.randint(10, 25)
                ember_chests = random.randint(1,2)
                ember_coins = random.randint(5, 40)
                self.hp = min(200, self.hp + heal)
                self.chests += ember_chests
                self.coins += ember_coins
                self.ember_aura_turns -= 1
                print(f"Ember aura detonated on block: +{heal} HP, +{ember_chests} chests, +{ember_coins} coins (remaining {self.ember_aura_turns})")

            print("You blocked the distraction!")
        else:
            loss = random.randint(2, 32)
            self.hp -= loss
            print(f"You got distracted and lost {loss} HP! OOF")
            if self.hp <= 0:
                print("You have been defeated by distractions! GAME OVER!!")
                print("Revive using a reward? (yes/no)")
                choice = input().lower()
                if choice == "yes":
                    self.revive()
                else:
                    print("ummm. wat")
                    print("Your save file for dis session is gone i guess....")
                    print("not sure why u wud do dis but ok")
                    exit()

    def revive(self):
        if self.rewards_earned:
            deleted_reward = random.choice(self.rewards_earned)
            self.rewards_earned.remove(deleted_reward)
            print(f"You used the reward '{deleted_reward}' to revive! You are back in the game with 50 HP!")
            self.hp = 100
        else:
            print("No rewards available to revive. GAME OVER!!")
            # instead of exiting, reset player to starting state
            self.level = 1
            self.hp = 100
            self.xp = 0
            self.chests = 0
            self.coins = 0
            self.abilities = ["Heal"]
            self.ability_levels = {"Heal": 1}
            self.type = None
            self.cooldown = 0
            self.stash = []
            self.backpack = []
            print("You have been restarted at level 1 with base stats.")
            # allow game loop to continue

    def choose_type(self, player_type):
        self.type = player_type
        if player_type == "Lust":
            self.abilities.append("Greed")
            print("LUST SHALL FOREVER BE YOUR COMPANION AS YOU HUNGER FOR MORE POWER!!")
            print("NEW ABILITY: Greed - Chance to gain a chest or lose one chest")
        elif player_type == "Dismissal":
            self.abilities.append("Blockah'")
            print("DISMISSAL SHALL GUARD YOU AGAINST ALL HARM!!")
            print("NEW ABILITY: Blockah' - Block a distaction when used")
    def print_stats(self):
        print("-------------------------------")
        print(f"Player: {self.name}")
        print(f"HP: {self.hp}")
        print(f"XP: {self.xp}")
        print(f"Level: {self.level}")
        print(f"Chests: {self.chests}")
        print(f"Type: {self.type}")
        print("Abilities: " + ", ".join(self.abilities))
        print("-------------------------------")
    def save_progress(self):
        data = {
            "name": self.name,
            "rewards_earned": self.rewards_earned,
            "hp": self.hp,
            "xp": self.xp,
            "level": self.level,
            "stash": self.stash,
            "backpack": self.backpack,
            "chests": self.chests,
            "abilities": self.abilities,
            "ability_levels": self.ability_levels,
            "type": self.type,
            "cooldown": self.cooldown,
            "coins": self.coins
        }
        with open(f"{self.name}_progress.json", "w") as f:
            json.dump(data, f)
        print("Progress saved.")
    def load_progress(self):
        path = f"{self.name}_progress.json"
        if not os.path.exists(path):
            print("No save file found.")
            return
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Failed to load save: {e}")
            return
        self.rewards_earned = data.get("rewards_earned", [])
        self.hp = data.get("hp", 100)
        self.xp = data.get("xp", 0)
        self.level = data.get("level", 1)
        self.stash = data.get("stash", [])
        self.backpack = data.get("backpack", [])
        self.chests = data.get("chests", 0)
        self.abilities = data.get("abilities", ["Heal"]) or ["Heal"]
        self.type = data.get("type")
        self.cooldown = data.get("cooldown", 0)
        self.coins = data.get("coins", 0)
        # restore ability levels if saved, otherwise default to 1
        saved_levels = data.get("ability_levels")
        if isinstance(saved_levels, dict):
            self.ability_levels = saved_levels
            # ensure new abilities have at least level 1
            for a in self.abilities:
                self.ability_levels.setdefault(a, 1)
        else:
            self.ability_levels = {a: 1 for a in self.abilities}
        print("Progress loaded. YIPEEEEEE!!")
    def use_ability(self, ability):
        if ability not in self.abilities:
            print("Ability not available.")
            return

        if ability == "Heal":
            lvl = self.ability_levels.get("Heal", 1)
            if lvl == 1:
                self.hp += 15
                print("You used Heal! +15 HP")
            elif lvl == 2:
                self.hp += 50
                print("You used Medic! +50 HP")
            else:
                self.hp += 70
                gained = random.randint(1, 2)
                self.chests += gained
                print(f"You used Bloodsteal! +70 HP and gained {gained} chests!")
            return

        if ability == "Greed":
            lvl = self.ability_levels.get("Greed", 1)
            if lvl == 1:
                if random.random() < 0.5:
                    self.chests += 1
                    print("Double or Nothing succeeded! +1 Chest")
                else:
                    self.chests = max(0, self.chests - 1)
                    print("Double or Nothing failed! -1 Chest")
            else:
                if random.random() < 0.6:
                    self.chests += 2
                    print("Bloodlust succeeded! +2 Chests")
                else:
                    print("Bloodlust gave 1 chest")
                    self.chests += 1
            self.cooldown = 2
            return

        if ability == "Bloodlust":
            if random.random() < 0.6:
                gained = random.randint(1, 3)
                self.chests += gained
                coins = random.randint(5, 30)
                self.coins += coins
                print(f"Bloodlust surges! +{gained} chests and +{coins} coins")
            else:
                self.chests = max(0, self.chests - 1)
                print("Bloodlust backfired! -1 chest")
            self.cooldown = 3
            return

        if ability == "Greed v3":
            sacrifice_type = random.random()
            if sacrifice_type > 0.5:
                sacrifice = random.randint(30, 50)
            else:
                sacrifice = "random item from stash"
            confirm = input(f"Awaken the Greed Maw? Sacrifice {sacrifice} for massive gain (yes/no): ").lower()
            if confirm not in ("yes", "y"):
                print("You resisted the Maw.")
                return
            if sacrifice == "random item from stash":
                if self.stash:
                    sacrificed_item = random.choice(self.stash)
                    self.stash.remove(sacrificed_item)
                    print(f"You sacrificed {sacrificed_item} from your stash to awaken the Greed Maw!")
                else:
                    print("No items in stash to sacrifice! bruh.ur v3 lol.")
                    return
            elif isinstance(sacrifice, int) and sacrifice > self.hp - 1:
                print("Sacrifice would be lethal! The Maw hungers but you resist to avoid death...")
                return
            elif isinstance(sacrifice, int):
                self.hp -= sacrifice
                print(f"You sacrificed {sacrifice} HP to awaken the Greed Maw!")
            immediate_chests = random.randint(1, 5)
            immediate_coins = random.randint(100, 400)
            self.chests += immediate_chests
            self.coins += immediate_coins
            self.greed_maw_turns = 2
            self.cooldown = 5
            print(f"The Greed Maw awakens! -{sacrifice if isinstance(sacrifice,int) else 'item'} sacrifice, +{immediate_chests} chests, +{immediate_coins} coins. Greed Maw will devour for {self.greed_maw_turns} tasks.")
            return
        
        if ability == "Blockah'":
            if self.cooldown > 0:
                print("Blockah' is on cooldown.")
                return
            self.block = True
            self.block_count = max(self.block_count, 1)
            self.cooldown = 2
            print("You used Blockah' - will block the next distraction.")
            return

        if ability == "Shield of Light":
            if self.cooldown > 0:
                print("Shield of Light is on cooldown.")
                return
            self.block = True
            self.block_count = max(self.block_count, 2)
            self.hp += 40
            self.coins += random.randint(1,6)
            self.cooldown = 3
            print("Shield of Light activated! Block next 2 distractions and +40 HP")
            return

        if ability == "Instinct":
            if self.cooldown > 0:
                print("Instinct is on cooldown.")
                return
            self.block = True
            self.block_count = max(self.block_count, 3)
            self.instinct_reflect_turns = 3
            self.hp = min(200, self.hp + 50)
            bonus = random.randint(1, 3)
            self.chests += bonus
            self.cooldown = 5
            print(f"Instinct awakened! For the next 3 blocks distractions will be reflected: +50 HP and +{bonus} chests immediately.")
            return

        if ability == "Ember Surge":
            if self.cooldown > 0:
                print("Ember Surge is on cooldown.")
                return
            self.ember_aura_turns = 2
            coins_to_burn = min(self.coins, 100)
            if coins_to_burn >= 10:
                burn_choice = input(f"Ember Surge can convert up to 100 coins into chests at a rate of 10 coins per chest. Burn {coins_to_burn} coins for {coins_to_burn // 10} chests? (yes/no): ").lower()
                if burn_choice in ("yes", "y"):
                    converted = coins_to_burn // 10
                    self.coins -= coins_to_burn
                    self.chests += converted
                    print(f"Ember Surge consumed {coins_to_burn} coins to create {converted} extra chests.")
            self.block = True
            self.block_count = max(self.block_count, 2)
            self.cooldown = 6
            self.hp += 50
            print("Ember Surge erupted! +50 HP, ember aura for 2 blocked distractions, and consumed coins -> chests if available.")
            self.abilities.remove("Ember Surge")
            return
        
        if ability == "Dark Rainbow":
            if self.cooldown > 0:
                print("Dark Rainbow is on cooldown.")
                return
            outcome = random.random()
            if outcome < 0.5:
                chests = random.randint(1, 3)
                coins = random.randint(20, 50)
                xp = random.randint(5, 20)
                self.chests += chests
                self.coins += coins
                self.xp += xp
                print(f"Dark Rainbow granted {chests} chests, {coins} coins, and {xp} XP!")
            else:
                loss_hp = random.randint(10, 25)
                loss_coins = random.randint(5, 15)
                self.hp -= loss_hp
                self.coins = max(0, self.coins - loss_coins)
                print(f"The Dark Rainbow backfired! Lost {loss_hp} HP and {loss_coins} coins.")
            self.cooldown = 4
            return

        if ability == "Fertility":
            if self.cooldown > 0:
                print("Fertility is on cooldown.")
                return
            self.xp_boost_turns = 3
            self.cooldown = 5
            print("Fertility activated! Tasks grant extra XP for the next 3 completions.")
            return

        if ability == "Blue Flame":
            if self.cooldown > 0:
                print("Blue Flame is on cooldown.")
                return

            possible = [a for a in self.abilities if a in ("Heal", "Greed", "Blockah'", "Medic", "Bloodlust") and a != "Blue Flame"]
            if not possible:
                print("Nothing for Blue Flame to copy right now.")
                return
            ability_to_copy = random.choice(possible)
            if ability_to_copy == "Heal":
                self.hp += 20
                print("Blue Flame copied Heal! +20 HP")
            elif ability_to_copy == "Greed":
                if random.random() < 0.5:
                    self.chests += 2
                    print("Blue Flame copied Greed and Double or Nothing succeeded! +2 Chests")
                else:
                    self.chests = max(0, self.chests - 1)
                    print("Blue Flame copied Greed and Double or Nothing failed! -1 Chest")
            elif ability_to_copy == "Blockah'":
                self.block = True
                print("Blue Flame copied Blockah'! You are now blocking the next distraction!")
            elif ability_to_copy == "Medic":
                self.hp += 60
                print("Blue Flame copied Medic! +60 HP")
            elif ability_to_copy == "Bloodlust":
                if random.random() < 0.6:
                    self.chests += 2
                    print("Blue Flame copied Bloodlust and it was lucky! +2 Chests")
                else:
                    self.chests += 1
                    print("Blue Flame copied Bloodlust and it was unlucky! +1 Chest")
            self.abilities.remove("Blue Flame")
            return



if __name__ == "__main__":
    name = input("Enter your name: ")
    player = Player(name)
    if name.strip() == "Tester":
        commands_unlocked = True
        print("Tester mode onini bananini!")
        while True:
            command = input("Enter command: ")
            if command == "add item":
                print("Items you can add: Potion of Healing, Potion of Vitality, Potion of Luck, Potion of Shielding, Crystal of Revisal, Aegis, Clove of Fortune, BloodHeart, XyolemHeart, EmberHeart, Bag of Coins")
                item_to_add = input("Enter item to add to stash: ")
                player.stash.append(item_to_add)
            elif command == "spawn boss":
                if player.level < BOSS_UNLOCK_LEVEL:
                    player.level = BOSS_UNLOCK_LEVEL
                print("Spawning a boss battle...")
                player.boss_battle()
            elif command == "upgrade ability":
                player.upgrade_ability()
            elif command == "redeem reward":
                player.redeem_reward()
            elif command == "reset cooldown":
                player.cooldown = 0
                print("Cooldown reset!")
            elif command == "get reward":
                reward = player.get_random_reward()
                print(f"Random reward: {reward}")
            elif command == "print stats":
                player.print_stats()
            elif command == "task":
                player.task_completed()
            elif command == "add ability":
                print("Abilities you can add: Heal, Medic, Bloodsteal, Greed, Bloodlust, Greed v3, Blockah', Shield of Light, Instinct, Ember Surge, Dark Rainbow, Fertility")
                ability_to_add = input("Enter ability to add: ")
                if ability_to_add in all_abilities and ability_to_add not in player.abilities:
                    player.abilities.append(ability_to_add)
                    player.ability_levels[ability_to_add] = 1
                    print(f"Added ability: {ability_to_add}")
                else:
                    print("Invalid or duplicate ability.")
            elif command == "set coins":
                set_coins = int(input("Enter number of coins to set: "))
                player.coins = set_coins
                print(f"Coins set to {set_coins} money money man")
            elif command == "add xp":
                print("Adding exp (aka xp but idc)...")
                set_xp = int(input("Enter XP to set: "))
                player.xp = set_xp
            elif command == "level up":
                print("Leveling up...")
                player.task_completed()
                player.level_up()
            
            elif command == "ability":
                print("Enter the ability you want to use:")
                ability = input()
                player.use_ability(ability)
            elif command == "open":
                player.open_chest()
            elif command in ("list stash", "list_stash"):
                player.list_stash()
            elif command in ("list backpack", "list_backpack"):
                player.list_backpack()
            elif command in ("use stash", "use_stash"):
                player.use_item()
            elif command in ("use backpack", "use_backpack"):
                player.use_backpack()
            elif command == "distraction":
                player.distraction()
            elif command == "set_level":
                new_level = int(input("Enter level to set: "))
                player.level = new_level
                print(f"Level set to {new_level}")
            elif command == "set_hp":
                new_hp = int(input("Enter HP to set: "))
                player.hp = new_hp
                print(f"HP set to {new_hp}")
            elif command == "set_xp":
                new_xp = int(input("Enter XP to set: "))
                player.xp = new_xp
                print(f"XP set to {new_xp}")
            elif command == "set_chests":
                new_chests = int(input("Enter number of chests to set: "))
                player.chests = new_chests
                print(f"Chests set to {new_chests}")
            elif command == "set_type":
                new_type = input("Enter type to set (Lust/Dismissal): ")
                player.type = new_type
                print(f"Type set to {new_type}")
            elif command == "help":
                print("Commands:")
                print("  spawn chest - Add a chest to your inventory")
                print("  add item - Add an item to your stash")
                print("  spawn boss - Trigger a boss battle (requires level 5)")
                print("  set coins - Set your coin count")
                print("  add xp - Set your XP")
                print("  level up - Gain XP and attempt to level up")
                print("  ability - Use an ability")
                print("  open - Open a chest")
                print("  list stash - List items in your stash")
                print("  list backpack - List items in your backpack")
                print("  use stash - Use an item from your stash")
                print("  use backpack - Use an item from your backpack")
                print("  distraction - Trigger a distraction event")
                print("  help - Show this help message")
            else:
                print("Unknown command.")
    if os.path.exists(f"{name}_progress.json"):
        print("Save file found. Do you want to load it? (yes/no)")
        choice = input().lower()
        if choice == "yes":
            player.load_progress()
    while True: 
        player.print_stats()
        if player.needs_type_choice:
            choice = input("Choose your type: Lust (DOUBLER) or Dismissal (BLOCKER): ")
            player.choose_type(choice)
        print("You can do: done, ability, distraction, open, list stash, list backpack, use stash, use backpack, exit")
        action = input().lower()
        if action == "done":
            player.task_completed()
            player.level_up()
            if random.random() >= 0.8 and player.level >= 3:
                player.boss_battle()
        elif action == "ability":
            print("Enter the ability you want to use:")
            ability = input()
            player.use_ability(ability)
        elif action == "open":
            player.open_chest()
        elif action in ("list stash", "list_stash"):
            player.list_stash()
        elif action in ("list backpack", "list_backpack"):
            player.list_backpack()
        elif action in ("use stash", "use_stash"):
            player.use_item()
        elif action in ("use backpack", "use_backpack"):
            player.use_backpack()
        elif action == "distraction":
            player.distraction()
        elif action == "exit":
            player.save_progress()
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")


