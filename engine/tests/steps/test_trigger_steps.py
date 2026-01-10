import numpy as np
from pytest_bdd import given, parsers, scenarios, then, when

from engine.game.game_state import MemberCard
from engine.models.ability import Ability, AbilityCostType, Cost, Effect, EffectType, TargetType, TriggerType

scenarios("../features/triggers.feature")


@given('the player has a member "Shizuku" with an optional discard cost ability')
def setup_shizuku(context, game_state):
    p = game_state.players[0]

    # Create Shizuku member
    mid = 777
    shizuku = MemberCard(
        card_id=mid,
        card_no="SZ-01",
        name="Shizuku",
        cost=1,
        groups=[],
        hearts=np.zeros(6),
        blade_hearts=np.zeros(7),
        blades=1,
    )

    # Add ability: Discard 1 (Optional) -> Recover Live
    abi = Ability(
        raw_text="Test Shizuku",
        trigger=TriggerType.ACTIVATED,  # Using ACTIVATED for manual trigger in test
        costs=[Cost(AbilityCostType.DISCARD_HAND, 1, is_optional=True)],
        effects=[Effect(EffectType.RECOVER_LIVE, 1, TargetType.CARD_DISCARD, {"group": "Niji"})],
    )
    shizuku.abilities.append(abi)

    game_state.member_db[mid] = shizuku
    p.stage[0] = mid

    # Needs discard for RECOVER_LIVE not to fail logic?
    # Actually if cost skipped, effect won't run.
    context["shizuku_id"] = mid


@when('the player activates the ability of "Shizuku"')
def activate_shizuku(context, game_state):
    # Action 200 = Activate ability of Member at Slot 0
    # (200 + area)
    game_state = game_state.step(200)
    context["game_state"] = game_state


@then("the choice should be optional")
def check_optional_choice(context, game_state):
    current_state = context["game_state"]
    choice = current_state.pending_choices[0]
    params = choice[1]
    # Check if params has is_optional=True
    # Currently engine mismatch: engine doesn't set it yet. Expect failure.
    assert params.get("is_optional") is True, f"Choice params {params} should have is_optional=True"


@when("the player chooses to skip the optional cost")
def skip_optional_cost(context, game_state):
    current_state = context["game_state"]
    # Verify action 0 is legal?
    actions = current_state.get_legal_actions()
    assert actions[0], "Action 0 (SKIP) should be legal"

    current_state = current_state.step(0)
    context["game_state"] = current_state


@then(parsers.parse("the player's hand size should remain {count:d}"))
def check_hand_remain(context, game_state, count):
    current_state = context["game_state"]
    p = current_state.players[0]
    assert len(p.hand) == count


@then("the ability effects should not execute")
def check_no_effect(context, game_state):
    current_state = context["game_state"]
    # Check pending effects are empty
    assert len(current_state.pending_effects) == 0
    # Check pending choices are empty
    assert len(current_state.pending_choices) == 0
