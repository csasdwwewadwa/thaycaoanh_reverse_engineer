import torch
import torch.nn as nn
from vector_quantize_pytorch import FSQ

class HierarchicalFSQNet(nn.Module):
    def __init__(self, input_dim=162, output_dim=195):
        super().__init__()
        
        # We project to a 5-dimensional grid with 5 levels per dimension. 
        # Total possible codes per FSQ stage = 5^5 = 3,125 discrete points.
        fsq_levels = [5, 5, 5, 5, 5] 
        fsq_dim = len(fsq_levels) # 5
        
        # Block 1
        self.mlp1 = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.GELU(),
            nn.Linear(512, fsq_dim)
        )
        self.fsq1 = FSQ(levels=fsq_levels)
        
        # Block 2
        self.mlp2 = nn.Sequential(
            nn.Linear(fsq_dim, 512),
            nn.GELU(),
            nn.Linear(512, fsq_dim)
        )
        self.fsq2 = FSQ(levels=fsq_levels)
        
        # Block 3
        self.mlp3 = nn.Sequential(
            nn.Linear(fsq_dim, 512),
            nn.GELU(),
            nn.Linear(512, fsq_dim)
        )
        self.fsq3 = FSQ(levels=fsq_levels)
        
        # Final Output MLP
        self.mlp_out = nn.Sequential(
            nn.Linear(fsq_dim, 1024),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(1024, output_dim)
        )

    def forward(self, x):
        # Stage 1
        x = self.mlp1(x)
        x_quant1, _ = self.fsq1(x)
        
        # Stage 2
        x = self.mlp2(x_quant1)
        x_quant2, _ = self.fsq2(x)
        
        # Stage 3
        x = self.mlp3(x_quant2)
        x_quant3, _ = self.fsq3(x)
        
        # Output
        logits = self.mlp_out(x_quant3)
        
        # Return dummy 0.0 for VQ loss to seamlessly fit into your existing training pipeline!
        return logits, torch.tensor(0.0, device=x.device)