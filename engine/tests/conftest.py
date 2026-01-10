import random

import pytest
from pytest_bdd import given, parsers, then, when

from compiler.parser import AbilityParser
from engine.game.data_loader import CardDataLoader
from engine.game.game_state import GameState, Phase
from engine.models.ability import TriggerType

# --- Common Fixtures ---


@pytest.fixture
def loader():
    return CardDataLoader("engine/data/cards.json")


@pytest.fixture
def data(loader):
    member_db, live_db, energy_pool = loader.load()
    GameState.member_db = member_db
    GameState.live_db = live_db
    return member_db, live_db


@pytest.fixture
def context():
    return {}


@pytest.fixture
def game_state(data, context):
    gs = GameState()
    # Setup simple decks
    member_db, live_db = data
    available_members = list(member_db.keys())

    for p in gs.players:
        if available_members:
            # Create a simple deck
            p.main_deck = [random.choice(available_members) for _ in range(20)]
            p.hand = []  # Clear hand for controlled tests

    gs.phase = Phase.MAIN

    # Store in context for steps to access and update
    context["game_state"] = gs
    return gs


# --- Common Steps ---


@given("a player with a deck", target_fixture="player_state")
def player_with_deck(context, game_state):
    # game_state fixture ensures context is populated
    p = game_state.players[0]
    context["initial_hand_size"] = len(p.hand)
    context["initial_deck_size"] = len(p.main_deck)
    return p


# --- Parser Steps (Generic) ---


@when(parsers.parse('I parse the ability text "{text}"'), target_fixture="parsed_abilities")
def parse_ability(text):
    return AbilityParser.parse_ability_text(text)


@then(parsers.parse('I should get an ability with trigger "{trigger}"'))
def check_trigger(parsed_abilities, trigger):
    assert len(parsed_abilities) > 0
    # Map string to enum if needed, or check name
    expected_trigger = getattr(TriggerType, trigger)
    assert parsed_abilities[0].trigger == expected_trigger


@then(parsers.parse('the ability should have an effect type "{effect}"'))
def check_effect(parsed_abilities, effect):
    if effect == "NONE":
        assert len(parsed_abilities[0].effects) == 0
        return

    found = False
    for abi in parsed_abilities:
        for eff in abi.effects:
            if eff.effect_type.name == effect:
                found = True
                break
    assert found, f"Effect {effect} not found in {parsed_abilities[0].effects}"


@when(parsers.parse("the player draws {count:d} cards"))
def draw_cards(context, player_state, count):
    # Note: _draw_cards is in-place
    game_state = context["game_state"]
    # We must ensure player_state is from the current game_state
    # If player_state is passed, it is the initial state object usually.
    # But usually draw_cards just acts on P0.
    p = game_state.players[player_state.player_id]
    game_state._draw_cards(p, count)


@then(parsers.parse("the player's hand size should increase by {count:d}"))
def check_hand_size(context, count):
    game_state = context["game_state"]
    player_state = game_state.players[0]
    expected = context["initial_hand_size"] + count
    assert len(player_state.hand) == expected, f"Expected {expected}, got {len(player_state.hand)}"


@then(parsers.parse("the player's deck size should decrease by {count:d}"))
def check_deck_size(context, count):
    game_state = context["game_state"]
    player_state = game_state.players[0]
    expected = context["initial_deck_size"] - count
    assert len(player_state.main_deck) == expected, f"Expected {expected}, got {len(player_state.main_deck)}"


@given(parsers.parse("the player has {count:d} cards in hand"))
def player_has_cards(context, game_state, count):
    p = game_state.players[0]
    # Use simple integers 100+
    p.hand = list(range(100, 100 + count))
    context["hand_cards"] = p.hand.copy()


@then(parsers.parse("the player should be prompted to select {count:d} card from hand"))
def check_prompt_select_hand(context, game_state, count):
    current_state = context.get("game_state", game_state)
    assert len(current_state.pending_choices) > 0
    choice = current_state.pending_choices[0]
    assert choice[0] == "TARGET_HAND"
    # Action for TARGET_HAND 0 is 500.
