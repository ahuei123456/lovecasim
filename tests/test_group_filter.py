import unittest
import sys
import os
import numpy as np

# Adjust path to find game module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game_state import GameState, Condition, ConditionType, MemberCard

class TestGroupFilter(unittest.TestCase):
    def setUp(self):
        self.game = GameState()
        self.p0 = self.game.players[0]
        
        # Mock Member DB
        # ID 1: Liella! Member
        self.game.member_db[1] = MemberCard(
            card_id=1, card_no="L-001", name="Kanon", cost=1,
            hearts=np.zeros(6, dtype=np.int32), blade_hearts=np.zeros(7, dtype=np.int32), blades=1,
            group="ラブライブ！スーパースター!!"
        )
        # ID 2: Aqours Member
        self.game.member_db[2] = MemberCard(
            card_id=2, card_no="A-001", name="Chika", cost=1,
            hearts=np.zeros(6, dtype=np.int32), blade_hearts=np.zeros(7, dtype=np.int32), blades=1,
            group="ラブライブ！サンシャイン!!"
        )
        
    def test_zone_check_stage(self):
        """Test checking for group member existence on stage."""
        self.p0.stage[0] = 1 # Liella! on Left
        
        cond = Condition(ConditionType.GROUP_FILTER, {'group': 'Liella!', 'zone': 'STAGE'})
        
        # Should be True (Liella member is on stage)
        self.assertTrue(self.game._check_condition(self.p0, cond))
        
        # Clear stage
        self.p0.stage[0] = -1
        self.assertFalse(self.game._check_condition(self.p0, cond))
        
    def test_zone_check_discard(self):
        """Test checking for group member existence in discard."""
        self.p0.discard.append(1) # Liella! in discard
        
        cond = Condition(ConditionType.GROUP_FILTER, {'group': 'Liella!', 'zone': 'DISCARD'})
        self.assertTrue(self.game._check_condition(self.p0, cond))
        
        self.p0.discard = []
        self.assertFalse(self.game._check_condition(self.p0, cond))

    def test_context_check_self(self):
        """Test checking if 'this' card belongs to group."""
        cond = Condition(ConditionType.GROUP_FILTER, {'group': 'Aqours'})
        
        # Context is card ID 2 (Aqours)
        context = {'card_id': 2}
        self.assertTrue(self.game._check_condition(self.p0, cond, context))
        
        # Context is card ID 1 (Liella) -> Should fail for checking Aqours
        context = {'card_id': 1}
        self.assertFalse(self.game._check_condition(self.p0, cond, context))

    def test_context_check_revealed(self):
        """Test checking if observed/revealed cards belong to group."""
        self.game.looked_cards = [1, 1] # Two Liella cards
        
        cond = Condition(ConditionType.GROUP_FILTER, {'group': 'Liella!', 'context': 'revealed'})
        
        # Should pass because all looked cards are Liella
        self.assertTrue(self.game._check_condition(self.p0, cond))
        
        # Mixed group
        self.game.looked_cards = [1, 2] # Liella and Aqours
        # Should fail because logic requires ALL to match (match_count == len)
        self.assertFalse(self.game._check_condition(self.p0, cond))

    def test_icon_filter(self):
        """Test checking for heart icons via GROUP_FILTER."""
        # Member with Pink heart (0)
        h0 = np.zeros(6, dtype=np.int32)
        h0[0] = 1
        self.game.member_db[3] = MemberCard(
            card_id=3, card_no="P-001", name="Pinky", cost=1,
            hearts=h0, blade_hearts=np.zeros(7, dtype=np.int32), blades=1,
            group="μ's"
        )
        
        # Condition from parser: match 'heart01' (Pink)
        cond = Condition(ConditionType.GROUP_FILTER, {'group': '{{heart_01.png|heart01}}'})
        
        context = {'card_id': 3}
        self.assertTrue(self.game._check_condition(self.p0, cond, context))
        
        # Fail case
        context = {'card_id': 1} # Kanon has 0 hearts
        self.assertFalse(self.game._check_condition(self.p0, cond, context))

if __name__ == '__main__':
    unittest.main()
