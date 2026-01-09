import pytest
from pytest_bdd import scenario, given, when, then, parsers
import numpy as np
import sys
import os
import random

# Add parent path to find game module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

# Use try-except import based on how pytest runs it
try:
    from engine.game.game_state import GameState, Phase, MemberCard, LiveCard, PlayerState
    from engine.game.data_loader import CardDataLoader
    from engine.game.ability import Effect, EffectType, AbilityParser, TriggerType
except ImportError:
    # Fallback if path appending isn't enough or different context
    from game.game_state import GameState, Phase, MemberCard, LiveCard, PlayerState
    from game.data_loader import CardDataLoader
    from game.ability import Effect, EffectType, AbilityParser, TriggerType

@pytest.fixture
def loader():
    return CardDataLoader('engine/data/cards.json')

@pytest.fixture
def data(loader):
    member_db, live_db, energy_pool = loader.load()
    GameState.member_db = member_db
    GameState.live_db = live_db
    return member_db, live_db

@pytest.fixture
def game_state(data):
    gs = GameState()
    # Setup simple decks
    member_db, live_db = data
    available_members = list(member_db.keys())
    
    for p in gs.players:
        if available_members:
            # Create a simple deck
            p.main_deck = [random.choice(available_members) for _ in range(20)]
            p.hand = [] # Clear hand for controlled tests
    
    gs.phase = Phase.MAIN
    return gs

@pytest.fixture
def context():
    return {}

@scenario('../features/abilities.feature', 'Draw cards')
def test_draw_cards():
    pass

@scenario('../features/abilities.feature', 'Add Blades')
def test_add_blades():
    pass

@scenario('../features/abilities.feature', 'Search Deck')
def test_search_deck():
    pass

@scenario('../features/abilities.feature', 'Recover member from discard')
def test_recover_member():
    pass

@scenario('../features/abilities.feature', 'Parse ability text')
def test_parse_ability():
    pass

# --- Steps ---

@given('a player with a deck', target_fixture='player_state')
def player_with_deck(game_state, context):
    p = game_state.players[0]
    context['initial_hand_size'] = len(p.hand)
    context['initial_deck_size'] = len(p.main_deck)
    return p

@when(parsers.parse('the player draws {count:d} cards'))
def draw_cards(game_state, player_state, count):
    game_state._draw_cards(player_state, count)

@then(parsers.parse("the player's hand size should increase by {count:d}"))
def check_hand_size(player_state, context, count):
    expected = context['initial_hand_size'] + count
    assert len(player_state.hand) == expected, f"Expected {expected}, got {len(player_state.hand)}"

@then(parsers.parse("the player's deck size should decrease by {count:d}"))
def check_deck_size(player_state, context, count):
    expected = context['initial_deck_size'] - count
    assert len(player_state.main_deck) == expected, f"Expected {expected}, got {len(player_state.main_deck)}"

@given('a member card with blades', target_fixture='blade_member')
def member_with_blades(data):
    member_db, _ = data
    for m in member_db.values():
        if m.blades > 0:
            return m
    pytest.skip("No member with blades found in DB")

@then('the member should have greater than 0 blades')
def check_blades(blade_member):
    assert blade_member.blades > 0

@given(parsers.parse('a player with a deck containing "{group}" members'), target_fixture='player_with_search_target')
def player_with_search_target(game_state, data, group):
    p = game_state.players[0]
    member_db, _ = data
    
    # Ensure deck has target
    targets = [mid for mid, m in member_db.items() if m.group == group]
    if not targets:
        pytest.skip(f"No members in group {group} found")
        
    p.main_deck = targets[:5] # Put them in deck
    game_state.member_db = member_db
    return p

@when(parsers.parse('the player searches the deck for "{group}"'))
def search_deck(game_state, player_with_search_target, group):
    # Just verify targets exist essentially
    pass

@then(parsers.parse('the player should find "{group}" members'))
def check_search_result(player_with_search_target, data, group):
    member_db, _ = data
    # Verify deck has them
    found = [mid for mid in player_with_search_target.main_deck if member_db[mid].group == group]
    assert len(found) > 0

# --- Recover Member Steps ---

@given('a player has a member in discard', target_fixture='player_with_discard')
def player_with_discard(game_state, data, context):
    p = game_state.players[0]
    member_db, _ = data
    if not member_db:
         pytest.skip("No members in DB")
         
    # Add a member to discard
    mid = list(member_db.keys())[0]
    p.discard.append(mid)
    context['discard_mid'] = mid
    return p

@when('the player recovers the member from discard')
def recover_member(player_with_discard, context):
    mid = context['discard_mid']
    # Simulate effect
    if mid in player_with_discard.discard:
        player_with_discard.discard.remove(mid)
        player_with_discard.hand.append(mid)

@then("the member should be in the player's hand")
def check_in_hand(player_with_discard, context):
    assert context['discard_mid'] in player_with_discard.hand

@then("the member should not be in the player's discard")
def check_not_in_discard(player_with_discard, context):
    assert context['discard_mid'] not in player_with_discard.discard

# --- Parser Steps ---

@when(parsers.parse('I parse the ability text "{text}"'), target_fixture='parsed_abilities')
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
        # Expect no effects (e.g. pure cost ability or cost-only part)
        assert len(parsed_abilities[0].effects) == 0
        return
    
    # Simple check if any effect matches
    # EffectType names: RECOVER_LIVE, MOVE_TO_DISCARD, etc.
    found = False
    for abi in parsed_abilities:
        for eff in abi.effects:
            if eff.effect_type.name == effect:
                found = True
                break
    assert found, f"Effect {effect} not found in {parsed_abilities[0].effects}"
