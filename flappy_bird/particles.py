import random
import pygame

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Random movement offsets
        self.vx = random.uniform(-0.6, 0.6)
        self.vy = random.uniform(2.0, 4.0)
        # Particle lifetime and initial size
        self.life = random.randint(220, 320)  # in ms
        self.size = random.randint(3, 6)

        # Flame colors
        self.color1 = (255, 240, 120)  # yellow
        self.color2 = (255, 140, 30)   # orange

    def update(self, dt):
        """Update particle position and shrink it over time."""
        self.x += self.vx
        self.y += self.vy
        self.life -= dt
        if self.size > 1:
            self.size -= 0.04 * (dt / 16.67)

    def dead(self):
        """Check if particle should be removed."""
        return self.life <= 0 or self.size <= 0.8

    def draw(self, screen):
        """Draw a glowing circle (flame effect)."""
        r1 = max(1, int(self.size))
        r2 = max(1, int(self.size * 0.6))
        pygame.draw.circle(screen, self.color1, (int(self.x), int(self.y)), r1)
        pygame.draw.circle(screen, self.color2, (int(self.x), int(self.y) + 1), r2)
