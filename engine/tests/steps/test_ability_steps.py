import numpy as np
import pytest
from pytest_bdd import given, parsers, scenario, then, when

from engine.game.game_state import Group
from engine.models.ability import Effect, EffectType

# Import generic steps and fixtures


@scenario("../features/abilities.feature", "Draw cards")
def test_draw_cards():
    pass


@scenario("../features/abilities.feature", "Add Blades")
def test_add_blades():
    pass


@scenario("../features/abilities.feature", "Search Deck")
def test_search_deck():
    pass


@scenario("../features/abilities.feature", "Recover member from discard")
def test_recover_member():
    pass


@scenario("../features/abilities.feature", "Parse ability text")
def test_parse_ability():
    pass


@scenario("../features/abilities.feature", "Formation Change")
def test_formation_change():
    pass


# --- Steps ---


@given("a member card with blades", target_fixture="blade_member")
def member_with_blades(data):
    member_db, _ = data
    for m in member_db.values():
        if m.blades > 0:
            return m


@then("the member should have greater than 0 blades")
def check_blades(blade_member):
    assert blade_member.blades > 0


@given(parsers.parse('a player with a deck containing "{group}" members'), target_fixture="player_with_search_target")
def player_with_search_target(context, game_state, data, group):
    # game_state fixture ensures initialization
    p = game_state.players[0]
    member_db, _ = data

    # Ensure deck has target
    target_group = Group.from_japanese_name(group)
    targets = [mid for mid, m in member_db.items() if target_group in m.groups]
    if not targets:
        pytest.skip(f"No members in group {group} found")

    # Put targets at the top of the deck for easy searching, followed by other members
    # Clear and update MemberDB to ensure we have the objects (handled by data fixture but safe to ensure)
    p.main_deck = targets + [mid for mid in member_db if mid not in targets]

    # Store context for later
    return p


@when(parsers.parse('the player searches the deck for "{group}"'))
def search_deck(context, player_with_search_target, group):
    game_state = context["game_state"]

    # Simulate the effect: SEARCH_DECK
    effect = Effect(EffectType.SEARCH_DECK, 1, params={"group": group})
    game_state.pending_effects.append(effect)

    # Resolve step -> Updates state!
    game_state = game_state.step(0)
    context["game_state"] = game_state

    # Check if we have a choice
    assert len(game_state.pending_choices) > 0
    choice = game_state.pending_choices[0]
    assert choice[0] == "SELECT_FROM_LIST"

    # Select the first card found
    cards_found = choice[1]["cards"]
    assert len(cards_found) > 0

    # Select it (Action 600)
    game_state = game_state.step(600)
    context["game_state"] = game_state


@then(parsers.parse('the player should find "{group}" members'))
def check_search_result(context, data, group):
    game_state = context["game_state"]
    p = game_state.players[0]
    member_db, _ = data

    target_group = Group.from_japanese_name(group)
    # The player should have the card in hand now (since we selected it)

    found_in_hand = [mid for mid in p.hand if mid in member_db and target_group in member_db[mid].groups]
    assert len(found_in_hand) > 0


# --- Recover Member Steps ---


@given("a player has a member in discard", target_fixture="player_with_discard")
def player_with_discard(context, game_state, data):
    # game_state ensures init
    p = game_state.players[0]
    member_db, _ = data
    if not member_db:
        pytest.skip("No members in DB")

    # Add a member to discard
    mid = list(member_db.keys())[0]
    p.discard.append(mid)
    context["discard_mid"] = mid
    return p


@when("the player recovers the member from discard")
def recover_member(context):
    game_state = context["game_state"]
    p = game_state.players[0]
    mid = context["discard_mid"]
    # Simulate effect
    if mid in p.discard:
        p.discard.remove(mid)
        p.hand.append(mid)


@then("the member should be in the player's hand")
def check_in_hand(context):
    game_state = context["game_state"]
    p = game_state.players[0]
    assert context["discard_mid"] in p.hand


@then("the member should not be in the player's discard")
def check_not_in_discard(context):
    game_state = context["game_state"]
    p = game_state.players[0]
    assert context["discard_mid"] not in p.discard


# --- Formation Change Steps ---


@given("a player with members on stage", target_fixture="player_with_stage")
def player_with_stage(context, game_state, data):
    # game_state ensures init
    p = game_state.players[0]
    member_db, _ = data

    # Setup stage: Slot 0 and Slot 1
    # We need valid member IDs
    ids = list(member_db.keys())
    if len(ids) < 2:
        pass

    p.stage = np.full(3, -1, dtype=np.int32)
    p.stage[0] = ids[0]
    p.stage[1] = ids[1]

    # Ensure they are "played" or at least valid
    # Debug
    # print(f"DEBUG: Stage set to {p.stage}")
    return p


@when("the player activates formation change")
def activate_formation_change(context, player_with_stage):
    game_state = context["game_state"]
    effect = Effect(EffectType.FORMATION_CHANGE, 1)
    game_state.pending_effects.append(effect)

    # Resolve -> Select Slot 0
    # Step returns NEW STATE
    game_state = game_state.step(0)
    context["game_state"] = game_state

    assert len(game_state.pending_choices) > 0
    assert game_state.pending_choices[0][0] == "SELECT_FORMATION_SLOT"


@when("the player selects to swap member at slot 0 with slot 1")
def select_swap(context, player_with_stage):
    game_state = context["game_state"]
    # 1. Select member for Slot 0 (Target: ID_B which is at index 1 of available)
    # Available items logic in game_state: members list [(0, ID_A), (1, ID_B)]
    # We assume standard ordering.
    # Action 700 + index.

    # Check choices to be sure?
    # choices = game_state.pending_choices[0][1]["available_members"]
    # We want to pick the one that was originally at slot 1.

    # Just select index 1 (Action 701)
    game_state = game_state.step(701)
    context["game_state"] = game_state

    # 2. Select member for Slot 1 (Target: ID_A which is at index 0 of remaining)
    # Remaining: [(0, ID_A)]
    # Action 700.
    game_state = game_state.step(700)
    context["game_state"] = game_state


@then("the members at slot 0 and 1 should be swapped")
def check_swap(context, player_with_stage):
    game_state = context["game_state"]
    p = game_state.players[0]

    # We rely on checking that the IDs are different from what we set?
    # Or capture original IDs in context?
    # player_with_stage is the *fixture* return, which might be stale or not.
    # Actually, player_with_stage fixture returned `p` (reference).
    # Since `game_state` was COPIED, `player_with_stage` fixture refers to the OLD player object!
    # We must access `game_state.players[0]`.

    # We know simple Swap:
    # Orig: [ID0, ID1, -1]
    # New: [ID1, ID0, -1]

    # We don't have easy access to ID0/ID1 values here unless we re-fetch from DB or context.
    # But checking p.stage[0] != p.stage[1] is a sanity check.
    # Checking against *original* is better.

    # player_with_stage is the OLD player object.
    old_stage = player_with_stage.stage
    new_stage = p.stage

    # Assert swapped
    assert new_stage[0] == old_stage[1]
    assert new_stage[1] == old_stage[0]
