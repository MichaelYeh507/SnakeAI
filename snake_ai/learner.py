import torch
import torch.nn as nn

class Learner:
    def __init__(self, model, lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr = self.lr)

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype = torch.float)
        action = torch.tensor(action, dtype = torch.long)
        reward = torch.tensor(reward, dtype = torch.long)
        next_state = torch.tensor(next_state, dtype = torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)

            done = (done,)

        pred = self.model(state)
        target = pred.clone()
        for idx in range(len(done)):
            if done[idx]:
                value = reward[idx]
            else:
                value = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))


            target[idx][torch.argmax(action[idx]).item()]=value

        self.optimizer.zero_grad()

        loss = ((pred - target)**2).mean()
        loss.backward()

        self.optimizer.step()
            

