# model.py - Continuous ModuloNet (No VQ)

import torch
import torch.nn as nn

class TrainableFourierProjection(nn.Module):
    def __init__(self, in_features=1, latent_dim=512):
        super().__init__()
        self.proj = nn.Linear(in_features, latent_dim // 2)
        nn.init.normal_(self.proj.weight, mean=0.0, std=1.0)
        nn.init.constant_(self.proj.bias, 0.0)

    def forward(self, x):
        projected = self.proj(x)
        sin_features = torch.sin(projected)
        cos_features = torch.cos(projected)
        return torch.cat([sin_features, cos_features], dim=-1)


class TransformerBottleneckBlock(nn.Module):
    def __init__(self, latent_dim, num_heads=4, ff_dim=256, dropout=0.1):
        super().__init__()
        self.attention = nn.MultiheadAttention(
            embed_dim=latent_dim, 
            num_heads=num_heads, 
            batch_first=True
        )
        self.norm1 = nn.LayerNorm(latent_dim)
        self.norm2 = nn.LayerNorm(latent_dim)
        
        self.ff = nn.Sequential(
            nn.Linear(latent_dim, ff_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(ff_dim, latent_dim),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        attn_out, _ = self.attention(x, x, x)
        x = self.norm1(x + attn_out)
        ff_out = self.ff(x)
        x = self.norm2(x + ff_out)
        return x


class ModuloNetNoVQ(nn.Module):
    """
    3-Phase Architecture using a Continuous MLP Bottleneck instead of VQ
    """
    def __init__(self, in_features=1, latent_dim=512, num_heavy_blocks=2):
        super().__init__()
        # Phase 1: Periodic Encoder
        self.phase1_encoder = TrainableFourierProjection(in_features, latent_dim)
        
        # --- NEW: Learned Positional Embeddings ---
        # Vital so the Transformer knows which position is "Sex", "Year", "Palace", etc.
        self.pos_embedding = nn.Parameter(torch.zeros(1, 9, latent_dim))
        nn.init.normal_(self.pos_embedding, std=0.02)
        
        # Phase 2: Heavy Bottleneck Blocks
        self.phase2_blocks = nn.ModuleList([
            TransformerBottleneckBlock(latent_dim=latent_dim)
            for _ in range(num_heavy_blocks)
        ])
        
        # Phase 3: Simple MLP Bottleneck (Replacing VQ)
        self.phase3_mlp = nn.Sequential(
            nn.Linear(latent_dim, latent_dim),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(latent_dim, latent_dim)
        )

    def forward(self, x):
        # Phase 1: Projection + Positional Alignment
        x = self.phase1_encoder(x) + self.pos_embedding
        
        # Phase 2: Attention layers
        for block in self.phase2_blocks:
            x = block(x)
            
        # Phase 3: Continuous MLP Bottleneck
        continuous_latent = self.phase3_mlp(x)
        
        # Mimic VQ return values to maintain train.py compatibility
        dummy_vq_loss = torch.tensor(0.0, device=x.device)
        dummy_indices = None
        
        return continuous_latent, dummy_vq_loss, dummy_indices