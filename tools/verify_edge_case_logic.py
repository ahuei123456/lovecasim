import sys
import os
sys.path.append(os.getcwd())

from game.ability import AbilityParser, TriggerType, EffectType, ConditionType, TargetType

def verify():
    test_cases = [
        {
            "id": "LL-PR-004-PR (Merged)",
            "text": "{{live_start.png|ライブ開始時}}相手に何が好き？と聞く。\n回答があなたの場合、自分と相手はカードを1枚引く。",
            "assert": lambda abs: (len(abs) == 1 and 
                                 any(e.effect_type == EffectType.FLAVOR_ACTION for e in abs[0].effects) and 
                                 any(c.type == ConditionType.MODAL_ANSWER for c in abs[0].conditions))
        },
        {
            "id": "Daydream Mermaid (Merged)",
            "text": "{{live_success.png|ライブ成功時}}以下から1つを選ぶ。自分の成功ライブカード置き場に『虹ヶ咲』のカードがある場合、代わりに1つ以上を選ぶ。",
            "assert": lambda abs: abs[0].conditions[0].params.get('zone') == 'SUCCESS_LIVE'
        },
        {
            "id": "Optionality Test",
            "text": "カードを1枚引いてもよい。",
            "assert": lambda abs: abs[0].effects[0].is_optional == True
        },
        {
            "id": "Once Per Turn Test",
            "text": "1ターンに1回、カードを1枚引く。",
            "assert": lambda abs: abs[0].is_once_per_turn == True
        },
        {
            "id": "Global Test",
            "text": "相手のステージにいるすべてのメンバーをウェイトにする。",
            "assert": lambda abs: abs[0].effects[0].params.get('all') == True
        },
        {
            "id": "Color Icon Test",
            "text": "{{icon_red.png|赤}}のメンバーがいる場合",
            "assert": lambda abs: any(c.type == ConditionType.HAS_COLOR and c.params['color'] == '赤' for c in abs[0].conditions)
        },
        {
            "id": "Negation Test",
            "text": "『Aqours』のメンバー以外がいる場合",
            "assert": lambda abs: any(c.type == ConditionType.GROUP_FILTER and c.is_negated == True for c in abs[0].conditions)
        },
        {
            "id": "Opponent Hand Test",
            "text": "相手の手札を1枚控え室に置く。",
            "assert": lambda abs: any(e.effect_type == EffectType.SWAP_CARDS and e.target == TargetType.OPPONENT_HAND for e in abs[0].effects)
        }
    ]

    print("=== Verifying Advanced Parsing Logic ===\n")
    passed = 0
    for case in test_cases:
        try:
            abs = AbilityParser.parse_ability_text(case["text"])
            if not abs and case["text"]:
                # Fallback for activated if no trigger
                text = f"{{{{activated.png|起動}}}}{case['text']}"
                abs = AbilityParser.parse_ability_text(text)
            
            if case["assert"](abs):
                print(f"[PASS] {case['id']}")
                passed += 1
            else:
                print(f"[FAIL] {case['id']} - Assertion failed")
                # Debug print
                if abs:
                    print(f"       Parsed: {abs[0]}")
                    if abs[0].conditions: print(f"       Cond Params: {abs[0].conditions[0].params}")
                    if abs[0].effects: 
                         print(f"       Eff Optional: {abs[0].effects[0].is_optional}")
                         print(f"       Eff Params: {abs[0].effects[0].params}")
        except Exception as e:
            print(f"[ERROR] {case['id']} - {e}")

    print(f"\nPassed {passed}/{len(test_cases)} cases.")

if __name__ == "__main__":
    verify()
