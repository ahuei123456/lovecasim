
import pytest
import numpy as np
import sys
import os
from engine.game.game_state import GameState, Phase, MemberCard, LiveCard, PlayerState, HeartColor
from engine.game.ability import Ability, TriggerType, Effect, EffectType, TargetType, AbilityCostType, Condition, ConditionType, AbilityParser, Cost

@pytest.fixture
def game_state():
    state = GameState()
    # Reset variables
    GameState.member_db = {}
    GameState.live_db = {}
    return state

def test_shizuku_parsing(game_state):
    """Test that Shizuku's ability is parsed correctly with optional cost."""
    text = "{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。"
    abilities = AbilityParser.parse_ability_text(text)
    
    assert len(abilities) == 1, "Should parse into 1 ability"
    abi = abilities[0]
    
    # Check trigger
    assert abi.trigger == TriggerType.ON_PLAY, "Trigger should be ON_PLAY"
    
    # Check cost is optional
    assert len(abi.costs) >= 1, "Should have at least 1 cost"
    discard_cost = next((c for c in abi.costs if c.type == AbilityCostType.DISCARD_HAND), None)
    assert discard_cost is not None, "Should have DISCARD_HAND cost"
    assert discard_cost.is_optional, "Cost should be marked as optional (てもよい)"
    
    # Check effect
    assert any(e.effect_type == EffectType.RECOVER_LIVE for e in abi.effects), "Should have RECOVER_LIVE effect"

def test_shizuku_optional_skip(game_state):
    """Test that player can SKIP the optional discard cost."""
    state = game_state
    p0 = state.players[0]
    
    # Create ability with optional cost
    abi = Ability(
        raw_text="Test Shizuku",
        trigger=TriggerType.ON_PLAY,
        costs=[Cost(AbilityCostType.DISCARD_HAND, 1, is_optional=True)],
        effects=[Effect(EffectType.RECOVER_LIVE, 1, TargetType.CARD_DISCARD, {'group': '虹ヶ咲'})]
    )
    
    # Setup: Shizuku is played, has cards in hand
    p0.hand = [10, 11]  # Cards that could be discarded
    GameState.member_db[10] = MemberCard(10, "SZ-01", "Card1", 1, np.zeros(6), np.zeros(7), 1)
    GameState.member_db[11] = MemberCard(11, "SZ-02", "Card2", 1, np.zeros(6), np.zeros(7), 1)
    
    # Setup: Live card in discard
    p0.discard = [200]
    GameState.live_db[200] = LiveCard(200, "L-200", "NijiLive", 1, np.zeros(7))
    
    # Simulate: Push the pending choice for optional discard
    # When ability triggers, game should offer SKIP option (action 0)
    # along with selecting cards to discard
    
    # Verify: get_legal_actions should include action 0 (pass/skip) for optional costs
    # We manually simulate the pending choice state pushed by _pay_costs usually
    state.pending_choices = [("TARGET_HAND", {"effect": "discard", "is_optional": True, "count": 1})]
    mask = state.get_legal_actions()
    
    # Action 0 should be available to skip
    assert mask[0], "Action 0 (SKIP/PASS) should be available for optional cost"
    
    # Actions 500+ should be available to select cards
    assert mask[500], "Action 500 should be available to select first card"
    assert mask[501], "Action 501 should be available to select second card"

def test_shizuku_execution_with_skip(game_state):
    """Test that choosing SKIP does not trigger the effect."""
    state = game_state
    p0 = state.players[0]
    
    # Setup
    p0.hand = [10]
    p0.discard = [200]
    p0.main_deck = [300, 301] # Prevent auto-refresh
    GameState.live_db[200] = LiveCard(200, "L-200", "NijiLive", 1, np.zeros(7))
    initial_hand = len(p0.hand)
    initial_discard = len(p0.discard)
    
    # When player chooses action 0 (skip) for optional cost
    state.pending_choices = [("TARGET_HAND", {"effect": "discard", "is_optional": True, "count": 1})]
    
    # Execute action 0
    state._handle_choice(0)
    
    # Result: Cost NOT paid, Effect NOT executed
    # Note: _handle_choice logic for optional skip usually clears choices and aborts ability or moves to next step?
    # Ideally, if cost cancelled, ability stops.
    
    # Verify hand count unchanged (no discard, no recovery)
    assert len(p0.hand) == initial_hand, "Hand size should be unchanged (1)"
    assert len(p0.discard) == initial_discard, "Discard size should be unchanged (1)"
    assert 200 in p0.discard, "Live card should still be in discard"
