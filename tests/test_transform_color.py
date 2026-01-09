import unittest
import sys
import os
import numpy as np

# Adjust path to find game module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game_state import GameState, Effect, EffectType, TargetType, MemberCard, Phase

class TestTransformColor(unittest.TestCase):
    def setUp(self):
        self.game = GameState()
        self.p0 = self.game.players[0]
        
        # ID 1: Member with Pink(0) and Red(1) hearts
        h = np.zeros(6, dtype=np.int32)
        h[0] = 1
        h[1] = 1
        self.game.member_db[1] = MemberCard(
            card_id=1, card_no="M-001", name="Duelist", cost=1,
            hearts=h, blade_hearts=np.zeros(7, dtype=np.int32), blades=1,
            group="μ's"
        )
        self.p0.stage[0] = 1 # Put on Left
        
    def test_transform_color(self):
        """Test transforming all hearts to a specific color."""
        # Before transform: 1 Pink, 1 Red
        h_before = self.p0.get_effective_hearts(0, self.game.member_db)
        self.assertEqual(h_before[0], 1)
        self.assertEqual(h_before[1], 1)
        
        # Add transform effect: all become Yellow (2)
        eff = Effect(EffectType.TRANSFORM_COLOR, 1, TargetType.PLAYER, params={'target_color': '黄'})
        self.p0.continuous_effects.append({
            'effect': eff,
            'target_slot': -1,
            'expiry': 'TURN_END'
        })
        
        # After transform: 0 Pink, 0 Red, 2 Yellow
        h_after = self.p0.get_effective_hearts(0, self.game.member_db)
        self.assertEqual(h_after[2], 2)
        self.assertEqual(h_after[0], 0)
        self.assertEqual(h_after[1], 0)

    def test_transform_color_icon(self):
        """Test transforming using icon string 'heart04' (Green)."""
        # Add transform effect: all become Green (3)
        eff = Effect(EffectType.TRANSFORM_COLOR, 1, TargetType.PLAYER, params={'target_color': '{{heart_04.png|heart04}}'})
        self.p0.continuous_effects.append({
            'effect': eff,
            'target_slot': -1,
            'expiry': 'TURN_END'
        })
        
        h_after = self.p0.get_effective_hearts(0, self.game.member_db)
        self.assertEqual(h_after[3], 2)
        self.assertEqual(h_after[0], 0)

if __name__ == '__main__':
    unittest.main()
