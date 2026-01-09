import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.ability import AbilityParser, TriggerType, EffectType, ConditionType, TargetType

def test_group_propagation():
    """Test that group names in conditions propagate to effects."""
    text = "{{toujyou.png|登場}}自分の控え室からコスト4以下の『Aqours』のメンバーカードを1枚手札に加える。"
    print(f"\n--- Testing Group Propagation ---")
    print(f"Text: {text}")
    abilities = AbilityParser.parse_ability_text(text)
    assert len(abilities) == 1
    ability = abilities[0]
    
    print(f"Parsed Ability Trigger: {ability.trigger.name}")
    for i, eff in enumerate(ability.effects):
        print(f"Effect {i}: Type={eff.effect_type.name}, Target={eff.target.name}, Params={eff.params}")
    for i, cond in enumerate(ability.conditions):
        print(f"Condition {i}: Type={cond.type.name}, Params={cond.params}")

    # Check if 'group' is in effect params
    found_group = False
    for effect in ability.effects:
        if effect.params.get('group') == 'Aqours':
            found_group = True
            break
    
    if not found_group:
        print("FAIL: Group 'Aqours' not found in any effect params.")
    else:
        print("PASS: Group 'Aqours' found in effect params.")
    
    assert found_group, "Group 'Aqours' should have propagated to effect params"

def test_score_compare_condition():
    """Test detection of score comparison conditions."""
    text = "{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高く、かつ自分のステージに『蓮ノ空』のメンバーがいる場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。"
    print(f"\n--- Testing Score Comparison ---")
    print(f"Text: {text}")
    abilities = AbilityParser.parse_ability_text(text)
    assert len(abilities) == 1
    ability = abilities[0]
    
    for i, cond in enumerate(ability.conditions):
        print(f"Condition {i}: Type={cond.type.name}, Params={cond.params}")

    # Check for SCORE_COMPARE condition
    score_comp = [c for c in ability.conditions if c.type == ConditionType.SCORE_COMPARE]
    if not score_comp:
        print("FAIL: SCORE_COMPARE condition not found.")
    else:
        print(f"PASS: SCORE_COMPARE found with params: {score_comp[0].params}")
    
    assert len(score_comp) > 0
    assert score_comp[0].params['comparison'] == 'GT'
    assert score_comp[0].params['target'] == 'opponent'

def test_choice_detection():
    """Test that choice keywords are detected and flagged."""
    text = "{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。"
    print(f"\n--- Testing Choice Detection ---")
    print(f"Text: {text}")
    abilities = AbilityParser.parse_ability_text(text)
    assert len(abilities) == 1
    ability = abilities[0]
    
    for i, cond in enumerate(ability.conditions):
        print(f"Condition {i}: Type={cond.type.name}, Params={cond.params}")

    # Check for HAS_CHOICE condition
    choice_cond = [c for c in ability.conditions if c.type == ConditionType.HAS_CHOICE]
    if not choice_cond:
        print("FAIL: HAS_CHOICE condition not found.")
    else:
        print("PASS: HAS_CHOICE found.")
    
    assert len(choice_cond) > 0

def test_tap_opponent_variants():
    """Test various tap opponent phrases."""
    print(f"\n--- Testing Tap Opponent Variants ---")
    texts = [
        "相手はウェイトにする。",
        "相手1人を休みにする。",
        "相手全員をウェイトにする。"
    ]
    for text in texts:
        print(f"Text: {text}")
        abilities = AbilityParser.parse_ability_text(text)
        found = any(e.effect_type == EffectType.TAP_OPPONENT for e in abilities[0].effects)
        if not found:
            print(f"FAIL: TAP_OPPONENT not found in effects: {[e.effect_type.name for e in abilities[0].effects]}")
        else:
            print("PASS: TAP_OPPONENT found.")
        assert found, f"Failed to detect TAP_OPPONENT in: {text}"

if __name__ == "__main__":
    try:
        test_group_propagation()
        test_score_compare_condition()
        test_choice_detection()
        test_tap_opponent_variants()
        print("\n" + "="*30)
        print("✓ All parser accuracy tests passed!")
        print("="*30)
    except AssertionError as e:
        print(f"\nFATAL: Test Failed: {e}")
        sys.exit(1)
