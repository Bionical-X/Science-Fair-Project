import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
#font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

#hazards
moving_blocks = []
move = False

#Walls
wall_positions = []



# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 40

class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        moving_blocks.clear()
        wall_positions.clear()


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        wallX = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        wallY = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        wall_positions.append(Point(wallX, wallY))
        if move:
            blockX = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
            blockY = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
            moving_blocks.append(movingBlock(blockX, blockY))

            
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        if self.food in moving_blocks:
            self._place_food()
        if self.food in wall_positions:
            self._place_food()


    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        for block in moving_blocks:
            block.move(self.w, self.h,self.snake)

        # 3. paint blocks
        
        # 3. check if game over
        reward = 0
        game_over = False
            
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        if pt in wall_positions:
            return True
        for block in moving_blocks:
            val = block.kill(self.snake)
            if val:
                return val
        

        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        for block in moving_blocks:
            block.paint(self.display)

        for wall in wall_positions:
            pygame.draw.rect(self.display, WHITE, pygame.Rect(wall[0],wall[1],BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)




class movingBlock:
        def __init__(self, positionX, positionY):
                self.active = True
                self.Ydirection = random.choice([-1,1])
                self.Xdirection = random.choice([-1,1])
                self.XPosition = positionX
                self.YPosition = positionY
        def move(self, width, height, snakeBody):
                self.XPosition += self.Xdirection*BLOCK_SIZE
                self.YPosition += self.Ydirection*BLOCK_SIZE
                if self.XPosition < 0 or self.XPosition > width-BLOCK_SIZE:
                        self.Xdirection *= -1
                if self.YPosition < 0 or self.YPosition > height-BLOCK_SIZE:
                        self.Ydirection *= -1
                if [self.XPosition, self.YPosition] in snakeBody:
                        self.Ydirection *= -1
                        self.YPosition += self.Ydirection*10
                        self.Xdirection *= -1
                        self.XPosition += self.Xdirection*10
        def kill(self, snake):
                if self.XPosition == snake[0][0] and self.YPosition == snake[0][1]:
                    return True
                return False
        def paint(self, display):
                pygame.draw.rect(display, WHITE, pygame.Rect(self.XPosition, self.YPosition, BLOCK_SIZE,BLOCK_SIZE))
                
        

