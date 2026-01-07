"""
Unit tests for Love Live Card Game rules.
Focuses on:
1. Baton Touch cost reduction
2. Ability Trigger ordering
3. Live Heart requirements
"""

import unittest
import numpy as np
import sys
import os

# Add game directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.game_state import GameState, MemberCard, LiveCard, PlayerState, Phase, Effect, EffectType
from game.ability import Ability, TriggerType

class TestRules(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        # Mock DB
        GameState.member_db = {}
        GameState.live_db = {}
        
    def test_baton_touch_cost(self):
        """Verify Baton Touch reduces cost correctly"""
        # Card 1: Cost 2 (on stage)
        c1 = MemberCard(1, "Fan1", 2, np.zeros(6), np.zeros(6), 1)
        # Card 2: Cost 5 (in hand)
        c2 = MemberCard(2, "Fan2", 5, np.zeros(6), np.zeros(6), 1)
        
        GameState.member_db = {1: c1, 2: c2}
        
        p = self.state.players[0]
        p.stage[0] = 1 # Card 1 on Left
        p.hand = [2]   # Card 2 in hand
        # Energy: 3 available (enough for 5-2=3, but not 5)
        p.energy_zone = [100, 101, 102]
        p.tapped_energy[:] = False
        
        self.state.phase = Phase.MAIN
        self.state.current_player = 0
        
        # Action: Play Card 2 (idx 0) on Area 0 (Left)
        # Action encoding: 1 + hand_idx*3 + area = 1 + 0 + 0 = 1
        
        # Check if legal (should be, cost 5-2=3 <= 3 energy)
        legal = self.state.get_legal_actions()
        self.assertTrue(legal[1], "Baton touch play should be legal")
        
        # Execute
        new_state = self.state.step(1)
        np0 = new_state.players[0]
        
        # Verify result
        self.assertEqual(np0.stage[0], 2, "Card 2 should be on stage")
        self.assertIn(1, np0.discard, "Card 1 should be in discard")
        self.assertEqual(np0.count_untapped_energy(), 0, "Should use all 3 energy (5-2=3)")
        
    def test_live_heart_requirements(self):
        """Verify Live card heart checking logic"""
        # Req: 1 Pink, 1 Red, 1 Any
        req = np.zeros(7, dtype=np.int32)
        req[0] = 1 # Pink
        req[1] = 1 # Red
        req[6] = 1 # Any
        
        live = LiveCard(100, "Song", 1, req)
        GameState.live_db = {100: live}
        
        p = self.state.players[0]
        p.live_zone = [100]
        
        # Case 1: Exact match (Pink, Red, Blue for Any)
        hearts1 = np.zeros(6, dtype=np.int32)
        hearts1[0] = 1
        hearts1[1] = 1
        hearts1[4] = 1 # Blue
        self.assertTrue(self.state._check_hearts_meet_requirement(hearts1, req), "Should match with exact + blue")
        
        # Case 2: Insufficient Color (2 Pink, 0 Red, 1 Blue) -> Fail Red
        hearts2 = np.zeros(6, dtype=np.int32)
        hearts2[0] = 2
        hearts2[4] = 1
        self.assertFalse(self.state._check_hearts_meet_requirement(hearts2, req), "Should fail missing red")
        
        # Case 3: Insufficient Any (1 Pink, 1 Red) -> Fail Any
        hearts3 = np.zeros(6, dtype=np.int32)
        hearts3[0] = 1
        hearts3[1] = 1
        self.assertFalse(self.state._check_hearts_meet_requirement(hearts3, req), "Should fail missing any")

    def test_trigger_stack(self):
        """Verify On Play triggers add to stack"""
        # Card with On Play logic
        ability = Ability("Test", TriggerType.ON_PLAY, [Effect(EffectType.DRAW, 1)])
        c1 = MemberCard(1, "TriggerMember", 1, np.zeros(6), np.zeros(6), 1, abilities=[ability])
        GameState.member_db = {1: c1}
        
        p = self.state.players[0]
        p.hand = [1]
        p.energy_zone = [100] # For cost
        
        self.state.phase = Phase.MAIN
        
        # Play card
        new_state = self.state.step(1)
        
        # Should have pending effect
        self.assertEqual(len(new_state.pending_effects), 1, "Should have 1 pending effect")
        self.assertEqual(new_state.pending_effects[0].effect_type, EffectType.DRAW, "Should be Draw effect")
        
        # Step again to resolve
        final_state = new_state.step(0) # Action doesn't matter for auto-resolve currently
        self.assertEqual(len(final_state.pending_effects), 0, "Effect should be resolved")
        # Player should have drawn (hand size: start 1 -> play 1 -> draw 1 = 1)
        # Note: deck is empty so might fail draw unless handled. 
        # But logic should try.

if __name__ == '__main__':
    unittest.main()
