import pygame
import random
from collections import namedtuple
import numpy as np

Point = namedtuple('Point', 'x, y')



class Direction:
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


GAME_TITLE = "SnakeAI"

BLACK = (0, 0, 0)
BLUE1 = (0, 0, 225)
BLUE2 = (0, 100, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

BLACK = (0, 0, 0)
SPEED = 20
BLOCK_SIZE = 20
INDENT = 4
IN_MANUAL_MODE = False

pygame.init()
font = pygame.font.Font(None, 25)

class SnakeAI:
    def __init__(self, width= 640, height=480):
        self.width = width
        self.height = height

        self.display = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption(GAME_TITLE)

        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = None if IN_MANUAL_MODE else Direction.RIGHT
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y), Point(self.head.x-2*BLOCK_SIZE, self.head.y)]
        self.place_food()
        self.score = 0
        self.frame_iteration = 0

    

    def place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y= random.randint(0, (self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.move(action)
        self.snake.insert(0, self.head)

        game_over = False
        reward = 0
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        if self.head == self.food:
            self.score +=1
            reward = 10
            self.place_food()
        else:
            self.snake.pop()

        self.update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    def manual_play(self):
        game_over = False
        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT:
                        self.direction = Direction.RIGHT
                    elif event.key == pygame.K_UP:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN:
                        self.direction = Direction.DOWN

            if self.direction is not None:
                self.move()
                self.snake.insert(0, self.head)

                if self.is_collision():
                    game_over = True
            
                if self.head == self.food:
                    self.score +=1
                    self.place_food()
                else:
                    self.snake.pop()

            #self.snake.pop()

            self.update_ui()
            self.clock.tick(SPEED)

    def is_collision(self, pt = None):
        if pt is None:
            pt = self.head
        if pt.x < 0 or pt.x > self.width - BLOCK_SIZE or pt.y < 0 or pt.y > self.height - BLOCK_SIZE:
            return True

        if pt in self.snake[1:]:
            return True

        return False

    def update_ui(self):
        
        self.display.fill(BLACK)
        # print(self.snake)
        for pt in self.snake:
            pygame.draw.rect(self.display, (BLUE1), pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))        
            pygame.draw.rect(self.display, (BLUE2), pygame.Rect(pt.x+INDENT, pt.y+INDENT, BLOCK_SIZE-2*INDENT, BLOCK_SIZE-2*INDENT))

        pygame.draw.rect(self.display, (RED), pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, (0,0))

        pygame.display.flip()


    def move(self, action = None):
        if action is not None:
            # [1, 0, 0] -> straight, [0, 1, 0] -> right, [0, 0, 1] -> left
            directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
            idx = directions.index(self.direction)

            if np.array_equal(action, [1, 0, 0]):
                new_dir = directions[idx]
            elif np.array_equal(action, [0, 1, 0]):
                new_dir = directions[(idx+1)%4]
            elif np.array_equal(action, [0, 0, 1]):
                new_dir = directions[idx-1]

            self.direction = new_dir

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x+= BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x-= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)



if __name__ == '__main__':
    IN_MANUAL_MODE = True
    game = SnakeAI()
    game.manual_play()