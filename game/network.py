"""
Neural Network for AlphaZero-style training.

This module provides a simple neural network architecture for policy and value
prediction. For a production system, you would use a more sophisticated
architecture (e.g., ResNet with attention) and train on GPU with PyTorch/TensorFlow.
"""

import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class NetworkConfig:
    """Configuration for the neural network"""
    input_size: int = 60  # Size of observation vector
    hidden_size: int = 256
    num_hidden_layers: int = 3
    action_size: int = 200  # Size of action space
    learning_rate: float = 0.001
    l2_reg: float = 0.0001


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(0, x)


def softmax(x: np.ndarray) -> np.ndarray:
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum()


def tanh(x: np.ndarray) -> np.ndarray:
    return np.tanh(x)


class SimpleNetwork:
    """
    Simple feedforward neural network for policy and value prediction.
    
    Architecture:
    - Input layer (observation)
    - Hidden layers with ReLU
    - Policy head (softmax over actions)
    - Value head (tanh for [-1, 1])
    """
    
    def __init__(self, config: NetworkConfig = None):
        self.config = config or NetworkConfig()
        self._init_weights()
        
    def _init_weights(self) -> None:
        """Initialize weights using He initialization"""
        config = self.config
        
        # Shared layers
        self.hidden_weights = []
        self.hidden_biases = []
        
        in_size = config.input_size
        for _ in range(config.num_hidden_layers):
            std = np.sqrt(2.0 / in_size)
            w = np.random.randn(in_size, config.hidden_size) * std
            b = np.zeros(config.hidden_size)
            self.hidden_weights.append(w)
            self.hidden_biases.append(b)
            in_size = config.hidden_size
        
        # Policy head
        std = np.sqrt(2.0 / config.hidden_size)
        self.policy_weight = np.random.randn(config.hidden_size, config.action_size) * std
        self.policy_bias = np.zeros(config.action_size)
        
        # Value head
        self.value_weight = np.random.randn(config.hidden_size, 1) * std
        self.value_bias = np.zeros(1)
        
    def forward(self, observation: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Forward pass.
        
        Args:
            observation: Input features
            
        Returns:
            (policy probabilities, value)
        """
        # Store activations for backward pass
        self.activations = [observation]
        
        x = observation
        for w, b in zip(self.hidden_weights, self.hidden_biases):
            x = relu(x @ w + b)
            self.activations.append(x)
        
        # Policy head
        policy_logits = x @ self.policy_weight + self.policy_bias
        policy = softmax(policy_logits)
        
        # Value head
        value = tanh(x @ self.value_weight + self.value_bias)[0]
        
        self.last_policy_logits = policy_logits
        self.last_value = value
        
        return policy, value
    
    def predict(self, state) -> Tuple[np.ndarray, float]:
        """Get policy and value for a game state"""
        obs = state.get_observation()
        policy, value = self.forward(obs)
        
        # Mask illegal actions
        legal = state.get_legal_actions()
        masked_policy = policy * legal
        if masked_policy.sum() > 0:
            masked_policy /= masked_policy.sum()
        else:
            # Fall back to uniform over legal
            masked_policy = legal.astype(np.float32)
            masked_policy /= masked_policy.sum()
        
        return masked_policy, value
    
    def train_step(self, 
                   observations: np.ndarray,
                   target_policies: np.ndarray,
                   target_values: np.ndarray) -> Tuple[float, float, float]:
        """
        One training step.
        
        Args:
            observations: Batch of observations (batch_size, input_size)
            target_policies: Target policy distributions (batch_size, action_size)
            target_values: Target values (batch_size,)
            
        Returns:
            (total_loss, policy_loss, value_loss)
        """
        batch_size = len(observations)
        total_policy_loss = 0.0
        total_value_loss = 0.0
        
        # Simple SGD - for production use Adam or similar
        config = self.config
        
        # Accumulate gradients
        grad_hidden_w = [np.zeros_like(w) for w in self.hidden_weights]
        grad_hidden_b = [np.zeros_like(b) for b in self.hidden_biases]
        grad_policy_w = np.zeros_like(self.policy_weight)
        grad_policy_b = np.zeros_like(self.policy_bias)
        grad_value_w = np.zeros_like(self.value_weight)
        grad_value_b = np.zeros_like(self.value_bias)
        
        for i in range(batch_size):
            obs = observations[i]
            target_p = target_policies[i]
            target_v = target_values[i]
            
            # Forward
            pred_policy, pred_value = self.forward(obs)
            
            # Policy loss (cross-entropy)
            policy_loss = -np.sum(target_p * np.log(pred_policy + 1e-8))
            total_policy_loss += policy_loss
            
            # Value loss (MSE)
            value_loss = (pred_value - target_v) ** 2
            total_value_loss += value_loss
            
            # Backward pass (simplified)
            # Policy gradient: d(CE)/d(logits) = pred - target
            d_policy = pred_policy - target_p
            
            # Value gradient: d(MSE)/d(value) = 2 * (pred - target)
            d_value = 2 * (pred_value - target_v) * (1 - pred_value ** 2)  # tanh derivative
            
            # Gradients for heads
            hidden_out = self.activations[-1]
            grad_policy_w += np.outer(hidden_out, d_policy) / batch_size
            grad_policy_b += d_policy / batch_size
            grad_value_w += np.outer(hidden_out, d_value).reshape(-1, 1) / batch_size
            grad_value_b += d_value / batch_size
            
            # Backprop through hidden layers
            d_hidden = (d_policy @ self.policy_weight.T + 
                       d_value * self.value_weight.T.flatten())
            
            for layer_idx in range(len(self.hidden_weights) - 1, -1, -1):
                # ReLU derivative
                d_hidden = d_hidden * (self.activations[layer_idx + 1] > 0)
                
                prev_activation = self.activations[layer_idx]
                grad_hidden_w[layer_idx] += np.outer(prev_activation, d_hidden) / batch_size
                grad_hidden_b[layer_idx] += d_hidden / batch_size
                
                if layer_idx > 0:
                    d_hidden = d_hidden @ self.hidden_weights[layer_idx].T
        
        # Apply gradients with L2 regularization
        for i in range(len(self.hidden_weights)):
            self.hidden_weights[i] -= config.learning_rate * (
                grad_hidden_w[i] + config.l2_reg * self.hidden_weights[i])
            self.hidden_biases[i] -= config.learning_rate * grad_hidden_b[i]
        
        self.policy_weight -= config.learning_rate * (
            grad_policy_w + config.l2_reg * self.policy_weight)
        self.policy_bias -= config.learning_rate * grad_policy_b
        
        self.value_weight -= config.learning_rate * (
            grad_value_w + config.l2_reg * self.value_weight)
        self.value_bias -= config.learning_rate * grad_value_b
        
        return (total_policy_loss + total_value_loss) / batch_size, \
               total_policy_loss / batch_size, \
               total_value_loss / batch_size
    
    def save(self, filepath: str) -> None:
        """Save network weights to file"""
        np.savez(filepath,
                 hidden_weights=self.hidden_weights,
                 hidden_biases=self.hidden_biases,
                 policy_weight=self.policy_weight,
                 policy_bias=self.policy_bias,
                 value_weight=self.value_weight,
                 value_bias=self.value_bias)
    
    def load(self, filepath: str) -> None:
        """Load network weights from file"""
        data = np.load(filepath, allow_pickle=True)
        self.hidden_weights = list(data['hidden_weights'])
        self.hidden_biases = list(data['hidden_biases'])
        self.policy_weight = data['policy_weight']
        self.policy_bias = data['policy_bias']
        self.value_weight = data['value_weight']
        self.value_bias = data['value_bias']


class NeuralMCTS:
    """MCTS that uses a neural network for policy and value"""
    
    def __init__(self, network: SimpleNetwork, num_simulations: int = 100):
        self.network = network
        self.num_simulations = num_simulations
        self.c_puct = 1.4
        self.root = None
        
    def get_policy_value(self, state) -> Tuple[np.ndarray, float]:
        """Get policy and value from neural network"""
        return self.network.predict(state)
    
    def search(self, state) -> np.ndarray:
        """Run MCTS with neural network guidance"""
        from mcts import MCTSNode
        
        policy, _ = self.get_policy_value(state)
        self.root = MCTSNode()
        self.root.expand(state, policy)
        
        for _ in range(self.num_simulations):
            self._simulate(state)
        
        # Return visit count distribution
        visits = np.zeros(self.network.config.action_size, dtype=np.float32)
        for action, child in self.root.children.items():
            visits[action] = child.visit_count
        
        if visits.sum() > 0:
            visits /= visits.sum()
        
        return visits
    
    def _simulate(self, root_state) -> None:
        """Run one MCTS simulation"""
        from mcts import MCTSNode
        
        node = self.root
        state = root_state.copy()
        search_path = [node]
        
        while node.is_expanded() and not state.is_terminal():
            action, node = node.select_child(self.c_puct)
            state = state.step(action)
            search_path.append(node)
        
        if state.is_terminal():
            value = state.get_reward(root_state.current_player)
        else:
            policy, value = self.get_policy_value(state)
            node.expand(state, policy)
        
        for node in reversed(search_path):
            node.visit_count += 1
            node.value_sum += value
            value = -value


def train_network(network: SimpleNetwork, training_data: list, epochs: int = 10) -> None:
    """
    Train network on self-play data.
    
    Args:
        network: Network to train
        training_data: List of (states, policies, winner) tuples
        epochs: Number of training epochs
    """
    print(f"Training on {len(training_data)} games...")
    
    # Flatten data with rewards
    all_states = []
    all_policies = []
    all_values = []
    
    for states, policies, winner in training_data:
        for i, (s, p) in enumerate(zip(states, policies)):
            all_states.append(s)
            all_policies.append(p)
            
            # Value from perspective of player who made the move
            # Alternating players, so invert value based on position
            if winner == 2:  # Draw
                all_values.append(0.0)
            else:
                # Simple: +1 if this player won, -1 if lost
                player_idx = i % 2
                if winner == player_idx:
                    all_values.append(1.0)
                else:
                    all_values.append(-1.0)
    
    all_states = np.array(all_states)
    all_policies = np.array(all_policies)
    all_values = np.array(all_values)
    
    n_samples = len(all_states)
    batch_size = 32
    
    for epoch in range(epochs):
        # Shuffle data
        indices = np.random.permutation(n_samples)
        total_loss = 0.0
        
        for i in range(0, n_samples, batch_size):
            batch_idx = indices[i:i+batch_size]
            loss, p_loss, v_loss = network.train_step(
                all_states[batch_idx],
                all_policies[batch_idx],
                all_values[batch_idx]
            )
            total_loss += loss
        
        num_batches = (n_samples + batch_size - 1) // batch_size
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / num_batches:.4f}")


if __name__ == "__main__":
    # Test network
    from game_state import initialize_game
    
    print("Testing neural network...")
    config = NetworkConfig()
    network = SimpleNetwork(config)
    
    # Test forward pass
    state = initialize_game()
    policy, value = network.predict(state)
    
    print(f"Policy shape: {policy.shape}")
    print(f"Policy sum: {policy.sum():.4f}")
    print(f"Value: {value:.4f}")
    
    # Test training step
    obs = state.get_observation()
    target_p = np.zeros(config.action_size)
    target_p[0] = 0.8
    target_p[1] = 0.2
    target_v = 0.5
    
    loss, p_loss, v_loss = network.train_step(
        obs.reshape(1, -1),
        target_p.reshape(1, -1),
        np.array([target_v])
    )
    print(f"Training loss: {loss:.4f} (policy: {p_loss:.4f}, value: {v_loss:.4f})")
