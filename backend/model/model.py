import torch
import torch.nn as nn

class WorldModel(nn.Module):
    def __init__(self, vocab_size=1000, embed_dim=32):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.net = nn.Sequential(
            nn.Linear(embed_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 6)
        )

    def forward(self, x):
        x = self.embedding(x)
        x = x.mean(dim=1)
        return self.net(x)