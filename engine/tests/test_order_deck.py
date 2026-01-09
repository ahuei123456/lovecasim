import pytest

from engine.game.ability import Effect, EffectType, TargetType
from engine.game.game_state import GameState, Phase


@pytest.fixture
def game_state():
    state = GameState()
    state.players[0].main_deck = list(range(10))  # [0, 1, 2, ..., 9] (9 is top)
    state.phase = Phase.MAIN
    state.current_player = 0
    return state


def test_shuffle_deck_top_3(game_state):
    print("\n--- Testing Shuffle Top 3 ---")
    state = game_state
    p0 = state.players[0]
    # [0, 1, ..., 9] -> 0 is Top
    original_deck = p0.main_deck.copy()

    # Effect: Order Deck (Shuffle Top 3)
    effect = Effect(
        effect_type=EffectType.ORDER_DECK,
        value=3,
        target=TargetType.PLAYER,
        params={"shuffle": True, "position": "top"},
    )

    # Apply effect manually
    state.pending_effects.append(effect)
    state._resolve_pending_effect(0)

    new_deck = p0.main_deck

    print(f"Original: {original_deck}")
    print(f"New:      {new_deck}")

    # Verify length unchanged
    assert len(new_deck) == 10

    # Verify bottom 7 are unchanged (indices 3 to 9)
    assert new_deck[3:] == original_deck[3:]

    # Verify top 3 are the same set of cards (indices 0 to 2)
    # Original top 3: [0, 1, 2]
    assert set(new_deck[:3]) == set(original_deck[:3])


def test_shuffle_deck_bottom_3(game_state):
    print("\n--- Testing Shuffle Top 3 to Bottom ---")
    state = game_state
    p0 = state.players[0]
    # Reset deck
    p0.main_deck = list(range(10))
    original_deck = p0.main_deck.copy()  # [0..9]
    top_cards_set = {0, 1, 2}

    # Effect: Shuffle Top 3 and place on bottom
    effect = Effect(
        effect_type=EffectType.ORDER_DECK,
        value=3,
        target=TargetType.PLAYER,
        params={"shuffle": True, "position": "bottom"},
    )

    state.pending_effects.append(effect)
    state._resolve_pending_effect(0)

    new_deck = p0.main_deck
    print(f"Original: {original_deck}")
    print(f"New:      {new_deck}")

    # Verify length
    assert len(new_deck) == 10

    # The top 3 from original should now be at the bottom (indices -3 to end)
    bottom_3 = new_deck[-3:]
    assert set(bottom_3) == top_cards_set

    # The rest should be shifted up
    # Original [3..9] should be at [0..6]
    assert new_deck[:-3] == original_deck[3:]


def test_order_rearrange(game_state):
    print("\n--- Testing Rearrange (No Shuffle) ---")
    state = game_state
    p0 = state.players[0]
    p0.main_deck = list(range(10))

    # Effect: Look at top 3, rearrange
    effect = Effect(
        effect_type=EffectType.ORDER_DECK,
        value=3,
        target=TargetType.PLAYER,
        params={"shuffle": False, "position": "top"},
    )

    state.pending_effects.append(effect)
    state._resolve_pending_effect(0)

    # Expectation: Should trigger SELECT_ORDER choice
    if state.pending_choices:
        print("SUCCESS: Choice triggered for rearranging!")
        choice = state.pending_choices[0]
        print(f"Choice: {choice}")
        assert choice[0] == "SELECT_ORDER"
        assert len(choice[1]["cards"]) == 3

        # Simulate selection (picking index 0 recursively)
        # 1. Pick first card
        state._handle_choice(700 + 0)  # Assuming SELECT_ORDER uses 700+ base

        # 2. Pick next card (index 0 of remaining)
        if state.pending_choices:
            state._handle_choice(700 + 0)

        # 3. Pick last card
        if state.pending_choices:
            state._handle_choice(700 + 0)

        # Deck should be restored
        assert len(p0.main_deck) == 10

    else:
        print("FAILURE: No choice triggered. Effect was a no-op.")
        pytest.fail("Rearrange should trigger choice")
