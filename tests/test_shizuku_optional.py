"""
Test for Shizuku (PL!N-bp1-003-P) Optional Discard Ability
Card Text: {{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
           {{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。

Expected Behavior:
1. ON_PLAY trigger: Player MAY discard 1 card. If they do, recover a Nijigasaki Live card from discard.
2. ON_LIVE_START trigger: Player MAY pay 1 Energy. If they do, select a heart color to gain until Live end.

Bug Report: "No option to not discard for first part of ability"
Expected: When the ability triggers, player should have the option to SKIP/PASS the optional cost.
"""

import sys
import os
import numpy as np
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState, Phase, MemberCard, LiveCard, PlayerState, HeartColor
from game.ability import Ability, TriggerType, Effect, EffectType, TargetType, AbilityCostType, Condition, ConditionType, AbilityParser, Cost

class TestShizukuOptionalDiscard(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.p0 = self.state.players[0]
        self.p1 = self.state.players[1]
        
        # Setup mock DBs
        GameState.member_db = {}
        GameState.live_db = {}
        
    def test_shizuku_parsing(self):
        """Test that Shizuku's ability is parsed correctly with optional cost."""
        text = "{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。"
        abilities = AbilityParser.parse_ability_text(text)
        
        self.assertEqual(len(abilities), 1, "Should parse into 1 ability")
        abi = abilities[0]
        
        # Check trigger
        self.assertEqual(abi.trigger, TriggerType.ON_PLAY, "Trigger should be ON_PLAY")
        
        # Check cost is optional
        self.assertTrue(len(abi.costs) >= 1, "Should have at least 1 cost")
        discard_cost = next((c for c in abi.costs if c.type == AbilityCostType.DISCARD_HAND), None)
        self.assertIsNotNone(discard_cost, "Should have DISCARD_HAND cost")
        self.assertTrue(discard_cost.is_optional, "Cost should be marked as optional (てもよい)")
        
        # Check effect
        self.assertTrue(any(e.effect_type == EffectType.RECOVER_LIVE for e in abi.effects), 
                        "Should have RECOVER_LIVE effect")
        
    def test_shizuku_optional_skip(self):
        """Test that player can SKIP the optional discard cost."""
        # Create ability with optional cost
        abi = Ability(
            raw_text="Test Shizuku",
            trigger=TriggerType.ON_PLAY,
            costs=[Cost(AbilityCostType.DISCARD_HAND, 1, is_optional=True)],
            effects=[Effect(EffectType.RECOVER_LIVE, 1, TargetType.CARD_DISCARD, {'group': '虹ヶ咲'})]
        )
        
        # Setup: Shizuku is played, has cards in hand
        self.p0.hand = [10, 11]  # Cards that could be discarded
        GameState.member_db[10] = MemberCard(card_id=10, card_no="M10", name="Card1", cost=1, hearts=np.zeros(6, dtype=np.int32), blade_hearts=np.zeros(7, dtype=np.int32), blades=1)
        GameState.member_db[11] = MemberCard(card_id=11, card_no="M11", name="Card2", cost=1, hearts=np.zeros(6, dtype=np.int32), blade_hearts=np.zeros(7, dtype=np.int32), blades=1)
        
        # Setup: Live card in discard
        self.p0.discard = [200]
        GameState.live_db[200] = LiveCard(card_id=200, card_no="L200", name="NijiLive", score=1, required_hearts=np.zeros(7, dtype=np.int32))
        
        # Simulate: Push the pending choice for optional discard
        # When ability triggers, game should offer SKIP option (action 0)
        # along with selecting cards to discard
        
        # Verify: get_legal_actions should include action 0 (pass/skip) for optional costs
        self.state.pending_choices = [("TARGET_HAND", {"effect": "discard", "is_optional": True, "count": 1})]
        mask = self.state.get_legal_actions()
        
        # Action 0 should be available to skip
        self.assertTrue(mask[0], "Action 0 (SKIP/PASS) should be available for optional cost")
        
        # Actions 500+ should be available to select cards
        self.assertTrue(mask[500], "Action 500 should be available to select first card")
        self.assertTrue(mask[501], "Action 501 should be available to select second card")
        
    def test_shizuku_execution_with_skip(self):
        """Test that choosing SKIP does not trigger the effect."""
        # Setup
        self.p0.hand = [10]
        self.p0.discard = [200]
        initial_hand = len(self.p0.hand)
        initial_discard = len(self.p0.discard)
        
        # When player chooses action 0 (skip) for optional cost
        self.state.pending_choices = [("TARGET_HAND", {"effect": "discard", "is_optional": True, "count": 1})]
        
        # Execute skip action (action 0)
        self.state.step(0)
        
        # Verify: No cards moved, effect not triggered
        self.assertEqual(len(self.p0.hand), initial_hand, "Hand size should not change")
        self.assertEqual(len(self.p0.discard), initial_discard, "Discard size should not change")


class TestSimilarOptionalAbilities(unittest.TestCase):
    """Test other cards with similar optional cost patterns."""
    
    def setUp(self):
        self.state = GameState()
        self.p0 = self.state.players[0]
        
    def test_optional_cost_detection(self):
        """Test that 'てもよい' pattern is correctly detected as optional."""
        # Various optional cost patterns
        test_cases = [
            "手札を1枚控え室に置いてもよい",   # May discard 1
            "エネルギーを支払ってもよい",       # May pay energy
            "このメンバーをウェイトにしてもよい", # May tap self
        ]
        
        for text in test_cases:
            abilities = AbilityParser.parse_ability_text(f"【登場時】{text}：効果")
            if abilities and abilities[0].costs:
                self.assertTrue(
                    any(c.is_optional for c in abilities[0].costs),
                    f"Cost should be optional for: {text}"
                )


if __name__ == "__main__":
    unittest.main()
