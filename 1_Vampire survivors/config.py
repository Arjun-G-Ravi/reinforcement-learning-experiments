# Enemy and Boss Configuration
# You can edit these values to balance the game

# Base enemy stats
ENEMY_STATS = {
    "normal": {
        "speed": 80,
        "health": 20,
        "damage_rate": 20,
        "sprite_size": (45, 45)
    },
    "fast": {
        "speed": 200,
        "health": 10,  # + player_level
        "damage_rate": 10,
        "sprite_size": (45, 45)
    },
    "strong": {
        "speed": 50,
        "health": 100,  # + 3 * player_level
        "damage_rate": 30,
        "sprite_size": (55, 55)
    }
}

# Boss stats for different kill count milestones
BOSS_STATS = {
    100: {
        "bigfoot": {
            "speed": 50,
            "health": 300,  # + 5 * player_level
            "damage_rate": 140,
            "sprite_size": (90, 90)
        },
        "minotaur": {
            "speed": 150,
            "health": 300,  # + 5 * player_level
            "damage_rate": 100,
            "sprite_size": (85, 85)
        }
    },
    200: {
        "cyclops": {
            "speed": 40,
            "health": 600,  # + 8 * player_level
            "damage_rate": 70,
            "sprite_size": (100, 100)
        },
        "giant": {
            "speed": 40,
            "health": 800,  # + 8 * player_level
            "damage_rate": 55,
            "sprite_size": (130, 130)
        },
        "monster": {
            "speed": 140,
            "health": 450,  # + 8 * player_level
            "damage_rate": 65,
            "sprite_size": (95, 95)
        }
    },
    300: {
        "cerberus": {
            "speed": 120,
            "health": 1000,  # + 10 * player_level
            "damage_rate": 120,
            "sprite_size": (120, 120)
        },
        "chimera": {
            "speed": 100,
            "health": 750,  # + 10 * player_level
            "damage_rate": 100,
            "sprite_size": (115, 115)
        }
    },
    400: {
        "medusa": {
            "speed": 80,
            "health": 1000,  # + 12 * player_level
            "damage_rate": 100,
            "sprite_size": (140, 140)
        }
    },
    401: {
        "echidna": {
            "speed": 50,
            "health": 1500,  # + 12 * player_level
            "damage_rate": 110,
            "sprite_size": (140, 140)
        }
    },
    500: {
        "devil": {
            "speed": 150,
            "health": 2000,  # + 15 * player_level
            "damage_rate": 200,
            "sprite_size": (150, 150)
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
        "experience_value": 10,
        "sprite_size": (20, 20)
    },
    "emerald": {
        "health_value": (10, 25),  # random range
        "sprite_size": (25, 25)
    }
}

# Drop probabilities
DROP_PROBABILITIES = {
    "gem": 0.5,
    "mana": 0.01,
    "emerald": 0.05
}
