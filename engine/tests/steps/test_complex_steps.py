import numpy as np
from pytest_bdd import given, parsers, scenarios, then, when

from engine.game.game_state import MemberCard
from engine.models.ability import Ability, Effect, EffectType, TriggerType

scenarios("../features/complex.feature")


@given(parsers.parse('a player has a "Complex Member" with ability "Order -> Tap -> Draw"'))
def setup_complex_member(context, game_state):
    p = game_state.players[0]
    mid = 888

    complex_ability = Ability(
        raw_text="Test Ability",
        trigger=TriggerType.ACTIVATED,
        effects=[
            Effect(EffectType.ORDER_DECK, 2, params={"position": "bottom", "shuffle": True}),
            Effect(EffectType.TAP_OPPONENT, 1),
            Effect(EffectType.DRAW, 1),
        ],
        costs=[],
    )

    m = MemberCard(
        card_id=mid,
        card_no="TEST-888",
        name="Complex Test Card",
        cost=1,
        groups=[],
        hearts=np.zeros(6),
        blade_hearts=np.zeros(7),
        blades=1,
        abilities=[complex_ability],
    )
    game_state.member_db[mid] = m
    p.stage[0] = mid
    return m


@given("the opponent has a member on stage at slot 0")
def setup_opponent_member(context, game_state):
    opp = game_state.players[1]
    mid = 999
    # Ensure in DB
    if mid not in game_state.member_db:
        game_state.member_db[mid] = MemberCard(
            card_id=mid,
            card_no="OPP-01",
            name="Opponent",
            cost=1,
            groups=[],
            hearts=np.zeros(6),
            blade_hearts=np.zeros(7),
            blades=1,
        )

    opp.stage[0] = mid
    opp.tapped_members[0] = False


@given("the player's deck has 5 cards")
def setup_deck_5(context, game_state):
    p = game_state.players[0]
    p.main_deck = [10, 20, 30, 40, 50]


@when('the player activates the ability of "Complex Member"')
def activate_complex(context, game_state):
    # Action 200 = Activate Slot 0
    game_state = game_state.step(200)
    context["game_state"] = game_state


@then("the player should be prompted to select an opponent member")
def check_prompt_opponent(context, game_state):
    current_state = context["game_state"]
    assert len(current_state.pending_choices) > 0
    assert current_state.pending_choices[0][0] == "TARGET_OPPONENT_MEMBER"


@then(parsers.parse('the pending effects should contain "{effect_name}"'))
def check_pending_effect_contain(context, game_state, effect_name):
    current_state = context["game_state"]
    # effect types are enums. name property gives string.
    names = [e.effect_type.name for e in current_state.pending_effects]
    assert effect_name in names


@when("the player selects the opponent member at slot 0")
def select_opponent(context, game_state):
    # Action 600 = Target Opponent Slot 0
    current_state = context["game_state"]
    current_state = current_state.step(600)
    context["game_state"] = current_state


@then("the opponent member at slot 0 should be tapped")
def check_opponent_tapped(context, game_state):
    current_state = context["game_state"]
    opp = current_state.players[1]
    assert opp.tapped_members[0]  # Boolean truthiness check is safer for numpy


@then("the player should draw 1 card")
def check_draw_1(context, game_state):
    # Check hand size increased by 1 from initial?
    # Initial hand size was?
    # generic setup usually clears hand unless specified.
    # We didn't set hand size explicitly, so it's empty (generic `player_with_deck` not used here, we manually set main_deck).
    # Hand is empty by default in GameState? No, `init_game` sets it?
    # `GameState()` constructor initializes empty hand.
    # So expected 1.
    current_state = context["game_state"]
    p = current_state.players[0]
    assert len(p.hand) == 1


@then("the pending effects should be empty")
def check_pending_empty(context, game_state):
    current_state = context["game_state"]
    assert len(current_state.pending_effects) == 0
