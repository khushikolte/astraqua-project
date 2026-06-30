import torch
import torch.nn as nn


class ScenarioModel(nn.Module):
    def __init__(
        self,
        input_dim=32,
        hidden=64,
        output_dim=8,
    ):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),

            nn.Linear(hidden, hidden),
            nn.ReLU(),

            nn.Linear(hidden, output_dim),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.net(x)