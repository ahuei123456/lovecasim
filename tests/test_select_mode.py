import unittest
import sys
import os
import numpy as np

# Adjust path to find game module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game_state import GameState, Ability, TriggerType, Effect, EffectType, TargetType, MemberCard

class TestSelectMode(unittest.TestCase):
    def setUp(self):
        self.game = GameState()
        self.p0 = self.game.players[0]
        # Add cards to deck for drawing
        self.p0.main_deck.extend([1, 2, 3, 4, 5])
        
    def test_select_mode_ability(self):
        """Test ability with multiple modal options."""
        # 登場: 以下から1つを選ぶ
        # ・1枚引く
        # ・1回エールチャージ
        ability = Ability(
            raw_text="Choose one: Draw 1 or Energy Charge 1",
            trigger=TriggerType.ON_PLAY,
            effects=[Effect(EffectType.SELECT_MODE, 1)],
            modal_options=[
                [Effect(EffectType.DRAW, 1)],
                [Effect(EffectType.ENERGY_CHARGE, 1)]
            ]
        )
        
        # Manually trigger
        self.game._play_automatic_ability(0, ability, {})
        
        # Choice should be pending
        self.assertEqual(len(self.game.pending_choices), 1)
        m_type, params = self.game.pending_choices[0]
        self.assertEqual(m_type, "SELECT_MODE")
        self.assertEqual(len(params['options']), 2)
        
        # Select first option (Draw 1)
        # SELECT_MODE actions start at 570
        self.game._handle_choice(570)
        
        # DRAW effect should be resolved already (if it was the only one)
        # Check hand size
        self.assertEqual(len(self.p0.hand), 1)

if __name__ == '__main__':
    unittest.main()
