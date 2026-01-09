"""
Unit test recovery mechanics (RECOVER_LIVE, RECOVER_MEMBER).
Tests based on real card examples from the 100-card analysis.
"""

import pytest

from engine.game.ability import AbilityParser, Effect, EffectType  # Added Effect explicitly
from engine.game.game_state import GameState


@pytest.fixture
def game_state():
    state = GameState()
    p0 = state.players[0]
    # Setup hand and discard
    p0.hand = [101, 102, 103]
    p0.main_deck = [201, 202, 203, 204, 205]
    
    # Ensure live and member cards are in DB using simple objects
    state.live_db[300] = type('obj', (object,), {'card_id': 300, 'name': 'TestLive'})()
    state.live_db[301] = type('obj', (object,), {'card_id': 301, 'name': 'TestLive2'})()
    state.member_db[400] = type('obj', (object,), {'card_id': 400, 'name': 'TestMember'})()
    state.member_db[401] = type('obj', (object,), {'card_id': 401, 'name': 'TestMember2'})()
    
    # Put them in discard
    p0.discard = [300, 301, 400, 401]
    return state

def test_recover_live_parser():
    """Card #1: 高坂 穂乃果 - RECOVER_LIVE"""
    text = "{{toujyou.png|登場}}自分の成功ライブカード置き場にカードが2枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。"
    
    abilities = AbilityParser.parse_ability_text(text)
    assert len(abilities) > 0, "Should parse at least one ability"
    
    # Find RECOVER_LIVE effect
    has_recover = any(e.effect_type == EffectType.RECOVER_LIVE for e in abilities[0].effects)
    assert has_recover, "Should have RECOVER_LIVE effect"

def test_recover_live_execution(game_state):
    """Test RECOVER_LIVE effect execution"""
    state = game_state
    p0 = state.players[0]
    initial_hand = len(p0.hand)
    initial_discard = len(p0.discard)
    
    # Execute RECOVER_LIVE effect
    effect = Effect(EffectType.RECOVER_LIVE, 1)
    state.pending_effects.append(effect)
    state._resolve_pending_effect(0)
    
    # Should create a SELECT_FROM_DISCARD choice
    assert len(state.pending_choices) == 1
    choice_type, params = state.pending_choices[0]
    assert choice_type == "SELECT_FROM_DISCARD"
    
    # Should offer only live cards from discard
    offered_cards = params['cards']
    assert len(offered_cards) == 2  # 300, 301
    assert all(c in state.live_db for c in offered_cards)
    
    # Simulate player choosing card 300 (action 660)
    state.take_action(660)
    
    # Verify: card moved from discard to hand
    assert 300 in p0.hand
    assert 300 not in p0.discard
    assert len(p0.hand) == initial_hand + 1
    assert len(p0.discard) == initial_discard - 1

def test_recover_member_parser():
    """Card #2: 絢瀬 絵里 - RECOVER_MEMBER"""
    text = "{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。"
    
    abilities = AbilityParser.parse_ability_text(text)
    assert len(abilities) > 0
    
    # Find RECOVER_MEMBER effect
    has_recover = any(e.effect_type == EffectType.RECOVER_MEMBER for e in abilities[0].effects)
    assert has_recover, "Should have RECOVER_MEMBER effect"

def test_recover_member_execution(game_state):
    """Test RECOVER_MEMBER effect execution"""
    state = game_state
    p0 = state.players[0]
    initial_hand = len(p0.hand)
    
    # Execute RECOVER_MEMBER effect
    effect = Effect(EffectType.RECOVER_MEMBER, 1)
    state.pending_effects.append(effect)
    state._resolve_pending_effect(0)
    
    # Should create SELECT_FROM_DISCARD choice
    assert len(state.pending_choices) == 1
    choice_type, params = state.pending_choices[0]
    assert choice_type == "SELECT_FROM_DISCARD"
    
    # Should offer only member cards
    offered_cards = params['cards']
    assert len(offered_cards) == 2  # 400, 401
    assert all(c in state.member_db for c in offered_cards)
    
    # Simulate player choosing card 400 (action 660)
    state.take_action(660)
    
    # Verify recovery
    assert 400 in p0.hand
    assert 400 not in p0.discard
    assert len(p0.hand) == initial_hand + 1
