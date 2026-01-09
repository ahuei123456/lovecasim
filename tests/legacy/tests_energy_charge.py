"""
Unit test for ENERGY_CHARGE mechanics.
"""
import unittest
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from game.game_state import GameState, MemberCard
from game.ability import AbilityParser, EffectType, Effect

class TestEnergyCharge(unittest.TestCase):
    
    def setUp(self):
        self.state = GameState()
        self.p0 = self.state.players[0]
        self.p0.main_deck = [10, 11, 12] # Top is 12
        self.p0.hand = [100, 101]
        self.p0.energy_zone = []
        self.p0.tapped_energy = []

    def test_energy_charge_from_deck(self):
        """Test charging energy from top of deck"""
        eff = Effect(EffectType.ENERGY_CHARGE, 1, params={'from': 'deck'})
        
        self.state.pending_effects.append(eff)
        self.state._resolve_pending_effect(0)
        
        self.assertEqual(len(self.p0.energy_zone), 1)
        self.assertEqual(self.p0.energy_zone[0], 12)
        self.assertEqual(len(self.p0.tapped_energy), 1)
        self.assertFalse(self.p0.tapped_energy[0]) # Should be untapped
        self.assertEqual(len(self.p0.main_deck), 2)

    def test_energy_charge_from_hand(self):
        """Test charging energy from hand (interactive)"""
        eff = Effect(EffectType.ENERGY_CHARGE, 1, params={'from': 'hand'})
        
        self.state.pending_effects.append(eff)
        self.state._resolve_pending_effect(0)
        
        # Should have choice
        self.assertEqual(len(self.state.pending_choices), 1)
        choice_type, params = self.state.pending_choices[0]
        self.assertEqual(choice_type, "TARGET_HAND")
        self.assertEqual(params['effect'], "energy_charge")
        
        # Simulate choosing hand index 1 (card 101) -> Action 501
        self.state.take_action(501)
        
        self.assertEqual(len(self.p0.energy_zone), 1)
        self.assertEqual(self.p0.energy_zone[0], 101)
        self.assertEqual(len(self.p0.hand), 1)
        self.assertEqual(self.p0.hand[0], 100)
        self.assertFalse(self.p0.tapped_energy[0])

if __name__ == '__main__':
    unittest.main()
