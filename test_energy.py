from game.game_state import initialize_game, Phase, GameState

def test_initial_state():
    print("Initializing game...")
    state = initialize_game()
    
    print(f"Initial Phase: {state.phase.name}")
    print(f"P0 Energy Zone: {len(state.players[0].energy_zone)}")
    print(f"P0 Hand Size: {len(state.players[0].hand)}")
    
    if len(state.players[0].energy_zone) != 0:
        print("FAIL: Energy zone should be 0")
    else:
        print("PASS: Energy zone is 0")

    if state.phase != Phase.MULLIGAN_P1:
        print(f"FAIL: Phase should be MULLIGAN_P1, got {state.phase.name}")
    else:
        print("PASS: Phase is MULLIGAN_P1")

if __name__ == "__main__":
    test_initial_state()
