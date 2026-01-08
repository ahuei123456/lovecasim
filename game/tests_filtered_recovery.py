"""
Unit test for filtered recovery mechanics (GROUP, COST).
"""
import unittest
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from game.game_state import GameState, MemberCard
from game.ability import AbilityParser, EffectType

class TestFilteredRecovery(unittest.TestCase):
    
    def setUp(self):
        self.state = GameState()
        self.p0 = self.state.players[0]
        
        # Setup DB with members of different groups and costs
        # Member 400: μ's, Cost 3
        self.state.member_db[400] = MemberCard(card_id=400, name="Kotori", cost=3, group="μ's", hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1)
        # Member 401: μ's, Cost 5
        self.state.member_db[401] = MemberCard(card_id=401, name="Honoka", cost=5, group="μ's", hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1)
        # Member 402: Aqours, Cost 2
        self.state.member_db[402] = MemberCard(card_id=402, name="Chika", cost=2, group="Aqours", hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1)
        
        # Put all in discard
        self.p0.discard = [400, 401, 402]
        self.p0.hand = []

    def test_parser_filtered_recovery(self):
        """Card #3: 南 ことり - コスト4以下の『μ's』"""
        text = "自分の控え室からコスト4以下の『μ's』のメンバーカードを1枚手札に加える。"
        abilities = AbilityParser.parse_ability_text(text)
        eff = abilities[0].effects[0]
        
        self.assertEqual(eff.effect_type, EffectType.RECOVER_MEMBER)
        self.assertEqual(eff.params.get('group'), "μ's")
        self.assertEqual(eff.params.get('cost_max'), 4)

    def test_execution_filtered_recovery(self):
        """Test filtered recovery execution results in restricted choices"""
        text = "自分の控え室からコスト4以下の『μ's』のメンバーカードを1枚手札に加える。"
        abilities = AbilityParser.parse_ability_text(text)
        eff = abilities[0].effects[0]
        
        self.state.pending_effects.append(eff)
        self.state._resolve_pending_effect(0)
        
        # Should have choice
        self.assertEqual(len(self.state.pending_choices), 1)
        choice_type, params = self.state.pending_choices[0]
        self.assertEqual(choice_type, "SELECT_FROM_DISCARD")
        
        # Candidate cards should only be 400 (μ's, Cost 3)
        # 401 is μ's but Cost 5 (too high)
        # 402 is Cost 2 but Aqours (wrong group)
        candidates = params['cards']
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0], 400)
        
        # Perform recovery
        self.state.take_action(660)
        self.assertIn(400, self.p0.hand)
        self.assertEqual(len(self.p0.hand), 1)

if __name__ == '__main__':
    unittest.main()
