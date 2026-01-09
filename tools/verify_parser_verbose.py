import os
import sys

sys.path.append(os.getcwd())

from game.ability import Ability, AbilityParser


def print_ability(a: Ability):
    print(f"  Trigger: {a.trigger.name}")
    if a.conditions:
        print(f"  Conditions: {[f'{c.type.name} {c.params}' for c in a.conditions]}")
    if a.costs:
        print(f"  Costs: {[f'{c.type.name} val={c.value}' for c in a.costs]}")
    for e in a.effects:
        print(f"  Effect: {e.effect_type.name} (Val={e.value}) Params={e.params}")

def run_verification():
    test_cases = [
        (
            "Meta Rule", 
            "(登場能力がコストを持つ場合、支払って発動させる。)",
            "Clarification text about paying costs."
        ),
        (
            "Select Mode", 
            "登場以下から1つを選ぶ。",
            "Start of a modal ability choice."
        ),
        (
            "Deck Ordering (Top)", 
            "登場自分の控え室からカードを1枚までデッキの一番上に置く。",
            "Moving card from waiting room to Top of Deck."
        ),
        (
            "Deck Ordering (Bottom)", 
            "登場自分の控え室からライブカードを1枚までデッキの一番下に置く。",
            "Moving card from waiting room to Bottom of Deck."
        ),
        (
            "Tap Opponent", 
            "登場相手のステージにいる元々持つブレードの数が1つ以下のメンバー1人をウェイトにする。",
            "Targeting opponent member to Tap (make Wait)."
        ),
        (
            "Restriction (Live)", 
            "常時自分のステージにほかのメンバーがいない場合、自分はライブできない。",
            "Player cannot perform Live if alone."
        ),
        (
            "Baton Touch Mod", 
            "常時このカードのプレイに際し、2人のメンバーとバトンタッチしてもよい。",
            "Allows Baton Touch with 2 members instead of standard."
        ),
        (
            "Flavor Action", 
            "ライブ開始時相手に何が好き？と聞く。",
            "Joke/Flavor effect asking opponent a question."
        ),
        (
            "Set Score", 
            "ライブ成功時このカードのスコアは４になる。",
            "Overriding score calculation to fixed value 4."
        ),
        (
            "Place Under", 
            "登場自分のエネルギー置き場にあるエネルギー2枚をこのメンバーの下に置いてもよい。",
            "Moving energy cards under character."
        ),
        (
            "Multi-Target Logic",
            "ライブ成功時自分のステージに「澁谷かのん」、「唐 可可」、「嵐 千砂都」がいる場合、追加で1枚引く。",
            "Check for 3 specific names, then Draw 1."
        )
    ]

    print("=== Verbose Parser Verification ===\n")
    
    for name, text, desc in test_cases:
        print(f"--- Case: {name} ---")
        print(f"Desc: {desc}")
        print(f"Input: {text}")
        
        abilities = AbilityParser.parse_ability_text(text)
        
        if not abilities:
            print("RESULT: No Ability Parsed (Failed? or Empty?)")
        else:
            for i, a in enumerate(abilities):
                print(f"Parsed Ability {i+1}:")
                print_ability(a)
        print("")

if __name__ == "__main__":
    run_verification()
