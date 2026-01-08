
import sys
import os
import numpy as np

# Add CWD to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.game_state import GameState, MemberCard, LiveCard
from game.ability import AbilityParser, Ability, ConditionType, EffectType

def debug_honoka():
    print("--- Debug Honoka (PL!-sd1-001-SD) ---")
    
    # 1. Parsing Test
    text = "【登場時】自分の成功ライブカード置き場にカードが2枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。"
    abilities = AbilityParser.parse_ability_text(text)
    
    if len(abilities) != 1:
        print(f"FAIL: Parsed {len(abilities)} abilities, expected 1")
        return
        
    abi = abilities[0]
    cond = abi.conditions[0]
    eff = abi.effects[0]
    
    with open('debug_result.txt', 'w', encoding='utf-8') as f:
        f.write(f"Parsed Condition Value: {cond.type}\n")
        f.write(f"Parsed Condition Name: {cond.type.name}\n")
        f.write(f"Min param: {cond.params.get('min')}\n")
    
    # print(f"Parsed Condition Value: {cond.type}")
    
    if cond.type != ConditionType.COUNT_SUCCESS_LIVE or cond.params.get('min') != 2:
        print("FAIL: Condition type or min param mismatch")
        return
        
    if eff.effect_type != EffectType.RECOVER_LIVE:
        print("FAIL: Effect type mismatch")
        return

    # 2. Execution Test
    print("\n--- Execution Test ---")
    state = GameState()
    p0 = state.players[0]
    
    # Mock DB
    GameState.live_db = {
        200: LiveCard(200, "Live1", 1, np.zeros(7))
    }
    GameState.member_db = {} 
    
    # Case 1: Fail Condition (0 lives)
    print("Checking Condition (0 lives)...")
    res = state._check_condition(p0, cond)
    print(f"Result: {res} (Expected: False)")
    if res: print("FAIL: Should be False")
    
    # Case 2: Pass Condition (2 lives)
    print("Checking Condition (2 lives)...")
    p0.success_lives = [101, 102]
    res = state._check_condition(p0, cond)
    print(f"Result: {res} (Expected: True)")
    if not res: print("FAIL: Should be True")
    
    # Case 3: Effect (Recover Live)
    print("Executing Effect (Recover Live)...")
    p0.discard = [200] # Live card
    state.pending_effects.append(eff)
    state._resolve_pending_effect(0)
    
    if not state.pending_choices:
        print("FAIL: No choices generated")
    else:
        choice = state.pending_choices[0]
        print(f"Generated Choice: {choice[0]}")
        params = choice[1]
        print(f"Filter: {params.get('filter')}")
        print(f"Cards: {params.get('cards')}")
        
        if choice[0] == "SELECT_FROM_DISCARD" and params.get('filter') == 'live' and 200 in params.get('cards'):
            print("SUCCESS: Effect logic correct")
        else:
            print("FAIL: Choice params incorrect")

if __name__ == "__main__":
    debug_honoka()
