import torch
import torch.nn as nn
from vector_quantize_pytorch import FSQ

class HierarchicalFSQNet(nn.Module):
    def __init__(self, input_dim=162, output_dim=195):
        super().__init__()
        
        # 1. Prime frequencies for GPU projection
        frequencies = [2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 17.0, 19.0, 31.0]
        self.register_buffer("frequencies", torch.tensor(frequencies, dtype=torch.float32))
        
        # 2. Expanded FSQ Config: 6 dimensions, 5 levels each (5^6 = 15,625 code capacity)
        fsq_levels = [5, 5, 5, 5, 5, 5] 
        fsq_dim = len(fsq_levels) # 6
        
        # Block 1
        self.mlp1 = nn.Sequential(
            nn.Linear(162, 512),
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

    def _expand_features(self, x):
        x_unsqueezed = x.unsqueeze(-1)
        freqs = self.frequencies.unsqueeze(0).unsqueeze(0)
        scaled = x_unsqueezed * freqs
        sin_feats = torch.sin(scaled).flatten(start_dim=1)
        cos_feats = torch.cos(scaled).flatten(start_dim=1)
        return torch.cat([sin_feats, cos_feats], dim=-1)

    def _quantize_stage(self, x, fsq_block):
        x_seq = x.unsqueeze(1)
        quantized_seq, _ = fsq_block(x_seq)
        return quantized_seq.squeeze(1)

    def forward(self, x):
        if x.shape[-1] == 9:
            x = self._expand_features(x)
        x = x.view(-1, 162)
        
        # Stage 1 + Residual Bypass
        h1 = self.mlp1(x)
        x_quant1 = self._quantize_stage(h1, self.fsq1) + h1 # <-- Residual Connection
        
        # Stage 2 + Residual Bypass
        h2 = self.mlp2(x_quant1)
        x_quant2 = self._quantize_stage(h2, self.fsq2) + h2 # <-- Residual Connection
        
        # Stage 3 + Residual Bypass
        h3 = self.mlp3(x_quant2)
        x_quant3 = self._quantize_stage(h3, self.fsq3) + h3 # <-- Residual Connection
        
        # Output
        logits = self.mlp_out(x_quant3)
        return logits, torch.tensor(0.0, device=x.device)