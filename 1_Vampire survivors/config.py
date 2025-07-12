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
        "speed": (50, 150),  # Random range
        "health": (50, 120),  # Random range
        "damage_rate": (10, 30),  # Random range
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
        },
        "monster": {
            "speed": 80,
            "health": 700,  # + 8 * player_level
            "damage_rate": 100,
            "sprite_size": (130, 130)
        }
    },
    150: {
        "cyclops": {
            "speed": 40,
            "health": 1000,  # + 8 * player_level
            "damage_rate": 200,
            "sprite_size": (250, 250)
        },
        "giant": {
            "speed": 40,
            "health": 1000,  # + 8 * player_level
            "damage_rate": 200,
            "sprite_size": (300, 300)
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
            "health": 2500,  # + 12 * player_level
            "damage_rate": 100,
            "sprite_size": (150, 150)
        }
    },
    351: {
        "echidna": {
            "speed": 50,
            "health": 3500,  # + 12 * player_level
            "damage_rate": 100,
            "sprite_size": (250, 250)
        }
    },
    500: {
        "devil": {
            "speed": 150,
            "health": 5000,  # + 15 * player_level
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

# Spawn rate configuration
SPAWN_CONFIG = {
    "base_spawn_interval": 1,
    "min_spawn_interval": 0.2,  # Minimum spawn interval after level 30
    "level_30_interval": 0.3,   # Spawn interval at level 30+
    "devil_battle_interval": 0.5,  # Slower spawning during devil fight
    "spawn_reduction_per_level": 0.05,  # How much to reduce spawn time per level
    "max_enemies": 50,  # Maximum number of enemies on screen
    "overcrowded_spawn_interval": 1.0  # Spawn interval when enemy limit is reached
}

# Enemy type probabilities based on player level and kill count
ENEMY_SPAWN_WEIGHTS = {
    # Before kill 500 (no mini-devils)
    "before_500": {
        "level_0_5": {"zombie": 95, "vampire": 5, "golem": 0},
        "level_5_10": {"zombie": 70, "vampire": 20, "golem": 10},
        "level_10_15": {"zombie": 50, "vampire": 40, "golem": 10},
        "level_15_20": {"zombie": 20, "vampire": 60, "golem": 20},
        "level_20_25": {"zombie": 10, "vampire": 10, "golem": 80},
        "level_25_30": {"zombie": 0, "vampire": 70, "golem": 30},
        "level_30_plus": {"zombie": 0, "vampire": 50, "golem": 50}
    },
    # After kill 500 (include mini-devils)
    "after_500": {
        "level_0_5": {"zombie": 85, "vampire": 15, "golem": 0, "mini-devil": 10},
        "level_5_10": {"zombie": 60, "vampire": 20, "golem": 10, "mini-devil": 10},
        "level_10_15": {"zombie": 40, "vampire": 30, "golem": 15, "mini-devil": 15},
        "level_15_20": {"zombie": 15, "vampire": 45, "golem": 20, "mini-devil": 20},
        "level_20_25": {"zombie": 5, "vampire": 5, "golem": 40, "mini-devil": 50},
        "level_25_30": {"zombie": 0, "vampire": 25, "golem": 25, "mini-devil": 50},
        "level_30_plus": {"zombie": 0, "vampire": 20, "golem": 10, "mini-devil": 70}
    }
}

# Boss spawn configuration - easily modify kill count requirements
BOSS_SPAWN_CONFIG = {
    50: ["bigfoot", "minotaur", "monster"],  # Random choice from this list
    150: ["cyclops", "giant"],               # Random choice from this list
    350: ["cerberus", "chimera"],            # Random choice from this list
    500: ["medusa"],                         # Single boss
    501: ["echidna"],                        # Single boss
    700: ["devil"]                           # Final boss
}

# Mini devil spawn configuration - spawn mini devils when devil spawns
MINI_DEVIL_SPAWN_CONFIG = {
    700: 3  # Spawn 3 mini devils when devil spawns at kill 700
}

# Weapon upgrades
upgrade_gun = {
    1: {"damage": 7, "cooldown": 2},
    2: {"damage": 10, "cooldown": 1},
    3: {"damage": 12, "cooldown": 1},
    4: {"damage": 14, "cooldown": 1},
    5: {"damage": 15, "cooldown": 0.9},
    6: {"damage": 15, "cooldown": 0.8},
    7: {"damage": 20, "cooldown": 0.7},
    8: {"damage": 25, "cooldown": 0.6},
    9: {"damage": 30, "cooldown": 0.5},
    10: {"damage": 30, "cooldown": 0.4},
    11: {"damage": 32, "cooldown": 0.5},
    12: {"damage": 35, "cooldown": 0.5},
    13: {"damage": 37, "cooldown": 0.4},
    14: {"damage": 40, "cooldown": 0.4},
    15: {"damage": 20, "cooldown": 0.1},
}

upgrade_blob = {
    1: {"damage": 5, "speed": 2, "size": 30, "radius": 100, "count": 1},
    2: {"damage": 5, "speed": 2, "size": 32, "radius": 100, "count": 1},
    3: {"damage": 5, "speed": 1.7, "size": 34, "radius": 100, "count": 2},
    4: {"damage": 5, "speed": 1.7, "size": 36, "radius": 120, "count": 2},
    5: {"damage": 10, "speed": 1.5, "size": 32, "radius": 120, "count": 3},
    6: {"damage": 10, "speed": 1.5, "size": 36, "radius": 150, "count": 3},
    7: {"damage": 12, "speed": 1.3, "size": 40, "radius": 150, "count": 4},
    8: {"damage": 12, "speed": 1.3, "size": 44, "radius": 150, "count": 4},
    9: {"damage": 12, "speed": 1.1, "size": 48, "radius": 180, "count": 5},
    10: {"damage": 12, "speed": 1.1, "size": 50, "radius": 180, "count": 5},
    11: {"damage": 12, "speed": 1, "size": 50, "radius": 180, "count": 6},
    12: {"damage": 15, "speed": 1, "size": 52, "radius": 200, "count": 6},
    13: {"damage": 15, "speed": 1.1, "size": 54, "radius": 200, "count": 7},
    14: {"damage": 15, "speed": 1.2, "size": 60, "radius": 200, "count": 7},
    15: {"damage": 20, "speed": 2, "size": 60, "radius": 250, "count": 8},
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