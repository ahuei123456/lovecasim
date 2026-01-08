
import sys
import os
import traceback

# Add current dir to path
sys.path.append(os.getcwd())

try:
    from server import init_game, serialize_state, game_state
    
    print("Initializing game...")
    init_game()
    
    print("Serializing state (Mulligan)...")
    state = serialize_state()
    
    # ADVANCE TO LIVE_SET
    print("Advancing to LIVE_SET...")
    from game.game_state import Phase
    game_state.phase = Phase.LIVE_SET
    game_state.players[0].hand = [100, 101, 102] # Mock IDs
    
    print("Serializing state (LIVE_SET)...")
    state = serialize_state()
    print("Serialization successful!")
    # print(state) # Don't print huge JSON
except Exception:
    with open('crash_output.txt', 'w', encoding='utf-8') as f:
        f.write(traceback.format_exc())
    print("Crash caught and written to crash_output.txt")
