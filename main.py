import pygame
import random

GRID_LINES = (12, 11)
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

    def __init__(self, i, j):
        super().__init__()
        self.counter = 0
        self.alive = True
        self.direction = "right"
        self.next_direction = self.direction
        snake_head = SnakeHead(i, j)
        segment_count = 3
        self.body = [SnakeSegment(i - count - 1, j) for count in range(segment_count)]
        self.head = snake_head
        self.grid_filled = [[False for _ in range(GRID_LINES[1])] for _ in range(GRID_LINES[0])]
        for i in range(segment_count):
            self.grid_filled[int(i - i)][int(j)] = True

        self.add(self.body)
        self.add(snake_head)

        # Add apple
        self.apple = Apple(self.grid_filled)
        self.add(self.apple)

    # Moving the snake
    def update(self):
        self.counter += 1

        if self.alive:
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
                return True

            self.counter = 0

            if (self.head.i == 0 and self.next_direction == "left" 
            or self.head.i == GRID_LINES[0] - 1 and self.next_direction == "right" 
            or self.head.j == 0 and self.next_direction == "up" 
            or self.head.j == GRID_LINES[1] - 1 and self.next_direction == "down"):
                self.alive = False
                return self.alive

            self.direction = self.next_direction

            last_segment = self.body.pop()
            new_segment_i = last_segment.i()
            new_segment_j = last_segment.j()
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

            self.grid_filled[int(self.head.i)][int(self.head.j)] = True
            self.grid_filled[int(new_segment_i)][int(new_segment_j)] = False

            if self.head.i == self.apple.i and self.head.j == self.apple.j:
                self.apple.spawn(self.grid_filled)
                new_segment = SnakeSegment(new_segment_i, new_segment_j)
                self.body.append(new_segment)
                self.add(new_segment)
        
        return self.alive

# Snake definition
class SnakeHead(pygame.sprite.Sprite):

    # Draw the snake
    def __init__(self, i, j):
        super().__init__()
        self.i = i
        self.j = j
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.image, "#525680", pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (i * SQUARE_SIZE + DIST_TO_GRID[0] + SQUARE_SIZE / 2, j * SQUARE_SIZE + DIST_TO_GRID[1] + SQUARE_SIZE / 2)

    def move_by(self, i, j):
        self.i += i
        self.j += j
        self.rect.center = (self.i * SQUARE_SIZE + DIST_TO_GRID[0] + SQUARE_SIZE / 2, self.j * SQUARE_SIZE + DIST_TO_GRID[1] + SQUARE_SIZE / 2)

class SnakeSegment(pygame.sprite.Sprite):

    # Draw the snake
    def __init__(self, i, j):
        super().__init__()
        self.counter = 0
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.image, "#525680", pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (i * SQUARE_SIZE + DIST_TO_GRID[0] + SQUARE_SIZE / 2, j * SQUARE_SIZE + DIST_TO_GRID[1] + SQUARE_SIZE / 2)

    def i(self):
        return (self.rect.x - DIST_TO_GRID[0]) / SQUARE_SIZE

    def j(self):
        return (self.rect.y - DIST_TO_GRID[1]) / SQUARE_SIZE

class Apple(pygame.sprite.Sprite):

    def __init__(self, grid_filled):
        super().__init__()
        self.spawn(grid_filled)

    def spawn(self, grid_filled):
        available_squares = []
        for i in range(GRID_LINES[0]):
           for j in range(GRID_LINES[1]):
               if grid_filled[i][j] == False:
                   available_squares.append([i, j])
        self.apple_location = random.randint(0, len(available_squares) - 1)
        i = available_squares[self.apple_location][0]
        j = available_squares[self.apple_location][1]
        self.i = i
        self.j = j
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(self.image, "#b53c42", pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (i * SQUARE_SIZE + DIST_TO_GRID[0] + SQUARE_SIZE / 2, j * SQUARE_SIZE + DIST_TO_GRID[1] + SQUARE_SIZE / 2)

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
    vertical_lines.append(Line(i, SQUARE_SIZE / 12, "vertical"))
grid_sprites.add(vertical_lines)

# Add horizontal lines for grid
horizontal_lines = []
for i in range(GRID_LINES[1] + 1):
    horizontal_lines.append(Line(i, SQUARE_SIZE / 12, "horizontal"))
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

    if game.update() == False:
        print("Game over")

    game.clear(screen, bgd=bg_surface)
    game.draw(screen, bg_surface)
    grid_sprites.draw(screen)
    pygame.display.update()

    clock.tick(60)

pygame.quit()