
import unittest
from game_state import GameState, Phase
from ability import Effect, EffectType, TargetType
import numpy as np

class TestPlaceUnder(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.phase = Phase.MAIN
        self.state.current_player = 0
        p0 = self.state.players[0]
        p0.hand = [101, 102, 103]
        # Place a member on stage (Area 0)
        p0.stage[0] = 10 # Some member ID
        # Mock member DB entry
        class MockMember:
            def __init__(self):
                self.name = "Test Member"
                self.group = "Test"
                self.cost = 1
                self.blades = 1
                self.hearts = np.zeros(7)
                self.abilities = []
                self.img_path = ""
                self.ability_text = ""
                self.volume_icons = 0
                self.draw_icons = 0
            def total_hearts(self): return np.zeros(7)
            def total_blade_hearts(self): return np.zeros(7)
            
        self.state.member_db[10] = MockMember()

    def test_place_under_self(self):
        print("\n--- Testing Place Under Self ---")
        p0 = self.state.players[0]
        
        # Effect: Place 1 card from hand under Self
        effect = Effect(
            effect_type=EffectType.PLACE_UNDER,
            value=1,
            target=TargetType.MEMBER_SELF,
            params={'from': 'hand'}
        )
        
        # Manually resolving with context (Area 0)
        self.state.pending_effects.append(effect)
        self.state._resolve_pending_effect(0, context={'area': 0})
        
        # Expect Choice: TARGET_HAND
        self.assertTrue(self.state.pending_choices, "Should trigger TARGET_HAND choice")
        choice = self.state.pending_choices[0]
        print(f"Choice: {choice}")
        self.assertEqual(choice[0], "TARGET_HAND")
        self.assertEqual(choice[1]['effect'], 'place_under')
        self.assertEqual(choice[1]['target_area'], 0)
        
        # Execute choice: Pick first card (101)
        # Action ID for TARGET_HAND 0 is 500 + 0 = 500
        self.state._handle_choice(500)
        
        # Verify card 101 is now in stage_energy[0]
        self.assertIn(101, p0.stage_energy[0])
        self.assertNotIn(101, p0.hand)
        print(f"Stage Energy[0]: {p0.stage_energy[0]}")

if __name__ == '__main__':
    unittest.main()
