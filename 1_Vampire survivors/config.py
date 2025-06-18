# Enemy and Boss Configuration
# You can edit these values to balance the game

# Base enemy stats
ENEMY_STATS = {
    "zombie": {
        "speed": 80,
        "health": 20,
        "damage_rate": 20,
        "sprite_size": (45, 45)
    },
    "vampire": {
        "speed": 200,
        "health": 10,
        "damage_rate": 10,
        "sprite_size": (45, 45)
    },
    "golem": {
        "speed": 50,
        "health": 100,
        "damage_rate": 30,
        "sprite_size": (55, 55)
    },
    "mini-devil": {
        "speed": (50, 250),  # Random range
        "health": (50, 200),  # Random range
        "damage_rate": (10, 50),  # Random range
        "sprite_size": (50, 50)
    }
}

# Boss stats for different kill count milestones
BOSS_STATS = {
    50: {
        "bigfoot": {
            "speed": 100,
            "health": 500,  # + 5 * player_level
            "damage_rate": 140,
            "sprite_size": (120, 120)
        },
        "minotaur": {
            "speed": 100,
            "health": 600,  # + 5 * player_level
            "damage_rate": 100,
            "sprite_size": (100, 100)
        }
    },
    150: {
        "cyclops": {
            "speed": 60,
            "health": 1000,  # + 8 * player_level
            "damage_rate": 200,
            "sprite_size": (160, 160)
        },
        "giant": {
            "speed": 20,
            "health": 1000,  # + 8 * player_level
            "damage_rate": 200,
            "sprite_size": (250, 250)
        },
        "monster": {
            "speed": 80,
            "health": 1000,  # + 8 * player_level
            "damage_rate": 200,
            "sprite_size": (130, 130)
        }
    },
    250: {
        "cerberus": {
            "speed": 180,
            "health": 1700,  # + 10 * player_level
            "damage_rate": 140,
            "sprite_size": (130, 130)
        },
        "chimera": {
            "speed": 140,
            "health": 2000,  # + 10 * player_level
            "damage_rate": 140,
            "sprite_size": (125, 125)
        }
    },
    350: {
        "medusa": {
            "speed": 150,
            "health": 2000,  # + 12 * player_level
            "damage_rate": 100,
            "sprite_size": (150, 150)
        }
    },
    351: {
        "echidna": {
            "speed": 50,
            "health": 3500,  # + 12 * player_level
            "damage_rate": 110,
            "sprite_size": (250, 250)
        }
    },
    500: {
        "devil": {
            "speed": 150,
            "health": 4000,  # + 15 * player_level
            "damage_rate": 200,
            "sprite_size": (200, 200)
        }
    }
}

# Item stats
ITEM_STATS = {
    "gem": {
        "experience_value": 1,
        "sprite_size": (20, 20)
    },
    "mana": {
        "experience_value": (1, 10),  # Random range 1-10
        "sprite_size": (20, 20)
    },
    "emerald": {
        "health_value": (5, 20),  # random range
        "sprite_size": (25, 25)
    }
}

# Drop probabilities
DROP_PROBABILITIES = {
    "gem": 0.6,
    "mana": 0.05,
    "emerald": 0.02
}

# Weapon upgrades
upgrade_gun = {
    1: {"damage": 5, "cooldown": 2},
    2: {"damage": 5, "cooldown": 1},
    3: {"damage": 7, "cooldown": 1},
    4: {"damage": 9, "cooldown": 1},
    5: {"damage": 12, "cooldown": 0.9},
    6: {"damage": 15, "cooldown": 0.8},
    7: {"damage": 20, "cooldown": 0.7},
    8: {"damage": 25, "cooldown": 0.6},
    9: {"damage": 30, "cooldown": 0.5},
    10: {"damage": 30, "cooldown": 0.4},
    11: {"damage": 32, "cooldown": 0.5},
    12: {"damage": 35, "cooldown": 0.5},
    13: {"damage": 37, "cooldown": 0.5},
    14: {"damage": 40, "cooldown": 0.5},
    15: {"damage": 20, "cooldown": 0.1},
}

upgrade_blob = {
    1: {"damage": 5, "speed": 2, "size": 30, "radius": 100, "count": 1},
    2: {"damage": 5, "speed": 2, "size": 32, "radius": 100, "count": 1},
    3: {"damage": 5, "speed": 1.7, "size": 34, "radius": 100, "count": 2},
    4: {"damage": 5, "speed": 1.7, "size": 36, "radius": 120, "count": 2},
    5: {"damage": 10, "speed": 1.5, "size": 32, "radius": 120, "count": 3},
    6: {"damage": 10, "speed": 1.5, "size": 36, "radius": 150, "count": 3},
    7: {"damage": 10, "speed": 1.3, "size": 40, "radius": 150, "count": 4},
    8: {"damage": 10, "speed": 1.3, "size": 44, "radius": 150, "count": 4},
    9: {"damage": 10, "speed": 1.1, "size": 48, "radius": 180, "count": 5},
    10: {"damage": 10, "speed": 1.1, "size": 50, "radius": 180, "count": 5},
    11: {"damage": 10, "speed": 1, "size": 50, "radius": 180, "count": 6},
    12: {"damage": 12, "speed": 1, "size": 52, "radius": 200, "count": 6},
    13: {"damage": 12, "speed": 1.1, "size": 54, "radius": 200, "count": 7},
    14: {"damage": 15, "speed": 1.2, "size": 60, "radius": 200, "count": 7},
    15: {"damage": 10, "speed": 2, "size": 80, "radius": 250, "count": 8},
}

upgrade_heavy = {
    1: {"damage": 5, "cooldown": 30.0, "num_shots": 4},
    2: {"damage": 10, "cooldown": 30.0, "num_shots": 4},
    3: {"damage": 15, "cooldown": 25.0, "num_shots": 4},
    4: {"damage": 15, "cooldown": 25.0, "num_shots": 8},
    5: {"damage": 20, "cooldown": 25.0, "num_shots": 8},
    6: {"damage": 20, "cooldown": 25.0, "num_shots": 16},
    7: {"damage": 25, "cooldown": 25.0, "num_shots": 16},
    8: {"damage": 25, "cooldown": 25.0, "num_shots": 32},
    9: {"damage": 30, "cooldown": 25.0, "num_shots": 32},
    10: {"damage": 35, "cooldown": 20.0, "num_shots": 32},
    11: {"damage": 35, "cooldown": 20.0, "num_shots": 40},
    12: {"damage": 40, "cooldown": 20.0, "num_shots": 40},
    13: {"damage": 40, "cooldown": 20.0, "num_shots": 50},
    14: {"damage": 40, "cooldown": 20.0, "num_shots": 50},
    15: {"damage": 30, "cooldown": 10.0, "num_shots": 64},
}