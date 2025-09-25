# bird.py
# Iron Man class (player), handles movement, sprite, and hand thruster flames

import pygame
import random
from settings import WIDTH, HEIGHT, GRAVITY, JUMP_STRENGTH
from particles import Particle

class Bird:
    def __init__(self, x, y, image_path="assets/ironman.png", scale=0.9, offset_x=0, offset_y=0):
        self.x = x
        self.y = y
        self.vy = 0
        self.offset_x = offset_x
        self.offset_y = offset_y

        # Load Iron Man image (fallback to a red circle if missing)
        try:
            img = pygame.image.load(image_path).convert_alpha()
        except Exception:
            img = pygame.Surface((96, 96), pygame.SRCALPHA)
            pygame.draw.circle(img, (200, 40, 40), (48, 48), 46)

        # Uniform scale based on height
        w, h = img.get_size()
        target_h = int(96 * scale)  # base target height for the sprite
        factor = target_h / h
        img = pygame.transform.smoothscale(img, (int(w * factor), int(h * factor)))
        self.sprite = img

        sw, sh = self.sprite.get_size()
        self.size = max(sw, sh)  # rough square hitbox size
        self._hitbox = pygame.Rect(0, 0, self.size, self.size)

        # -------------------------------
        # Hand thrusters (emit points)
        # -------------------------------
        # These ratios are relative to the sprite center. Tune if your image differs.
        # dx is horizontal offset; dy is vertical offset (positive = down).
        # Try tweaking HAND_DX and HAND_DY to align exactly with your image's palms.
        HAND_DX_RATIO = 0.15   # how far from center to the left/right (0.20 ~ 20% of width)
        HAND_DY_RATIO = -0.05  # slightly above center; increase if palms are higher (negative = up)

        hand_dx = int(sw * HAND_DX_RATIO)
        hand_dy = int(sh * HAND_DY_RATIO)

        # Two emitters: left hand and right hand
        self.emit_points = [
            (-hand_dx, hand_dy),  # left hand
            ( hand_dx, hand_dy),  # right hand
        ]

        # Particles list and emission timer
        self.particles = []
        self.emit_ms_left = 0  # how long to keep emitting after a flap (in ms)

        # Optional: set this True to visualize emit points (debug)
        self.debug_emit_points = False

    @property
    def rect(self):
        """Collision hitbox (square around the sprite)."""
        self._hitbox.center = (int(self.x), int(self.y))
        return self._hitbox

    def flap(self):
        """Jump upwards and start short flame emission from hands."""
        self.vy = JUMP_STRENGTH
        self.emit_ms_left = 180  # emit flames for ~0.18s after pressing SPACE

    def update(self, dt):
        """Apply gravity, clamp within screen, and update particles."""
        self.vy += GRAVITY
        self.y += self.vy

        # Keep within vertical bounds
        if self.y > HEIGHT - self.size / 2:
            self.y = HEIGHT - self.size / 2
            self.vy = 0
        if self.y < self.size / 2:
            self.y = self.size / 2
            self.vy = 0

        # Emit particles from both hands while timer is active
        if self.emit_ms_left > 0:
            self.emit_ms_left -= dt
            # 1–2 particles per hand per frame for a soft stream
            for _ in range(random.randint(1, 2)):
                for dx, dy in self.emit_points:
                    self.particles.append(Particle(self.x + dx, self.y + dy))

        # Update and prune particles
        for pr in self.particles:
            pr.update(dt)
        self.particles = [p for p in self.particles if not p.dead()]

    def draw(self, screen):
        """Draw flames first (behind), then the sprite."""
        for p in self.particles:
            p.draw(screen)

        rect = self.sprite.get_rect(center=(int(self.x) + self.offset_x, int(self.y) + self.offset_y))
        screen.blit(self.sprite, rect)

        # Debug: visualize hand emit points
        if self.debug_emit_points:
            for dx, dy in self.emit_points:
                cx, cy = int(self.x + dx), int(self.y + dy)
                pygame.draw.circle(screen, (255, 0, 0), (cx, cy), 3)
