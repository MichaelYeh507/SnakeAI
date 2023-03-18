from game import * 
from agent import *

class TrainAIAgent:
    def __init__(self):
        self.agent = Agent()
        self.game = SnakeAI()


    def train(self):
        record = 0
        total_score = 0

        while True:
            state = self.agent.get_observation(self.game)
            action = self.agent.get_action(state)
            reward, done, score = self.game.play_step(action)
            next_state = self.agent.get_observation(self.game)

            #experience -> (state, action, reward, next_state, done)

            self.agent.learn_from_experience(state, action, reward, next_state, done)

            self.agent.store_to_memory(state, action, reward, next_state, done)

            if done:
                self.game.reset()
                self.agent.n_games +=1
                self.agent.experience_review()

                if score > record:
                    record = score
                    self.agent.model.save()

                total_score += score
                avg_score = total_score / self.agent.n_games
                print(f"Game {[self.agent.n_games]}: Score = {score}, Record = {record}, Avg score = {avg_score}")


if __name__ == '__main__':
    ta = TrainAIAgent()
    ta.train()