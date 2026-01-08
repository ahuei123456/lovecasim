"""
Unit test for interactive TAP_OPPONENT mechanic.
"""
import unittest
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from game.game_state import GameState, MemberCard
from game.ability import AbilityParser, EffectType, TriggerType

class TestTapOpponent(unittest.TestCase):
    
    def setUp(self):
        self.state = GameState()
        self.p0 = self.state.players[0]
        self.p1 = self.state.players[1]
        
        # Setup p1 (opponent) with members
        self.state.member_db[100] = MemberCard(card_id=100, name="OppMem0", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1)
        self.state.member_db[101] = MemberCard(card_id=101, name="OppMem1", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1)
        
        self.p1.stage[0] = 100
        self.p1.stage[1] = 101
        self.p1.tapped_members = [False, False, False]

    def test_parser_tap_opponent(self):
        """Card #12: 相手のメンバーを1人選び、ウェイトにする。"""
        text = "相手のメンバーを1人選び、ウェイトにする。"
        abilities = AbilityParser.parse_ability_text(text)
        eff = abilities[0].effects[0]
        
        self.assertEqual(eff.effect_type, EffectType.TAP_OPPONENT)
        # Note: target might be SELF or OPPONENT depending on parser state, 
        # but the handler now triggers a choice regardless if it's TAP_OPPONENT.
        
    def test_execution_tap_opponent(self):
        """Test interactive tapping of opponent member"""
        from game.ability import Effect
        eff = Effect(EffectType.TAP_OPPONENT, 1)
        
        # Player 0 resolves effect
        self.state.pending_effects.append(eff)
        self.state._resolve_pending_effect(0)
        
        # Should have choice to target opponent member
        self.assertEqual(len(self.state.pending_choices), 1)
        choice_type, params = self.state.pending_choices[0]
        self.assertEqual(choice_type, "TARGET_OPPONENT_MEMBER")
        self.assertEqual(params['effect'], "tap")
        
        # In get_legal_actions, 720 and 721 should be True (p1 has members there)
        legal = self.state.get_legal_actions()
        self.assertTrue(legal[720])
        self.assertTrue(legal[721])
        self.assertFalse(legal[722]) # No member at slot 2
        
        # Simulate choosing opponent member at slot 1 (action 721)
        self.state.take_action(721)
        
        # Verify p1 member at slot 1 is tapped
        self.assertTrue(self.p1.tapped_members[1])
        self.assertFalse(self.p1.tapped_members[0])

if __name__ == '__main__':
    unittest.main()
