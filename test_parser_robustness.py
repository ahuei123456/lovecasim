
from game.ability import AbilityParser, TriggerType, EffectType
import sys

def debug_parser():
    parser = AbilityParser()
    
    cases = [
        ("Slash", "{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}} カードを1枚引く。"),
        ("Parens", "{{toujyou.png|登場}} カードを1枚引く。（これは説明文です。）"),
        ("Modal-", "以下から1回を選ぶ。\\n- カードを1枚引く。\\n- スコア+1。"),
        ("Choose2", "以下から2つを選ぶ。\\n・カードを1枚引く。\\n・スコア+1。\\n・エネチャージ。"),
    ]
    
    with open('test_output.log', 'w', encoding='utf-8') as f:
        for name, text in cases:
            f.write(f"\n=== Testing {name} ===\n")
            f.write(f"Text: {text}\n")
            abs_list = parser.parse_ability_text(text)
            f.write(f"Result count: {len(abs_list)}\n")
            for idx, a in enumerate(abs_list):
                f.write(f"  Ability {idx}: Trigger={a.trigger.name}\n")
                f.write(f"    Effects: {[e.effect_type.name for e in a.effects]}\n")
                if a.modal_options:
                    f.write(f"    Modal Options: {len(a.modal_options)}\n")
                    for midx, opt in enumerate(a.modal_options):
                        f.write(f"      Opt {midx}: {[e.effect_type.name for e in opt]}\n")

if __name__ == "__main__":
    debug_parser()
