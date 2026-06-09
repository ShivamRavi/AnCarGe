import random
import json
import time
import os

from arecarge.ui.pages import gui_home, upgrade_page, boss_page, distracted_page as disp, done_page as dope
from arecarge import abilities          
from arecarge.data import constants         
from arecarge.io import IO, ConsoleIO       
from arecarge import bosses                 
from arecarge.abilities import ABILITY_HANDLERS
from arecarge.shared import sq


rewards = {}
rewards.update(constants.rewards)
rarities = constants.rarities





console = ConsoleIO()

#tnd
BOSS_UNLOCK_LEVEL = 3
commands_unlocked = False


class Player:
    def __init__(self, name, IO: IO = ConsoleIO()):
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
        This helper keeps item effects consistent when they reset cooldown. being pythionic be
        """
        self.cooldown = 0
    def get_random_reward(self):
        rarity = random.choices(rarities, weights=[37, 32, 14, 9, 4], k=1)[0]
        reward = random.choice(rewards[rarity])
        return f"{reward} ({rarity})"
    def boss_battle(self, boss=None):
        if self.level < BOSS_UNLOCK_LEVEL:
            console.display(f"Boss battles are unlocked at Level {BOSS_UNLOCK_LEVEL}!")
            console.display("how dare thee hack ur own script...................")
            return
        if boss is None:
            boss = bosses.get_boss()
        if boss is None:
            console.display("Boss not found or invalid boss data.")
            return
        console.display(f"You have encountered the {boss.name}!")
        console.display(f"Boss HP: {boss.hp}")
        console.display("Boss Drop Table:")
        for item, chance in boss.drop_table.items():
            if chance > 0:
                console.display(f"  {item}: {chance * 100}% chance")
        challenge_time = bosses.get_boss_challenge(boss.name)
        console.display(f"You must focus for {challenge_time} minutes to defeat the boss!")
        sq.put({"type": "boss", "boss": boss, "time": challenge_time})
        console.prompt("Press Enter to start the challenge...")
        items_got = bosses.complete_challenge(boss, challenge_time)
        success = random.random() > 0.35
        if success:
            for item in items_got:
                self.stash.append(item)
                if item == "EmberHeart":
                    self.abilities.append("Ember Surge")
                    self.ability_levels["Ember Surge"] = 1
                    console.display("The dragon in you Rages. dun dun dunnnnn")
                elif item == "BloodHeart":
                    self.abilities.append("Dark Rainbow")
                    self.ability_levels["Dark Rainbow"] = 1
                    console.display("Not every rainbow has a unicorn")
                elif item == "XyolemHeart":
                    self.abilities.append("Fertility")
                    self.ability_levels["Fertility"] = 1
                    console.display("The XyolemHear pulses with green aura")
            sq.put({"type": "boss_success", "boss": boss, "drops": items_got})
        else:
            console.display("The boss proved too strong this time. Better luck next run.")
            sq.put({"type": "boss_failure", "boss": boss})
    def use_item(self):
        if not self.stash:
            console.display("Your stash is empty! No items to use.")
            return
        console.display("Your stash items:")
        for idx, item in enumerate(self.stash, 1):
            console.display(f"{idx}. {item}")
        choice = int(console.prompt("Enter the number of the item you want to use: "))
        if 1 <= choice <= len(self.stash):
            used_item = self.stash.pop(choice - 1)
            console.display(f"You used: {used_item}")
            if used_item == "Potion of Healing":
                self.hp += 40
                console.display("You healed for 40 HP!")
            elif used_item == "Potion of Vitality":
                self.hp += 90
                console.display("You healed for 90 HP!")    
                self.reset_cooldown()
                console.display("Your abilities are no longer on cooldown!")
            elif used_item == "Potion of Luck":
                clf_choice = random.random()
                if clf_choice > 0.5:
                   self.chests+= 2
                   console.display("Potion of Luck was lucky! +2 Chests")
                else:
                    console.display("Potion of Luck was lucky! 1 chest gain :)")
                    self.chests+=1
            elif used_item == "Potion of Shielding":
                self.block = True
                self.block_count = max(self.block_count, 1)
                console.display("You are now blocking the next distraction!")
            elif used_item == "Crystal of Revisal":
                self.block = True
                self.hp += 30
                console.display("You are now blocking the next distraction and healed for 30 HP!")
            elif used_item == "Aegis":
                self.block = True
                self.hp += 22
                self.chests += 1
                self.reset_cooldown()
                console.display("You are now blocking the next distraction, healed for 22 HP, gained 1 chest, and your abilities are no longer on cooldown!")
                console.display("NEW ABILITY ACQUIRED!")
                self.abilities.append("Blue Flame")
                self.ability_levels["Blue Flame"] = 1
            elif used_item == "Clove of Fortune":
                clf_choice = random.random()
                if clf_choice > 0.4:
                   self.chests+= 2
                   if clf_choice >= 0.7:
                       self.chests += 1
                       console.display("Clove of Fortune was lucky! +3 Chests")
                       if clf_choice >= 0.8:
                           self.chests += 2
                           console.display("LUCKYYYYY!!!!! FAIYOH!!! +5 Chests")
                           if clf_choice >= 0.9:
                               self.chests += 2
                               console.display("Clove of Fortune was extremely lucky! +7 Chests")
                               console.display("wth, you should buy a lottery ticket or smth")
                else:
                    self.chests+=1
            elif used_item == "BloodHeart" or used_item == "XyolemHeart" or used_item == "EmberHeart":
                console.display("too op for u to use :)")
                self.stash.append(used_item)
            elif used_item == "Bag of Coins":
                coins_gained = random.randint(30, 100)
                self.coins += coins_gained
                console.display(f"You used Bag of Coins and gained {coins_gained} coins!")
                
        else:
            console.display("Invalid choice.")

    def list_stash(self):
        sq.put("inventory")
        if not self.stash:
            console.display("Stash is empty.")
            return
        console.display("Stash items:")
        for idx, item in enumerate(self.stash, 1):
            console.display(f"{idx}. {item}")

    def list_backpack(self):
        sq.put("inventory")
        if not self.backpack:
            console.display("Backpack is empty.")
            return
        console.display("Backpack items:")
        for idx, item in enumerate(self.backpack, 1):
            console.display(f"{idx}. {item}")

    def use_backpack(self):
        if not self.backpack:
            console.display("Backpack is empty. Nothing to use.")
            return
        console.display("Backpack items:")
        for idx, item in enumerate(self.backpack, 1):
            console.display(f"{idx}. {item}")
        try:
            choice = int(console.prompt("Enter the number of the backpack item you want to use: "))
        except Exception:
            console.display("Invalid console.prompt.")
            return
        if 1 <= choice <= len(self.backpack):
            used = self.backpack.pop(choice - 1)
            self.rewards_earned.append(used)
            console.display(f"You used backpack item and moved it to rewards: {used}")
        else:
            console.display("Invalid choice.")


    def open_chest(self):
        if self.chests > 0:
            self.chests -= 1
            reward = self.get_random_reward()
            self.rewards_earned.append(reward)
            console.display(f"You opened a chest and received: {reward}")
            save_choice = console.prompt("Do you want to add your reward to backpack (yes/no): ").lower()
            if save_choice == "yes":
                self.backpack.append(reward)
        else:
            console.display("No chests to open. Womp Womp")
    def redeem_reward(self):
        console.display("Your rewards:")
        for idx, reward in enumerate(self.rewards_earned, 1):
            console.display(f"{idx}. {reward}")
        choice = int(console.prompt("Enter the number of the reward you want to redeem: "))
        if 1 <= choice <= len(self.rewards_earned):
            redeemed_reward = self.rewards_earned.pop(choice - 1)
    
            console.display(f"You redeemed: {redeemed_reward}")
    def upgrade_ability(self):
        console.display("Your abilities:")
        for idx, ability in enumerate(self.abilities, 1):
            console.display(f"{idx}. {ability}")
        choice = int(console.prompt("Enter the number of the ability you want to upgrade: "))
        if 1 <= choice <= len(self.abilities):
            ability_to_upgrade = self.abilities[choice - 1]
            upgrade_info = constants.lookup(ability_to_upgrade,upgradeprev = True)
            if upgrade_info and isinstance(upgrade_info, constants.upgrade):
                if upgrade_info.prev == ability_to_upgrade and upgrade_info.name not in self.abilities and upgrade_info.name in constants.all_abilities:
                    console.display(f"To upgrade {ability_to_upgrade} to {upgrade_info.name}, you need {upgrade_info.required_items} and {upgrade_info.coins_required} coins.")
                    for item in upgrade_info.required_items:
                        if item not in self.stash:
                            console.display("You don't have the required items to upgrade this ability! (missing " + item + ")")
                            return
                    if self.coins < upgrade_info.coins_required:
                        console.display("You don't have enough coins to upgrade this ability!")
                        return
                    for item in upgrade_info.required_items:
                        self.stash.remove(item)
                    self.coins -= upgrade_info.coins_required
                    self.abilities.append(upgrade_info.name)
                    self.ability_levels[upgrade_info.name] = 1
                    self.abilities.remove(ability_to_upgrade)
                    if ability_to_upgrade in self.ability_levels:
                        del self.ability_levels[ability_to_upgrade]
                else:
                    console.display("Ability not found in constants.")
    

    def task_completed(self):
        sq.put("task_completed")

        xp_gain = 30
        if self.xp_boost_turns > 0:
            extra = random.randint(10, 20)
            xp_gain += extra
            self.xp_boost_turns -= 1
            console.display(f"Fertility bonus! +{extra} extra XP ({self.xp_boost_turns} turns left)")
        self.xp += xp_gain
        if random.random() > 0.1:
            self.chests += 1
            console.display("You found a chest for completing your task! YAY!")
        else:
            console.display("No chestu???")
            if random.random() > 0.5:
                self.chests += 1
            else:
                console.display("nooo nooo chestuuu")
        if random.random() > 0.3:
            coins_earned = random.randint(5, 25)
            self.coins += coins_earned
            console.display(f"You earned {coins_earned} coins for completing the task.")
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
            console.display(f"Greed Maw hungers! +{bonus_chests} chests and +{bonus_coins} coins (remaining {self.greed_maw_turns} turns)")
            if self.greed_maw_turns == 0:
                console.display("The Greed Maw has bcom quet... for now.")

    def level_up(self):
        sq.put("level_up")
        if self.xp >= self.level * 100:
            self.level += 1
            self.hp += 20
            self.xp = 0
            console.display(f"LEVEL UP!! You leveled up to Level {self.level}!")
        if self.level >= 3 and self.type is None:
            self.needs_type_choice = True


    def distraction(self):
        sq.put("distraction")
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
                console.display(f"Instinct reflected the distraction! Healed {heal} HP, +{gained_chests} chests and +{gained_coins} coins (remaining {self.instinct_reflect_turns})")
                if self.instinct_reflect_turns == 0:
                    console.display("Instinct off")
            if getattr(self, 'ember_aura_turns', 0) > 0:
                heal = random.randint(10, 25)
                ember_chests = random.randint(1,2)
                ember_coins = random.randint(5, 40)
                self.hp = min(200, self.hp + heal)
                self.chests += ember_chests
                self.coins += ember_coins
                self.ember_aura_turns -= 1
                console.display(f"Ember aura detonated: +{heal} HP, +{ember_chests} chests, +{ember_coins} coins (remaining {self.ember_aura_turns})")

            console.display("You blocked the distraction!")
        else:
            loss = random.randint(2, 32)
            self.hp -= loss
            console.display(f"You got distracted and lost {loss} HP! OOF")
            if self.hp <= 0:
                console.display("You have been defeated by distractions! GAME OVER!!")
                console.display("Revive using a reward? (yes/no)")
                choice = console.prompt(None).lower()
                if choice == "yes":
                    self.revive()
                else:
                    console.display("ummm. wat")
                    console.display("Your save file for dis session is gone i guess....")
                    console.display("not sure why u wud do dis but ok")
                    exit()

    def revive(self):
        if self.rewards_earned:
            deleted_reward = random.choice(self.rewards_earned)
            self.rewards_earned.remove(deleted_reward)
            console.display(f"You used the reward '{deleted_reward}' to revive! You are back in the game with 50 HP!")
            self.hp = 100
        else:
            console.display("No rewards available to revive. GAME OVER!!")
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
            console.display("You have been restarted at level 1 with base stats.")

            

    def choose_type(self, player_type):
        sq.put("choose_type")
        #cnsole v
        self.type = player_type
        if player_type == "Lust":
            self.abilities.append("Greed")
            console.display("LUST SHALL FOREVER BE YOUR COMPANION AS YOU HUNGER FOR MORE POWER!!")
            console.display("NEW ABILITY: Greed - Chance to gain a chest or lose one chest")
        elif player_type == "Dismissal":
            self.abilities.append("Blockah'")
            console.display("DISMISSAL SHALL GUARD YOU AGAINST ALL HARM!!")
            console.display("NEW ABILITY: Blockah' - Block a distaction when used")
        #now to add guiv
        
    def print_stats(self):
        console.display("-------------------------------")
        console.display(f"Player: {self.name}")
        console.display(f"HP: {self.hp}")
        console.display(f"XP: {self.xp}")
        console.display(f"Level: {self.level}")
        console.display(f"Chests: {self.chests}")
        console.display(f"Type: {self.type}")
        console.display("Abilities: " + ", ".join(self.abilities))
        console.display("-------------------------------")
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
        console.display("Progress saved.")
    def load_progress(self):
        path = f"{self.name}_progress.json"
        if not os.path.exists(path):
            console.display("No save file found.")
            return
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except Exception as e:
            console.display(f"Failed to load save: {e}")
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
        saved_levels = data.get("ability_levels")
        if isinstance(saved_levels, dict):
            self.ability_levels = saved_levels
            for a in self.abilities:
                self.ability_levels.setdefault(a, 1)
        else:
            self.ability_levels = {a: 1 for a in self.abilities}
        console.display("Progress loaded. YIPEEEEEE!!")
    

    def use_ability(self, ability, io: IO = console, rng=random):
        abilities_lower = [a.lower() for a in self.abilities]
        if ability.lower() not in abilities_lower:
            print("Ability not available.")
            return

        sq.put({"type": "ability", "ability": ability})
        handler = ABILITY_HANDLERS.get(ability)
        if callable(handler):
            handler(self, io, rng)
        else:
            io.display("Ability not implemented yet.")
