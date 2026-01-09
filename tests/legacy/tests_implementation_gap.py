
import sys
import os
import numpy as np
import unittest

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState, Phase, MemberCard, LiveCard, PlayerState
from game.ability import Ability, TriggerType, Effect, EffectType, TargetType, AbilityCostType, Condition, ConditionType, Cost

class TestImplementationGap(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.p0 = self.state.players[0]
        self.p1 = self.state.players[1]
        
        # Setup mock DBs
        GameState.member_db = {}
        GameState.live_db = {}
        
        # Setup basic cards
        GameState.member_db[1] = MemberCard(1, "MemberAqours", 3, np.zeros(6), np.zeros(6), 1, group="Aqours")
        GameState.member_db[2] = MemberCard(2, "MemberMuse", 4, np.zeros(6), np.zeros(6), 1, group="μ's")
        GameState.live_db[100] = LiveCard(100, "LiveAqours", 1, np.zeros(7), group="Aqours")

    def test_group_filter_condition(self):
        """Test GROUP_FILTER condition logic"""
        cond = Condition(ConditionType.GROUP_FILTER, {'group': 'Aqours'})
        
        # Test 1: Self is Aqours
        self.assertTrue(self.state._check_condition(self.p0, cond, context={'card_id': 1}))
        # Test 2: Self is μ's -> Fail
        self.assertFalse(self.state._check_condition(self.p0, cond, context={'card_id': 2}))
        
        # Test 3: Revealed context
        cond_revealed = Condition(ConditionType.GROUP_FILTER, {'group': 'Aqours', 'context': 'revealed'})
        self.state.looked_cards = [1, 100]
        self.assertTrue(self.state._check_condition(self.p0, cond_revealed)) # All are Aqours
        
        self.state.looked_cards = [1, 2]
        self.assertFalse(self.state._check_condition(self.p0, cond_revealed)) # One is μ's

    def test_cost_check_condition(self):
        """Test COST_CHECK condition logic"""
        cond_le = Condition(ConditionType.COST_CHECK, {'value': 3, 'comparison': 'LE'})
        cond_ge = Condition(ConditionType.COST_CHECK, {'value': 4, 'comparison': 'GE'})
        
        # Member 1 (Cost 3)
        self.assertTrue(self.state._check_condition(self.p0, cond_le, context={'card_id': 1}))
        self.assertFalse(self.state._check_condition(self.p0, cond_ge, context={'card_id': 1}))
        
        # Member 2 (Cost 4)
        self.assertFalse(self.state._check_condition(self.p0, cond_le, context={'card_id': 2}))
        self.assertTrue(self.state._check_condition(self.p0, cond_ge, context={'card_id': 2}))

    def test_opponent_has_condition(self):
        """Test OPPONENT_HAS condition logic"""
        cond = Condition(ConditionType.OPPONENT_HAS)
        
        # Opponent has no members
        self.assertFalse(self.state._check_condition(self.p0, cond))
        
        # Add member to opponent stage
        self.p1.stage[0] = 2
        self.assertTrue(self.state._check_condition(self.p0, cond))

    def test_reveal_cards_effect(self):
        """Test REVEAL_CARDS effect"""
        eff = Effect(EffectType.REVEAL_CARDS, 2, params={'from': 'deck'})
        self.p0.main_deck = [10, 20, 30] # Top to bottom: 30, 20, 10? In engine it uses pop() which is end of list
        
        self.state.pending_effects.insert(0, eff)
        self.state._resolve_pending_effect(0)
        
        self.assertEqual(len(self.state.looked_cards), 2)
        # Verify it popped from end of list
        self.assertIn(30, self.state.looked_cards)
        self.assertIn(20, self.state.looked_cards)
        self.assertEqual(len(self.p0.main_deck), 1)

    def test_cost_reduction_member(self):
        """Test REDUCE_COST affects playing a member"""
        # Member 2 costs 4
        self.p0.energy_zone = [101, 102, 103] # Only 3 energy
        self.p0.hand = [2]
        self.p0.tapped_energy = np.zeros(50, dtype=bool)
        
        # Try playing without reduction -> Should fail or (if we call directly) not pay correctly
        # Here we check get_legal_actions
        self.state.phase = Phase.MAIN
        mask = self.state.get_legal_actions()
        action_id = 1 + 0 * 3 + 0 # Play card 0 to area 0
        self.assertFalse(mask[action_id], "Should not be able to play cost 4 member with 3 energy")
        
        # Add reduction effect
        eff_red = Effect(EffectType.REDUCE_COST, 1)
        self.p0.continuous_effects.append({'effect': eff_red, 'expiry': 'TURN_END'})
        
        mask = self.state.get_legal_actions()
        self.assertTrue(mask[action_id], "Should be able to play cost 4 member with 3 energy (reduced to 3)")
        
        # Actually play it
        self.state._play_member(0, 0)
        self.assertTrue(all(self.p0.tapped_energy[:3]), "Should have tapped 3 energy")
        self.assertFalse(self.p0.tapped_energy[3])

    def test_baton_touch_limit(self):
        """Test Baton Touch limit logic"""
        # Slot 0 has member 1 (Cost 3)
        self.p0.stage[0] = 1
        self.p0.energy_zone = [101, 102, 103, 104, 105] 
        self.p0.tapped_energy = np.zeros(50, dtype=bool)
        
        # Hand has member 2 (Cost 4)
        self.p0.hand = [2]
        
        # Baton touch reduction: 4 - 3 = 1
        self.state._play_member(0, 0)
        self.assertEqual(np.sum(self.p0.tapped_energy), 1, "Baton touch should reduce cost to 1")
        self.assertEqual(self.p0.baton_touch_count, 1)
        
        # Try another baton touch on same turn to slot 1
        self.p0.stage[1] = 1 # Dummy
        self.p0.hand = [2] # New member 2 in hand
        # Limit is 1. Cost should be full 4.
        self.state._play_member(0, 1)
        self.assertEqual(np.sum(self.p0.tapped_energy), 1 + 4, "Second baton touch should cost full 4 since limit is 1")

    def test_negate_next_effect(self):
        """Test NEGATE_EFFECT skip logic"""
        self.p0.negate_next_effect = True
        
        eff = Effect(EffectType.DRAW, 1)
        self.p0.hand = []
        
        self.state.pending_effects.insert(0, eff)
        self.state._resolve_pending_effect(0)
        
        self.assertEqual(len(self.p0.hand), 0, "Draw effect should have been negated")
        self.assertFalse(self.p0.negate_next_effect, "Negation flag should be reset")

    def test_restrictions(self):
        """Test RESTRICTION 'placement' blocks playing members"""
        self.p0.restrictions.add("placement")
        self.p0.energy_zone = [101, 102, 103, 104, 105]
        self.p0.hand = [2]
        self.state.phase = Phase.MAIN
        
        mask = self.state.get_legal_actions()
        action_id = 1 + 0 * 3 + 0
        self.assertFalse(mask[action_id], "Placement restriction should mask out play member actions")

    def test_cheer_reveal_effect(self):
        """Test CHEER_REVEAL effect"""
        eff = Effect(EffectType.CHEER_REVEAL, 1)
        self.p0.main_deck = [99] # Top card
        self.state.looked_cards = []
        
        self.state.pending_effects.insert(0, eff)
        self.state._resolve_pending_effect(0)
        
        self.assertEqual(self.state.looked_cards, [99], "Cheer reveal should move top deck to looked_cards")

    def test_cost_reduction_ability(self):
        """Test REDUCE_COST affects activated ability costs"""
        # Member 1 on stage area 0
        self.p0.stage[0] = 1
        # It has an activated ability with energy cost 1
        # (Mocking ability on member 1)
        self.state.member_db[1].abilities = [Ability(
            raw_text="Test", 
            trigger=TriggerType.ACTIVATED, 
            costs=[Cost(AbilityCostType.ENERGY, 1)],
            effects=[Effect(EffectType.DRAW, 1)]
        )]
        
        self.p0.energy_zone = [] # 0 energy
        self.p0.tapped_energy = np.zeros(50, dtype=bool)
        self.state.phase = Phase.MAIN
        
        mask = self.state.get_legal_actions()
        action_id = 200 # Area 0
        self.assertFalse(mask[action_id], "Should not be able to pay cost 1 with 0 energy")
        
        # Add reduction
        eff_red = Effect(EffectType.REDUCE_COST, 1)
        self.p0.continuous_effects.append({'effect': eff_red, 'expiry': 'TURN_END'})
        
        mask = self.state.get_legal_actions()
        self.assertTrue(mask[action_id], "Should be able to pay cost 1 with 0 energy (reduced to 0)")

if __name__ == "__main__":
    unittest.main()
