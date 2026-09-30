import math
import random
import pygame

VIEW_W, VIEW_H = 800, 560
WORLD_W = 3200
RADAR_H = 56
PLAY_TOP = RADAR_H + 6
HUMANOID_COUNT = 6
FALL_LIMIT = 160
PHASES = [random.uniform(0, math.tau) for _ in range(3)]


def sky_color(wave):
    """Return a distinct dark sky colour for each wave."""
    palette = [
        (5, 5, 20),    # Wave 1: near-black
        (15, 35, 90),  # Wave 2: deep blue
        (60, 20, 90),  # Wave 3: purple
        (90, 20, 30),  # Wave 4: dark red
        (10, 70, 70),  # Wave 5: teal
    ]
    return palette[(int(wave) - 1) % len(palette)]


def on_humanoid_rescued(humanoid):
    """Show a rescue popup and briefly protect the player."""
    game = active_game
    game.popups.append({"x": humanoid.x, "y": humanoid.y - 18, "life": 1.0})
    game.player.invulnerable = max(game.player.invulnerable, 2.0)


def bonus_life_threshold():
    """Return the score threshold for earning an extra life."""
    # 500 is for the demo video; use 10000 for real play.
    return 500


def wrap_delta(a, b):
    """Shortest signed distance from world x=a to world x=b on a wrapping world."""
    return (b - a + WORLD_W / 2) % WORLD_W - WORLD_W / 2


def ground_y(x):
    angle = math.tau * x / WORLD_W
    return 505 - 25 * math.sin(3 * angle + PHASES[0]) - 14 * math.sin(7 * angle + PHASES[1]) - 6 * math.sin(13 * angle + PHASES[2])


class Humanoid:
    def __init__(self, x):
        self.x, self.y = x, ground_y(x) - 8
        self.state = "ground"
        self.fall_from = self.y
        self.vy = 0.0

    def update(self, dt):
        if self.state == "falling":
            self.vy += 300 * dt
            self.y += self.vy * dt
            floor = ground_y(self.x) - 8
            if self.y >= floor:
                self.y = floor
                self.vy = 0
                self.state = "dead" if floor - self.fall_from > FALL_LIMIT else "ground"


class Lander:
    def __init__(self, x):
        self.x, self.y = x, PLAY_TOP + 20
        self.target = None
        self.mutant = False

    def pick_target(self, humanoids, landers):
        free = [h for h in humanoids if h.state == "ground" and not any(h is l.target for l in landers)]
        self.target = random.choice(free) if free else None

    def update(self, dt, player, humanoids, landers, wave):
        if self.mutant:
            dx = wrap_delta(self.x, player.x)
            dy = player.y - self.y
            dist = math.hypot(dx, dy) or 1
            speed = 110 + wave * 10
            self.x = (self.x + dx / dist * speed * dt + random.uniform(-40, 40) * dt) % WORLD_W
            self.y += dy / dist * speed * dt
            return
        if self.target is None or self.target.state not in ("ground", "carried"):
            self.target = None
            self.pick_target(humanoids, landers)
        target = self.target
        if target is None:
            dx, dy = wrap_delta(self.x, player.x), player.y - self.y
            dist = math.hypot(dx, dy) or 1
            self.x = (self.x + dx / dist * 60 * dt) % WORLD_W
            self.y += dy / dist * 60 * dt
        elif target.state == "carried":
            self.y -= 45 * dt
            target.x, target.y = self.x, self.y + 20
            if self.y <= PLAY_TOP + 8:
                humanoids.remove(target)
                self.target, self.mutant = None, True
        else:
            dx, dy = wrap_delta(self.x, target.x), target.y - 18 - self.y
            dist = math.hypot(dx, dy)
            if dist < 6:
                target.state = "carried"
            else:
                self.x = (self.x + dx / dist * 70 * dt) % WORLD_W
                self.y += dy / dist * 70 * dt


class Player:
    def __init__(self):
        self.x, self.y, self.vx, self.facing = WORLD_W / 2, 250.0, 0.0, 1
        self.invulnerable, self.cooldown = 1.5, 0.0

    def update(self, dt, keys):
        thrust = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        if thrust:
            self.facing = thrust
        self.vx = max(-520, min(520, self.vx + thrust * 900 * dt))
        self.vx *= 1 - min(1.0, 0.8 * dt)
        self.x = (self.x + self.vx * dt) % WORLD_W
        self.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 260 * dt
        self.y = max(PLAY_TOP + 10, min(VIEW_H - 30, self.y))
        self.invulnerable = max(0.0, self.invulnerable - dt)
        self.cooldown -= dt


class Game:
    def __init__(self):
        global active_game
        self.font = pygame.font.Font(None, 26)
        self.reset()
        active_game = self

    def reset(self):
        self.player = Player()
        self.humanoids = [Humanoid(i * WORLD_W / HUMANOID_COUNT + 100) for i in range(HUMANOID_COUNT)]
        self.landers, self.bullets = [], []
        self.score, self.lives, self.wave, self.state = 0, 3, 1, "play"
        self.bonus_awarded = 0
        self.popups = []
        self.start_wave()

    def start_wave(self):
        self.to_spawn = 3 + self.wave * 2
        self.spawn_timer = 1.0
        while len(self.humanoids) < HUMANOID_COUNT:
            self.humanoids.append(Humanoid(random.uniform(0, WORLD_W)))

    def shoot_lander(self, lander):
        self.landers.remove(lander)
        if lander.target is not None and lander.target.state == "carried":
            lander.target.state = "falling"
            lander.target.fall_from = lander.target.y
        self.score += 150

    def update(self, dt, keys):
        if self.state != "play":
            return
        for popup in self.popups:
            popup["y"] -= 35 * dt
            popup["life"] -= dt
        self.popups = [popup for popup in self.popups if popup["life"] > 0]
        player = self.player
        player.update(dt, keys)
        threshold = bonus_life_threshold()
        if threshold:
            bonus_milestones = self.score // threshold
            if bonus_milestones > self.bonus_awarded:
                self.lives += bonus_milestones - self.bonus_awarded
                self.bonus_awarded = bonus_milestones
        if keys[pygame.K_SPACE] and player.cooldown <= 0:
            player.cooldown = 0.18
            self.bullets.append({"x": player.x + player.facing * 20, "y": player.y, "dir": player.facing, "life": 0.7})
        self.spawn_timer -= dt
        if self.to_spawn > 0 and self.spawn_timer <= 0:
            self.landers.append(Lander(random.uniform(0, WORLD_W)))
            self.to_spawn -= 1
            self.spawn_timer = 1.5
        for lander in self.landers:
            lander.update(dt, player, self.humanoids, self.landers, self.wave)
        for humanoid in self.humanoids[:]:
            humanoid.update(dt)
            if humanoid.state == "dead":
                self.humanoids.remove(humanoid)
            elif humanoid.state == "falling" and abs(wrap_delta(player.x, humanoid.x)) < 24 and abs(humanoid.y - player.y) < 24:
                humanoid.state, humanoid.y = "ground", ground_y(humanoid.x) - 8
                # Release any stale lander reference before the humanoid can be targeted again.
                for lander in self.landers:
                    if lander.target is humanoid:
                        lander.target = None
                self.score += 500
                on_humanoid_rescued(humanoid)
        self.update_bullets(dt)
        if player.invulnerable <= 0:
            for lander in self.landers:
                if abs(wrap_delta(player.x, lander.x)) < 22 and abs(lander.y - player.y) < 18:
                    self.lives -= 1
                    self.player = Player()
                    if self.lives <= 0:
                        self.state = "lose"
                    break
        if self.to_spawn == 0 and not self.landers:
            self.wave += 1
            self.start_wave()

    def update_bullets(self, dt):
        for bullet in self.bullets:
            old_x = bullet["x"]
            travel = bullet["dir"] * 900 * dt
            bullet["x"] = (old_x + travel) % WORLD_W
            bullet["life"] -= dt
            for lander in self.landers[:]:
                # Check the whole bullet path this frame so fast bullets cannot skip over landers.
                start_offset = wrap_delta(lander.x, old_x)
                end_offset = start_offset + travel
                crossed_lander = min(start_offset, end_offset) <= 16 and max(start_offset, end_offset) >= -16
                if crossed_lander and abs(bullet["y"] - lander.y) < 12:
                    self.shoot_lander(lander)
                    bullet["life"] = 0
                    break
        self.bullets = [b for b in self.bullets if b["life"] > 0]

    def screen_x(self, x):
        return VIEW_W / 2 + wrap_delta(self.player.x, x)

    def draw_radar(self, screen):
        pygame.draw.rect(screen, (10, 10, 30), (0, 0, VIEW_W, RADAR_H))
        pygame.draw.rect(screen, (90, 90, 140), (0, 0, VIEW_W, RADAR_H), 1)
        blips = [(h.x, h.y, (90, 230, 120)) for h in self.humanoids]
        blips += [(l.x, l.y, (255, 90, 90) if l.mutant else (230, 200, 60)) for l in self.landers]
        blips.append((self.player.x, self.player.y, (255, 255, 255)))
        for x, y, color in blips:
            rx = x / WORLD_W * VIEW_W
            ry = (y - PLAY_TOP) / (VIEW_H - PLAY_TOP) * (RADAR_H - 8) + 4
            pygame.draw.rect(screen, color, (rx - 2, ry - 2, 4, 4))

    def draw(self, screen):
        screen.fill(sky_color(self.wave) or (5, 5, 20))
        points = [(sx, ground_y(self.player.x + sx - VIEW_W / 2)) for sx in range(0, VIEW_W + 8, 8)]
        pygame.draw.polygon(screen, (110, 70, 40), points + [(VIEW_W, VIEW_H), (0, VIEW_H)])
        pygame.draw.lines(screen, (230, 150, 60), False, points, 2)
        for humanoid in self.humanoids:
            sx = self.screen_x(humanoid.x)
            if -20 < sx < VIEW_W + 20:
                pygame.draw.rect(screen, (90, 230, 120), (sx - 3, humanoid.y - 10, 6, 14))
        for lander in self.landers:
            sx = self.screen_x(lander.x)
            if -20 < sx < VIEW_W + 20:
                color = (255, 90, 90) if lander.mutant else (230, 200, 60)
                pygame.draw.ellipse(screen, color, (sx - 14, lander.y - 9, 28, 18))
        for bullet in self.bullets:
            sx = self.screen_x(bullet["x"])
            pygame.draw.line(screen, (255, 255, 200), (sx - 8, bullet["y"]), (sx + 8, bullet["y"]), 2)
        player = self.player
        if player.invulnerable <= 0 or int(player.invulnerable * 10) % 2 == 0:
            f, cx = player.facing, VIEW_W / 2
            pygame.draw.polygon(screen, (240, 240, 250), [(cx + f * 18, player.y), (cx - f * 14, player.y - 8), (cx - f * 14, player.y + 8)])
        for popup in self.popups:
            sx = self.screen_x(popup["x"])
            alpha = max(0, min(255, int(255 * popup["life"])))
            popup_surface = self.font.render("+500", True, (255, 240, 120))
            popup_surface.set_alpha(alpha)
            screen.blit(popup_surface, (sx - popup_surface.get_width() // 2, popup["y"]))
        self.draw_radar(screen)
        hud = self.font.render(f"Score {self.score}  Lives {self.lives}  Wave {self.wave}  Humanoids {len(self.humanoids)}", True, (240, 240, 240))
        screen.blit(hud, (10, RADAR_H + 4))
        if self.state == "lose":
            label = self.font.render("GAME OVER - Press R", True, (255, 255, 120))
            screen.blit(label, label.get_rect(center=(VIEW_W // 2, VIEW_H // 2)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((VIEW_W, VIEW_H))
    pygame.display.set_caption("Defender")
    clock = pygame.time.Clock()
    game = Game()
    running = True
    while running:
        dt = min(clock.tick(60) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()
        game.update(dt, pygame.key.get_pressed())
        game.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
