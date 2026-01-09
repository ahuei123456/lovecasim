import unittest
import sys
import os
import numpy as np

# Adjust path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game_state import GameState, ConditionType, EffectType, TriggerType, MemberCard
from game.ability import AbilityParser

class TestCardIssues(unittest.TestCase):
    def setUp(self):
        self.game = GameState()
        self.p0 = self.game.players[0]
        self.p1 = self.game.players[1]

    def test_chika_condition(self):
        """
        PL!S-pb1-001-R: Opponent hand >= Self + 2
        Report: Pulls ability even with opponent having less cards.
        """
        text = "{{toujyou.png|登場}}相手の手札の枚数が自分より2枚以上多い場合、自分の控え室からライブカードを1枚手札に加える。"
        abilities = AbilityParser.parse_ability_text(text)
        ab = abilities[0]
        
        # Check parsed conditions
        print(f"Chika Conditions: {ab.conditions}")
        
        # Scenario 1: Opponent has LESS cards (Should be False)
        self.p0.hand = [1, 2, 3] # 3 cards
        self.p1.hand = [1]       # 1 card
        # Diff = 1 - 3 = -2. Condition (>=2) should be False.
        
        # If no conditions are parsed, check_condition returns True by default (if empty list passed? No, check_condition iterates)
        # Actually check if any condition logic exists for this
        if not ab.conditions:
            print("FAILURE: Chika has NO conditions parsed!")
            self.fail("Chika parsed with NO conditions.")
            
        allowed = True
        for cond in ab.conditions:
            if not self.game._check_condition(self.p0, cond):
                 allowed = False
                 break
        self.assertFalse(allowed, "Chika ability allowed despite Condition Failure (Opponent has less cards)")

        # Scenario 2: Opponent has +2 cards (Should be True)
        self.p0.hand = [1]
        self.p1.hand = [1, 2, 3] # 3 cards. 3 - 1 = 2.
        allowed = True
        for cond in ab.conditions:
            if not self.game._check_condition(self.p0, cond):
                 allowed = False
                 break
        self.assertTrue(allowed, "Chika ability NOT allowed despite Condition Met (Opponent has +2 cards)")

    def test_wien_look_and_choose(self):
        """
        PL!SP-bp1-010-R: Look 5, choose 1 Liella!
        Report: Bad action text, nothing happens.
        """
        text = "{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：自分のデッキの上からカードを5枚見る。その中から『Liella!』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。"
        abilities = AbilityParser.parse_ability_text(text)
        ab = abilities[0]
        
        print(f"Wien Effects: {ab.effects}")
        
        # Check 1: LOOK_DECK effect exists
        has_look = any(e.effect_type == EffectType.LOOK_DECK and e.value == 5 for e in ab.effects)
        self.assertTrue(has_look, "Missing LOOK_DECK 5 effect")
        
        # Check 2: LOOK_AND_CHOOSE effect exists AND has filter
        choose_eff = next((e for e in ab.effects if e.effect_type == EffectType.LOOK_AND_CHOOSE), None)
        self.assertIsNotNone(choose_eff, "Missing LOOK_AND_CHOOSE effect")
        
        print(f"Choose Params: {choose_eff.params}")
        self.assertEqual(choose_eff.params.get('group'), 'Liella!', "Missing 'group: Liella!' in choose effect params")
        self.assertEqual(choose_eff.params.get('source'), 'looked', "Missing 'source: looked' in choose effect params")

if __name__ == '__main__':
    unittest.main()
