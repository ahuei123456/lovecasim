import numpy as np

from engine.game.game_state import GameState, MemberCard, Phase
from engine.models.ability import Ability, AbilityCostType, Cost, TriggerType


def test_activated_ability():
    print("Testing Activated Ability and Targeting...")

    state = GameState()

    # Setup card with activated ability: "Discard 1 card from hand"
    ability = Ability(
        raw_text="起動: 手札を1枚捨てる",
        trigger=TriggerType.ACTIVATED,
        costs=[Cost(AbilityCostType.DISCARD_HAND, 1)],
        effects=[],  # No effect for this test, just cost payment
    )

    # Mock Member
    card = MemberCard(
        card_id=1,
        card_no="TEST-01",
        name="TestCard",
        cost=1,
        hearts=np.zeros(6),
        blade_hearts=np.zeros(7),
        blades=1,
        abilities=[ability],
    )

    GameState.member_db = {1: card}

    p0 = state.players[0]
    p0.stage[0] = 1  # Card on stage

    # Give hand cards to pay cost
    p0.hand = [101, 102]
    # Add dummy 101/102
    GameState.member_db[101] = MemberCard(101, "D-01", "Dummy", 1, np.zeros(6), np.zeros(7), 1)
    GameState.member_db[102] = MemberCard(102, "D-02", "Dummy", 1, np.zeros(6), np.zeros(7), 1)

    # Add dummy card to main deck to prevent auto-refresh IndexError
    p0.main_deck = [999]
    GameState.member_db[999] = MemberCard(999, "D-99", "DeckDummy", 1, np.zeros(6), np.zeros(7), 1)

    state.phase = Phase.MAIN

    # 1. Activate Ability
    # Action ID for activating ability of member at slot 0: 200 + 0 = 200
    legal = state.get_legal_actions()
    assert legal[200], f"Action 200 should be legal. Legal actions: {[i for i, x in enumerate(legal) if x]}"

    state = state.step(200)
    p0 = state.players[0]

    # 2. Should Trigger Cost Payment (Target Hand)
    assert len(state.pending_choices) > 0, "Should have pending choice for cost"
    choice = state.pending_choices[0]
    assert choice[0] == "TARGET_HAND"

    # 3. Select card to discard
    # TARGET_HAND actions: 500 + index
    # Discard first card (index 0) -> Action 500
    state = state.step(500)
    p0 = state.players[0]

    # 4. Verify Discard
    assert 101 in p0.discard, "Card 101 should be discarded"
    assert len(p0.hand) == 1, "Hand size should decr to 1"
