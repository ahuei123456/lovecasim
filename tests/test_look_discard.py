import unittest
import sys
import os
import numpy as np

# Adjust path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game_state import GameState, Effect, EffectType, TargetType, MemberCard

class TestLookDiscard(unittest.TestCase):
    def setUp(self):
        self.game = GameState(verbose=True)
        self.p0 = self.game.players[0]
        
    def test_look_and_discard_mechanic(self):
        """
        Verify effectively: Look 5, Choose 1, Discard 4.
        """
        # 1. Setup Deck with known cards
        # We need 5 cards in deck.
        # Let's mock cards.
        for i in range(1, 6):
            self.game.member_db[i] = MemberCard(
                card_id=i, card_no=f"M{i}", name=f"Member {i}", cost=1, 
                hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1,
                group="Group", unit="", img_path=""
            )
        
        self.p0.main_deck = [1, 2, 3, 4, 5]
        self.p0.hand = []
        self.p0.discard = []
        
        # 2. Trigger LOOK_AND_CHOOSE Effect manually
        # This simulates an ability like "Look 5, add 1 to hand"
        effect = Effect(EffectType.LOOK_AND_CHOOSE, 1, params={'group': 'Group'}) # Filter shouldn't matter if all match or we skip filter logic
        
        # We need to populate looked_cards first? 
        # Usually EffectType.LOOK_DECK does that, then LOOK_AND_CHOOSE follows.
        # Or does LOOK_AND_CHOOSE do both?
        # Checking parser/game_state... 
        # Parser creates:
        # 1. LOOK_DECK (val)
        # 2. LOOK_AND_CHOOSE (val)
        
        # So we must simulate that sequence or manually populate.
        
        # Step A: LOOK_DECK
        look_effect = Effect(EffectType.LOOK_DECK, 5)
        # Manually resolving for test isolation
        # Logic from _resolve_pending_effect roughly:
        self.game.looked_cards = []
        for _ in range(5):
             self.game.looked_cards.append(self.p0.main_deck.pop(0))
             
        self.assertEqual(len(self.game.looked_cards), 5, "Should have looked at 5 cards")
        self.assertEqual(self.game.looked_cards, [1, 2, 3, 4, 5])
        
        # Step B: LOOK_AND_CHOOSE
        # This sets up the choice
        # Logic relies on pending_choice being created.
        # We can call _resolve_pending_effect if we push it, or manual setup.
        self.game.pending_effects.append(effect)
        self.game._resolve_pending_effect(0)
        
        # Verify choice is created
        self.assertTrue(self.game.pending_choices, "Should have a pending choice")
        choice_type, params = self.game.pending_choices[0]
        self.assertEqual(choice_type, "SELECT_FROM_LIST")
        self.assertEqual(len(params['cards']), 5)
        
        # 3. Execute Selection
        # Choose index 2 (Card 3)
        # Action ID mapping: 600 + index
        action_id = 602 
        
        # Step returns new state
        self.game = self.game.step(action_id)
        self.p0 = self.game.players[0]
        
        # 4. Verify Results
        # Card 3 in hand
        self.assertIn(3, self.p0.hand)
        self.assertEqual(len(self.p0.hand), 1)
        
        # Others (1, 2, 4, 5) in discard
        self.assertEqual(len(self.p0.discard), 4)
        expected_discard = {1, 2, 4, 5}
        self.assertEqual(set(self.p0.discard), expected_discard)
        
        # Looked cards cleared
        self.assertEqual(len(self.game.looked_cards), 0)
        
if __name__ == '__main__':
    unittest.main()
