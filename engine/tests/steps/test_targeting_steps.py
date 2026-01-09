import pytest
from pytest_bdd import scenario, given, when, then, parsers
import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from engine.game.game_state import GameState, MemberCard
from engine.game.ability import Effect, EffectType

@pytest.fixture
def game_state():
    return GameState()

@scenario('../features/targeting.feature', 'Tap Opponent Member')
def test_tap_opponent():
    pass

@given('an opponent has a member on stage', target_fixture='opponent_setup')
def opponent_has_member(game_state):
    p1 = game_state.players[1]
    # Setup dummy members
    # card_id, card_no, name, cost, hearts, blade_hearts, blades, ..., abilities
    m1 = MemberCard(100, "OPP-01", "Ops", 1, np.zeros(6), np.zeros(7), 1)
    game_state.member_db[100] = m1
    p1.stage[0] = 100
    p1.tapped_members[0] = False
    return p1

@when('the player uses "Tap Opponent" effect')
def use_tap_effect(game_state):
    eff = Effect(EffectType.TAP_OPPONENT, 1)
    # Player 0 uses it
    game_state.pending_effects.append(eff)
    game_state._resolve_pending_effect(0)

@then('a pending choice should be created for "TARGET_OPPONENT_MEMBER"')
def check_target_choice(game_state):
    assert len(game_state.pending_choices) > 0
    assert game_state.pending_choices[0][0] == "TARGET_OPPONENT_MEMBER"

@then("the opponent's member should be a valid target")
def check_target_validity(game_state):
    legal = game_state.get_legal_actions()
    # Action 600 corresponds to Opponent Stage 0
    assert legal[600], "Action 600 (Target Opponent Slot 0) should be legal"
