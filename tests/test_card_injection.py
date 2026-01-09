
import unittest
import sys
import os
import numpy as np

# Add parent directory to path to import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState, Phase, MemberCard, LiveCard

class TestCardInjection(unittest.TestCase):
    def setUp(self):
        # Create a fresh game state for each test
        self.state = GameState()
        # Ensure we have dummy DBs
        GameState.member_db = {
            101: MemberCard(101, "m1", "M1", 1, np.zeros(6), np.zeros(7), 1, "", "", [], ""),
            102: MemberCard(102, "m2", "M2", 2, np.zeros(6), np.zeros(7), 1, "", "", [], "")
        }
        GameState.live_db = {
            201: LiveCard(201, "l1", "L1", 100, np.zeros(7), [], "", "", "", 0, 0, np.zeros(7))
        }

    def test_inject_hand(self):
        # Inject into empty hand
        self.state.players[0].hand = []
        self.state.inject_card(0, 101, 'hand')
        self.assertEqual(len(self.state.players[0].hand), 1)
        self.assertEqual(self.state.players[0].hand[0], 101)
        
        # Inject at position 0
        self.state.inject_card(0, 102, 'hand', 0)
        self.assertEqual(self.state.players[0].hand[0], 102)
        self.assertEqual(self.state.players[0].hand[1], 101)

    def test_inject_stage(self):
        self.state.inject_card(0, 101, 'stage', 0) # Left
        self.state.inject_card(0, 102, 'stage', 2) # Right
        
        self.assertEqual(self.state.players[0].stage[0], 101)
        self.assertEqual(self.state.players[0].stage[1], -1) # Center empty
        self.assertEqual(self.state.players[0].stage[2], 102)

    def test_inject_energy(self):
        self.state.players[0].energy_zone = []
        self.state.inject_card(0, 200, 'energy')
        self.assertEqual(len(self.state.players[0].energy_zone), 1)
        self.assertEqual(self.state.players[0].energy_zone[0], 200)

    def test_inject_live(self):
        self.state.players[0].live_zone = []
        self.state.inject_card(0, 201, 'live')
        self.assertEqual(len(self.state.players[0].live_zone), 1)
        self.assertEqual(self.state.players[0].live_zone[0], 201)
        # Check revealed array grew
        self.assertEqual(len(self.state.players[0].live_zone_revealed), 1)
        self.assertEqual(self.state.players[0].live_zone_revealed[0], 0)

    def test_inject_opponent(self):
        # Verify we can mess with player 1
        self.state.players[1].hand = []
        self.state.inject_card(1, 101, 'hand')
        self.assertEqual(len(self.state.players[1].hand), 1)
        self.assertEqual(self.state.players[1].hand[0], 101)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.state.inject_card(2, 101, 'hand') # Bad player
        with self.assertRaises(ValueError):
            self.state.inject_card(0, 101, 'invalid_zone') # Bad zone
        with self.assertRaises(ValueError):
            self.state.inject_card(0, 101, 'stage', 3) # Bad stage pos

if __name__ == '__main__':
    unittest.main()
