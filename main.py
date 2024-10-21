import pygame

GRID_LINES = (15, 15)
SQUARE_SIZE = 30
GRID_DIMENSIONS = (GRID_LINES[0] * SQUARE_SIZE, GRID_LINES[1] * SQUARE_SIZE)
SCREEN_DIMENSIONS = (GRID_DIMENSIONS[0] + 800, GRID_DIMENSIONS[1] + 400)
DIST_TO_GRID = ((SCREEN_DIMENSIONS[0] - GRID_DIMENSIONS[0]) / 2, (SCREEN_DIMENSIONS[1] - GRID_DIMENSIONS[1]) / 2)

# How to draw the lines for the grid
class Line(pygame.sprite.Sprite):
    def __init__(self, position, thickness, direction):
        super().__init__()
        if direction == "horizontal":
            self.image = pygame.Surface((GRID_DIMENSIONS[0], thickness))
            pygame.draw.rect(self.image, "#222421", pygame.Rect(0, 0, GRID_DIMENSIONS[0], thickness))
        elif direction == "vertical":
            self.image = pygame.Surface((thickness, GRID_DIMENSIONS[1]))
            pygame.draw.rect(self.image, "#222421", pygame.Rect(0, 0, thickness, GRID_DIMENSIONS[1]))
        else:
            Exception("YOU CAN'T DO THAT!")

        self.rect = self.image.get_rect()
        if direction == "horizontal":
            self.rect.center = (SCREEN_DIMENSIONS[0] / 2, position * SQUARE_SIZE + DIST_TO_GRID[1])
        elif direction == "vertical":
            self.rect.center = (position * SQUARE_SIZE + DIST_TO_GRID[0], SCREEN_DIMENSIONS[1] / 2)

# Snake definition
class SnakeHead(pygame.sprite.Sprite):
    
    # Draw the snake
    def __init__(self, x, y):
        super().__init__()
        self.counter = 0
        self.direction = "right"
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.image, "#666b94", pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x * SQUARE_SIZE + DIST_TO_GRID[0] - SQUARE_SIZE / 2, y * SQUARE_SIZE + DIST_TO_GRID[1] - SQUARE_SIZE / 2)

    # Moving the snake
    def update(self):
        self.counter += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and (self.direction == "left" or self.direction == "right"):
                self.direction = "up"
            if event.key == pygame.K_DOWN and (self.direction == "left" or self.direction == "right"):
                self.direction = "down"
            if event.key == pygame.K_LEFT and (self.direction == "up" or self.direction == "down"):
                self.direction = "left"
            if event.key == pygame.K_RIGHT and (self.direction == "up" or self.direction == "down"):
                self.direction = "right"

        if self.counter < 20:
            return
        
        self.counter = 0
        if self.direction == "up":
            self.rect.y -= SQUARE_SIZE
        if self.direction == "down":
            self.rect.y += SQUARE_SIZE 
        if self.direction == "left":
            self.rect.x -= SQUARE_SIZE
        if self.direction == "right":
            self.rect.x += SQUARE_SIZE

class SnakeSegment(pygame.sprite.Sprite):
    
    # Draw the snake
    def __init__(self, x, y):
        super().__init__()
        self.counter = 0
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.image, "#446b94", pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x * SQUARE_SIZE + DIST_TO_GRID[0] - SQUARE_SIZE / 2, y * SQUARE_SIZE + DIST_TO_GRID[1] - SQUARE_SIZE / 2)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")
grid_sprites = pygame.sprite.RenderPlain()

# Add snake
snake = pygame.sprite.RenderUpdates()
x = (GRID_LINES[0] + 1) // 2.5
y = (GRID_LINES[1] + 1) / 2
snake_head = SnakeHead(x, y)
snake.add(snake_head)

# Add vertical lines for grid
vertical_lines = []
for i in range(GRID_LINES[0] + 1):
    vertical_lines.append(Line(i, SQUARE_SIZE / 8, "vertical"))
grid_sprites.add(vertical_lines)

# Add horizontal lines for grid
horizontal_lines = []
for i in range(GRID_LINES[1] + 1):
    horizontal_lines.append(Line(i, SQUARE_SIZE / 8, "horizontal"))
grid_sprites.add(horizontal_lines)

bg_surface = pygame.Surface(SCREEN_DIMENSIONS)
pygame.draw.rect(bg_surface, "#222421", pygame.Rect(0, 0, SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]))
pygame.draw.rect(bg_surface, "#9cb087", pygame.Rect(DIST_TO_GRID[0], DIST_TO_GRID[1], GRID_DIMENSIONS[0], GRID_DIMENSIONS[1]))
pygame.draw.circle(bg_surface, "#34cc23", (SCREEN_DIMENSIONS[0] / 2, SCREEN_DIMENSIONS[1] / 2), GRID_DIMENSIONS[0] / 2, width = 0)
screen.blit(bg_surface, (0, 0))

grid_sprites.draw(screen)

running = True
counter = 0

while running:
    counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    snake.update()

    snake.clear(screen, bgd=bg_surface)
    snake.draw(screen, bg_surface)
    grid_sprites.draw(screen)
    pygame.display.update()

    clock.tick(60)

pygame.quit()