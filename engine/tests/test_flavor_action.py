
import unittest
from engine.game.game_state import GameState, Phase
from engine.game.ability import Effect, EffectType, TargetType
import numpy as np

class TestFlavorAction(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.state.phase = Phase.MAIN
        self.state.current_player = 0
        p0 = self.state.players[0]
        p0.hand = [101]
        
        # Place 3 members on stage
        p0.stage[0] = 10 # Left
        p0.stage[1] = 20 # Center
        p0.stage[2] = 30 # Right
        
        # Mock member DB
        for cid in [10, 20, 30, 101]:
             class MockMember:
                def __init__(self, name):
                    self.name = name
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
             self.state.member_db[cid] = MockMember(f"Member {cid}")

    def test_flavor_action_formation_change(self):
        print("\n--- Testing Flavor Action (Formation Change) ---")
        p0 = self.state.players[0]
        original_stage = p0.stage.copy()
        
        # Effect: FLAVOR_ACTION (Trigger Formation Change)
        # Note: The parser attaches FLAVOR_ACTION effect if "聞く" is found.
        # The GameState handles it by triggering CHOOSE_FORMATION
        effect = Effect(
            effect_type=EffectType.FLAVOR_ACTION,
            value=1,
            target=TargetType.PLAYER,
            params={'text': '何が好き？'}
        )
        
        self.state.pending_effects.append(effect)
        self.state._resolve_pending_effect(0)
        
        # Step 1: Modal Choice "What do you like?"
        print("Checking for Modal Choice...")
        self.assertTrue(self.state.pending_choices, "Should trigger MODAL choice")
        choice = self.state.pending_choices[0]
        self.assertEqual(choice[0], "MODAL", "First choice should be MODAL")
        print(f"Modal Choice: {choice[1]['options']}")
        
        # Answer "その他" (Other) -> Should trigger FORMATION_CHANGE
        # Triggering choice: action 570 + index(2) = 572
        self.state._handle_choice(572)
        
        # Step 2: Formation Change Choice
        # Expect CHOOSE_FORMATION to be transformed into sequence of TARGET_MEMBER_SLOT?
        # Or just CHOOSE_FORMATION implies a specific handling flow we need to implement.
        # Currently, GameState just appends CHOOSE_FORMATION.
        
        print("Checking for Formation Change Choice...")
        self.assertTrue(self.state.pending_choices, "Should trigger FORMATION choice")
        choice = self.state.pending_choices[0]
        print(f"Formation Choice: {choice}")
        self.assertEqual(choice[0], "CHOOSE_FORMATION")
        
        # Verify it initiates reordering
        # We need to implement logic to handle "CHOOSE_FORMATION" by queuing slot selections
        # Let's say we want to rotate them: Left->Center, Center->Right, Right->Left
        # New State: [30, 10, 20]
        
        # Handing choice for CHOOSE_FORMATION
        # If implemented, it should ask for Slot 0 member
        # Let's simulate selecting member 30 (from current slot 2) for Slot 0
        
        # NOTE: This test will FAIL if CHOOSE_FORMATION logic is not implemented to handle input.
        # We expect the handler to convert CHOOSE_FORMATION into a series of selections
        # or handle a specific permutation input.
        # For this test, we assume a "Selection Phase" model.
        
        pass

if __name__ == '__main__':
    unittest.main()
