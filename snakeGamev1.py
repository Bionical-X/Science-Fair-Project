# importing libraries
import pygame
import time
import random
import math
from neuralNetwork import neuralNetwork
import numpy as np

snake_speed = 10

#size of the box
s = 38

# Window size 17x42 each dimension
window_x = 17*s
window_y = 17*s

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('GeeksforGeeks Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [6*s, 9*s]

# defining first 4 blocks of snake body
snake_body = [[6*s, 378],
			[5*s, 9*s],
			[4*s, 9*s],
			[3*s, 9*s]
			]
# fruit position
fruit_position = [random.randrange(1, (window_x//s)) * s,
				random.randrange(1, (window_y//s)) * s]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'

# initial score
score = 0
layerOneSize = 11
layerTwoSize = 6
layerThreeSize = 3

network = neuralNetwork(layerOneSize, layerTwoSize, layerThreeSize)
count = 0
"""
        Return the state.
        The state is a numpy array of 11 values, representing:
            - Danger  ahead
            - Danger  on the right
            - Danger on the left
            - Snake is moving up
            - Snake is moving down
            - Snake is moving left
            - Snake is moving right
            - The food is up
            - The food is down
            - The food is left
            - The food is right   
        """

state = np.zeros(11)

# displaying Score function
def show_score(choice, color, font, size):

	# creating font object score_font
	score_font = pygame.font.SysFont(font, size)
	
	# create the display surface object
	# score_surface
	score_surface = score_font.render('Score : ' + str(score), True, color)
	
	# create a rectangular object for the text
	# surface object
	score_rect = score_surface.get_rect()
	
	# displaying text
	game_window.blit(score_surface, score_rect)

# game over function
def game_over():
        time.sleep(2)
        snake_position = [6*s, 9*s]

        # defining first 4 blocks of snake body
        snake_body = [[6*s, 9*s],
                                [6*s, 9*s],
                                [6*s, 9*s],
                                [6*s, 9*s]
                                ]
        # fruit position
        fruit_position = [random.randrange(1, (window_x//s)) * s,
                                        random.randrange(1, (window_y//s)) * s]

        fruit_spawn = True

        # setting default snake direction towards
        # right
        direction = 'RIGHT'
        change_to = direction

        # initial score
        score = 0

# Main Function
while True:
        game = True
        if count % 100 == 0 and count >0:
                print("optimizing...")
                network.adjust()
                game = False
        reward = 0.0
        #Preparing state information to send to network
        state.fill(0)
        #Snake body ahead
        right = False
        left = False
        up = False
        down = False

        #danger from snake body around
        for block in snake_body[1:]:
                if snake_position[0]+s == block[0] and snake_position[1] == block[1]:
                        right = True
                if snake_position[0]-s == block[0] and snake_position[1] == block[1]:
                        left = True
                if snake_position[1] == block[0] and snake_position[1]-s == block[1]:
                        up = True
                if snake_position[1] == block[0] and snake_position[1]+s == block[1]:
                        down = True
                        
        #danger ahead
        if ((direction == 'UP' and (snake_position[1]-s < 0 or up)) or (direction ==
            'DOWN' and (snake_position[1]+s > window_y-10 or down)) or (direction ==
                'LEFT' and (snake_position[0]-s<0 or left)) or (direction ==
                        'RIGHT' and (snake_position[0]+s>window_x-10))):
                state[0] = 1

        #danger left
        if ((direction == 'UP' and (snake_position[0]-s < 0 or left)) or (direction ==
            'DOWN' and (snake_position[0]+s > window_x-10 or right)) or (direction ==
                'LEFT' and (snake_position[1]+s>window_y-10 or down)) or (direction ==
                        'RIGHT' and (snake_position[1]-s<0))):
                state[1] = 1

        #danger right
        if ((direction == 'UP' and (snake_position[0]+s < window_x-10 or right)) or (direction ==
            'DOWN' and (snake_position[0]-s <0 or left)) or (direction ==
                'LEFT' and (snake_position[1]-s>0 or up)) or (direction ==
                        'RIGHT' and (snake_position[1]+s>window_y-10))):
                state[2] = 1

        #moving up
        if direction == 'UP':
                state[3] = 1

        #moving down
        if direction == 'DOWN':
                state[4] = 1

        #moving left
        if direction == 'LEFT':
                state[5] = 1

        #moving right
        if direction == 'RIGHT':
                state[6] = 1

        #food up
        if snake_position[1] > fruit_position[1]:
                state[7] = 1

        #food down
        if snake_position[1] < fruit_position[1]:
                state[8] = 1

        #food left
        if snake_position[0] > fruit_position[0]:
                state[9] = 1

        #food right
        if snake_position[0] < fruit_position[0]:
                state[10] = 1

        #print(state)
        choice = network.choose(state)
                
        # If two keys pressed simultaneously
        # we don't want snake to move into two
        # directions simultaneously
        if choice == 1:
                if direction == 'UP':
                        direction = 'LEFT'
                elif direction == 'LEFT':
                        direction = 'DOWN'
                elif direction == 'DOWN':
                        direction = 'RIGHT'
                elif direction == 'RIGHT':
                        direction = 'UP'
        if choice == 2:
                if direction == 'UP':
                        direction = 'RIGHT'
                elif direction == 'LEFT':
                        direction = 'UP'
                elif direction == 'DOWN':
                        direction = 'LEFT'
                elif direction == 'RIGHT':
                        direction = 'DOWN'
                
                
        distance=-math.sqrt(math.pow(snake_position[0]-fruit_position[0],2)+math.pow(snake_position[1]-fruit_position[1],2))


        # Moving the snake
        if direction == 'UP':
                snake_position[1] -= s
        if direction == 'DOWN':
                snake_position[1] += s
        if direction == 'LEFT':
                snake_position[0] -= s
        if direction == 'RIGHT':
                snake_position[0] += s

        distance+=math.sqrt(math.pow(snake_position[0]-fruit_position[0],2)+math.pow(snake_position[1]-fruit_position[1],2))
        if distance<0:
                reward += 2.0
        else:
                reward -= 1.0
        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                score += 10
                fruit_spawn = False
                reward = 10.0
        else:
                snake_body.pop()
                        
        if not fruit_spawn:
                fruit_position = [random.randrange(1, (window_x//s)) * s,
                                                        random.randrange(1, (window_y//s)) * s]
                        
        fruit_spawn = True
        game_window.fill(black)
                

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > window_x-10:
                game = False
        elif snake_position[1] < 0 or snake_position[1] > window_y-10:
                game = False

        # Touching the snake body
        for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                        game = False
        if not game:
                time.sleep(2)
                snake_position = [6*s, 9*s]

                # defining first 4 blocks of snake body
                snake_body = [[6*s, 9*s],
                                        [6*s, 9*s],
                                        [6*s, 9*s],
                                        [6*s, 9*s]
                                        ]
                # fruit position
                fruit_position = [random.randrange(1, (window_x//s)) * s,
                                                random.randrange(1, (window_y//s)) * s]

                fruit_spawn = True

                # setting default snake direction towards
                # right
                direction = 'RIGHT'
                change_to = direction

                # initial score
                score = 0
                reward = -10.0
                
        network.remember(state, choice, reward)
        count += 1
                                
        for pos in snake_body:
                pygame.draw.rect(game_window, green,
                                                        pygame.Rect(pos[0], pos[1], s, s))
        pygame.draw.rect(game_window, white, pygame.Rect(
                fruit_position[0], fruit_position[1], s, s))

        # displaying score countinuously
        show_score(1, white, 'times new roman', 20)

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second /Refresh Rate
        fps.tick(snake_speed)

        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                                #deactivating pygame library
                                pygame.quit()
	
                                # quit the program
                                quit()
