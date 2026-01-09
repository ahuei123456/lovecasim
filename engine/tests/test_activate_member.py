"""
Unit test for interactive ACTIVATE_MEMBER mechanic.
"""


import pytest
import numpy as np
from engine.game.game_state import GameState, MemberCard
from engine.game.ability import AbilityParser, EffectType, Effect

@pytest.fixture
def game_state():
    state = GameState()
    p0 = state.players[0]
    
    # Setup p0 with members
    state.member_db[100] = MemberCard(card_id=100, card_no="TEST-01", name="MyMem0", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(7), blades=1)
    state.member_db[101] = MemberCard(card_id=101, card_no="TEST-02", name="MyMem1", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(7), blades=1)
    
    p0.stage[0] = 100
    p0.stage[1] = 101
    # slot 0 is tapped, slot 1 is active
    p0.tapped_members = [True, False, False]
    return state

def test_parser_activate_member():
    """Card #29: 自分のメンバーを1人選び、アクティブにする。"""
    text = "自分のメンバーを1人選び、アクティブにする。"
    abilities = AbilityParser.parse_ability_text(text)
    eff = abilities[0].effects[0]
    
    assert eff.effect_type == EffectType.ACTIVATE_MEMBER

def test_execution_activate_member(game_state):
    """Test interactive activation of a tapped member"""
    state = game_state
    p0 = state.players[0]
    eff = Effect(EffectType.ACTIVATE_MEMBER, 1)
    
    # Player 0 resolves effect
    state.pending_effects.append(eff)
    state._resolve_pending_effect(0)
    
    # Should have choice to target member
    assert len(state.pending_choices) == 1
    choice_type, params = state.pending_choices[0]
    assert choice_type == "TARGET_MEMBER"
    assert params['effect'] == "activate"
    
    # In get_legal_actions, only slot 0 should be legal (slot 1 is already active)
    legal = state.get_legal_actions()
    assert legal[560] # Slot 0 (Tapped)
    assert not legal[561] # Slot 1 (Active)
    assert not legal[562] # Slot 2 (Empty)
    
    # Simulate choosing member at slot 0 (action 560)
    state.take_action(560)
    
    # Verify slot 0 is now active
    assert not p0.tapped_members[0]
