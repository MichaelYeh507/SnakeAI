import torch
import torch.nn as nn 

class ValueNetwork(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dim):
        super().__init__()
        #input: [1,11]
        self.lin1 = nn.Linear(input_dim, hidden_dim)
        self.lin2 = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        # return self.lin2(self.relu(self.lin1(x)))
        x = self.lin1(x)
        x = self.relu(x)
        x = self.lin2(x)
        
        return x


    def save(self, file_name='model.pth'):
        torch.save(self.state_dict(), file_name)