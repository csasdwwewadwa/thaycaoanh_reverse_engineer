import torch.nn as nn
import torch

class BigMLP(nn.Module):
    def __init__(self, input_dim=162, output_dim=195):
        super().__init__()
        
        # 1. Prime frequencies for GPU projection
        frequencies = [2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 17.0, 19.0, 31.0]
        self.register_buffer("frequencies", torch.tensor(frequencies, dtype=torch.float32))

        self.net = nn.Sequential(
            nn.Linear(input_dim, 1024),
            nn.BatchNorm1d(1024),
            nn.GELU(),
            nn.Dropout(0.1),
            
            nn.Linear(1024, 1024),
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

    def _expand_features(self, x):
        x_unsqueezed = x.unsqueeze(-1)
        freqs = self.frequencies.unsqueeze(0).unsqueeze(0)
        scaled = x_unsqueezed * freqs
        sin_feats = torch.sin(scaled).flatten(start_dim=1)
        cos_feats = torch.cos(scaled).flatten(start_dim=1)
        return torch.cat([sin_feats, cos_feats], dim=-1)
        
    def forward(self, x):
        if x.shape[-1] == 9:
            x = self._expand_features(x)
        x = x.view(-1, 162)
        # Returns logits (no VQ loss)
        return self.net(x), torch.tensor(0.0, device=x.device)