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

class GameOverScreen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("game_over.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_DIMENSIONS[0] / 2, SCREEN_DIMENSIONS[1] / 2)
        self.opacity = 0
        self.image.set_alpha(self.opacity)
        self.counter = 0
        self.game_over_song = pygame.mixer.Sound("game_over.wav")
        pygame.mixer.Sound.play(self.game_over_song)
    
    def update(self):
        if self.counter < 15:
            self.counter += 1
            return
    
        if self.opacity < 255:
            self.opacity += 5
        else:
            self.opacity = 255
        self.image.set_alpha(self.opacity)

class Game(pygame.sprite.LayeredUpdates):

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
        for c in range(segment_count):
            self.grid_filled[int(i - c)][int(j)] = True

        self.add(self.body)
        self.add(snake_head)
 
        # Add apple
        self.apple = Apple(self.grid_filled)
        self.add(self.apple)

        # Add sounds
        self.eating_sound = pygame.mixer.Sound("apple_eating.wav")
        self.up_sound = pygame.mixer.Sound("up.wav")
        self.right_sound = pygame.mixer.Sound("right.wav")
        self.left_sound = pygame.mixer.Sound("left.wav")
        self.down_sound = pygame.mixer.Sound("down.wav")
        self.collision_sound = pygame.mixer.Sound("collision.wav")

        # Add vertical lines for grid
        vertical_lines = []
        for c in range(GRID_LINES[0] + 1):
            vertical_lines.append(Line(c, SQUARE_SIZE / 12, "vertical"))
        self.add(vertical_lines, layer = 1)

        # Add horizontal lines for grid
        horizontal_lines = []
        for c in range(GRID_LINES[1] + 1):
            horizontal_lines.append(Line(c, SQUARE_SIZE / 12, "horizontal"))
        self.add(horizontal_lines, layer = 1)

    # Moving the snake
    def update(self):
        self.counter += 1

        if self.alive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and (self.direction == "left" or self.direction == "right") and self.next_direction != "up":
                    self.next_direction = "up"
                    pygame.mixer.Sound.play(self.up_sound)
                if event.key == pygame.K_DOWN and (self.direction == "left" or self.direction == "right") and self.next_direction != "down":
                    self.next_direction = "down"
                    pygame.mixer.Sound.play(self.down_sound)
                if event.key == pygame.K_LEFT and (self.direction == "up" or self.direction == "down") and self.next_direction != "left":
                    self.next_direction = "left"
                    pygame.mixer.Sound.play(self.left_sound)
                if event.key == pygame.K_RIGHT and (self.direction == "up" or self.direction == "down") and self.next_direction != "right":
                    self.next_direction = "right"
                    pygame.mixer.Sound.play(self.right_sound)
            
            #### AI ####

            # if self.direction == "right" and self.head.i == GRID_LINES[0] - 1 or self.direction == "left" and self.head.j == GRID_LINES[1] - 2:
            #     self.next_direction = "up"
            #     pygame.mixer.Sound.play(self.up_sound)
            # elif self.head.i == 0 and self.head.j == 0 or self.direction == "left" and self.head.j == 0:
            #     self.next_direction = "down"
            #     pygame.mixer.Sound.play(self.down_sound)
            # elif self.head.i == GRID_LINES[0] - 1 and self.head.j == 0 or (self.direction == "down" or self.direction == "up") and self.head.i != 0 and self.head.i != GRID_LINES[0] - 1 and (self.head.j == GRID_LINES[1] - 2 or self.head.j == 0):
            #     self.next_direction = "left"
            #     pygame.mixer.Sound.play(self.left_sound)
            # elif self.head.i == 0 and self.head.j == GRID_LINES[1] - 1:
            #     self.next_direction = "right"
            #     pygame.mixer.Sound.play(self.right_sound)

            ############

            if self.counter < 12:
                return

            self.counter = 0

            if (self.head.i == 0 and self.next_direction == "left" 
            or self.head.i == GRID_LINES[0] - 1 and self.next_direction == "right" 
            or self.head.j == 0 and self.next_direction == "up" 
            or self.head.j == GRID_LINES[1] - 1 and self.next_direction == "down"
            or self.head.i != 0 and self.grid_filled[int(self.head.i) - 1][int(self.head.j)] == True and self.next_direction == "left" 
            or self.head.i != GRID_LINES[0] - 1 and self.grid_filled[int(self.head.i) + 1][int(self.head.j)] == True and self.next_direction == "right" 
            or self.head.j != 0 and self.grid_filled[int(self.head.i)][int(self.head.j) - 1] == True and self.next_direction == "up" 
            or self.head.j != GRID_LINES[1] - 1 and self.grid_filled[int(self.head.i)][int(self.head.j) + 1] == True and self.next_direction == "down"):

                pygame.mixer.Sound.play(self.collision_sound)
                self.alive = False
                # Move grid to bottom layer
                grid_sprite_list = self.remove_sprites_of_layer(1)
                for sprite in grid_sprite_list:
                    self.add(sprite)
                self.game_over = GameOverScreen()
                self.add(self.game_over)

            else:
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
                    pygame.mixer.Sound.play(self.eating_sound)
                    new_segment = SnakeSegment(new_segment_i, new_segment_j)
                    self.body.append(new_segment)
                    self.add(new_segment)
                    self.apple.spawn(self.grid_filled)
        else:
            self.game_over.update()

# Snake definition
class SnakeHead(pygame.sprite.Sprite):

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

# Add snake
x = (GRID_LINES[0] + 1) // 2.5
y = (GRID_LINES[1] + 1) / 2
game = Game(x, y)


bg_surface = pygame.Surface(SCREEN_DIMENSIONS)
pygame.draw.rect(bg_surface, "#17181f", pygame.Rect(0, 0, SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1]))
pygame.draw.rect(bg_surface, "#9d9fb3", pygame.Rect(DIST_TO_GRID[0], DIST_TO_GRID[1], GRID_DIMENSIONS[0], GRID_DIMENSIONS[1]))

screen.blit(bg_surface, (0, 0))

running = True
counter = 0

while running:
    counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.update()

    game.clear(screen, bgd=bg_surface)
    game.draw(screen, bg_surface)
    pygame.display.update()

    clock.tick(60)

pygame.quit()