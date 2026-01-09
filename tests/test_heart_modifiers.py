import unittest
import sys
import os
import numpy as np

# Adjust path to find game module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game_state import GameState, Ability, TriggerType, Effect, EffectType, MemberCard

class TestHeartModifiers(unittest.TestCase):
    def setUp(self):
        self.game = GameState()
        self.p0 = self.game.players[0]
        
        # Setup specific member cards for testing
        # Card 1: 1 Heart of each Color (Total 6)
        self.card1 = MemberCard(
            card_id=1, card_no="T01", name="Test Member 1", cost=1,
            hearts=np.array([1, 1, 1, 1, 1, 1]), # 6 colors
            blade_hearts=np.zeros(7), blades=1
        )
        
        # Register card
        GameState.member_db[1] = self.card1
        
        # Place on stage
        self.p0.stage[0] = 1
        
    def test_add_hearts(self):
        """Test adding hearts via EffectType.ADD_HEARTS"""
        # Add 1 Red Heart (Index 1)
        # Heart Colors: P=0, R=1, Y=2, G=3, B=4, V=5
        
        add_effect = Effect(EffectType.ADD_HEARTS, np.array([0, 1, 0, 0, 0, 0]))
        
        # Apply continuous effect
        self.p0.continuous_effects.append({
             "effect": add_effect,
             "target_slot": 0,
             "expiry": "TURN_END"
        })
        
        hearts = self.p0.get_effective_hearts(0, GameState.member_db)
        
        # Original Red was 1, should be 2
        self.assertEqual(hearts[1], 2)
        # Others remain 1
        self.assertEqual(hearts[0], 1)
        self.assertEqual(hearts[2], 1)

    def test_set_hearts(self):
        """Test setting hearts via EffectType.SET_HEARTS"""
        # Set to 2 Blue Hearts (Index 4)
        set_val = np.zeros(6, dtype=np.int32)
        set_val[4] = 2
        
        set_effect = Effect(EffectType.SET_HEARTS, set_val)
        
        self.p0.continuous_effects.append({
             "effect": set_effect,
             "target_slot": 0,
             "expiry": "TURN_END"
        })
        
        hearts = self.p0.get_effective_hearts(0, GameState.member_db)
        
        # Blue should be 2
        self.assertEqual(hearts[4], 2)
        # Red should be 0 (overwritten)
        self.assertEqual(hearts[1], 0)
        
    def test_transform_color(self):
        """Test transforming hearts to a specific color"""
        # Transform all to Green (Index 3)
        
        trans_effect = Effect(EffectType.TRANSFORM_COLOR, 0)
        # Params: target_color = "緑"
        trans_effect.params['target_color'] = "緑"
        
        self.p0.continuous_effects.append({
             "effect": trans_effect,
             "target_slot": 0,
             "expiry": "TURN_END"
        })
        
        hearts = self.p0.get_effective_hearts(0, GameState.member_db)
        
        # Total hearts on card was 6. All become Green.
        self.assertEqual(hearts[3], 6)
        self.assertEqual(hearts[1], 0)

    def test_set_then_add(self):
        """Test SET_HEARTS followed by ADD_HEARTS (Layers)"""
        # Set to 2 Blue (Layer 4)
        set_val = np.zeros(6, dtype=np.int32)
        set_val[4] = 2
        set_effect = Effect(EffectType.SET_HEARTS, set_val)
        
        # Add 1 Red (Layer 5)
        add_val = np.zeros(6, dtype=np.int32)
        add_val[1] = 1
        add_effect = Effect(EffectType.ADD_HEARTS, add_val)
        
        self.p0.continuous_effects.append({"effect": set_effect, "target_slot": 0})
        self.p0.continuous_effects.append({"effect": add_effect, "target_slot": 0})
        
        hearts = self.p0.get_effective_hearts(0, GameState.member_db)
        
        # Should have 2 Blue (from Set) and 1 Red (from Add)
        self.assertEqual(hearts[4], 2)
        self.assertEqual(hearts[1], 1)
        # Original hearts are gone
        self.assertEqual(hearts[0], 0) 

    def test_transform_then_add(self):
        """Test TRANSFORM_COLOR followed by ADD_HEARTS"""
        # Transform all to Green (Layer 4)
        trans_effect = Effect(EffectType.TRANSFORM_COLOR, 0)
        trans_effect.params['target_color'] = "緑"
        
        # Add 1 Red (Layer 5)
        add_val = np.zeros(6, dtype=np.int32)
        add_val[1] = 1
        add_effect = Effect(EffectType.ADD_HEARTS, add_val)
        
        self.p0.continuous_effects.append({"effect": trans_effect, "target_slot": 0})
        self.p0.continuous_effects.append({"effect": add_effect, "target_slot": 0})
        
        hearts = self.p0.get_effective_hearts(0, GameState.member_db)
        
        # Total 6 -> 6 Green
        # Plus 1 Red
        self.assertEqual(hearts[3], 6)
        self.assertEqual(hearts[1], 1)

if __name__ == '__main__':
    unittest.main()
