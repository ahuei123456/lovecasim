import numpy as np
from pytest_bdd import given, parsers, scenarios, then, when

from engine.game.game_state import GameState
from engine.models.ability import Effect, EffectType
from engine.models.card import LiveCard, MemberCard
from engine.models.enums import Group

scenarios("../features/recovery.feature")

# --- Fixtures & Givens ---


@given("a player with a discard pile", target_fixture="player_with_discard")
def player_with_discard(context, game_state):
    p = game_state.players[0]
    p.hand = []
    p.discard = []
    context["initial_hand_size"] = 0
    return p


@given(parsers.parse('the discard pile contains a live card "{name}" with ID {cid:d}'))
def add_live_to_discard(context, game_state, data, name, cid):
    p = game_state.players[0]
    _, live_db = data

    # Create simple live card if not in DB
    if cid not in live_db:
        # Create a mock/real live card
        # We need to insert it into the DB fixture?
        # The data fixture loads from JSON. We can monkeypatch into the generic DB.
        # Use real LiveCard
        live_db[cid] = LiveCard(
            card_id=cid,
            card_no=f"LIVE-{cid}",
            name=name,
            score=1000,
            required_hearts=np.zeros(7),
            abilities=[],
            groups=[],
            units=[],
            img_path="",
        )

    p.discard.append(cid)
    context[f"card_id_{name}"] = cid


@given(parsers.parse('the discard pile contains a member card "{name}" with ID {cid:d}'))
def add_member_to_discard(context, game_state, data, name, cid):
    p = game_state.players[0]
    member_db, _ = data

    # Create mock/real member
    if cid not in member_db:
        member_db[cid] = MemberCard(
            card_id=cid,
            card_no=f"TEST-{cid}",
            name=name,
            cost=1,
            groups=[],
            hearts=np.zeros(6),
            blade_hearts=np.zeros(7),
            blades=1,
        )

    p.discard.append(cid)
    context[f"card_id_{name}"] = cid


@given("the discard pile contains the following members:")
def add_members_table(context, game_state, data, datatable):
    # p = game_state.players[0]
    member_db, _ = data

    # datatable is a list of rows (if supported by pytest-bdd table parser)?
    # Actually pytest-bdd "datatable" usually comes from Examples or manual parsing if step uses "datatable" param name?
    # No, generic steps don't support table automatically unless parsed.
    # We should use `scenarios` and `parsers` carefully or manual table parsing.
    # For now, we assume simple step implementation parsing context logic manually or using simple loop if possible?
    # Actually, allow `datatable` or similar logic.
    # Wait, BDD standard step doesn't pass a table object unless specifically configured.
    # I'll manually parse headings if needed, but `pytest-bdd` doesn't pass table in step args automatically like Behave.
    # I'll implement it by parsing row by row or assume the step handles setup manually?
    # Ah, pytest-bdd uses `target_fixture` or we access `request`?
    # Actually, simpler: just iterate in the test code? No.
    # I will replace the datatable step with individual "And" steps in the feature file if I can't easily parse table.
    # BUT, I want to learn. Let's use simple multiple "And" steps or parse distinct lines.
    # Actually, let's keep it simple for now and use specific step setups in the feature, or handle dict-like parsing?
    # I'll use a simplified implementation where I define specific members in the python code matching the scenario.

    # Let's pivot: The step definition will just setup specific hardcoded data for this scenario "Recover a member with filters".
    # Or I can use `parsers.parse`? No.
    # I'll implement "the discard pile contains the following members:" but the datatable handling is tricky.
    # I'll rewrite the feature to be explicit step-by-step to avoid table parsing complexity in `pytest-bdd`.
    pass


# Simplified step for the specific scenario
@given("the discard pile contains the test members for filtering")
def add_test_members_filtering(context, game_state, data):
    p = game_state.players[0]
    member_db, _ = data

    members = [
        (400, "Kotori", "μ's", 3),
        (401, "Honoka", "μ's", 5),
        (402, "Chika", "Aqours", 2),
    ]

    for cid, name, group, cost in members:
        member_db[cid] = MemberCard(
            card_id=cid,
            card_no=f"TEST-{cid}",
            name=name,
            cost=cost,
            groups=[Group.from_japanese_name(group)],
            hearts=np.zeros(6),
            blade_hearts=np.zeros(7),
            blades=1,
        )
        p.discard.append(cid)
        context[f"card_id_{name}"] = cid


# --- Whhen steps ---


@when("the player activates an effect to recover a live card")
def activate_recover_live(context, game_state):
    p = game_state.players[0]
    print(f"DEBUG: Discard before recovery: {p.discard}")
    print(f"DEBUG: LiveDB keys: {list(GameState.live_db.keys())}")
    print(f"DEBUG: Checking discard: {[cid in GameState.live_db for cid in p.discard]}")

    effect = Effect(EffectType.RECOVER_LIVE, 1)
    game_state.pending_effects.append(effect)

    # Check pending
    print(f"DEBUG: Pending effects: {game_state.pending_effects}")

    print(f"DEBUG: Post-step pending choices: {game_state.pending_choices}")


@when("the player activates an effect to recover a member card")
def activate_recover_member(context, game_state):
    effect = Effect(EffectType.RECOVER_MEMBER, 1)
    game_state.pending_effects.append(effect)
    game_state = game_state.step(0)
    context["game_state"] = game_state


@when(parsers.parse('the player activates an effect to recover a member with group "{group}" and max cost {cost:d}'))
def activate_recover_filtered(context, game_state, group, cost):
    effect = Effect(EffectType.RECOVER_MEMBER, 1, params={"group": group, "cost_max": cost})
    game_state.pending_effects.append(effect)
    game_state = game_state.step(0)
    context["game_state"] = game_state


@when(parsers.parse('the player selects "{name}" from the recovery choices'))
def select_card_by_name(context, game_state, name):
    current_state = context["game_state"]
    cid = context[f"card_id_{name}"]

    # Validate choice exists
    assert len(current_state.pending_choices) > 0
    choice = current_state.pending_choices[0]
    assert choice[0] == "SELECT_FROM_DISCARD"

    available = choice[1]["cards"]
    assert cid in available, f"Card {name} ({cid}) not in available choices {available}"

    idx = available.index(cid)
    # Action 660 + index
    current_state = current_state.step(660 + idx)
    context["game_state"] = current_state


# --- Then steps ---


@then(parsers.parse('"{name}" should be in the player\'s hand'))
def check_in_hand_named(context, game_state, name):
    current_state = context["game_state"]
    p = current_state.players[0]
    cid = context[f"card_id_{name}"]
    assert cid in p.hand


@then(parsers.parse('"{name}" should not be in the player\'s discard'))
def check_not_in_discard_named(context, game_state, name):
    current_state = context["game_state"]
    p = current_state.players[0]
    cid = context[f"card_id_{name}"]
    assert cid not in p.discard


@then(parsers.parse('the recovery choices should include "{name}"'))
def check_choice_includes(context, game_state, name):
    current_state = context["game_state"]
    cid = context[f"card_id_{name}"]
    choice = current_state.pending_choices[0]
    available = choice[1]["cards"]
    assert cid in available


@then(parsers.parse('the recovery choices should not include "{name}"'))
def check_choice_excludes(context, game_state, name):
    current_state = context["game_state"]
    cid = context[f"card_id_{name}"]
    choice = current_state.pending_choices[0]
    available = choice[1]["cards"]
    assert cid not in available
