import pygame
import random
from settings import HEIGHT, PIPE_GAP, PIPE_WIDTH, PIPE_COLOR, PIPE_SPEED

class PipePair:
    def __init__(self, x):
        self.x = x
        self.passed = False #indicates whether the player has already passed this pair of pipes.
        # Random vertical position for the gap
        gap_center = random.randint(120, HEIGHT - 120)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, gap_center - PIPE_GAP // 2)
        self.bot_rect = pygame.Rect(self.x, gap_center + PIPE_GAP // 2, PIPE_WIDTH, HEIGHT - (gap_center + PIPE_GAP // 2))

    def update(self):
        """Move pipes to the left."""
        self.x -= PIPE_SPEED
        self.top_rect.x = int(self.x)
        self.bot_rect.x = int(self.x)

    def offscreen(self):
        """Check if pipes moved off the screen."""
        return self.x + PIPE_WIDTH < 0

    def draw(self, screen):
        """Draw top and bottom pipes."""
        pygame.draw.rect(screen, PIPE_COLOR, self.top_rect, border_radius=6)
        pygame.draw.rect(screen, PIPE_COLOR, self.bot_rect, border_radius=6)

    def collides(self, bird_rect):
        """Collision check with player."""
        return self.top_rect.colliderect(bird_rect) or self.bot_rect.colliderect(bird_rect)
