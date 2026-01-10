"""
Main training script for AlphaZero-style self-play training.

Usage:
    python train.py --games 100 --simulations 50 --epochs 10
"""

import argparse
import time
from pathlib import Path

import numpy as np
from game.game_state import GameState, create_sample_cards, initialize_game
from mcts import MCTS, MCTSConfig
from network import NetworkConfig, NeuralMCTS, SimpleNetwork, train_network


def run_training(args):
    """Main training loop"""
    print("=" * 60)
    print("Love Live Card Game - AlphaZero Training")
    print("=" * 60)

    # Initialize card database
    members, lives = create_sample_cards()
    GameState.member_db = members
    GameState.live_db = lives
    print(f"Loaded {len(members)} member cards and {len(lives)} live cards")

    # Initialize network
    net_config = NetworkConfig(
        input_size=60,  # Observation size
        hidden_size=args.hidden_size,
        num_hidden_layers=args.num_layers,
        action_size=200,
    )
    network = SimpleNetwork(net_config)
    print(f"Initialized network with {args.hidden_size} hidden units, {args.num_layers} layers")

    # Training iterations
    for iteration in range(args.iterations):
        print(f"\n{'=' * 60}")
        print(f"Training Iteration {iteration + 1}/{args.iterations}")
        print(f"{'=' * 60}")

        # Self-play phase
        print(f"\nPhase 1: Self-play ({args.games} games)...")
        start_time = time.time()

        training_data = []
        mcts = NeuralMCTS(network, num_simulations=args.simulations)

        wins = [0, 0, 0]  # P0 wins, P1 wins, draws

        for game_idx in range(args.games):
            game = initialize_game()
            game_states = []
            game_policies = []

            move_count = 0
            max_moves = 300

            while not game.is_terminal() and move_count < max_moves:
                # Get policy from MCTS
                policy = mcts.search(game)

                # Store for training
                game_states.append(game.get_observation())
                game_policies.append(policy)

                # Select and apply action
                action = np.random.choice(len(policy), p=policy)
                game = game.step(action)
                move_count += 1

            winner = game.get_winner() if game.is_terminal() else 2
            wins[winner] += 1
            training_data.append((game_states, game_policies, winner))

            if (game_idx + 1) % 10 == 0:
                print(f"  Game {game_idx + 1}/{args.games} - Moves: {move_count}, Winner: {winner}")

        elapsed = time.time() - start_time
        print(f"Self-play complete in {elapsed:.1f}s")
        print(f"Results: P0 wins: {wins[0]}, P1 wins: {wins[1]}, Draws: {wins[2]}")

        # Training phase
        print("\nPhase 2: Training...")
        start_time = time.time()
        train_network(network, training_data, epochs=args.epochs)
        elapsed = time.time() - start_time
        print(f"Training complete in {elapsed:.1f}s")

        # Save checkpoint
        checkpoint_dir = Path("checkpoints")
        checkpoint_dir.mkdir(exist_ok=True)
        checkpoint_path = checkpoint_dir / f"model_iter{iteration + 1}.npz"
        network.save(str(checkpoint_path))
        print(f"Saved checkpoint to {checkpoint_path}")

        # Evaluation phase (optional)
        if args.eval_games > 0:
            print(f"\nPhase 3: Evaluation ({args.eval_games} games vs random)...")
            eval_wins = evaluate_network(network, args.eval_games, args.simulations)
            print(f"Evaluation: Neural wins: {eval_wins}, Random wins: {args.eval_games - eval_wins}")

    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)


def evaluate_network(network: SimpleNetwork, num_games: int, simulations: int) -> int:
    """Evaluate network against random player"""
    neural_wins = 0

    mcts = NeuralMCTS(network, num_simulations=simulations)
    random_mcts = MCTS(MCTSConfig(num_simulations=5))  # Very weak random

    for game_idx in range(num_games):
        game = initialize_game()
        neural_player = game_idx % 2  # Alternate who goes first

        move_count = 0
        max_moves = 300

        while not game.is_terminal() and move_count < max_moves:
            if game.current_player == neural_player:
                policy = mcts.search(game)
                action = np.random.choice(len(policy), p=policy)
            else:
                action = random_mcts.select_action(game)

            game = game.step(action)
            move_count += 1

        winner = game.get_winner() if game.is_terminal() else 2
        if winner == neural_player:
            neural_wins += 1

    return neural_wins


def quick_test():
    """Quick functionality test"""
    print("Running quick test...")

    # Initialize
    members, lives = create_sample_cards()
    GameState.member_db = members
    GameState.live_db = lives

    # Create game
    game = initialize_game()
    print(f"Game initialized, first player: {game.first_player}")

    # Test MCTS
    config = MCTSConfig(num_simulations=10)
    mcts = MCTS(config)

    for step in range(5):
        if game.is_terminal():
            break
        action = mcts.select_action(game)
        game = game.step(action)
        print(f"Step {step}: Phase={game.phase.name}, Action={action}")

    print("Quick test passed!")


def main():
    parser = argparse.ArgumentParser(description="AlphaZero training for Love Live Card Game")
    parser.add_argument("--iterations", type=int, default=10, help="Number of training iterations")
    parser.add_argument("--games", type=int, default=50, help="Self-play games per iteration")
    parser.add_argument("--simulations", type=int, default=50, help="MCTS simulations per move")
    parser.add_argument("--epochs", type=int, default=5, help="Training epochs per iteration")
    parser.add_argument("--hidden-size", type=int, default=256, help="Neural network hidden layer size")
    parser.add_argument("--num-layers", type=int, default=3, help="Number of hidden layers")
    parser.add_argument("--eval-games", type=int, default=10, help="Evaluation games per iteration (0 to skip)")
    parser.add_argument("--test", action="store_true", help="Run quick functionality test")

    args = parser.parse_args()

    if args.test:
        quick_test()
    else:
        run_training(args)


if __name__ == "__main__":
    main()
