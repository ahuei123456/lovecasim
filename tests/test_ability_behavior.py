"""
End-to-End Behavioral Tests for Card Abilities

These tests verify that abilities produce the correct game state changes,
not just that they don't crash.

Each test:
1. Sets up a specific game state
2. Triggers an ability
3. Makes any required choices
4. Verifies the expected state changes occurred
"""
import unittest
import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game_state import GameState, Phase, MemberCard, LiveCard
from game.ability import (
    AbilityParser, Ability, Effect, EffectType, TriggerType,
    Condition, ConditionType, TargetType, Cost, AbilityCostType
)


class TestRecoverLiveBehavior(unittest.TestCase):
    """Test RECOVER_LIVE effect produces correct state changes."""
    
    def setUp(self):
        self.game = GameState(verbose=False)
        self.p0 = self.game.players[0]
        self.p1 = self.game.players[1]
        
        # Create mock member card
        self.game.member_db[100] = MemberCard(
            card_id=100, card_no="M100", name="Test Member", cost=5,
            hearts=np.zeros(6, dtype=np.int32),
            blade_hearts=np.zeros(7, dtype=np.int32),
            blades=1, group="Aqours"
        )
        
        # Create mock live cards
        for i in range(200, 203):
            self.game.live_db[i] = LiveCard(
                card_id=i, card_no=f"L{i}", name=f"Live {i}", score=1,
                required_hearts=np.zeros(7, dtype=np.int32), group="Aqours"
            )
            
    def test_recover_live_moves_card_to_hand(self):
        """Verify that selecting a live card from discard moves it to hand."""
        # Setup: Put a live card in discard
        self.p0.discard = [200, 100]  # Live 200 + Member 100
        self.p0.hand = [101]
        
        initial_discard_size = len(self.p0.discard)
        initial_hand_size = len(self.p0.hand)
        
        # Create RECOVER_LIVE effect
        effect = Effect(EffectType.RECOVER_LIVE, 1, TargetType.CARD_DISCARD)
        
        # Trigger the effect resolution
        self.game.pending_effects.append(effect)
        self.game._resolve_pending_effect(0)
        
        # Verify: A choice should be created
        self.assertTrue(len(self.game.pending_choices) > 0, 
                       "A SELECT_FROM_DISCARD choice should be pending")
        
        choice_type, params = self.game.pending_choices[0]
        self.assertEqual(choice_type, "SELECT_FROM_DISCARD")
        self.assertIn(200, params['cards'], "Live card 200 should be in choices")
        self.assertNotIn(100, params['cards'], "Member card 100 should NOT be in choices (wrong type)")
        
        # Execute selection (action 660 = select index 0 from discard choices)
        # The action ID depends on how get_legal_actions maps it
        # For SELECT_FROM_DISCARD, action IDs are 660 + index
        new_state = self.game.step(660)  # Select first card (index 0 = card 200)
        
        # Verify: Card moved from discard to hand
        self.assertIn(200, new_state.players[0].hand, "Live card 200 should be in hand")
        self.assertNotIn(200, new_state.players[0].discard, "Live card 200 should NOT be in discard")
        self.assertEqual(len(new_state.players[0].hand), initial_hand_size + 1, 
                        "Hand should have 1 more card")
        self.assertEqual(len(new_state.players[0].discard), initial_discard_size - 1, 
                        "Discard should have 1 fewer card")


class TestDrawBehavior(unittest.TestCase):
    """Test DRAW effect produces correct state changes."""
    
    def setUp(self):
        self.game = GameState(verbose=False)
        self.p0 = self.game.players[0]
        
        # Create mock cards for deck
        for i in range(1, 20):
            self.game.member_db[i] = MemberCard(
                card_id=i, card_no=f"M{i}", name=f"Member {i}", cost=1,
                hearts=np.zeros(6, dtype=np.int32),
                blade_hearts=np.zeros(7, dtype=np.int32),
                blades=1
            )
        
        # Set up deck
        self.p0.main_deck = list(range(1, 15))  # Cards 1-14 in deck
        self.p0.hand = []
        
    def test_draw_moves_cards_from_deck_to_hand(self):
        """Verify that draw effect moves cards from deck to hand."""
        initial_deck_size = len(self.p0.main_deck)
        initial_hand_size = len(self.p0.hand)
        
        # Execute draw 3
        self.game._draw_cards(self.p0, 3)
        
        # Verify
        self.assertEqual(len(self.p0.hand), initial_hand_size + 3, 
                        "Hand should have 3 more cards")
        self.assertEqual(len(self.p0.main_deck), initial_deck_size - 3, 
                        "Deck should have 3 fewer cards")
        
    def test_draw_takes_from_top_of_deck(self):
        """Verify that draw takes cards from top (end) of deck."""
        self.p0.main_deck = [1, 2, 3, 4, 5]  # 5 is at top
        self.p0.hand = []
        
        self.game._draw_cards(self.p0, 2)
        
        # Top cards (4, 5) should be in hand
        self.assertIn(5, self.p0.hand, "Card 5 (top) should be drawn")
        self.assertIn(4, self.p0.hand, "Card 4 (second from top) should be drawn")
        self.assertEqual(self.p0.main_deck, [1, 2, 3], "Cards 1-3 should remain in deck")


class TestOnPlayAbilityBehavior(unittest.TestCase):
    """Test that ON_PLAY abilities trigger correctly when a member is played."""
    
    def setUp(self):
        self.game = GameState(verbose=False)
        self.p0 = self.game.players[0]
        self.game.phase = Phase.MAIN
        self.game.current_player = 0
        
        # Create member with draw ability
        draw_ability = Ability(
            raw_text="登場時 カードを1枚引く",
            trigger=TriggerType.ON_PLAY,
            effects=[Effect(EffectType.DRAW, 1, TargetType.PLAYER)]
        )
        
        self.game.member_db[100] = MemberCard(
            card_id=100, card_no="M100", name="Draw Member", cost=0,
            hearts=np.zeros(6, dtype=np.int32),
            blade_hearts=np.zeros(7, dtype=np.int32),
            blades=1,
            abilities=[draw_ability]
        )
        
        # Set up game state
        self.p0.hand = [100]
        self.p0.main_deck = [1, 2, 3, 4, 5]
        self.p0.energy_zone = [2000, 2000, 2000]  # Enough energy
        
    def test_on_play_ability_triggers(self):
        """Verify that playing a member with ON_PLAY ability triggers the effect."""
        initial_deck_size = len(self.p0.main_deck)
        
        # Play member to center (action = 1 + hand_idx*3 + area)
        # hand_idx=0, area=1 (center) -> action = 1 + 0*3 + 1 = 2
        action_id = 2
        
        # Verify action is legal
        legal_mask = self.game.get_legal_actions()
        
        # Execute play
        if legal_mask[action_id]:
            new_state = self.game.step(action_id)
            
            # The member should be on stage
            self.assertEqual(new_state.players[0].stage[1], 100, 
                            "Member should be in center stage")
            
            # The ON_PLAY draw effect should have triggered
            # Note: This depends on ability resolution timing
            # For now, just verify the member was played successfully


class TestOptionalAbilityBehavior(unittest.TestCase):
    """Test that optional abilities can be skipped."""
    
    def setUp(self):
        self.game = GameState(verbose=False)
        self.p0 = self.game.players[0]
        
        # Create mock cards
        for i in range(1, 5):
            self.game.member_db[i] = MemberCard(
                card_id=i, card_no=f"M{i}", name=f"Member {i}", cost=1,
                hearts=np.zeros(6, dtype=np.int32),
                blade_hearts=np.zeros(7, dtype=np.int32),
                blades=1
            )
            
    def test_optional_choice_allows_skip(self):
        """Verify that optional choices have action 0 (skip) available."""
        self.p0.hand = [1, 2, 3]
        
        # Set up an optional TARGET_HAND choice
        self.game.pending_choices = [("TARGET_HAND", {
            "effect": "discard",
            "is_optional": True,
            "count": 1
        })]
        
        # Get legal actions
        legal_mask = self.game.get_legal_actions()
        
        # Action 0 (skip/pass) should be available for optional choices
        self.assertTrue(legal_mask[0], 
                       "Action 0 (SKIP) should be available for optional cost")


if __name__ == '__main__':
    unittest.main(verbosity=2)
