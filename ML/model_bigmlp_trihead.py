import torch
import torch.nn as nn

# major
CAT1_INDICES = [
    15, 20, 21, 35, 44, 54, 67, 77, 92, 102, 103, 110, 118, 129, 
    131, 135, 136, 139, 141, 142, 144, 145, 147, 148, 150, 152, 
    153, 157, 158, 159, 161, 162, 163, 164, 166, 167, 170, 171, 
    172, 173, 174, 175, 177, 178, 179, 180, 181, 182, 183, 184, 
    185, 186, 187, 188, 189, 190
    ]

# transit
CAT2_INDICES = [
    5, 6, 7, 8, 13, 42, 53, 60, 61, 65, 75, 76, 83, 88, 122, 128
    ]

# aux
CAT3_INDICES = [
    0, 1, 2, 3, 4, 9, 10, 11, 12, 14, 16, 17, 18, 19, 22, 23, 24, 
    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 
    41, 43, 45, 46, 47, 48, 49, 50, 51, 52, 55, 56, 57, 58, 59, 
    62, 63, 64, 66, 68, 69, 70, 71, 72, 73, 74, 78, 79, 80, 81, 
    82, 84, 85, 86, 87, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 
    100, 101, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 
    115, 116, 117, 119, 120, 121, 123, 124, 125, 126, 127, 130, 
    132, 133, 134, 137, 138, 140, 143, 146, 149, 151, 154, 155, 
    156, 160, 165, 168, 169, 176, 191, 192, 193, 194
    ]


class TriHeadBigMLP(nn.Module):
    def __init__(self, input_dim=162, output_dim=195):
        super().__init__()
        
        # 1. Prime frequencies for GPU projection
        frequencies = [2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 17.0, 19.0, 31.0]
        self.register_buffer("frequencies", torch.tensor(frequencies, dtype=torch.float32))

        # 2. Register index tracking vectors as buffers
        # Reading directly from the hardcoded module constants above
        self.register_buffer("cat1_idx", torch.tensor(CAT1_INDICES, dtype=torch.long))
        self.register_buffer("cat2_idx", torch.tensor(CAT2_INDICES, dtype=torch.long))
        self.register_buffer("cat3_idx", torch.tensor(CAT3_INDICES, dtype=torch.long))

        # Safety assertions to make sure you didn't accidentally miscount the items
        assert len(self.cat1_idx) == 56, f"Expected Cat 1 size to be 56, got {len(self.cat1_idx)}"
        assert len(self.cat2_idx) == 16, f"Expected Cat 2 size to be 16, got {len(self.cat2_idx)}"
        assert len(self.cat3_idx) == 123, f"Expected Cat 3 size to be 123, got {len(self.cat3_idx)}"

        # 3. Shared representation network
        self.shared_net = nn.Sequential(
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
            nn.GELU()
        )
        
        # 4. Independent multi-category mapping heads
        self.head_cat1 = nn.Linear(512, 56)
        self.head_cat2 = nn.Linear(512, 16)
        self.head_cat3 = nn.Linear(512, 123)

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
        
        # Continuous feature routing
        features = self.shared_net(x)
        
        # Compute category logits completely independently
        logits1 = self.head_cat1(features)
        logits2 = self.head_cat2(features)
        logits3 = self.head_cat3(features)
        
        # Instantiate empty vector matching dataset dimensions (Batch, 195)
        out_logits = torch.zeros(x.size(0), 195, device=x.device)
        
        # Re-order the elements into the layout expected by the loss calculator
        out_logits[:, self.cat1_idx] = logits1
        out_logits[:, self.cat2_idx] = logits2
        out_logits[:, self.cat3_idx] = logits3
        
        return out_logits, torch.tensor(0.0, device=x.device)
    

if __name__ == "__main__":
    combined = CAT1_INDICES + CAT2_INDICES + CAT3_INDICES
    assert sorted(combined) == list(range(195)), "Indices are either missing values or overlapping!"
    print("All index rules verified perfectly!")