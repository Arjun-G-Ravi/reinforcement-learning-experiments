import pygame
import random
import math
from pygame.math import Vector2
from config import ENEMY_STATS, BOSS_STATS, ITEM_STATS, DROP_PROBABILITIES, upgrade_gun, upgrade_blob, upgrade_heavy

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)

screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Wizard Survivors")
clock = pygame.time.Clock()

def load_sprite(filename, size=None):
    try:
        image = pygame.image.load(filename).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error:
        surface = pygame.Surface(size if size else (50, 50))
        surface.fill(WHITE)
        return surface

wizard_sprite = load_sprite("wizard.png", (50, 50))
fire_sprite = load_sprite("icons8-fire-96.png", (30, 30))
zombie_sprite = load_sprite("icons8-zombie-64.png", ENEMY_STATS["zombie"]["sprite_size"])
vampire_sprite = load_sprite("icons8-vampire-64.png", ENEMY_STATS["vampire"]["sprite_size"])
golem_sprite = load_sprite("icons8-golem-64.png", ENEMY_STATS["golem"]["sprite_size"])

# Boss sprites
bigfoot_sprite = load_sprite("icons8-bigfoot-64.png", BOSS_STATS[100]["bigfoot"]["sprite_size"])
minotaur_sprite = load_sprite("icons8-minotaur-64.png", BOSS_STATS[100]["minotaur"]["sprite_size"])
cyclops_sprite = load_sprite("icons8-cyclops-64.png", BOSS_STATS[200]["cyclops"]["sprite_size"])
giant_sprite = load_sprite("icons8-giant-64.png", BOSS_STATS[200]["giant"]["sprite_size"])
monster_sprite = load_sprite("icons8-monster-64.png", BOSS_STATS[200]["monster"]["sprite_size"])
cerberus_sprite = load_sprite("icons8-cerberus-64.png", BOSS_STATS[300]["cerberus"]["sprite_size"])
chimera_sprite = load_sprite("icons8-chimera-64.png", BOSS_STATS[300]["chimera"]["sprite_size"])
medusa_sprite = load_sprite("icons8-medusa-64.png", BOSS_STATS[400]["medusa"]["sprite_size"])
echidna_sprite = load_sprite("icons8-echidna-64.png", BOSS_STATS[401]["echidna"]["sprite_size"])
devil_sprite = load_sprite("icons8-devil-64.png", BOSS_STATS[500]["devil"]["sprite_size"])

# Item sprites
gem_sprite = load_sprite("icons8-gem-96.png", ITEM_STATS["gem"]["sprite_size"])
mana_sprite = load_sprite("icons8-mana-100.png", ITEM_STATS["mana"]["sprite_size"])
emerald_sprite = load_sprite("icons8-emerald-64.png", ITEM_STATS["emerald"]["sprite_size"])

# Projectile sprites
red_orb_sprite = load_sprite("red-orb.png", (15, 15))
yellow_orb_sprite = load_sprite("yellow-orb.png", (20, 20))

font = pygame.font.SysFont(None, 28)
large_font = pygame.font.SysFont(None, 60)
kill_font = pygame.font.SysFont(None, 42)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
items = pygame.sprite.Group()

screen_rect = screen.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = wizard_sprite.copy()
        self.rect = self.image.get_rect(center=(screen_width / 2, screen_height / 2))
        # Smaller collision rectangle for more precise collision detection
        self.collision_rect = pygame.Rect(0, 0, 30, 30)  # Smaller than the 50x50 sprite
        self.collision_rect.center = self.rect.center
        self.pos = Vector2(self.rect.center)
        self.speed = 300
        self.health = 100
        self.experience = 0
        self.level = 1
        self.exp_to_next_level = self.level
        self.weapons = [Gun(self), BlobWeapon(self), HeavyAttack(self)]
        self.kill_count = 0
        # Hit effect variables
        self.hit_timer = 0.0
        self.hit_duration = 0.2  # Flash for 0.2 seconds
        self.is_hit = False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        velocity = Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]: velocity.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: velocity.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: velocity.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: velocity.x += 1
        if velocity.length() > 0:
            velocity = velocity.normalize() * self.speed
        self.pos += velocity * dt
        self.rect.center = self.pos
        self.collision_rect.center = self.pos  # Keep collision rect centered
        self.rect.clamp_ip(screen_rect)
        self.pos = Vector2(self.rect.center)
        self.collision_rect.center = self.pos  # Update collision rect after clamping
        for weapon in self.weapons:
            weapon.update(dt)
        
        # Update hit effect timer
        if self.is_hit:
            self.hit_timer -= dt
            if self.hit_timer <= 0:
                self.is_hit = False

    def take_damage(self, damage):
        """Apply damage and trigger hit effect"""
        self.health -= damage
        self.is_hit = True
        self.hit_timer = self.hit_duration

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_type="zombie", player_level=1, boss_name=None):
        super().__init__()
        self.enemy_type = enemy_type
        self.boss_name = boss_name
        
        if enemy_type in ENEMY_STATS:
            stats = ENEMY_STATS[enemy_type]
            if enemy_type == "zombie":
                self.image = zombie_sprite.copy()
                self.speed = stats["speed"]
                self.health = stats["health"]
                self.damage_rate = stats["damage_rate"]
            elif enemy_type == "vampire":
                self.image = vampire_sprite.copy()
                self.speed = stats["speed"]
                self.health = stats["health"] + player_level
                self.damage_rate = stats["damage_rate"]
            elif enemy_type == "golem":
                self.image = golem_sprite.copy()
                self.speed = stats["speed"]
                self.health = stats["health"] + 3 * player_level
                self.damage_rate = stats["damage_rate"]
        elif enemy_type == "boss" and boss_name:
            # Find boss stats from any kill milestone
            boss_stats = None
            for milestone_bosses in BOSS_STATS.values():
                if boss_name in milestone_bosses:
                    boss_stats = milestone_bosses[boss_name]
                    break
            
            if boss_stats:
                sprite_map = {
                    "bigfoot": bigfoot_sprite,
                    "minotaur": minotaur_sprite,
                    "cyclops": cyclops_sprite,
                    "giant": giant_sprite,
                    "monster": monster_sprite,
                    "cerberus": cerberus_sprite,
                    "chimera": chimera_sprite,
                    "medusa": medusa_sprite,
                    "echidna": echidna_sprite,
                    "devil": devil_sprite
                }
                
                self.image = sprite_map[boss_name].copy()
                self.speed = boss_stats["speed"]
                self.damage_rate = boss_stats["damage_rate"]
                
                # Calculate health based on boss type
                if boss_name in ["bigfoot", "minotaur"]:
                    self.health = boss_stats["health"] + 5 * player_level
                elif boss_name in ["cyclops", "giant", "monster"]:
                    self.health = boss_stats["health"] + 8 * player_level
                elif boss_name in ["cerberus", "chimera"]:
                    self.health = boss_stats["health"] + 10 * player_level
                elif boss_name in ["medusa", "echidna"]:
                    self.health = boss_stats["health"] + 12 * player_level
                elif boss_name == "devil":
                    self.health = boss_stats["health"] + 15 * player_level
        
        self.rect = self.image.get_rect(center=pos)
        # Create smaller collision rectangles for more precise collision detection
        if enemy_type in ENEMY_STATS:
            # Regular enemies get smaller collision rectangles (about 70% of sprite size)
            sprite_size = ENEMY_STATS[enemy_type]["sprite_size"]
            collision_size = (int(sprite_size[0] * 0.7), int(sprite_size[1] * 0.7))
        elif enemy_type == "boss" and boss_name:
            # Bosses get collision rectangles that are 60% of their sprite size
            for milestone_bosses in BOSS_STATS.values():
                if boss_name in milestone_bosses:
                    sprite_size = milestone_bosses[boss_name]["sprite_size"]
                    collision_size = (int(sprite_size[0] * 0.6), int(sprite_size[1] * 0.6))
                    break
        
        self.collision_rect = pygame.Rect(0, 0, collision_size[0], collision_size[1])
        self.collision_rect.center = pos
        self.pos = Vector2(pos)

    def update(self, dt):
        diff = player.pos - self.pos
        if diff.length_squared() == 0:  # Check if positions are identical
            direction = Vector2(0, 0)
        else:
            direction = diff.normalize()
        self.pos += direction * self.speed * dt
        self.rect.center = self.pos
        self.collision_rect.center = self.pos  # Keep collision rect centered

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, damage, color=RED, piercing=False, sprite=None):
        super().__init__()
        if sprite:
            self.image = sprite.copy()
        else:
            self.image = pygame.Surface((5, 5))
            self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.velocity = direction * 500
        self.damage = damage
        self.lifetime = 2.0
        self.piercing = piercing
        self.hit_enemies = set()

    def update(self, dt):
        self.pos += self.velocity * dt
        self.rect.center = self.pos
        self.lifetime -= dt
        if self.lifetime <= 0 or not screen_rect.contains(self.rect):
            self.kill()

class Blob(pygame.sprite.Sprite):
    def __init__(self, pos, damage, speed):
        super().__init__()
        self.size = 30
        self.image = fire_sprite.copy()
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.damage = damage
        self.rotation_speed = speed
        self.angle = 0
        self.distance = 120
        self.hit_enemies = set()

    def update(self, dt):
        self.angle += self.rotation_speed * dt
        self.pos = Vector2(
            player.pos.x + math.cos(self.angle) * self.distance,
            player.pos.y + math.sin(self.angle) * self.distance
        )
        self.rect.center = self.pos

class ExpItem(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = gem_sprite.copy()
        self.rect = self.image.get_rect(center=pos)
        self.value = ITEM_STATS["gem"]["experience_value"]

class ManaItem(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = mana_sprite.copy()
        self.rect = self.image.get_rect(center=pos)
        self.value = ITEM_STATS["mana"]["experience_value"]

class HealthItem(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = emerald_sprite.copy()
        self.rect = self.image.get_rect(center=pos)
        health_range = ITEM_STATS["emerald"]["health_value"]
        self.value = random.randint(health_range[0], health_range[1])

class Gun:
    def __init__(self, player):
        self.name = 'Gun'
        self.player = player
        self.level = 1
        self.damage = upgrade_gun[self.level]["damage"]
        self.cooldown = upgrade_gun[self.level]["cooldown"]
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.cooldown:
            self.fire()
            self.timer = 0

    def fire(self):
        nearest_enemy = find_nearest_enemy(self.player.pos)
        if nearest_enemy:
            direction = (nearest_enemy.pos - self.player.pos).normalize()
            projectile = Projectile(self.player.pos, direction, self.damage, RED, piercing=False, sprite=red_orb_sprite)
            all_sprites.add(projectile)
            projectiles.add(projectile)

    def upgrade(self):
        if self.level < 10:
            self.level += 1
            self.damage = upgrade_gun[self.level]["damage"]
            self.cooldown = upgrade_gun[self.level]["cooldown"]

    def stats(self):
        return f"Gun (Lvl {self.level}/10): Dmg {self.damage}, CD {self.cooldown:.2f}s"

    def stats_next_level(self):
        if self.level < 10:
            next_level = self.level + 1
            dmg_diff = upgrade_gun[next_level]["damage"] - self.damage
            return f"Gun (Lvl {next_level}/10): Dmg {upgrade_gun[next_level]['damage']} (+{dmg_diff}), CD {upgrade_gun[next_level]['cooldown']:.2f}s"
        return f"Gun (Maxed): Dmg {self.damage}, CD {self.cooldown:.2f}s"

class BlobWeapon:
    def __init__(self, player):
        self.name = "Blob"
        self.player = player
        self.level = 1
        self.damage = upgrade_blob[self.level]["damage"]
        self.speed = upgrade_blob[self.level]["speed"]
        self.cooldown = 0.5
        self.timer = 0
        self.blob = None

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.cooldown:
            self.fire()
            self.timer = 0
        if self.blob:
            self.blob.update(dt)

    def fire(self):
        if self.blob and self.blob.alive():
            self.blob.damage = self.damage
            self.blob.rotation_speed = self.speed
        else:
            self.blob = Blob(self.player.pos, self.damage, self.speed)
            self.blob.image = pygame.transform.scale(fire_sprite, (self.blob.size, self.blob.size))
            all_sprites.add(self.blob)
            projectiles.add(self.blob)

    def upgrade(self):
        if self.level < 10:
            self.level += 1
            self.damage = upgrade_blob[self.level]["damage"]
            self.speed = upgrade_blob[self.level]["speed"]
            self.size = upgrade_blob[self.level]["size"]
            if self.blob and self.blob.alive():
                self.blob.damage = self.damage
                self.blob.rotation_speed = self.speed
                self.blob.size = self.size
                self.blob.image = pygame.transform.scale(fire_sprite, (self.size, self.size))

    def stats(self):
        return f"Blob (Lvl {self.level}/10): Dmg {self.damage}, Spd {self.speed:.1f}"

    def stats_next_level(self):
        if self.level < 10:
            next_level = self.level + 1
            dmg_diff = upgrade_blob[next_level]["damage"] - self.damage
            spd_diff = upgrade_blob[next_level]["speed"] - self.speed
            return f"Blob (Lvl {next_level}/10): Dmg {upgrade_blob[next_level]['damage']} (+{dmg_diff}), Spd {upgrade_blob[next_level]['speed']:.1f} (+{spd_diff:.1f})"
        return f"Blob (Maxed): Dmg {self.damage}, Spd {self.speed:.1f}"

class HeavyAttack:
    def __init__(self, player):
        self.name = 'Heavy'
        self.player = player
        self.level = 1
        self.damage = upgrade_heavy[self.level]["damage"]
        self.cooldown = upgrade_heavy[self.level]["cooldown"]
        self.timer = self.cooldown
        self.num_shots = 4
        self.ready = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if not self.ready:
            self.timer += dt
            if self.timer >= self.cooldown:
                self.ready = True
                self.timer = self.cooldown
        if keys[pygame.K_SPACE] and self.ready:
            self.fire()
            self.ready = False
            self.timer = 0

    def fire(self):
        angle_step = 360 / self.num_shots
        for i in range(self.num_shots):
            angle = math.radians(i * angle_step)
            direction = Vector2(math.cos(angle), math.sin(angle)).normalize()
            projectile = Projectile(self.player.pos, direction, self.damage, BLUE, piercing=True, sprite=yellow_orb_sprite)
            all_sprites.add(projectile)
            projectiles.add(projectile)

    def upgrade(self):
        if self.level < 10:
            self.level += 1
            self.damage = upgrade_heavy[self.level]["damage"]
            self.cooldown = upgrade_heavy[self.level]["cooldown"]
            self.ready = False
            self.timer = self.cooldown
            self.num_shots = upgrade_heavy[self.level]["num_shots"]

    def stats(self):
        reload = self.cooldown - self.timer if not self.ready else 0
        return f"Heavy (Lvl {self.level}/10): Dmg {self.damage}, Rld {reload:.1f}s"

    def stats_next_level(self):
        if self.level < 10:
            next_level = self.level + 1
            dmg_diff = upgrade_heavy[next_level]["damage"] - self.damage
            reload = upgrade_heavy[next_level]["cooldown"] - self.timer if not self.ready else 0
            return f"Heavy (Lvl {next_level}/10): Dmg {upgrade_heavy[next_level]['damage']} (+{dmg_diff}), Rld {reload:.1f}s"
        reload = self.cooldown - self.timer if not self.ready else 0
        return f"Heavy (Maxed): Dmg {self.damage}, Rld {reload:.1f}s"

def find_nearest_enemy(position):
    nearest = None
    min_dist = float('inf')
    for enemy in enemies:
        dist = (enemy.pos - position).length()
        if dist < min_dist:
            min_dist = dist
            nearest = enemy
    return nearest

def check_collision_with_enemies(player):
    """Custom collision detection using smaller collision rectangles"""
    colliding_enemies = []
    for enemy in enemies:
        if player.collision_rect.colliderect(enemy.collision_rect):
            colliding_enemies.append(enemy)
    return colliding_enemies

player = Player()
all_sprites.add(player)

spawn_timer = 0
base_spawn_interval = 3

game_state = "playing"
game_result = None

# Debug option - set to True to see collision rectangles
SHOW_COLLISION_RECTS = False

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = "quit_confirm"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_q:
                if game_state not in ["quit_confirm", "end"]:
                    game_state = "quit_confirm"
            if game_state == "quit_confirm":
                if event.key == pygame.K_y:
                    running = False
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    game_state = "playing"
            elif game_state == "upgrading":
                if event.key == pygame.K_1 and player.weapons[0].level < 10:
                    player.weapons[0].upgrade()
                    game_state = "playing"
                elif event.key == pygame.K_2 and player.weapons[1].level < 10:
                    player.weapons[1].upgrade()
                    game_state = "playing"
                elif event.key == pygame.K_3 and player.weapons[2].level < 10:
                    player.weapons[2].upgrade()
                    game_state = "playing"
                elif event.key == pygame.K_4 or event.key == pygame.K_SPACE:
                    player.health = min(100, player.health + 25)
                    game_state = "playing"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "upgrading":
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(upgrade_rects):
                    if rect.collidepoint(mouse_pos):
                        if i < 3 and player.weapons[i].level < 10:
                            player.weapons[i].upgrade()
                            game_state = "playing"
                        elif i == 3:
                            player.health = min(100, player.health + 25)
                            game_state = "playing"
                        break

    if game_state == "playing":
        all_sprites.update(dt)

        spawn_interval = max(0.7, base_spawn_interval - 0.3 * (player.level - 1))
        spawn_timer += dt
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                pos = (random.randint(0, screen_width), -20)
            elif side == 'bottom':
                pos = (random.randint(0, screen_width), screen_height + 20)
            elif side == 'left':
                pos = (-20, random.randint(0, screen_height))
            else:
                pos = (screen_width + 20, random.randint(0, screen_height))
            if player.level < 5: enemy_type = random.choices(["zombie", "vampire", "golem"], weights=[95, 5, 0], k=1)[0]
            elif player.level < 10: enemy_type = random.choices(["zombie", "vampire", "golem"], weights=[70, 20, 10], k=1)[0]
            elif player.level < 15: enemy_type = random.choices(["zombie", "vampire", "golem"], weights=[50, 40, 10], k=1)[0]
            elif player.level < 20: enemy_type = random.choices(["zombie", "vampire", "golem"], weights=[20, 60, 20], k=1)[0]
            elif player.level < 25: enemy_type = random.choices(["zombie", "vampire", "golem"], weights=[10, 10, 80], k=1)[0]
            elif player.level < 30: enemy_type = random.choices(["zombie", "vampire", "golem"], weights=[0, 70, 30], k=1)[0]
            else: enemy_type = random.choices(["zombie", "vampire", "golem"], weights=[0, 50, 50], k=1)[0]
            enemy = Enemy(pos, enemy_type, player.level)
            all_sprites.add(enemy)
            enemies.add(enemy)

        for projectile in projectiles:
            if isinstance(projectile, Blob):
                hits = pygame.sprite.spritecollide(projectile, enemies, False)
                for enemy in hits:
                    if enemy not in projectile.hit_enemies:
                        enemy.health -= projectile.damage
                        projectile.hit_enemies.add(enemy)
                        if enemy.health <= 0:
                            enemy.kill()
                            drop = random.choices(["gem", "mana", "emerald"], 
                                                  weights=[DROP_PROBABILITIES["gem"], 
                                                           DROP_PROBABILITIES["mana"],
                                                           DROP_PROBABILITIES["emerald"]], 
                                                  k=1)[0]
                            if drop == "gem":
                                item = ExpItem(enemy.rect.center)
                            elif drop == "mana":
                                item = ManaItem(enemy.rect.center)
                            else:
                                item = HealthItem(enemy.rect.center)
                            all_sprites.add(item)
                            items.add(item)
                            player.kill_count += 1
                            
                            # Boss spawning logic
                            boss_name = None
                            if player.kill_count == 100:
                                boss_name = random.choice(["bigfoot", "minotaur"])
                            elif player.kill_count == 200:
                                boss_name = random.choice(["cyclops", "giant", "monster"])
                            elif player.kill_count == 300:
                                boss_name = random.choice(["cerberus", "chimera"])
                            elif player.kill_count == 400:
                                boss_name = "medusa"
                            elif player.kill_count == 401:
                                boss_name = "echidna"
                            elif player.kill_count == 500:
                                boss_name = "devil"
                            
                            if boss_name:
                                side = random.choice(['top', 'bottom', 'left', 'right'])
                                if side == 'top':
                                    pos = (random.randint(0, screen_width), -50)
                                elif side == 'bottom':
                                    pos = (random.randint(0, screen_width), screen_height + 50)
                                elif side == 'left':
                                    pos = (-50, random.randint(0, screen_height))
                                else:
                                    pos = (screen_width + 50, random.randint(0, screen_height))
                                boss = Enemy(pos, "boss", player.level, boss_name)
                                all_sprites.add(boss)
                                enemies.add(boss)
                            
                            if enemy.enemy_type == "boss" and enemy.boss_name == "devil":
                                game_state = "end"
                                game_result = "win"
                if projectile.angle >= 2 * math.pi:
                    projectile.hit_enemies.clear()
                    projectile.angle -= 2 * math.pi
            else:
                hits = pygame.sprite.spritecollide(projectile, enemies, False)
                for enemy in hits:
                    if enemy not in projectile.hit_enemies:
                        enemy.health -= projectile.damage
                        projectile.hit_enemies.add(enemy)
                        if not projectile.piercing:
                            projectile.kill()
                        if enemy.health <= 0:
                            enemy.kill()
                            drop = random.choices(["gem", "mana", "emerald"], 
                                                  weights=[DROP_PROBABILITIES["gem"], 
                                                           DROP_PROBABILITIES["mana"],
                                                           DROP_PROBABILITIES["emerald"]], 
                                                  k=1)[0]
                            if drop == "gem":
                                item = ExpItem(enemy.rect.center)
                            elif drop == "mana":
                                item = ManaItem(enemy.rect.center)
                            else:
                                item = HealthItem(enemy.rect.center)
                            all_sprites.add(item)
                            items.add(item)
                            player.kill_count += 1
                            
                            # Boss spawning logic
                            boss_name = None
                            if player.kill_count == 100:
                                boss_name = random.choice(["bigfoot", "minotaur"])
                            elif player.kill_count == 200:
                                boss_name = random.choice(["cyclops", "giant", "monster"])
                            elif player.kill_count == 300:
                                boss_name = random.choice(["cerberus", "chimera"])
                            elif player.kill_count == 400:
                                boss_name = "medusa"
                            elif player.kill_count == 401:
                                boss_name = "echidna"
                            elif player.kill_count == 500:
                                boss_name = "devil"
                            
                            if boss_name:
                                side = random.choice(['top', 'bottom', 'left', 'right'])
                                if side == 'top':
                                    pos = (random.randint(0, screen_width), -50)
                                elif side == 'bottom':
                                    pos = (random.randint(0, screen_width), screen_height + 50)
                                elif side == 'left':
                                    pos = (-50, random.randint(0, screen_height))
                                else:
                                    pos = (screen_width + 50, random.randint(0, screen_height))
                                boss = Enemy(pos, "boss", player.level, boss_name)
                                all_sprites.add(boss)
                                enemies.add(boss)
                            
                            if enemy.enemy_type == "boss" and enemy.boss_name == "devil":
                                game_state = "end"
                                game_result = "win"
                        break

        for item in items:
            if (player.pos - Vector2(item.rect.center)).length() < 50:
                if isinstance(item, ExpItem):
                    player.experience += item.value
                    if player.experience >= player.exp_to_next_level:
                        player.level += 1
                        player.experience -= player.exp_to_next_level
                        player.exp_to_next_level = player.level
                        game_state = "upgrading"
                elif isinstance(item, ManaItem):
                    player.experience += item.value
                    if player.experience >= player.exp_to_next_level:
                        player.level += 1
                        player.experience -= player.exp_to_next_level
                        player.exp_to_next_level = player.level
                        game_state = "upgrading"
                elif isinstance(item, HealthItem):
                    player.health = min(100, player.health + item.value)
                item.kill()

        # Player vs Enemies - Using custom collision detection with smaller collision rectangles
        colliding_enemies = check_collision_with_enemies(player)
        if colliding_enemies:
            total_damage_rate = sum(enemy.damage_rate for enemy in colliding_enemies)
            damage = total_damage_rate * dt
            player.take_damage(damage)

        # Check game over conditions
        if player.health <= 0:
            game_state = "end"
            game_result = "loss"

    # Drawing
    if game_state in ["playing", "upgrading"]:
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # Optional: Draw collision rectangles for debugging
        if SHOW_COLLISION_RECTS:
            pygame.draw.rect(screen, GREEN, player.collision_rect, 2)  # Player collision rect in green
            for enemy in enemies:
                pygame.draw.rect(screen, RED, enemy.collision_rect, 1)  # Enemy collision rects in red
        
        # Draw red hit effect overlay
        if player.is_hit:
            hit_surface = pygame.Surface((screen_width, screen_height))
            hit_surface.set_alpha(int(100 * (player.hit_timer / player.hit_duration)))  # Fade out effect
            hit_surface.fill(RED)
            screen.blit(hit_surface, (0, 0))

    if game_state == "upgrading":
        upgrade_rects = []
        pygame.draw.rect(screen, GRAY, (100, 200, 1000, 400))
        title_text = font.render("Level Up! Choose an upgrade:", True, WHITE)
        screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, 280))

        button_width = 200
        total_width = button_width * 4 + 30 * 3
        start_x = (screen_width - total_width) // 2
        
        for i, weapon in enumerate(player.weapons):
            x = start_x + i * (button_width + 30)
            if weapon.level >= 15:
                upgrade_text1 = font.render(f"{weapon.name}: Lv {weapon.level}", True, WHITE)
                upgrade_text2 = font.render("MAXED OUT", True, YELLOW)
                text_rect1 = upgrade_text1.get_rect(center=(x + button_width//2, 390))
                text_rect2 = upgrade_text2.get_rect(center=(x + button_width//2, 420))
                button_rect = pygame.Rect(x, 350, button_width, 120)
                pygame.draw.rect(screen, GRAY, button_rect)
                screen.blit(upgrade_text1, text_rect1)
                screen.blit(upgrade_text2, text_rect2)
            else:
                upgrade_text1 = font.render(f"{weapon.name}: Lv {weapon.level}", True, WHITE)
                upgrade_text2 = font.render(f"Damage: {weapon.damage}", True, WHITE)
                upgrade_text3 = font.render(f"Cooldown: {weapon.cooldown}", True, WHITE)
                text_rect1 = upgrade_text1.get_rect(center=(x + button_width//2, 380))
                text_rect2 = upgrade_text2.get_rect(center=(x + button_width//2, 410))
                text_rect3 = upgrade_text3.get_rect(center=(x + button_width//2, 440))
                button_rect = pygame.Rect(x, 350, button_width, 120)
                upgrade_rects.append(button_rect)
                pygame.draw.rect(screen, LIGHT_GRAY, button_rect)
                screen.blit(upgrade_text1, text_rect1)
                screen.blit(upgrade_text2, text_rect2)
                screen.blit(upgrade_text3, text_rect3)

        x = start_x + 3 * (button_width + 30)
        health_text1 = font.render("Health", True, WHITE)
        health_text2 = font.render("+25", True, WHITE)
        text_rect1 = health_text1.get_rect(center=(x + button_width//2, 400))
        text_rect2 = health_text2.get_rect(center=(x + button_width//2, 430))
        button_rect = pygame.Rect(x, 350, button_width, 120)
        upgrade_rects.append(button_rect)
        pygame.draw.rect(screen, LIGHT_GRAY, button_rect)
        screen.blit(health_text1, text_rect1)
        screen.blit(health_text2, text_rect2)

    elif game_state == "end":
        screen.fill(GRAY)
        if game_result == "win":
            end_text = large_font.render("You Won!", True, WHITE)
        else:
            end_text = large_font.render("You Lost!", True, WHITE)
        screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - 100))
        stats_text = font.render(f"Level: {player.level}  Kills: {player.kill_count}", True, WHITE)
        screen.blit(stats_text, (screen_width // 2 - stats_text.get_width() // 2, screen_height // 2))
        quit_text = font.render("Press Q to quit", True, WHITE)
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 50))

    elif game_state == "quit_confirm":
        # Draw the game in the background but slightly darkened
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Draw quit confirmation dialog
        dialog_width = 400
        dialog_height = 200
        dialog_x = (screen_width - dialog_width) // 2
        dialog_y = (screen_height - dialog_height) // 2
        
        pygame.draw.rect(screen, GRAY, (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height), 3)
        
        # Dialog text
        quit_title = large_font.render("Quit Game?", True, WHITE)
        quit_question = font.render("Are you sure you want to quit?", True, WHITE)
        quit_yes = font.render("Press Y to quit", True, GREEN)
        quit_no = font.render("Press N to continue", True, YELLOW)
        quit_esc = font.render("Press ESC to continue", True, YELLOW)
        
        screen.blit(quit_title, (dialog_x + dialog_width//2 - quit_title.get_width()//2, dialog_y + 30))
        screen.blit(quit_question, (dialog_x + dialog_width//2 - quit_question.get_width()//2, dialog_y + 80))
        screen.blit(quit_yes, (dialog_x + dialog_width//2 - quit_yes.get_width()//2, dialog_y + 120))
        screen.blit(quit_no, (dialog_x + dialog_width//2 - quit_no.get_width()//2, dialog_y + 145))
        screen.blit(quit_esc, (dialog_x + dialog_width//2 - quit_esc.get_width()//2, dialog_y + 170))

    if game_state in ["playing", "upgrading"]:
        health_bar_width = 200
        health_bar_height = 15
        health_ratio = max(0, player.health / 100)
        pygame.draw.rect(screen, RED, (10, 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (10, 10, health_bar_width * health_ratio, health_bar_height))
        health_text = font.render(f"Health: {int(max(0, player.health))}", True, WHITE)
        screen.blit(health_text, (220, 10))
        
        level_text = font.render(f"Level: {player.level}", True, WHITE)
        screen.blit(level_text, (10, 35))
        
        exp_ratio = player.experience / player.exp_to_next_level if player.exp_to_next_level > 0 else 0
        pygame.draw.rect(screen, BLUE, (10, 55, 200 * exp_ratio, 15))

        kill_text = kill_font.render(f"Kills: {player.kill_count}", True, WHITE)
        screen.blit(kill_text, (screen_width // 2 - kill_text.get_width() // 2, 10))

        for i, weapon in enumerate(player.weapons):
            if weapon.name == 'Heavy':
                color = WHITE if weapon.ready else RED
            else:
                color = WHITE
            stat_text = font.render(weapon.stats(), True, color)
            screen.blit(stat_text, (screen_width - 350, 15 + i * 35))

    pygame.display.flip()

pygame.quit()