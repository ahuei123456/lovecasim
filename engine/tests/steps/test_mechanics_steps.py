import pytest
from pytest_bdd import scenario, given, when, then
import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from engine.game.game_state import GameState, MemberCard, Phase
from engine.game.ability import Effect, EffectType

@pytest.fixture
def game_state():
    # Reset Class-level DBs
    GameState.member_db = {}
    gs = GameState()
    return gs

@scenario('../features/mechanics.feature', 'Baton Touch reduces cost')
def test_baton_touch_reduce():
    pass

@scenario('../features/mechanics.feature', 'Baton Touch limit')
def test_baton_touch_limit():
    pass

@scenario('../features/mechanics.feature', 'Cost Reduction for Member')
def test_cost_reduction():
    pass

@scenario('../features/mechanics.feature', 'Placement Restriction')
def test_placement_restriction():
    pass

@given('a player', target_fixture='p0')
def player_generic(game_state):
    return game_state.players[0]

@given('a player has a member on stage with cost 3', target_fixture='p0')
def player_with_stage_member(game_state):
    p0 = game_state.players[0]
    # Create member in DB
    m1 = MemberCard(1, "C1", "Mem1", 3, np.zeros(6), np.zeros(7), 1)
    # Ensure DB is ready
    GameState.member_db[1] = m1
    p0.stage[0] = 1
    return p0

@given('the player has a member in hand with cost 4')
def player_with_hand_member(game_state, p0):
    m2 = MemberCard(2, "C2", "Mem2", 4, np.zeros(6), np.zeros(7), 1)
    game_state.member_db[2] = m2
    p0.hand = [2]

@given('the player has 1 energy')
def player_energy_1(p0):
    p0.energy_zone = [100]
    p0.tapped_energy = np.zeros(100, dtype=bool)

@given('the player has 3 energy')
def player_energy_3(p0):
    p0.energy_zone = [100, 101, 102]
    p0.tapped_energy = np.zeros(100, dtype=bool)

@given('a player has a cost reduction effect of 1', target_fixture='p0_red')
def player_cost_reduction(game_state):
    p0 = game_state.players[0]
    eff = Effect(EffectType.REDUCE_COST, 1)
    p0.continuous_effects.append({'effect': eff, 'expiry': 'TURN_END'})
    return p0

@given('a player has a "placement" restriction', target_fixture='p0_res')
def player_restriction(game_state):
    p0 = game_state.players[0]
    p0.restrictions.add("placement")
    return p0

@when('the player plays the hand member onto the stage member')
def play_baton_touch(game_state, p0):
    # Action: Play card 2 (idx 0 in hand) to Area 0
    # Logic is hardcoded to area 0 for this test
    game_state.phase = Phase.MAIN
    game_state._play_member(0, 0)

@when('the player plays the member')
def play_member(game_state, p0_red):
    game_state.phase = Phase.MAIN
    game_state._play_member(0, 0) # Play from hand idx 0 to area 0

@then('the play should be successful')
def check_play_success(p0):
    # Check if member 2 is on stage 0
    assert p0.stage[0] == 2

@then('the energy used should be 1')
def check_energy_1(p0):
    assert np.sum(p0.tapped_energy) == 1

@then('the energy used should be 3')
def check_energy_3(p0):
    # Depending on which fixture was used, P0 might be passed as p0_red
    assert np.sum(p0.tapped_energy) == 3

@then('the baton touch count should be 1')
def check_baton_count(p0):
    assert p0.baton_touch_count == 1

@given('a player has performed a baton touch this turn')
def setup_baton_done(game_state, p0):
    # Force state
    p0.baton_touch_count = 1
    p0.baton_touch_limit = 1
    # Ensure stage matches post-baton state to allow another?
    # Or just test cost calculation.
    # Logic in _play_member checks limit.

@given('the player has another member in hand')
def player_has_another_member(game_state, p0):
    # Add member 3 to hand
    m3 = MemberCard(3, "C3", "Mem3", 3, np.zeros(6), np.zeros(7), 1)
    GameState.member_db[3] = m3
    p0.hand.append(3)

@when('the player attempts another baton touch')
def attempt_second_baton(game_state, p0):
    # This requires failing the action or checking legal actions
    pass

@then('the cost should not be reduced')
def check_no_reduction(game_state, p0):
    # We check mask instead of executing, as executing might crash or use weird logic if not enough energy
    # But wait, we didn't setup enough energy for full cost!
    
    # Let's say we have enough energy for reduced (1) but not full (4)
    # If cost is not reduced, checking legality should return False
    mask = game_state.get_legal_actions()
    action_id = 1 # Play hand 0 to area 0
    assert not mask[action_id], "Should not be legal if cost is not reduced"

@when('the player attempts to play a member')
def attempt_play_restriction(game_state, p0_res):
    # Setup necessary state for legality check
    p0_res.hand = [10]
    game_state.member_db[10] = MemberCard(10, "C", "N", 1, np.zeros(6), np.zeros(7), 1)
    p0_res.energy_zone = [100]
    p0_res.tapped_energy = np.zeros(100, dtype=bool)
    game_state.phase = Phase.MAIN

@then('the action should be illegal')
def check_illegal(game_state):
    mask = game_state.get_legal_actions()
    # Any play member action
    action_id = 1
    assert not mask[action_id]
