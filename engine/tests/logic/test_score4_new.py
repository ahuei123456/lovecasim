import numpy as np
import pytest

from engine.game.game_state import GameState, LiveCard, MemberCard
from engine.models.ability import (
    Ability,
    AbilityCostType,
    Condition,
    ConditionType,
    Cost,
    Effect,
    EffectType,
    TriggerType,
)


@pytest.fixture
def game_state():
    state = GameState()
    # Reset variables
    GameState.member_db = {}
    GameState.live_db = {}
    return state


# --- Ability Parser Tests ---


# --- Ability Parser Tests ---
# Moved to engine/tests/parser/test_card_parsing.py


# --- Execution Tests ---


def test_kanata_execution(game_state):
    """Test PL!N-PR-008-PR execution logic for Condition and Cost"""
    state = game_state
    p0 = state.players[0]

    # Create a mock ability
    abi = Ability(
        raw_text="Test Kanata",
        trigger=TriggerType.ACTIVATED,
        costs=[Cost(AbilityCostType.REVEAL_HAND_ALL)],
        conditions=[Condition(ConditionType.HAND_HAS_NO_LIVE)],
        effects=[Effect(EffectType.DRAW, 1)],  # Simple effect to verify success
    )

    # Test Case 1: Hand has NO live cards -> Should Succeed
    p0.hand = [10, 11]  # Assume member IDs
    GameState.member_db[10] = MemberCard(10, "M-01", "M1", 1, np.zeros(6), np.zeros(7), 1)
    GameState.member_db[11] = MemberCard(11, "M-02", "M2", 1, np.zeros(6), np.zeros(7), 1)

    # Verify condition
    assert state._check_condition(p0, abi.conditions[0]), "Condition HAND_HAS_NO_LIVE should be True (no lives)"

    # Test Case 2: Hand HAS live card -> Should Fail
    p0.hand.append(100)
    GameState.live_db[100] = LiveCard(100, "L-01", "L1", 1, np.zeros(7))

    assert not state._check_condition(p0, abi.conditions[0]), "Condition HAND_HAS_NO_LIVE should be False (has live)"
