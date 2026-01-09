import inspect
import os
import sys

sys.path.append(os.getcwd())
try:
    from engine.game.game_state import GameState

    print("Methods in GameState:")
    methods = inspect.getmembers(GameState, predicate=inspect.isfunction)
    found = False
    for name, _ in methods:
        if name == "_check_condition":
            print(f"FOUND: {name}")
            found = True
            break
    if not found:
        print("NOT FOUND: _check_condition")
        # Check if it's mixed in or something?

except Exception as e:
    print(e)
