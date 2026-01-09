import os
import sys

import pytest
from pytest_bdd import given, scenario, then, when

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from engine.game.game_state import Condition, ConditionType, GameState, MemberCard


@pytest.fixture
def game_state():
    return GameState()

@scenario('../features/conditions.feature', 'Group Filter Condition')
def test_group_filter():
    pass

@scenario('../features/conditions.feature', 'Cost Check Condition')
def test_cost_check():
    pass

@scenario('../features/conditions.feature', 'Opponent Has Member Condition')
def test_opponent_has():
    pass

@given('a condition requiring group "Aqours"', target_fixture='cond')
def cond_group():
    return Condition(ConditionType.GROUP_FILTER, {'group': 'Aqours'})

@given('a member card of group "Aqours"', target_fixture='context')
def member_aqours(game_state):
    m = MemberCard(1, "A1", "Aq", 1, [], [], 1, group="Aqours")
    game_state.member_db[1] = m
    return {'card_id': 1}

@when('the condition is checked for the member', target_fixture='result')
def check_condition_member(game_state, cond, context):
    p0 = game_state.players[0]
    return game_state._check_condition(p0, cond, context=context)

@then('the result should be True')
def check_true(result):
    assert result is True

@given('a condition requiring cost LE 3', target_fixture='cond')
def cond_cost_le():
    return Condition(ConditionType.COST_CHECK, {'value': 3, 'comparison': 'LE'})

@given('a member card with cost 3', target_fixture='context')
def member_cost_3(game_state):
    m = MemberCard(2, "C3", "Cost3", 3, [], [], 1)
    game_state.member_db[2] = m
    return {'card_id': 2}

@given('a condition requiring opponent to have a member', target_fixture='cond')
def cond_opponent_has():
    return Condition(ConditionType.OPPONENT_HAS)

@given('the opponent has a member on stage')
def opponent_has_stage(game_state):
    p1 = game_state.players[1]
    m = MemberCard(100, "O1", "Opp", 1, [], [], 1)
    game_state.member_db[100] = m
    p1.stage[0] = 100

@when('the condition is checked', target_fixture='result')
def check_condition_general(game_state, cond):
    p0 = game_state.players[0]
    return game_state._check_condition(p0, cond)
