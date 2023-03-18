import torch
from game import *
from model import *
from collections import deque
from learner import *

MAX_MEMORY = 100_000
BATCH_SIZE = 1000

class Agent:
    def __init__(self):
        self.n_games = 0
        self.model = ValueNetwork(11, 3,  256)
        self.learner = Learner(self.model, 0.001, 0.9)
        self.buffer = deque(maxlen=MAX_MEMORY)

    def get_observation(self, game):
        head = game.snake[0]

        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        obs = [
            (dir_r and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_d)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)),

            (dir_r and game.is_collision(point_d)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_u and game.is_collision(point_r)),

            (dir_r and game.is_collision(point_u)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_d)) or 
            (dir_d and game.is_collision(point_r)),

            dir_l,
            dir_r, 
            dir_u,
            dir_d,

            game.food.x < game.head.x,
            game.food.x > game.head.x,
            game.food.y < game.head.y,
            game.food.y > game.head.y

        ]

        return np.array(obs, dtype=int)


    def get_action(self, state):
        action = [0,0,0]
        self.e = 80 - self.n_games
        

        if random.randint(0, 200) < self.e:
            rand_idx = random.randint(0, 2)
            action[rand_idx] = 1
        else:
            state_tensor = torch.tensor(state).float()
            pred = self.model(state_tensor)
            model_decision_idx = torch.argmax(pred).item()
            action[model_decision_idx] = 1

        return action
        

    def learn_from_experience(self, state, action, reward, next_state, done):
        self.learner.train_step(state, action, reward, next_state, done)

    def store_to_memory(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def experience_review(self):
        if len(self.buffer) > BATCH_SIZE:
            mini_sample = random.sample(self.buffer, BATCH_SIZE)
        else:
            mini_sample = self.buffer
            

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.learner.train_step(states, actions, rewards, next_states, dones)