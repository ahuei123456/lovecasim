
import sys
import os
import numpy as np

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState, Phase, MemberCard, LiveCard, PlayerState
from game.ability import AbilityParser, Ability, TriggerType, Effect, EffectType, TargetType

def test_generic_modal():
    print("Testing Generic Modal (SELECT_MODE)...")
    
    # "登場：以下から1つを選ぶ。・1枚引く。・ブレードを1得る。"
    text = "登場以下から1つを選ぶ。\\n・1枚引く。\\n・ブレードを2得る。"
    abilities = AbilityParser.parse_ability_text(text)
    
    assert len(abilities) == 1
    assert abilities[0].effects[0].effect_type == EffectType.SELECT_MODE
    assert len(abilities[0].modal_options) == 2, f"Expected 2 options, got {len(abilities[0].modal_options)}"
    
    # Verify option content
    assert abilities[0].modal_options[0][0].effect_type == EffectType.DRAW
    assert abilities[0].modal_options[1][0].effect_type == EffectType.ADD_BLADES
    
    state = GameState()
    p0 = state.players[0]
    p0.main_deck = [100, 101]
    
    # Manually resolve the effect
    ability = abilities[0]
    effect = ability.effects[0] # SELECT_MODE
    
    # Prepare params with options for _resolve_pending_effect
    effect.params['options'] = ability.modal_options
    
    state.pending_effects.append(effect)
    state = state.step(0) # Logic dummy to trigger resolution
    
    assert len(state.pending_choices) > 0
    assert state.pending_choices[0][0] == "SELECT_MODE"
    
    # Select Option 0 (DRAW)
    state = state.step(270)
    p0 = state.players[0]
    assert len(p0.hand) == 1, "Should have drawn 1 card"
    assert p0.hand[0] == 100
    print("SELECT_MODE resolution (Option 0) PASSED.")

def test_color_select():
    print("\nTesting Color Selection (COLOR_SELECT)...")
    
    text = "ライブ開始時好きなハートの色を1つ指定する。"
    abilities = AbilityParser.parse_ability_text(text)
    
    assert len(abilities) == 1
    assert abilities[0].effects[0].effect_type == EffectType.COLOR_SELECT
    
    state = GameState()
    state.pending_effects.append(abilities[0].effects[0])
    
    # 1. Trigger choice
    state = state.step(0)
    assert len(state.pending_choices) > 0
    assert state.pending_choices[0][0] == "COLOR_SELECT"
    
    # 2. Check mask
    legal = state.get_legal_actions()
    for i in range(280, 286):
        assert legal[i], f"Action {i} should be legal"
        
    # 3. Select Blue (281)
    state = state.step(281)
    # Output check (logs "Player 0 selected color: 青")
    print("COLOR_SELECT masking and resolution PASSED.")

if __name__ == "__main__":
    test_generic_modal()
    test_color_select()
    print("\nAll Generic Modal Tests PASSED!")
