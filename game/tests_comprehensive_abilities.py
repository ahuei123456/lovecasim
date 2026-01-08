
import unittest
import sys
import os
import json
import time

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState, Phase
from game.ability import Effect, EffectType, TargetType
from game.data_loader import CardDataLoader
from game.serializer import serialize_state

class ComprehensiveAbilityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load real data once
        cls.loader = CardDataLoader("data/cards.json")
        cls.member_db, cls.live_db, cls.energy_db = cls.loader.load()
        # Set global DBs
        GameState.member_db = cls.member_db
        GameState.live_db = cls.live_db
        GameState.energy_db = cls.energy_db
        
        # Ensure replay dir exists
        os.makedirs("replays", exist_ok=True)

    def setUp(self):
        self.game = GameState(verbose=True)
        self.p0 = self.game.players[0]
        self.p1 = self.game.players[1]
        
        # Setup basic state
        self.game.phase = Phase.MAIN
        self.game.current_player = 0
        
        # Clear hands/stage for clean testing
        self.p0.hand = []
        self.p0.stage = [-1, -1, -1]
        self.p0.energy_zone = [200, 200, 200]
        
        # Replay History
        self.history = []
        self.record_state() # Initial state

    def record_state(self):
        try:
            state_json = serialize_state(self.game)
            self.history.append(state_json)
        except Exception as e:
            print(f"Warning: Serialization failed: {e}")

    def step(self, action):
        """Helper to step game and record state"""
        self.game = self.game.step(action)
        self.p0 = self.game.players[0] # Update Ref
        self.p1 = self.game.players[1]
        self.record_state()

    def tearDown(self):
        # Save Replay
        test_name = self.id().split('.')[-1]
        filename = f"replays/{test_name}.json"
        
        replay_data = {
            "game_id": test_name,
            "winner": self.game.winner,
            "states": self.history
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(replay_data, f, ensure_ascii=False, indent=2)
        print(f"Saved replay to {filename}")

    def test_order_deck_rearrange(self):
        print("\n[Test] ORDER_DECK (Rearrange)")
        # Setup: 3 cards in deck
        self.p0.main_deck = [201, 202, 203] 
        
        # Trigger ORDER_DECK (Top, No Shuffle, Count 3)
        effect = Effect(EffectType.ORDER_DECK, 3, TargetType.SELF, params={"position": "top", "shuffle": False})
        
        # Apply effect
        self.game._apply_effect(effect, self.p0)
        self.record_state()
        
        # Expect SELECT_ORDER choice
        self.assertEqual(self.game.pending_choices[0][0], "SELECT_ORDER")
        
        # Choice params should contain the cards
        params = self.game.pending_choices[0][1]
        self.assertEqual(len(params['cards']), 3)
        self.assertTrue(201 in params['cards'])
        
        # Execute chain of selections to reorder: 203 -> 202 -> 201 (Reverse)
        current_list = params['cards']
        idx_203 = current_list.index(203)
        
        # Assuming mapped to 600-659 for now based on SELECT_FROM_LIST similarity.
        action_id = 600 + idx_203 
        self.step(action_id)
        
        # Should now have 2 cards left to order
        self.assertEqual(len(self.game.pending_choices), 1)
        params = self.game.pending_choices[0][1]
        self.assertEqual(len(params['cards']), 2)
        
        # Select 202
        current_list = params['cards']
        idx_202 = current_list.index(202)
        action_id = 600 + idx_202
        self.step(action_id)
        
        # Select 201
        if self.game.pending_choices:
             params = self.game.pending_choices[0][1]
             idx_201 = params['cards'].index(201)
             action_id = 600 + idx_201
             self.step(action_id)
             
        # Deck should be [203, 202, 201] (Top is end of list)
        self.assertEqual(self.p0.main_deck[-1], 203)
        self.assertEqual(self.p0.main_deck[-2], 202)
        self.assertEqual(self.p0.main_deck[-3], 201)

    def test_order_deck_shuffle_bottom(self):
        print("\n[Test] ORDER_DECK (Shuffle to Bottom)")
        self.p0.main_deck = [101, 102, 103, 104, 105]
        
        # Trigger: Shuffle 3 cards to BOTTOM
        effect = Effect(EffectType.ORDER_DECK, 3, TargetType.SELF, params={"position": "bottom", "shuffle": True})
        
        self.game._apply_effect(effect, self.p0)
        self.record_state()
        
        # Should be no pending choices (Shuffled automatically)
        self.assertEqual(len(self.game.pending_choices), 0)
        
        # Deck count same
        self.assertEqual(len(self.p0.main_deck), 5)

    def test_place_under(self):
        print("\n[Test] PLACE_UNDER")
        # Setup: Hand has card 301, Stage has member at 0
        self.p0.hand = [301]
        self.p0.stage[0] = 101 # Member
        self.p0.stage_energy[0] = []
        
        # Effect: Place 1 card from hand under member
        effect = Effect(EffectType.PLACE_UNDER, 1, TargetType.MEMBER, params={})
        
        # Inject context target area
        effect.params['target_area'] = 0
        
        self.game._apply_effect(effect, self.p0)
        self.record_state()
        
        # Should ask for Hand selection (Action 500+)
        self.assertEqual(len(self.game.pending_choices), 1)
        self.assertEqual(self.game.pending_choices[0][0], "TARGET_HAND")
        
        # Select Card 301 (Index 0 in hand -> Action 500)
        self.step(500)
        
        # Verify: Hand empty, Stage Energy has 301
        self.assertEqual(len(self.p0.hand), 0)
        self.assertEqual(len(self.p0.stage_energy[0]), 1)
        self.assertEqual(self.p0.stage_energy[0][0], 301)

    def test_swap_zone(self):
        print("\n[Test] SWAP_ZONE (Success Live <-> Hand)")
        # Setup: Card in Success Live
        self.p0.success_lives.append(301)
        self.p0.hand = [401]
        
        effect = Effect(EffectType.SWAP_ZONE, 1, TargetType.PLAYER, params={}) 
        
        self.game._apply_effect(effect, self.p0)
        self.record_state()
        
        # 1. Select from Success Live (SELECT_SWAP_SOURCE -> 600+)
        self.assertEqual(self.game.pending_choices[0][0], "SELECT_SWAP_SOURCE")
        
        # Select 301 (Index 0)
        self.step(600)
        
        # 2. Select from Hand (SELECT_SWAP_TARGET -> 500+)
        self.assertEqual(self.game.pending_choices[0][0], "SELECT_SWAP_TARGET")
        
        # Select 401 (Index 0)
        self.step(500)
        
        # Verify Swap
        self.assertIn(401, self.p0.success_lives)
        self.assertNotIn(301, self.p0.success_lives)
        self.assertIn(301, self.p0.hand)

    def test_formation_change_flow(self):
        print("\n[Test] FORMATION_CHANGE Flow")
        # Setup: 3 Members
        self.p0.stage = [101, 102, 103]
        
        # Trigger via FLAVOR_ACTION (Modal)
        effect = Effect(EffectType.FLAVOR_ACTION, 1, TargetType.PLAYER, params={"text": "何が好き？"})
        
        self.game._apply_effect(effect, self.p0)
        self.record_state()
        
        # 1. Modal Choice (570-579)
        self.assertEqual(self.game.pending_choices[0][0], "MODAL")
        
        # Select "Others" -> Index 2 -> Action 572
        print("Modal Choice: その他")
        self.step(572)
        
        # Now triggers CHOOSE_FORMATION -> SELECT_FORMATION_SLOT
        # 1. Select for Slot 0 (Left)
        # Available: 101, 102, 103. Put 103 (index 2) -> Action 702
        self.step(702)
        
        # 2. Select for Slot 1 (Center)
        # Available: 101, 102. Put 101 (index 0) -> Action 700
        self.step(700)
        
        # 3. Select for Slot 2 (Right)
        # Available: 102 (index 0). Action 700
        self.step(700)
        
        # Result should be [103, 101, 102]
        self.assertEqual(self.p0.stage, [103, 101, 102])

if __name__ == '__main__':
    unittest.main()
