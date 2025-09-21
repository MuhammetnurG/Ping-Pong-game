import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()

# Font for score display
font = pygame.font.SysFont("Arial", 32)


# Game objects
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 7
        self.score = 0

    def move(self, direction):
        if direction == "up" and self.rect.top > 0:
            self.rect.y -= self.speed
        if direction == "down" and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.dx = random.choice([-4, 4])
        self.dy = random.choice([-4, 4])
        self.base_speed = 4
        self.speed_increase = 0.25

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def reset(self):
        self.rect.x = WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = HEIGHT // 2 - BALL_SIZE // 2
        self.dx = random.choice([-4, 4])
        self.dy = random.choice([-4, 4])

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


def main():
    # Create game objects
    left_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Paddle movement
        keys = pygame.key.get_pressed()

        # Left paddle (W/S keys)
        if keys[pygame.K_w]:
            left_paddle.move("up")
        if keys[pygame.K_s]:
            left_paddle.move("down")

        # Right paddle (Up/Down arrow keys)
        if keys[pygame.K_UP]:
            right_paddle.move("up")
        if keys[pygame.K_DOWN]:
            right_paddle.move("down")

        # Ball movement
        ball.move()

        # Ball collision with top and bottom
        if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
            ball.dy = -ball.dy

        # Ball collision with paddles
        if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
            ball.dx = -ball.dx
            # Increase ball speed slightly on each hit
            if ball.dx > 0:
                ball.dx += ball.speed_increase
            else:
                ball.dx -= ball.speed_increase
            if ball.dy > 0:
                ball.dy += ball.speed_increase / 2
            else:
                ball.dy -= ball.speed_increase / 2

        # Score points
        if ball.rect.left <= 0:
            right_paddle.score += 1
            ball.reset()
        if ball.rect.right >= WIDTH:
            left_paddle.score += 1
            ball.reset()

        # Draw everything
        screen.fill(BLACK)

        # Draw center line
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

        # Draw paddles and ball
        left_paddle.draw()
        right_paddle.draw()
        ball.draw()

        # Draw scores
        left_score_text = font.render(str(left_paddle.score), True, WHITE)
        right_score_text = font.render(str(right_paddle.score), True, WHITE)
        screen.blit(left_score_text, (WIDTH // 4, 20))
        screen.blit(right_score_text, (3 * WIDTH // 4, 20))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()