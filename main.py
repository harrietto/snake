import pygame

GRID_DIMENSIONS = (15, 15)
SQUARE_SIZE = 30
SCREEN_DIMENSIONS = (GRID_DIMENSIONS[0] * SQUARE_SIZE + 800, GRID_DIMENSIONS[1] * SQUARE_SIZE + 400)

# How to draw the lines for the grid
class Line(pygame.sprite.Sprite):
    def __init__(self, position, thickness, direction):
        super().__init__()
        if direction == "horizontal":
            self.image = pygame.Surface((GRID_DIMENSIONS[0] * SQUARE_SIZE, thickness))
            pygame.draw.rect(self.image, "white", pygame.Rect(0, 0, GRID_DIMENSIONS[0] * SQUARE_SIZE, thickness))
        elif direction == "vertical":
            self.image = pygame.Surface((thickness, GRID_DIMENSIONS[1] * SQUARE_SIZE))
            pygame.draw.rect(self.image, "white", pygame.Rect(0, 0, thickness, GRID_DIMENSIONS[1] * SQUARE_SIZE))
        else:
            Exception("YOU CAN'T DO THAT!")

        self.rect = self.image.get_rect()
        if direction == "horizontal":
            self.rect.center = (SCREEN_DIMENSIONS[0] / 2, position * SQUARE_SIZE + ((SCREEN_DIMENSIONS[1] - GRID_DIMENSIONS[1] * SQUARE_SIZE) / 2))
        elif direction == "vertical":
            self.rect.center = (position * SQUARE_SIZE + ((SCREEN_DIMENSIONS[0] - GRID_DIMENSIONS[0] * SQUARE_SIZE) / 2), SCREEN_DIMENSIONS[1] / 2)

# Snake definition
class Snake(pygame.sprite.Sprite):
    
    # Draw the snake
    def __init__(self):
        super().__init__()
        self.x = (GRID_DIMENSIONS[0] + 1) / 4
        self.y = (GRID_DIMENSIONS[1] + 1) / 2
        self.direction = "right"
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.image, "green", pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = ((self.x * SQUARE_SIZE + (SCREEN_DIMENSIONS[0] - GRID_DIMENSIONS[0] * SQUARE_SIZE) / 2) - SQUARE_SIZE / 2, (self.y * SQUARE_SIZE + (SCREEN_DIMENSIONS[1] - GRID_DIMENSIONS[1] * SQUARE_SIZE) / 2) - SQUARE_SIZE / 2)

    # Moving the snake
    def update(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and (self.direction == "left" or self.direction == "right"):
                self.direction = "up"
            if event.key == pygame.K_DOWN and (self.direction == "left" or self.direction == "right"):
                self.direction = "down"
            if event.key == pygame.K_LEFT and (self.direction == "up" or self.direction == "down"):
                self.direction = "left"
            if event.key == pygame.K_RIGHT and (self.direction == "up" or self.direction == "down"):
                self.direction = "right"

        if self.direction == "up":
            self.rect.y -= SQUARE_SIZE
        if self.direction == "down":
            self.rect.y += SQUARE_SIZE 
        if self.direction == "left":
            self.rect.x -= SQUARE_SIZE
        if self.direction == "right":
            self.rect.x += SQUARE_SIZE

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")
all_sprites = pygame.sprite.Group()

# Add vertical lines for grid
verticalLines = []
for i in range(GRID_DIMENSIONS[0] + 1):
    verticalLines.append(Line(i, 2, "vertical"))
all_sprites.add(verticalLines)

# Add horizontal lines for grid
horizontalLines = []
for i in range(GRID_DIMENSIONS[1] + 1):
    horizontalLines.append(Line(i, 2, "horizontal"))
all_sprites.add(horizontalLines)

# Add snake
snake = Snake()
all_sprites.add(snake)

# Run Pygame event loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
  
    screen.fill("black")

    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(6)

pygame.quit()