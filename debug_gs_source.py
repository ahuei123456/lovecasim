import inspect
import os
import sys

sys.path.append(os.getcwd())
try:
    from engine.game.game_state import GameState

    print(inspect.getsource(GameState._check_condition))

except Exception as e:
    print(e)
