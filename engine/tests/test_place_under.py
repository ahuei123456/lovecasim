import numpy as np
import pytest

from engine.game.ability import Effect, EffectType, TargetType
from engine.game.game_state import GameState, MemberCard, Phase


@pytest.fixture
def game_state():
    state = GameState()
    state.phase = Phase.MAIN
    state.current_player = 0
    p0 = state.players[0]
    p0.hand = [101, 102, 103]
    # Place a member on stage (Area 0)
    p0.stage[0] = 10

    # Member DB entry using MemberCard dataclass
    state.member_db[10] = MemberCard(
        card_id=10,
        card_no="TEST-10",
        name="Test Member",
        cost=1,
        group="Test",
        blades=1,
        hearts=np.zeros(7),
        blade_hearts=np.zeros(7),
    )
    return state


def test_place_under_self(game_state):
    print("\n--- Testing Place Under Self ---")
    state = game_state
    p0 = state.players[0]

    # Effect: Place 1 card from hand under Self
    effect = Effect(effect_type=EffectType.PLACE_UNDER, value=1, target=TargetType.MEMBER_SELF, params={"from": "hand"})

    # Manually resolving with context (Area 0)
    state.pending_effects.append(effect)
    state._resolve_pending_effect(0, context={"area": 0})

    # Expect Choice: TARGET_HAND
    assert state.pending_choices, "Should trigger TARGET_HAND choice"
    choice = state.pending_choices[0]
    print(f"Choice: {choice}")
    assert choice[0] == "TARGET_HAND"
    assert choice[1]["effect"] == "place_under"
    assert choice[1]["target_area"] == 0

    # Execute choice: Pick first card (101)
    # Action ID for TARGET_HAND 0 is 500 + 0 = 500
    state._handle_choice(500)

    # Verify card 101 is now in stage_energy[0]
    assert 101 in p0.stage_energy[0]
    assert 101 not in p0.hand
    print(f"Stage Energy[0]: {p0.stage_energy[0]}")
