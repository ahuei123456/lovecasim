import unittest
import sys
import os
import numpy as np

# Adjust path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game_state import GameState, LiveCard

class TestLiveSuccess(unittest.TestCase):
    def setUp(self):
        self.game = GameState(verbose=True)
        self.p0 = self.game.players[0]
        
    def test_select_success_live_handling(self):
        """
        Verify that SELECT_SUCCESS_LIVE action correctly moves card to success zone.
        """
        # Mock Live Cards
        live1 = LiveCard(
            card_id=1001, card_no="L1", name="Live 1", score=1, 
            required_hearts=np.zeros(7, dtype=int), 
            ability_text="", img_path="", group=""
        )
        live2 = LiveCard(
            card_id=1002, card_no="L2", name="Live 2", score=1, 
            required_hearts=np.zeros(7, dtype=int), 
            ability_text="", img_path="", group=""
        )
        
        self.game.live_db[1001] = live1
        self.game.live_db[1002] = live2
        
        # Setup state: Player won 2 lives, they are in passed_lives
        self.p0.passed_lives = [1001, 1002]
        
        # Setup Pending Choice (Normally done by _do_live_result)
        self.game.pending_choices.append(("SELECT_SUCCESS_LIVE", {
            "cards": [1001, 1002], # Options
        }))
        
        # Verify legal actions show up
        actions = self.game.get_legal_actions()
        # indices 600 and 601 should be legal
        self.assertTrue(actions[600], "Action 600 (Select 0) should be legal")
        self.assertTrue(actions[601], "Action 601 (Select 1) should be legal")
        
        # Execute Action 601 (Select Live 2 -> ID 1002)
        # Note: step return new state
        self.game = self.game.step(601)
        self.p0 = self.game.players[0]
        
        # Assertions
        self.assertIn(1002, self.p0.success_lives, "Selected card should be in success lives")
        self.assertEqual(len(self.p0.passed_lives), 0, "Passed lives should be cleared")
        self.assertIn(1001, self.p0.main_deck, "Unselected card should be in main deck")
        self.assertFalse(self.game.pending_choices, "Pending choice should be cleared")

if __name__ == '__main__':
    unittest.main()
