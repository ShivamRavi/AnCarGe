from dataclasses import dataclass
import os

@dataclass
class Boss:
    name: str
    hp: int
    drop_table: dict
    challenges: dict


def lookup(name: str, upgradeprev=False):
    
    for boss in bosses:
        if boss.name == name:
            return boss
    if upgradeprev:
        for upgrade in upgrades:
            if upgrade.prev == name:
                return upgrade
    else:
        for upgrade in upgrades:
            if upgrade.prev == name:
                return upgrade
    
    
    return None


@dataclass
class Item:
    name: str
    rarity: str
    description: str


@dataclass
class upgrade:
    name: str
    required_items: list
    coins_required: int
    prev: str



BOSS_UNLOCK_LEVEL = 5
rarities = ["Common", "Uncommon", "Rare", "Legendary", "Mythical"]
rewards = {
    "Common": ["DTOX 5 min", "Check memes 2 min"],
    "Uncommon": ["Rblox 5min", "DTOX 10 min", "Anything 7mins"],
    "Rare": ["Watch 10 min anime clip", "Play 15 min game", "YT 10 min (/no shorts)"],
    "Legendary": ["40min DTOX", "20min GD"],
    "Mythical": ["1hr BREAK", "45min GAME"]
}

'''
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
'''

all_abilities = ["Heal", "Medic", "Bloodsteal", "Greed", "Bloodlust", "Greed v3", "Blockah'", "Shield of Light", "Instinct", "Ember Surge", "Dark Rainbow", "Fertility", "Blue Flame"]



bosses = [
    Boss(
        name="Phoenix of Procrastination",
        hp=350,
        drop_table={"Potion of Healing": 1, "Phoenix Feather": 1, "Potion of Vitality": 0.6, "XyolemHeart": 0.09},
        challenges= {"20min Focus": 0.6, "30min Focus": 0.3, "45min Focus": 0.2}
    ),
    Boss(
        name="Bloodlust of Vampiric Deformity",
        hp=500,
        drop_table={"Bag of Coins": 1, "Potion of Luck": 0.6, "Clove of Fortune": 0.4, "BloodHeart": 0.06},
        challenges={"25min Focus": 0.4, "45min Focus": 0.3, "60min Focus": 0.2}
    ),
    Boss(
        name="Knight and Mage of Unmovable Will",
        hp=500,
        drop_table={"Potion of Shielding": 1, "Crystal of Revisal": 0.6, "Aegis": 0.35, "EmberHeart": 0.07},
        challenges={"25min Focus": 0.4, "45min Focus": 0.3, "60min Focus": 0.2}
    )

]


upgrades = [
    upgrade(
        name="Medic",
        required_items=["Potion of Healing", "Pheonix Feather"],
        coins_required=20,
        prev = "Heal"
    ),
    upgrade(
        name="Lifesteal",
        required_items=["Potion of Vitality", "XyolemHeart"],
        coins_required=80,
        prev = "Medic"
    ),
    upgrade(
        name="Bloodlust",
        required_items=["Bag of Coins", "Potion of Luck"],
        coins_required=50,
        prev = "Greed"
    ),
    upgrade(
        name="Blood Maw", #renameeeeeeeeeeeeeeeeeeeeeeeeee
        required_items=["Clove of Fortune", "BloodHeart"],
        coins_required=100,
        prev="Bloodlust"
    ),
    upgrade(
        name="Shield of Light",
        required_items=["Potion of Shielding", "Crystal of Revisal"],
        coins_required=50,
        prev="Blockah'"
    ),
    upgrade(
        name="Instinct",
        required_items=["Aegis", "EmberHeart"],
        coins_required=100, 
        prev = "Shield of Light"
    )


]