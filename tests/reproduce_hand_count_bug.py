
import sys
import os
import unittest
# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState, Phase
from game.ability import AbilityParser, Ability

class TestHandCountBug(unittest.TestCase):
    def setUp(self):
        self.game = GameState()
        self.game.players[0].hand = []
        self.game.players[1].hand = []
        self.parser = AbilityParser()
        
    def test_condition_opponent_hand_more(self):
        # Card: PL!S-pb1-001-R
        # Text: {{toujyou.png|登場}}相手の手札の枚数が自分より2枚以上多い場合、自分の控え室からライブカードを1枚手札に加える。
        # Condition: Opponent Hand Count >= Self Hand Count + 2
        
        card_text = "{{toujyou.png|登場}}相手の手札の枚数が自分より2枚以上多い場合、自分の控え室からライブカードを1枚手札に加える。"
        abilities = self.parser.parse_ability_text(card_text)
        self.assertTrue(len(abilities) > 0)
        ability = abilities[0]
        
        print(f"Parsed Condition: {ability.conditions}")
        if not ability.conditions:
            print("ERROR: No conditions parsed!")
            return

        cond = ability.conditions[0]
        
        # Scenario 1: Opponent has fewer cards (Should fail)
        # Self: 3 cards, Opp: 1 card
        self.game.players[0].hand = [1, 2, 3]
        self.game.players[1].hand = [10]
        
        # Use private method _check_condition (simulating internal engine check)
        check = self.game._check_condition(self.game.players[0], cond)
        print(f"Scenario 1 (Self=3, Opp=1, Expect False): {check}")
        self.assertFalse(check, "Scenario 1 failed: Condition met despite opponent having fewer cards")
        
        # Scenario 2: Opponent has equal cards (Should fail)
        # Self: 3, Opp: 3
        self.game.players[1].hand = [10, 11, 12]
        check = self.game._check_condition(self.game.players[0], cond)
        print(f"Scenario 2 (Self=3, Opp=3, Expect False): {check}")
        self.assertFalse(check, "Scenario 2 failed: Condition met despite equal hands")

        # Scenario 3: Opponent has 1 more (Should fail)
        # Self: 3, Opp: 4
        self.game.players[1].hand = [10, 11, 12, 13]
        check = self.game._check_condition(self.game.players[0], cond)
        print(f"Scenario 3 (Self=3, Opp=4, Expect False): {check}")
        self.assertFalse(check, "Scenario 3 failed: Condition met despite only +1 diff")
        
        # Scenario 4: Opponent has 2 more (Should Pass)
        # Self: 3, Opp: 5
        self.game.players[1].hand = [10, 11, 12, 13, 14]
        check = self.game._check_condition(self.game.players[0], cond)
        print(f"Scenario 4 (Self=3, Opp=5, Expect True): {check}")
        self.assertTrue(check, "Scenario 4 failed: Condition NOT met despite +2 diff")

if __name__ == '__main__':
    unittest.main()
