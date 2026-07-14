import torch.nn as nn
import torch

class BigMLP(nn.Module):
    def __init__(self, input_dim=162, output_dim=195):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 1024),
            nn.BatchNorm1d(1024),
            nn.GELU(),
            nn.Dropout(0.1),
            
            nn.Linear(1024, 1024),
            nn.BatchNorm1d(1024),
            nn.GELU(),
            nn.Dropout(0.1),
            
            nn.Linear(1024, 512),
            nn.BatchNorm1d(512),
            nn.GELU(),
            
            nn.Linear(512, output_dim)
        )
        
    def forward(self, x):
        # Returns logits (no VQ loss)
        return self.net(x), torch.tensor(0.0, device=x.device)