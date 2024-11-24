import pygame
import random

GRID_LINES = (16, 15)
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
            pygame.draw.rect(self.image, "#c9c9d1", pygame.Rect(0, 0, GRID_DIMENSIONS[0], thickness))
        elif direction == "vertical":
            self.image = pygame.Surface((thickness, GRID_DIMENSIONS[1]))
            pygame.draw.rect(self.image, "#c9c9d1", pygame.Rect(0, 0, thickness, GRID_DIMENSIONS[1]))
        else:
            Exception("YOU CAN'T DO THAT!")

        self.rect = self.image.get_rect()
        if direction == "horizontal":
            self.rect.center = (SCREEN_DIMENSIONS[0] / 2, position * SQUARE_SIZE + DIST_TO_GRID[1])
        elif direction == "vertical":
            self.rect.center = (position * SQUARE_SIZE + DIST_TO_GRID[0], SCREEN_DIMENSIONS[1] / 2)

class Game(pygame.sprite.RenderUpdates):

    def __init__(self, x, y):
        super().__init__()
        self.counter = 0
        self.direction = "right"
        self.next_direction = self.direction
        snake_head = SnakeHead(x, y)
        segment_count = 10
        self.body = [SnakeSegment(x - count - 1, y) for count in range(segment_count)]
        self.head = snake_head
        self.grid_filled = [[False for _ in range(GRID_LINES[1])] for _ in range(GRID_LINES[0])]
        self.grid_filled[int(x)][int(y)] = True
        self.grid_filled[int(x - 1)][int(y)] = True
        self.grid_filled[int(x - 2)][int(y)] = True
        self.grid_filled[int(x - 3)][int(y)] = True

        self.add(self.body)
        self.add(snake_head)

        # Add apple
        self.apple = Apple(self.grid_filled)
        self.add(self.apple)

    # Moving the snake
    def update(self):
        self.counter += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and (self.direction == "left" or self.direction == "right"):
                self.next_direction = "up"
            if event.key == pygame.K_DOWN and (self.direction == "left" or self.direction == "right"):
                self.next_direction = "down"
            if event.key == pygame.K_LEFT and (self.direction == "up" or self.direction == "down"):
                self.next_direction = "left"
            if event.key == pygame.K_RIGHT and (self.direction == "up" or self.direction == "down"):
                self.next_direction = "right"

        if self.counter < 12:
            return
        
        self.counter = 0

        self.direction = self.next_direction

        last_segment = self.body.pop()
        last_segment.rect.x = self.head.rect.x
        last_segment.rect.y = self.head.rect.y
        self.body.insert(0, last_segment)

        if self.direction == "up":
            self.head.move_by(0, -1)
        if self.direction == "down":
            self.head.move_by(0, 1)
        if self.direction == "left":
            self.head.move_by(-1, 0)
        if self.direction == "right":
            self.head.move_by(1, 0)

        if self.head.grid_x == self.apple.grid_x and self.head.grid_y == self.apple.grid_y:
            self.apple.spawn(self.grid_filled)

# Snake definition
class SnakeHead(pygame.sprite.Sprite):
    
    # Draw the snake
    def __init__(self, x, y):
        super().__init__()
        self.grid_x = x
        self.grid_y = y
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.image, "#525680", pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x * SQUARE_SIZE + DIST_TO_GRID[0] - SQUARE_SIZE / 2, y * SQUARE_SIZE + DIST_TO_GRID[1] - SQUARE_SIZE / 2)

    def move_by(self, i, j):
        self.grid_x += i
        self.grid_y += j
        self.rect.center = (self.grid_x * SQUARE_SIZE + DIST_TO_GRID[0] - SQUARE_SIZE / 2, self.grid_y * SQUARE_SIZE + DIST_TO_GRID[1] - SQUARE_SIZE / 2)

class SnakeSegment(pygame.sprite.Sprite):
    
    # Draw the snake
    def __init__(self, x, y):
        super().__init__()
        self.counter = 0
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.image, "#525680", pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x * SQUARE_SIZE + DIST_TO_GRID[0] - SQUARE_SIZE / 2, y * SQUARE_SIZE + DIST_TO_GRID[1] - SQUARE_SIZE / 2)

class Apple(pygame.sprite.Sprite):

    def __init__(self, grid_filled):
        super().__init__()
        self.spawn(grid_filled)

    def spawn(self, grid_filled):
        available_squares = []
        for x in range(GRID_LINES[0]):
           for y in range(GRID_LINES[1]):
               if grid_filled[x][y] == False:
                   available_squares.append([x + 1, y + 1])
        self.apple_location = random.randint(0, len(available_squares) - 1)
        x = available_squares[self.apple_location][0]
        y = available_squares[self.apple_location][1]
        self.grid_x = x
        self.grid_y = y
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.image, "#b53c42", pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x * SQUARE_SIZE + DIST_TO_GRID[0] - SQUARE_SIZE / 2, y * SQUARE_SIZE + DIST_TO_GRID[1] - SQUARE_SIZE / 2)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")
grid_sprites = pygame.sprite.RenderPlain()

# Add snake
x = (GRID_LINES[0] + 1) // 2.5
y = (GRID_LINES[1] + 1) / 2
game = Game(x, y)

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
pygame.draw.rect(bg_surface, "#17181f", pygame.Rect(0, 0, SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]))
pygame.draw.rect(bg_surface, "#9d9fb3", pygame.Rect(DIST_TO_GRID[0], DIST_TO_GRID[1], GRID_DIMENSIONS[0], GRID_DIMENSIONS[1]))
screen.blit(bg_surface, (0, 0))

grid_sprites.draw(screen)

running = True
counter = 0

while running:
    counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    game.update()
    #apple.update()

    game.clear(screen, bgd=bg_surface)
    game.draw(screen, bg_surface)
    #apple_draw.draw(screen, bg_surface)
    grid_sprites.draw(screen)
    pygame.display.update()

    clock.tick(60)

pygame.quit()