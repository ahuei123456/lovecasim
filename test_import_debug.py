import sys
import os

try:
    print(f"Importing game.models...")
    import game.models
    print(f"Game models path: {game.models.__file__}")
    print(f"Dir of game.models: {dir(game.models)}")
    
    # Try manual loading?
    import importlib.util
    spec = importlib.util.find_spec("game.models.ability")
    print(f"Spec for ability: {spec}")
    
    import game.models.ability
    print("Success!")
except Exception as e:
    print(f"FAIL: {e}")
