import numpy as np
import pytest

from engine.game.game_state import GameState, MemberCard, Phase
from engine.models.ability import Effect, EffectType, TargetType


@pytest.fixture
def game_state():
    state = GameState()
    state.phase = Phase.MAIN
    state.current_player = 0
    p0 = state.players[0]
    p0.hand = [101]

    # Place 3 members on stage
    p0.stage[0] = 10  # Left
    p0.stage[1] = 20  # Center
    p0.stage[2] = 30  # Right

    # Mock member DB
    for cid in [10, 20, 30, 101]:
        # Create a basic MemberCard.
        # Note: If specific behaviors are needed (like total_hearts), ensure MemberCard has them or mock appropriately.
        # The original test used a MockMember class. We'll use MemberCard and ensure it has defaults.
        # MemberCard is a dataclass, so we just instantiate it.
        state.member_db[cid] = MemberCard(
            card_id=cid,
            card_no=f"TEST-{cid}",
            name=f"Member {cid}",
            cost=1,
            blades=1,
            hearts=np.zeros(7),
            blade_hearts=np.zeros(7),
        )
    return state


def test_flavor_action_formation_change(game_state):
    print("\n--- Testing Flavor Action (Formation Change) ---")
    state = game_state
    state.players[0]

    # Effect: FLAVOR_ACTION (Trigger Formation Change)
    effect = Effect(
        effect_type=EffectType.FLAVOR_ACTION, value=1, target=TargetType.PLAYER, params={"text": "何が好き？"}
    )

    state.pending_effects.append(effect)
    state._resolve_pending_effect(0)

    # Step 1: Modal Choice "What do you like?"
    print("Checking for Modal Choice...")
    assert state.pending_choices, "Should trigger MODAL choice"
    choice = state.pending_choices[0]
    assert choice[0] == "MODAL", "First choice should be MODAL"
    print(f"Modal Choice: {choice[1]['options']}")

    # Answer "その他" (Other) -> Should trigger FORMATION_CHANGE
    # Triggering choice: action 570 + index(2) = 572
    state._handle_choice(572)

    # Step 2: Formation Change Choice
    print("Checking for Formation Change Choice...")
    assert state.pending_choices, "Should trigger FORMATION choice"
    choice = state.pending_choices[0]
    print(f"Formation Choice: {choice}")
    assert choice[0] == "CHOOSE_FORMATION"

    # Note: The original test ended here with a pass, acknowledging unfinished logic.
    # We maintain that behavior.
