import numpy as np
from pytest_bdd import given, parsers, scenarios, then, when

from engine.game.game_state import MemberCard
from engine.models.ability import Effect, EffectType, TargetType

scenarios("../features/placement.feature")


@given(parsers.parse("a player with a member on stage at slot {slot:d}"), target_fixture="player_with_stage_slot")
def player_with_stage_slot(context, game_state, data, slot):
    p = game_state.players[0]
    member_db, _ = data

    # Ensure a member exists in DB
    mid = 10
    if mid not in member_db:
        member_db[mid] = MemberCard(
            card_id=mid,
            card_no="TEST-10",
            name="Test Member",
            cost=1,
            groups=[],
            hearts=np.zeros(6),
            blade_hearts=np.zeros(7),
            blades=1,
        )

    p.stage[slot] = mid
    return p


@when(
    parsers.parse("the player activates an effect to place {count:d} card from hand under the member at slot {slot:d}")
)
def activate_place_under(context, game_state, count, slot):
    # Simulating activation from the member at `slot` (TargetType.MEMBER_SELF)
    effect = Effect(
        effect_type=EffectType.PLACE_UNDER, value=count, target=TargetType.MEMBER_SELF, params={"from": "hand"}
    )

    game_state.pending_effects.append(effect)

    # Resolve with context "area": slot
    # Note: access private _resolve_pending_effect or rely on logic?
    # Usually step(0) resolves pending. But step(0) calls _resolve_pending_effect(0) without extra context unless triggered?
    # BUT logic in game_state._activate_member_ability passes context.
    # Here we are manually pushing effect. We need to pass context.
    # We can't easily pass context via step(0) public API.
    # We must call _resolve_pending_effect directly or simulate full activation.
    # Calling internal method is fine for unit test steps.

    game_state._resolve_pending_effect(0, context={"area": slot})

    # The method mutates IN PLACE. No new state return from internal method (usually).
    # Wait, step() logic: new_state = self.copy(); new_state._resolve...
    # If we call on `game_state` fixture which is an instance, it mutates involved objects.
    # We must ensure `context["game_state"]` is updated if we want consistency,
    # but here we are mutating the object referenced by `context["game_state"]` (if shared) or `game_state` fixture.
    # Ideally, `test_generic_steps` stored `gs` in `context`.
    # So `game_state` arg IS `context["game_state"]`? No.
    # `test_generic_steps.py` defines `game_state` fixture.
    # `player_with_stage_slot` uses `game_state` fixture.
    # If we just mutate `game_state` (the fixture instance), it's fine.

    # But wait, did I update `context["game_state"]`?
    # `test_generic_steps` updates `context`.
    # So `context["game_state"]` IS the fixture instance.
    # So direct mutation works.
    pass


@when("the player selects the first card in hand")
def select_first_card(context, game_state):
    # Action 500 + index 0 = 500
    # Use step(500) to ensure full state transition if needed, OR _handle_choice(500).
    # step() returns NEW state.

    game_state = game_state.step(500)
    context["game_state"] = game_state

    # Need to track what was selected
    # Original hand was [100, 101, 102]
    # Selected 100.
    context["selected_card"] = 100


@then(parsers.parse("the selected card should be under the member at slot {slot:d}"))
def check_card_under_member(context, game_state, slot):
    current_state = context["game_state"]
    p = current_state.players[0]
    cid = context["selected_card"]

    assert cid in p.stage_energy[slot]


@then("the selected card should not be in the player's hand")
def check_card_not_in_hand(context, game_state):
    current_state = context["game_state"]
    p = current_state.players[0]
    cid = context["selected_card"]

    assert cid not in p.hand
