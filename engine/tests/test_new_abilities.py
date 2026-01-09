import unittest
import numpy as np
import sys
import os

# Add parent dir to path if needed (though pytest handles it usually)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from engine.game.game_state import GameState, Phase, MemberCard, PlayerState
from engine.game.ability import Ability, TriggerType, Effect, EffectType, TargetType, AbilityParser

class TestNewAbilities(unittest.TestCase):
    def test_deck_search(self):
        """Test SEARCH_DECK effect"""
        print("\n=== Testing SEARCH_DECK ===")
        state = GameState(verbose=True)
        p0 = state.players[0]
        # Setup deck with targets
        p0.main_deck = [1, 2, 3]
        GameState.member_db[1] = MemberCard(1, "AQ-01", "AqoursMember", 1, np.zeros(6), np.zeros(7), 1, group="Aqours")
        GameState.member_db[2] = MemberCard(2, "MS-01", "MuseMember", 1, np.zeros(6), np.zeros(7), 1, group="μ's")
        GameState.member_db[3] = MemberCard(3, "AQ-02", "AqoursMember", 2, np.zeros(6), np.zeros(7), 2, group="Aqours")

        # Effect: Search "μ's" member
        effect = Effect(EffectType.SEARCH_DECK, 1, params={'group': "μ's"})
        state.pending_effects.append(effect)

        # Resolve effect -> SELECT_FROM_LIST
        # Step 0 triggers auto-resolution of pending effects
        state = state.step(0)

        # We anticipate a choice
        self.assertTrue(len(state.pending_choices) > 0, "Should have pending choice for search")
        choice_type, choice_data = state.pending_choices[0]
        self.assertEqual(choice_type, "SELECT_FROM_LIST", "Choice should be SELECT_FROM_LIST")
        
        # Select first available option (which corresponds to action 600 + index)
        # Verify valid search results
        cards_found = choice_data['cards']
        self.assertIn(2, cards_found, "Should find Member 2 (μ's)")
        self.assertNotIn(1, cards_found, "Should NOT find Member 1 (Aqours)")

        # Select index 0 (Action 600)
        state = state.step(600)
        p0 = state.players[0]
        
        # Verify
        self.assertIn(2, p0.hand, "Member 2 should be in hand")
        self.assertEqual(len(p0.main_deck), 2, "Deck should have 2 cards left")

    def test_formation_change(self):
        """Test FORMATION_CHANGE effect"""
        print("\n=== Testing FORMATION_CHANGE ===")
        state = GameState(verbose=True)
        state.phase = Phase.MAIN
        p0 = state.players[0]
        # Setup stage: 1, 2, Empty
        p0.stage = np.array([1, 2, -1], dtype=np.int32) 
        GameState.member_db[1] = MemberCard(1, "M-01", "Member1", 1, np.zeros(6), np.zeros(7), 1)
        GameState.member_db[2] = MemberCard(2, "M-02", "Member2", 1, np.zeros(6), np.zeros(7), 1)
        
        # Trigger Formation Change
        effect = Effect(EffectType.FORMATION_CHANGE, 1)
        state.pending_effects.append(effect)

        # Start resolving -> SELECT_FORMATION_SLOT (Slot 0)
        state = state.step(0)

        # Choice 1: Select member for Slot 0 (Left)
        # We want to put Member 2 (currently at idx 1) into Slot 0
        # Available members should be indices 0 and 1.
        # Action 700 + MemberIndex?
        # SELECT_FORMATION_SLOT expects action: 700 + original_slot_index?
        # Let's check logic: Action range 700-702 for slot selection? 
        # game_state.py: elif 700 <= action <= 702:
        # Wait, usually 700+ is for formation selection relative to availability?
        # Let's assume standard logic: 700 + index_in_available_list
        # Available list: [(0, 1), (1, 2)] (Order: slot, card_id)
        # We want Member 2 (from slot 1). In available list, it is index 1.
        # So action 701.
        
        state = state.step(701)

        # Choice 2: Select for Slot 1 (Center)
        # Available: [(0, 1)] (Member 1 from slot 0)
        # We want Member 1. Index 0 in available list.
        # So action 700.
        
        state = state.step(700)

        p0 = state.players[0]
        # Expected: Slot 0 has Member 2, Slot 1 has Member 1
        self.assertEqual(p0.stage[0], 2, "Slot 0 should have Member 2")
        self.assertEqual(p0.stage[1], 1, "Slot 1 should have Member 1")

if __name__ == "__main__":
    unittest.main()
