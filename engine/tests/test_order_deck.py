
import unittest
from engine.game.game_state import GameState, PlayerState, Phase
from engine.game.ability import Effect, EffectType, TargetType
import numpy as np

class TestOrderDeck(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.players[0].main_deck = list(range(10)) # [0, 1, 2, ..., 9] (9 is top)
        self.state.phase = Phase.MAIN
        self.state.current_player = 0

    def test_shuffle_deck_top_3(self):
        print("\n--- Testing Shuffle Top 3 ---")
        p0 = self.state.players[0]
        # [0, 1, ..., 9] -> 0 is Top
        original_deck = p0.main_deck.copy()
        
        # Effect: Order Deck (Shuffle Top 3)
        effect = Effect(
            effect_type=EffectType.ORDER_DECK,
            value=3,
            target=TargetType.PLAYER,
            params={'shuffle': True, 'position': 'top'}
        )
        
        # Apply effect manually
        self.state.pending_effects.append(effect)
        self.state._resolve_pending_effect(0)
        
        new_deck = p0.main_deck
        
        print(f"Original: {original_deck}")
        print(f"New:      {new_deck}")
        
        # Verify length unchanged
        self.assertEqual(len(new_deck), 10)
        
        # Verify bottom 7 are unchanged (indices 3 to 9)
        self.assertEqual(new_deck[3:], original_deck[3:])
        
        # Verify top 3 are the same set of cards (indices 0 to 2)
        # Original top 3: [0, 1, 2]
        self.assertEqual(set(new_deck[:3]), set(original_deck[:3]))
        
    def test_shuffle_deck_bottom_3(self):
        print("\n--- Testing Shuffle Top 3 to Bottom ---")
        p0 = self.state.players[0]
        # Reset deck
        p0.main_deck = list(range(10))
        original_deck = p0.main_deck.copy() # [0..9]
        top_cards_set = {0, 1, 2}
        
        # Effect: Shuffle Top 3 and place on bottom
        effect = Effect(
            effect_type=EffectType.ORDER_DECK,
            value=3,
            target=TargetType.PLAYER,
            params={'shuffle': True, 'position': 'bottom'}
        )
        
        self.state.pending_effects.append(effect)
        self.state._resolve_pending_effect(0)
        
        new_deck = p0.main_deck
        print(f"Original: {original_deck}")
        print(f"New:      {new_deck}")
        
        # Verify length
        self.assertEqual(len(new_deck), 10)
        
        # The top 3 from original should now be at the bottom (indices -3 to end)
        bottom_3 = new_deck[-3:]
        self.assertEqual(set(bottom_3), top_cards_set)
        
        # The rest should be shifted up
        # Original [3..9] should be at [0..6]
        self.assertEqual(new_deck[:-3], original_deck[3:])

    def test_order_rearrange(self):
        print("\n--- Testing Rearrange (No Shuffle) ---")
        p0 = self.state.players[0]
        p0.main_deck = list(range(10))
        
        # Effect: Look at top 3, rearrange
        effect = Effect(
            effect_type=EffectType.ORDER_DECK,
            value=3,
            target=TargetType.PLAYER,
            params={'shuffle': False, 'position': 'top'}
        )
        
        self.state.pending_effects.append(effect)
        self.state._resolve_pending_effect(0)
        
        # Expectation: Should trigger SELECT_ORDER choice
        if self.state.pending_choices:
            print("SUCCESS: Choice triggered for rearranging!")
            choice = self.state.pending_choices[0]
            print(f"Choice: {choice}")
            self.assertEqual(choice[0], "SELECT_ORDER")
            self.assertEqual(len(choice[1]['cards']), 3)
            
            # Simulate selection (picking index 0 recursively)
            # 1. Pick first card
            self.state._handle_choice(700 + 0) # Assuming SELECT_ORDER uses 700+ base
            
            # 2. Pick next card (index 0 of remaining)
            if self.state.pending_choices:
                 self.state._handle_choice(700 + 0)
            
            # 3. Pick last card
            if self.state.pending_choices:
                 self.state._handle_choice(700 + 0)
                 
            # Deck should be restored
            self.assertEqual(len(p0.main_deck), 10)
            
        else:
            print("FAILURE: No choice triggered. Effect was a no-op.")
            self.fail("Rearrange should trigger choice")

if __name__ == '__main__':
    unittest.main()
