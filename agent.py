import torch
import random
import numpy as np
from collections import deque
from snakeGame import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001 #Learning rate
BLOCK_SIZE = 20
SPEED = 1000
N = int(640/BLOCK_SIZE*480/BLOCK_SIZE)
N = 0
class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness
        #gamma has to be value smaller than 1.0
        self.gamma = 0.8# discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(N+11,625,3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        
        # model, trainer

    def get_state(self, game):
        head = game.snake[0]
        #20 is for BLockSIze, yes this is hard coded
        point_l = Point(head.x-BLOCK_SIZE, head.y)
        point_r = Point(head.x+BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)

        
        #point_l2 = Point(head.x-40, head.y)
        #point_r2 = Point(head.x+40, head.y)
        #point_u2 = Point(head.x, head.y - 40)
        #point_d2 = Point(head.x, head.y + 40)

        #point_l3 = Point(head.x-60, head.y)
        #point_r3 = Point(head.x+60, head.y)
        #point_u3 = Point(head.x, head.y - 60)
        #point_d3 = Point(head.x, head.y + 60)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [False]*(int(N+11))
        # I am hard coding this for now probs fix later
        if N>0:
            for i in range(int(480/BLOCK_SIZE)):
                for j in range(int(640/BLOCK_SIZE)):
                    state[int(640/BLOCK_SIZE*i+j)] = game.is_collision(Point(480/BLOCK_SIZE*j,640/BLOCK_SIZE*i))
            
        # Danger straight
        state[N] = ((dir_r and game.is_collision(point_r)) or
        (dir_l and game.is_collision(point_l)) or
        (dir_u and game.is_collision(point_u)) or
        (dir_d and game.is_collision(point_d)))

        # Danger right
        state[N+1] = ((dir_u and game.is_collision(point_r)) or 
        (dir_d and game.is_collision(point_l)) or 
        (dir_l and game.is_collision(point_u)) or 
        (dir_r and game.is_collision(point_d)))

        # Danger left
        state[N+2] = ((dir_d and game.is_collision(point_r)) or 
        (dir_u and game.is_collision(point_l)) or 
        (dir_r and game.is_collision(point_u)) or 
        (dir_l and game.is_collision(point_d)))

        # Danger straight
        
        #(dir_r and game.is_collision(point_r2)) or
        #(dir_l and game.is_collision(point_l2)) or
        #(dir_u and game.is_collision(point_u2)) or
        #(dir_d and game.is_collision(point_d2)),

        # Danger right
        #(dir_u and game.is_collision(point_r2)) or 
        #(dir_d and game.is_collision(point_l2)) or 
        #(dir_l and game.is_collision(point_u2)) or 
        #(dir_r and game.is_collision(point_d2)),

        # Danger left
        #(dir_d and game.is_collision(point_r2)) or 
        #(dir_u and game.is_collision(point_l2)) or 
        #(dir_r and game.is_collision(point_u2)) or 
        #(dir_l and game.is_collision(point_d2)),


        #Move direction
        state[N+3] = (dir_l)
        state[N+4] = (dir_r)
        state[N+5] = (dir_u)
        state[N+6] = (dir_d)

        #food location
        state[N+7] = game.food.x < game.head.x #food left
        state[N+8] = game.food.x > game.head.x # food right
        state[N+9] = game.food.y < game.head.y # food up
        state[N+10] = game.food.y > game.head.y #food down


        """
        #Ratio of possible spaces forward
        if dir_l:
            t = -BLOCK_SIZE
        elif dir_r:
            t = BLOCK_SIZE
        elif dir_u:
            t = -BLOCK_SIZE
        else:
            t = BLOCK_SIZE
        if dir_l or dir_r:
            queue = [Point(game.head.x+t,game.head.y)]
        else:
            queue = [Point(game.head.x, game.head.y+t)]

        safe = []
        visited = [game.head]

        while len(queue)!=0:
            if (not game.is_collision(queue[0])):
                safe.append(1)
    
                if  visited.count(Point(queue[0].x,queue[0].y+BLOCK_SIZE))==0:
                    queue.append(Point(queue[0].x,queue[0].y+BLOCK_SIZE))
                    visited.append(Point(queue[0].x,queue[0].y+BLOCK_SIZE))

                if visited.count(Point(queue[0].x+BLOCK_SIZE,queue[0].y))==0:
                    queue.append(Point(queue[0].x+BLOCK_SIZE,queue[0].y))
                    visited.append(Point(queue[0].x+BLOCK_SIZE,queue[0].y))

                if visited.count(Point(queue[0].x,queue[0].y-BLOCK_SIZE))==0:
                    queue.append(Point(queue[0].x,queue[0].y-BLOCK_SIZE))
                    visited.append(Point(queue[0].x,queue[0].y-BLOCK_SIZE))

                if visited.count(Point(queue[0].x-BLOCK_SIZE,queue[0].y))==0:
                    queue.append(Point(queue[0].x-BLOCK_SIZE,queue[0].y))
                    visited.append(Point(queue[0].x-BLOCK_SIZE,queue[0].y))
                
            queue.pop(0)
        state[N+11] = len(safe)/24/32

        #Ratio of possible spaces Left
        if dir_l:
            t = BLOCK_SIZE
        elif dir_r:
            t = -BLOCK_SIZE
        elif dir_u:
            t = -BLOCK_SIZE
        else:
            t = BLOCK_SIZE
        if dir_l or dir_r:
            queue = [Point(game.head.x ,game.head.y+t)]
        else:
            queue = [Point(game.head.x+t, game.head.y)]

        safe = []
        visited = [game.head]

        while len(queue)!=0:
            if not (game.is_collision(queue[0])):
                safe.append(1)
    
                if  visited.count(Point(queue[0].x,queue[0].y+BLOCK_SIZE))==0:
                    queue.append(Point(queue[0].x,queue[0].y+BLOCK_SIZE))
                    visited.append(Point(queue[0].x,queue[0].y+BLOCK_SIZE))

                if visited.count(Point(queue[0].x+BLOCK_SIZE,queue[0].y))==0:
                    queue.append(Point(queue[0].x+BLOCK_SIZE,queue[0].y))
                    visited.append(Point(queue[0].x+BLOCK_SIZE,queue[0].y))

                if visited.count(Point(queue[0].x,queue[0].y-BLOCK_SIZE))==0:
                    queue.append(Point(queue[0].x,queue[0].y-BLOCK_SIZE))
                    visited.append(Point(queue[0].x,queue[0].y-BLOCK_SIZE))

                if visited.count(Point(queue[0].x-BLOCK_SIZE,queue[0].y))==0:
                    queue.append(Point(queue[0].x-BLOCK_SIZE,queue[0].y))
                    visited.append(Point(queue[0].x-BLOCK_SIZE,queue[0].y))
                
            queue.pop(0)
        state[N+12] = len(safe)/24/32

        #Ratio of possible spaces Right
        if dir_l:
            t = -BLOCK_SIZE
        elif dir_r:
            t = BLOCK_SIZE
        elif dir_u:
            t = BLOCK_SIZE
        else:
            t = -BLOCK_SIZE
        if dir_l or dir_r:
            queue = [Point(game.head.x ,game.head.y+t)]
        else:
            queue = [Point(game.head.x+t, game.head.y)]

        safe = []
        visited = [game.head]

        while len(queue)!=0:
            if not (game.is_collision(queue[0])):
                safe.append(1)
    
                if  visited.count(Point(queue[0].x,queue[0].y+BLOCK_SIZE))==0:
                    queue.append(Point(queue[0].x,queue[0].y+BLOCK_SIZE))
                    visited.append(Point(queue[0].x,queue[0].y+BLOCK_SIZE))

                if visited.count(Point(queue[0].x+BLOCK_SIZE,queue[0].y))==0:
                    queue.append(Point(queue[0].x+BLOCK_SIZE,queue[0].y))
                    visited.append(Point(queue[0].x+BLOCK_SIZE,queue[0].y))

                if visited.count(Point(queue[0].x,queue[0].y-BLOCK_SIZE))==0:
                    queue.append(Point(queue[0].x,queue[0].y-BLOCK_SIZE))
                    visited.append(Point(queue[0].x,queue[0].y-BLOCK_SIZE))

                if visited.count(Point(queue[0].x-BLOCK_SIZE,queue[0].y))==0:
                    queue.append(Point(queue[0].x-BLOCK_SIZE,queue[0].y))
                    visited.append(Point(queue[0].x-BLOCK_SIZE,queue[0].y))
                
            queue.pop(0)
        state[N+13] = len(safe)/24/32
        """

        state = np.array(state, dtype=int)
        return state




    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) #list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)
   

    def get_action(self,state):
        #random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    highest_score = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        #get old state
        state_old = agent.get_state(game)

        #get move
        final_move = agent.get_action(state_old)

        #perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        #remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            #Train long memeory, plot results
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > highest_score:
                highest_score = score
                agent.model.save()
            print("Game", agent.n_games, "Score", score, "Record", highest_score)

            #Plot
            plot_scores.append(score)
            total_score += score
            mean_score = total_score/agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
        

if __name__ == '__main__':
    train()
