import sys
import os
sys.path.append(os.getcwd())
from game.ability import AbilityParser, ConditionType, EffectType, TriggerType

def test_heart_colors():
    text = "{{live_start.png|ライブ開始時}} {{heart_04.png|heart04}}を持つカードがあれば..."
    abilities = AbilityParser.parse_ability_text(text)
    print(f"Text: {text}")
    for ab in abilities:
        print(f"  Trigger: {ab.trigger}")
        for cond in ab.conditions:
            print(f"  Condition: {cond.type} {cond.params}")
        if any(c.type == ConditionType.HAS_COLOR and c.params.get('color') == '黄' for c in ab.conditions):
            print("  SUCCESS: Heart04 mapped to Yellow")
        else:
            print("  FAILURE: Heart04 not found")

def test_zone_propagation():
    text = "{{toujyou.png|登場}}自分の控え室からメンバーカードを1枚手札に加える。"
    abilities = AbilityParser.parse_ability_text(text)
    print(f"\nText: {text}")
    for ab in abilities:
        for eff in ab.effects:
            print(f"  Effect: {eff.effect_type} Params: {eff.params}")
            if eff.params.get('from') == 'discard':
                print("  SUCCESS: Zone 'discard' propagated to effect")
            else:
                print("  FAILURE: Zone context lost")

if __name__ == "__main__":
    test_heart_colors()
    test_zone_propagation()
