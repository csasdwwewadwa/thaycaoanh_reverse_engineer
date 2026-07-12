import torch
import torch.nn as nn
import torch.nn.functional as F

class VectorQuantizerBlock(nn.Module):
    def __init__(self, num_embeddings=256, embedding_dim=128, commitment_cost=0.25):
        super(VectorQuantizerBlock, self).__init__()
        self.embedding_dim = embedding_dim
        self.num_embeddings = num_embeddings
        self.commitment_cost = commitment_cost
        
        self.codebook = nn.Embedding(self.num_embeddings, self.embedding_dim)
        self.codebook.weight.data.normal_(0, 1.0 / embedding_dim)

    def forward(self, x):
        # L2-normalize inputs and codebook weights.
        # This converts the distance check into a cosine-similarity check, 
        # guaranteeing that distances stay bounded between 0 and 4.
        x_norm = F.normalize(x, p=2, dim=1)
        codebook_norm = F.normalize(self.codebook.weight, p=2, dim=1)
        
        # Calculate Euclidean distances on normalized vectors
        distances = (torch.sum(x_norm**2, dim=1, keepdim=True) 
                     - 2 * torch.matmul(x_norm, codebook_norm.t())
                     + torch.sum(codebook_norm**2, dim=1))
        
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
    def __init__(self, output_dim=195, latent_dim=128, num_codes=256):
        super(SineVQModuloNet, self).__init__()
        
        input_feature_dim = 162
        
        self.input_projection = nn.Sequential(
            nn.Linear(input_feature_dim, latent_dim),
            nn.GELU()
        )
        
        self.ln1 = nn.LayerNorm(latent_dim)
        self.vq1 = VectorQuantizerBlock(num_embeddings=num_codes, embedding_dim=latent_dim)
        self.transit1 = nn.Sequential(nn.Linear(latent_dim, latent_dim), nn.GELU())
        
        self.ln2 = nn.LayerNorm(latent_dim)
        self.vq2 = VectorQuantizerBlock(num_embeddings=num_codes, embedding_dim=latent_dim)
        self.transit2 = nn.Sequential(nn.Linear(latent_dim, latent_dim), nn.GELU())
        
        self.ln3 = nn.LayerNorm(latent_dim)
        self.vq3 = VectorQuantizerBlock(num_embeddings=num_codes, embedding_dim=latent_dim)
        
        self.output_layer = nn.Linear(latent_dim, output_dim)

    def forward(self, x):
        latent = self.input_projection(x)
        
        ln_1 = self.ln1(latent)
        quantized1, vq_loss1 = self.vq1(ln_1)
        latent = latent + self.transit1(quantized1)
        
        ln_2 = self.ln2(latent)
        quantized2, vq_loss2 = self.vq2(ln_2)
        latent = latent + self.transit2(quantized2)
        
        ln_3 = self.ln3(latent)
        quantized3, vq_loss3 = self.vq3(ln_3)
        # Final block can directly feed the output layer via a skip connection
        final_latent = latent + quantized3
        
        total_vq_loss = vq_loss1 + vq_loss2 + vq_loss3
        logits = self.output_layer(final_latent)
        
        return logits, total_vq_loss