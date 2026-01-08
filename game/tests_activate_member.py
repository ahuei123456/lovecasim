"""
Unit test for interactive ACTIVATE_MEMBER mechanic.
"""
import unittest
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from game.game_state import GameState, MemberCard
from game.ability import AbilityParser, EffectType

class TestActivateMember(unittest.TestCase):
    
    def setUp(self):
        self.state = GameState()
        self.p0 = self.state.players[0]
        
        # Setup p0 with members
        self.state.member_db[100] = MemberCard(card_id=100, name="MyMem0", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1)
        self.state.member_db[101] = MemberCard(card_id=101, name="MyMem1", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1)
        
        self.p0.stage[0] = 100
        self.p0.stage[1] = 101
        # slot 0 is tapped, slot 1 is active
        self.p0.tapped_members = [True, False, False]

    def test_parser_activate_member(self):
        """Card #29: 自分のメンバーを1人選び、アクティブにする。"""
        text = "自分のメンバーを1人選び、アクティブにする。"
        abilities = AbilityParser.parse_ability_text(text)
        eff = abilities[0].effects[0]
        
        self.assertEqual(eff.effect_type, EffectType.ACTIVATE_MEMBER)

    def test_execution_activate_member(self):
        """Test interactive activation of a tapped member"""
        from game.ability import Effect
        eff = Effect(EffectType.ACTIVATE_MEMBER, 1)
        
        # Player 0 resolves effect
        self.state.pending_effects.append(eff)
        self.state._resolve_pending_effect(0)
        
        # Should have choice to target member
        self.assertEqual(len(self.state.pending_choices), 1)
        choice_type, params = self.state.pending_choices[0]
        self.assertEqual(choice_type, "TARGET_MEMBER")
        self.assertEqual(params['effect'], "activate")
        
        # In get_legal_actions, only slot 0 should be legal (slot 1 is already active)
        legal = self.state.get_legal_actions()
        self.assertTrue(legal[560]) # Slot 0 (Tapped)
        self.assertFalse(legal[561]) # Slot 1 (Active)
        self.assertFalse(legal[562]) # Slot 2 (Empty)
        
        # Simulate choosing member at slot 0 (action 560)
        self.state.take_action(560)
        
        # Verify slot 0 is now active
        self.assertFalse(self.p0.tapped_members[0])

if __name__ == '__main__':
    unittest.main()
