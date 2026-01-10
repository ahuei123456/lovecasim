import sys
import os

print(f"CWD: {os.getcwd()}")
try:
    import game
    print(f"Game: {game}")
    import game.models
    print(f"Game.models: {game.models}")
    # Check if directory exists
    print(f"Models dir: {os.path.exists('game/models')}")
    print(f"Models init: {os.path.exists('game/models/__init__.py')}")
    print(f"Ability file: {os.path.exists('game/models/ability.py')}")
    
    import game.models.ability
    print(f"Ability: {game.models.ability}")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
