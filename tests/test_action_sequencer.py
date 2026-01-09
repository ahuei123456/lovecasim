
import unittest
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState, Phase, MemberCard, LiveCard
from tools.debug.action_sequencer import ActionSequence

class TestActionSequencer(unittest.TestCase):
    def setUp(self):
        # Mock DBs
        GameState.member_db = {
            101: MemberCard(101, "m1", "M1", 1, np.zeros(6), np.zeros(7), 1, "", "", [], ""),
            102: MemberCard(102, "m2", "M2", 2, np.zeros(6), np.zeros(7), 1, "", "", [], "")
        }
    
    def test_setup_injection(self):
        seq = ActionSequence()
        seq.setup_inject(0, 101, 'hand')
        seq.verify(lambda v: v.assert_hand_contains(0, 101))

    def test_verifier_assertions(self):
        seq = ActionSequence()
        seq.setup_inject(0, 101, 'hand')
        
        # Should pass
        seq.verify(lambda v: v.assert_hand_contains(0, 101))
        
        # Should fail
        with self.assertRaises(AssertionError):
            seq.verify(lambda v: v.assert_hand_contains(0, 999))
            
        with self.assertRaises(AssertionError):
            seq.verify(lambda v: v.assert_hand_does_not_contain(0, 101))

    def test_auto_advance(self):
        # Test that it steps through automatic phases
        # ACTIVE -> ENERGY -> DRAW -> MULLIGAN (wait)
        seq = ActionSequence()
        
        # Force phase to ACTIVE to start
        seq.state.phase = Phase.ACTIVE
        
        # Should advance until non-automatic phase (Mulligan or Main)
        # Note: Default GameState starts at SETUP, then init_game moves to MULLIGAN usually.
        # But if we force ACTIVE, it should step 0 -> ENERGY, step 0 -> DRAW...
        
        # We need slightly more setup to make step(0) valid (e.g. decks)
        seq.state.players[0].main_deck = [101, 102]
        seq.state.players[0].energy_zone = []
        
        seq.action_auto()
        
        # Should be past ACTIVE/ENERGY/DRAW
        self.assertNotIn(seq.state.phase, [Phase.ACTIVE, Phase.ENERGY, Phase.DRAW])


if __name__ == '__main__':
    unittest.main()
