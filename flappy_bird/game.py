import pygame
import sys
from settings import WIDTH, HEIGHT, FPS, BG_COLOR, FG_COLOR, PIPE_WIDTH, PIPE_SPEED, PIPE_SPAWN_EVERY
from ironman import Bird
from pipe import PipePair

def main():
    pygame.init()
    pygame.display.set_caption("Flappy Iron Man")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 28)

    bird = Bird(100, HEIGHT // 2, image_path="assets/ironman.png", scale=0.9, offset_x=-8)
    pipes = []
    score = 0
    running = True
    game_over = False

    SPAWN_PIPE = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_PIPE, PIPE_SPAWN_EVERY)

    while running:
        dt = clock.tick(FPS)  # time since last frame in ms

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.flap()
                if event.type == SPAWN_PIPE:
                    pipes.append(PipePair(WIDTH + 20))
            else:
                # Restart on R key or mouse click
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    bird = Bird(100, HEIGHT // 2, image_path="assets/ironman.png", scale=0.7, offset_x=-8)
                    pipes.clear()
                    score = 0
                    game_over = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    bird = Bird(100, HEIGHT // 2, image_path="assets/ironman.png", scale=0.7, offset_x=-8)
                    pipes.clear()
                    score = 0
                    game_over = False

        # --- Update game state ---
        if not game_over:
            bird.update(dt)
            for p in pipes:
                p.update()
            pipes = [p for p in pipes if not p.offscreen()]

            # Score update
            for p in pipes:
                if not p.passed and p.x + PIPE_WIDTH < bird.x:
                    p.passed = True
                    score += 1

            # Collisions
            for p in pipes:
                if p.collides(bird.rect):
                    game_over = True
                    break
            if bird.y >= HEIGHT - bird.size / 2 or bird.y <= bird.size / 2:
                game_over = True

        # --- Draw ---
        screen.fill(BG_COLOR)

        # Simple scrolling background grid
        grid_spacing = 40
        t = pygame.time.get_ticks() * 0.001
        x_offset = int((t * PIPE_SPEED * 20) % grid_spacing)
        for gx in range(-x_offset, WIDTH, grid_spacing):
            pygame.draw.line(screen, (30, 30, 45), (gx, 0), (gx, HEIGHT), 1)

        for p in pipes:
            p.draw(screen)

        bird.draw(screen)

        # Draw score
        score_surf = font.render(f"{score}", True, FG_COLOR)
        screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 20))

        if game_over:
            over = font.render("GAME OVER - Press R to restart", True, FG_COLOR)
            screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 15))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
