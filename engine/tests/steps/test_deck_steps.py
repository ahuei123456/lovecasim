import pytest
from pytest_bdd import given, scenario, then, when

from engine.game.game_state import GameState
from engine.models.ability import Effect, EffectType


@pytest.fixture
def game_state():
    return GameState()


@scenario("../features/deck_operations.feature", "Reveal Cards Effect")
def test_reveal_cards():
    pass


@scenario("../features/deck_operations.feature", "Cheer Reveal Effect")
def test_cheer_reveal():
    pass


@given("a player has 3 cards in deck", target_fixture="p0")
def player_deck_3(game_state):
    p0 = game_state.players[0]
    p0.main_deck = [10, 20, 30]
    return p0


@given("a player has a card in deck", target_fixture="p0")
def player_deck_1(game_state):
    p0 = game_state.players[0]
    p0.main_deck = [99]
    return p0


@when('the player resolves a "Reveal 2 Cards" effect')
def resolve_reveal_2(game_state, p0):
    eff = Effect(EffectType.REVEAL_CARDS, 2, params={"from": "deck"})
    game_state.pending_effects.append(eff)
    game_state._resolve_pending_effect(0)


@when('the player resolves a "Cheer Reveal" effect')
def resolve_cheer(game_state, p0):
    eff = Effect(EffectType.CHEER_REVEAL, 1)
    game_state.pending_effects.append(eff)
    game_state._resolve_pending_effect(0)


@then("2 cards should be revealed")
def check_reveal_count(game_state):
    assert len(game_state.looked_cards) == 2


@then("the main deck should have 1 card remaining")
def check_deck_remaining(p0):
    assert len(p0.main_deck) == 1


@then("the top card should be revealed")
def check_top_reveal(game_state):
    assert game_state.looked_cards == [99]
