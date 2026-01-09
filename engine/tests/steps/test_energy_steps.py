import pytest
from pytest_bdd import given, parsers, scenario, then, when

from engine.game.ability import Effect, EffectType
from engine.game.game_state import GameState


@pytest.fixture
def game_state():
    return GameState()


@scenario("../features/energy.feature", "Charge energy from deck")
def test_charge_from_deck():
    pass


@scenario("../features/energy.feature", "Charge energy from hand")
def test_charge_from_hand():
    pass


@given("a player with a deck", target_fixture="player")
def player_with_deck(game_state):
    import numpy as np

    p = game_state.players[0]
    p.main_deck = [10, 11, 12]
    p.energy_zone = []
    # Reset tapped_energy to default numpy array
    p.tapped_energy = np.zeros(100, dtype=bool)
    return p


@given("a player with a hand", target_fixture="player_hand")
def player_with_hand(game_state):
    p = game_state.players[0]
    p.hand = [100, 101]
    p.energy_zone = []
    return p


@when("the player uses an ability to charge energy from deck")
def charge_from_deck(game_state, player):
    eff = Effect(EffectType.ENERGY_CHARGE, 1, params={"from": "deck"})
    game_state.pending_effects.append(eff)
    game_state._resolve_pending_effect(0)


@when("the player uses an ability to charge energy from hand")
def charge_from_hand(game_state, player_hand):
    eff = Effect(EffectType.ENERGY_CHARGE, 1, params={"from": "hand"})
    game_state.pending_effects.append(eff)
    game_state._resolve_pending_effect(0)


@then("the player's energy zone should increase by 1")
def check_energy_zone(player):
    assert len(player.energy_zone) == 1


@then("the player's deck size should decrease by 1")
def check_deck_size(player):
    assert len(player.main_deck) == 2


@then("the new energy card should be untapped")
def check_untapped(player):
    # tapped_energy is fixed size 100
    idx = len(player.energy_zone) - 1
    assert not player.tapped_energy[idx]


@then(parsers.parse('a pending choice should be created for "{choice_type}"'))
def check_pending_choice_simple(game_state, choice_type):
    assert len(game_state.pending_choices) > 0
    actual_type, _ = game_state.pending_choices[0]
    assert actual_type == choice_type
