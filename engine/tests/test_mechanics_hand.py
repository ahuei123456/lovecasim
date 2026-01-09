
import pytest
from engine.game.game_state import GameState, PlayerState
from engine.game.ability import AbilityParser, EffectType

@pytest.fixture
def game_state():
    state = GameState()
    p0 = state.players[0]
    # Ensure p0 has cards
    p0.hand = [101, 102, 103] # Mock card IDs
    p0.main_deck = [201, 202, 203, 204, 205]
    return state

def test_swap_cards_draw_discard(game_state):
    # "2枚引き、手札を1枚控え室に置く。"
    state = game_state
    p0 = state.players[0]
    text = "2枚引き、手札を1枚控え室に置く。"
    abilities = AbilityParser.parse_ability_text(text)
    
    assert len(abilities) > 0
    effects = abilities[0].effects
    
    # Expecting: Draw 2, then Swap(Discard) 1
    has_draw = False
    has_discard = False
    
    for eff in effects:
        if eff.effect_type == EffectType.DRAW:
            assert eff.value == 2
            has_draw = True
        elif eff.effect_type == EffectType.SWAP_CARDS:
            assert eff.value == 1
            assert eff.params.get('from') == 'hand'
            assert eff.params.get('target') == 'discard'
            has_discard = True
            
    assert has_draw, "Parser should find Draw effect"
    assert has_discard, "Parser should find Discard (Swap) effect"
    
    # Test Execution
    # Manually trigger effects on state
    initial_hand = len(p0.hand) # 3
    initial_deck = len(p0.main_deck) # 5
    
    # 1. Execute Draw
    draw_eff = next(e for e in effects if e.effect_type == EffectType.DRAW)
    state.pending_effects.append(draw_eff)
    state._resolve_pending_effect(0)
    
    assert len(p0.hand) == initial_hand + 2
    assert len(p0.main_deck) == initial_deck - 2
    
    # 2. Execute Discard
    # This should trigger a Pending Choice
    discard_eff = next(e for e in effects if e.effect_type == EffectType.SWAP_CARDS)
    state.pending_effects.append(discard_eff)
    state._resolve_pending_effect(0)
    
    assert len(state.pending_choices) > 0, "Should trigger a pending choice for discard"
    choice_type, params = state.pending_choices[-1]
    assert choice_type == "DISCARD_SELECT"
    assert params['count'] == 1
    
    # 3. Resolve Choice (Simulate user picking the first card)
    # Assuming we implement _handle_choice for DISCARD_SELECT
    # We need mock card indices. Hand size is now 3+2=5. Indices 0-4.
    # Let's discard idx 0 (card 101)
    
    # Depending on how choice is handled, maybe action input? 
    # For this test, we might need to manually call the choice handler if it's internal private
    # But let's assume valid action flow if possible, or direct method call.
    # self.state._handle_choice(0) # Logic for choice resolution
    pass 

def test_look_deck(game_state):
    # "山札の上から3枚見て、その中から1枚を手札に加え、残りを山札の下に置く。"
    state = game_state
    p0 = state.players[0]
    text = "山札の上から3枚見て、その中から1枚を手札に加え、残りを山札の下に置く。"
    abilities = AbilityParser.parse_ability_text(text)
    effects = abilities[0].effects
    
    # Verify Parser
    look_eff = next(e for e in effects if e.effect_type == EffectType.LOOK_DECK)
    assert look_eff.value == 3
    
    choose_eff = next(e for e in effects if e.effect_type == EffectType.LOOK_AND_CHOOSE)
    
    # Execution
    # 1. Look Deck
    state.pending_effects.append(look_eff)
    state._resolve_pending_effect(0)
    
    assert len(state.looked_cards) == 3
    assert len(p0.main_deck) == 2 # Started with 5
    
    # 2. Look and Choose
    state.pending_effects.append(choose_eff)
    state._resolve_pending_effect(0)
    
    assert len(state.pending_choices) > 0
    choice = state.pending_choices[-1]
    assert choice[0] == "SELECT_FROM_LIST"
    assert len(choice[1]['cards']) == 3
