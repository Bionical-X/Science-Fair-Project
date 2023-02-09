# importing libraries
import pygame
import time
import random
import math

snake_speed = 15

# Window size
window_x = 720
window_y = 480

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
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			]
# fruit position
fruit_position = [random.randrange(1, (window_x//10)) * 10,
				random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0
layerOneSize = 10
layerTwoSize = 6
layerThreeSize = 4

#network = neuralNetwork(10, 6, 4)
count = 0
#state is {snake right of fruit, snake above fruit, wall to right, wall to left, wall up, wall down, body right, body left, body up, body down}
state = [None]*10

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
        snake_position = [100, 50]

        # defining first 4 blocks of snake body
        snake_body = [[100, 50],
                                [90, 50],
                                [80, 50],
                                [70, 50]
                                ]
        # fruit position
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                                        random.randrange(1, (window_y//10)) * 10]

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
        if count % 50 == 0 and count >0:
                print("optimizing...")
                #network.optimize()
        else:
                reward = 0
                #Preparing state information to send to network
                if snake_position[0] > fruit_position[0]:
                        state[0] = 1
                else:
                        state[0] = 0
                if snake_position[1] > fruit_position[1]:
                        state[1] = 1
                else:
                        state[1] = 0
                if snake_position[0]+10 > window_x-10:
                        state[2] = 1
                else:
                        state[2] = 0
                if snake_position[0]-10 < 0:
                        state[3] = 1
                else:
                        state[3] = 0
                if snake_position[1]+10 > window_y-10:
                        state[4] = 1
                else:
                        state[4] = 0
                if snake_position[1]-10 < 0:
                        state[5] = 0
                else:
                        state[5] = 1
                state[6] = 0
                state[7]=0
                state[8]=0
                state[9]=0
                for block in snake_body[1:]:
                        if snake_position[0]+10 == block[0] and snake_position[1] == block[1]:
                                state[6] = 1
                        if snake_position[0]-10 == block[0] and snake_position[1] == block[1]:
                                state[7] = 1
                        if snake_position[0] == block[0] and snake_position[1]+10 == block[1]:
                                state[8] = 1
                        if snake_position[0] == block[0] and snake_position[1]-10 == block[1]:
                                state[9] = 1

                distance = -math.sqrt(math.pow(snake_position[0]-fruit_position[0],2) + math.pow(snake_position[1] - fruit_position[1],2))
                #choice = network.choose(state, direction)
                #change_to = choice
                
                # If two keys pressed simultaneously
                # we don't want snake to move into two
                # directions simultaneously
                if change_to == 'UP' and direction != 'DOWN':
                        direction = 'UP'
                if change_to == 'DOWN' and direction != 'UP':
                        direction = 'DOWN'
                if change_to == 'LEFT' and direction != 'RIGHT':
                        direction = 'LEFT'
                if change_to == 'RIGHT' and direction != 'LEFT':
                        direction = 'RIGHT'


                # Moving the snake
                if direction == 'UP':
                        snake_position[1] -= 10
                if direction == 'DOWN':
                        snake_position[1] += 10
                if direction == 'LEFT':
                        snake_position[0] -= 10
                if direction == 'RIGHT':
                        snake_position[0] += 10

                distance += math.sqrt(math.pow(snake_position[0]-fruit_position[0],2) + math.pow(snake_position[1] - fruit_position[1],2))
                if distance<0:
                        reward = 1
                else:
                        reward = -1
                #network.adjust(state, choice, reward)
                # Snake body growing mechanism
                # if fruits and snakes collide then scores
                # will be incremented by 10
                snake_body.insert(0, list(snake_position))
                if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                        score += 10
                        fruit_spawn = False
                else:
                        snake_body.pop()
                        
                if not fruit_spawn:
                        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                                                        random.randrange(1, (window_y//10)) * 10]
                        
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
                        snake_position = [100, 50]

                        # defining first 4 blocks of snake body
                        snake_body = [[100, 50],
                                                [90, 50],
                                                [80, 50],
                                                [70, 50]
                                                ]
                        # fruit position
                        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                                                        random.randrange(1, (window_y//10)) * 10]

                        fruit_spawn = True

                        # setting default snake direction towards
                        # right
                        direction = 'RIGHT'
                        change_to = direction

                        # initial score
                        score = 0

                                
                for pos in snake_body:
                        pygame.draw.rect(game_window, green,
                                                        pygame.Rect(pos[0], pos[1], 10, 10))
                pygame.draw.rect(game_window, white, pygame.Rect(
                        fruit_position[0], fruit_position[1], 10, 10))

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
