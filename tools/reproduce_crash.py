import sys
import os
import json
import numpy as np
import traceback

sys.path.append(os.getcwd())

from game.game_state import GameState, PlayerState, MemberCard
from game.ability import Effect, EffectType
from tools.ability_bulk_tester import MockGame, setup_test_state

def reproduce_swap_crash():
    print("Reproducing SWAP_CARDS crash...")
    try:
        # 1. Setup minimal state
        # Create a mock card dict similar to PL!N-bp3-007-R
        card_data = {'name': 'Test', 'ability': 'discard 1 draw 1'} # Dummy ability text
        game, member = setup_test_state('TEST-001', card_data)
        p0 = game.p0
        
        # 2. Mimic SWAP_CARDS logic
        effect = Effect(EffectType.SWAP_CARDS, 1)
        discard_count = effect.value
        initial_discard_len = len(p0.discard)
        
        print(f"Initial hand type: {type(p0.hand)}")
        print(f"Initial discard type: {type(p0.discard)}")
        
        # Mock having cards to discard
        while len(p0.hand) < discard_count:
            p0.hand.append(6000)
            
        print("Hand populated.")
            
        # Perform discard (mock implementation)
        for _ in range(discard_count):
            card = p0.hand.pop()
            print(f"Popped card: {card} type: {type(card)}")
            p0.discard.append(card)
            
        print("Discard logic complete.")
        
        if len(p0.discard) == initial_discard_len + discard_count:
             print("SUCCESS")
        else:
             print("FAIL: count mismatch")

    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    reproduce_swap_crash()
