import torch
import torch.nn as nn
import torch.nn.functional as F

class VectorQuantizerBlock(nn.Module):
    """
    A single differentiable Lookup Table (VQ Layer).
    Maps continuous latent states to the closest discrete codebook vector.
    """
    def __init__(self, num_embeddings=64, embedding_dim=128, commitment_cost=0.25):
        super(VectorQuantizerBlock, self).__init__()
        self.embedding_dim = embedding_dim
        self.num_embeddings = num_embeddings
        self.commitment_cost = commitment_cost
        
        self.codebook = nn.Embedding(self.num_embeddings, self.embedding_dim)
        self.codebook.weight.data.uniform_(-1/num_embeddings, 1/num_embeddings)

    def forward(self, x):
        # Calculate Euclidean distances: (a - b)^2 = a^2 - 2ab + b^2
        distances = (torch.sum(x**2, dim=1, keepdim=True) 
                     - 2 * torch.matmul(x, self.codebook.weight.t())
                     + torch.sum(self.codebook.weight**2, dim=1))
        
        encoding_indices = torch.argmin(distances, dim=1)
        quantized = self.codebook(encoding_indices)
        
        # VQ Losses
        q_loss = F.mse_loss(quantized, x.detach())
        e_loss = F.mse_loss(quantized.detach(), x)
        vq_loss = q_loss + self.commitment_cost * e_loss
        
        # Straight-Through Estimator Trick
        quantized = x + (quantized - x).detach()
        
        return quantized, vq_loss


class SineVQModuloNet(nn.Module):
    def __init__(self, output_dim=195, latent_dim=128, num_codes=64):
        super(SineVQModuloNet, self).__init__()
        
        # 9 inputs * (9 frequencies * 2 [sine + cosine]) = 162 features precomputed by train.py
        input_feature_dim = 162
        
        self.input_projection = nn.Sequential(
            nn.Linear(input_feature_dim, latent_dim),
            nn.GELU()
        )
        
        # 3 successive Vector Quantization layers to mimic nested lookup tables
        self.vq1 = VectorQuantizerBlock(num_embeddings=num_codes, embedding_dim=latent_dim)
        self.vq2 = VectorQuantizerBlock(num_embeddings=num_codes, embedding_dim=latent_dim)
        self.vq3 = VectorQuantizerBlock(num_embeddings=num_codes, embedding_dim=latent_dim)
        
        self.transit1 = nn.Sequential(nn.Linear(latent_dim, latent_dim), nn.GELU())
        self.transit2 = nn.Sequential(nn.Linear(latent_dim, latent_dim), nn.GELU())
        
        self.output_layer = nn.Linear(latent_dim, output_dim)

    def forward(self, x):
        # x is already the 162-dimensional preprocessed periodic feature tensor
        latent = self.input_projection(x)
        
        # Run through the VQ blocks (Differentiable Lookups)
        latent, vq_loss1 = self.vq1(latent)
        latent = self.transit1(latent)
        
        latent, vq_loss2 = self.vq2(latent)
        latent = self.transit2(latent)
        
        latent, vq_loss3 = self.vq3(latent)
        
        total_vq_loss = vq_loss1 + vq_loss2 + vq_loss3
        logits = self.output_layer(latent)
        
        return logits, total_vq_loss