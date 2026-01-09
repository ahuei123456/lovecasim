"""
PyTorch implementation of AlphaZero network.
Supports GPU acceleration and batch processing.
"""

from typing import Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class ResBlock(nn.Module):
    """
    Residual Block using Linear layers (ResMLP style).
    Suitable for non-spatial inputs like our feature vector.
    """
    def __init__(self, size: int):
        super().__init__()
        self.fc1 = nn.Linear(size, size)
        self.bn1 = nn.BatchNorm1d(size)
        self.fc2 = nn.Linear(size, size)
        self.bn2 = nn.BatchNorm1d(size)
        
    def forward(self, x):
        residual = x
        out = F.relu(self.bn1(self.fc1(x)))
        out = self.bn2(self.fc2(out))
        out += residual
        out = F.relu(out)
        return out

class AlphaZeroNet(nn.Module):
    def __init__(self, input_size: int, action_size: int, hidden_size: int = 256, num_res_blocks: int = 5):
        super().__init__()
        
        # Input processing
        self.start_fc = nn.Linear(input_size, hidden_size)
        self.start_bn = nn.BatchNorm1d(hidden_size)
        
        # Residual Tower
        self.res_blocks = nn.ModuleList([
            ResBlock(hidden_size) for _ in range(num_res_blocks)
        ])
        
        # Policy Head
        self.policy_fc = nn.Linear(hidden_size, action_size)
        
        # Value Head
        self.value_fc1 = nn.Linear(hidden_size, 64)
        self.value_fc2 = nn.Linear(64, 1)
        
    def forward(self, x):
        # x shape: (batch_size, input_size)
        x = F.relu(self.start_bn(self.start_fc(x)))
        
        for block in self.res_blocks:
            x = block(x)
            
        # Policy
        p_logits = self.policy_fc(x)
        p = F.softmax(p_logits, dim=1)
        
        # Value
        v = F.relu(self.value_fc1(x))
        v = torch.tanh(self.value_fc2(v))
        
        return p, v

class TorchNetworkWrapper:
    """Wrapper to interface with the MCTS/Training loop"""
    def __init__(self, config, device=None):
        self.config = config
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        self.net = AlphaZeroNet(
            input_size=config.input_size,
            action_size=config.action_size,
            hidden_size=config.hidden_size,
            num_res_blocks=config.num_hidden_layers
        ).to(self.device)
        
        self.optimizer = optim.Adam(self.net.parameters(), lr=config.learning_rate, weight_decay=config.l2_reg)
        
    def predict(self, state) -> Tuple[np.ndarray, float]:
        """Inference for a single state (used in MCTS)"""
        self.net.eval()
        obs = state.get_observation()
        # Add batch dim
        x = torch.tensor(obs, dtype=torch.float32).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            p, v = self.net(x)
            
        p = p.cpu().numpy()[0]
        v = v.item()
        
        # Mask illegal
        legal = state.get_legal_actions()
        masked_policy = p * legal
        if masked_policy.sum() > 0:
            masked_policy /= masked_policy.sum()
        else:
            masked_policy = legal.astype(np.float32)
            masked_policy /= masked_policy.sum()
            
        return masked_policy, v

    def train_step(self, observations, target_policies, target_values) -> Tuple[float, float, float]:
        """Batched training step"""
        self.net.train()
        
        # Convert to tensor
        obs = torch.tensor(observations, dtype=torch.float32).to(self.device)
        targets_p = torch.tensor(target_policies, dtype=torch.float32).to(self.device)
        targets_v = torch.tensor(target_values, dtype=torch.float32).to(self.device).view(-1, 1)
        
        self.optimizer.zero_grad()
        
        pred_p, pred_v = self.net(obs)
        
        # Policy Loss (Cross Entropy)
        # Add epsilon to log to prevent nan
        loss_p = -torch.sum(targets_p * torch.log(pred_p + 1e-8)) / obs.size(0)
        
        # Value Loss (MSE)
        loss_v = F.mse_loss(pred_v, targets_v)
        
        total_loss = loss_p + loss_v
        
        total_loss.backward()
        self.optimizer.step()
        
        return total_loss.item(), loss_p.item(), loss_v.item()

    def save(self, path: str):
        torch.save(self.net.state_dict(), path)
        
    def load(self, path: str):
        self.net.load_state_dict(torch.load(path, map_location=self.device))
