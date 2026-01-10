"""
Spot-check key effect types for semantic accuracy.
For each major effect type, show one example and verify parsing makes sense.
"""
import json
import sys
import os
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.ability import AbilityParser, EffectType

def verify_effect_type(effect_type: str, expected_keywords: list):
    """Check if cards with this effect type contain expected Japanese keywords."""
    with open('data/cards.json', encoding='utf-8') as f:
        cards = json.load(f)
    
    matches = []
    mismatches = []
    
    for card_no, card in cards.items():
        ability_text = card.get('ability', '')
        if not ability_text:
            continue
        
        abilities = AbilityParser.parse_ability_text(ability_text)
        has_effect = any(
            any(e.effect_type.name == effect_type for e in ab.effects)
            for ab in abilities
        )
        
        if has_effect:
            has_keyword = any(kw in ability_text for kw in expected_keywords)
            if has_keyword:
                matches.append(card_no)
            else:
                mismatches.append((card_no, card.get('name', '?'), ability_text[:80]))
    
    return matches, mismatches

# Define expected keywords for each effect type
EFFECT_KEYWORDS = {
    'DRAW': ['引く', 'ドロー', '手札に加え'],
    'SWAP_CARDS': ['控え室', '置く', '入れ替え'],
    'ADD_BLADES': ['ブレード', 'blade'],
    'RECOVER_MEMBER': ['メンバーカード', '控え室から', '手札に加え'],
    'RECOVER_LIVE': ['ライブカード', '控え室から', '手札に加え'],
    'LOOK_AND_CHOOSE': ['見', '選', 'デッキ'],
    'ADD_HEARTS': ['ハート', 'heart'],
    'ENERGY_CHARGE': ['エネルギー', 'チャージ', 'エナジー'],
    'BUFF_POWER': ['ブレード', '得る', '増え'],
    'BOOST_SCORE': ['スコア', '加算'],
}

print("=" * 60)
print("SEMANTIC VERIFICATION - Effect Type Keyword Matching")
print("=" * 60)

results = []
for effect, keywords in EFFECT_KEYWORDS.items():
    matches, mismatches = verify_effect_type(effect, keywords)
    total = len(matches) + len(mismatches)
    if total == 0:
        continue
    
    accuracy = len(matches) / total * 100 if total > 0 else 0
    status = "✅" if accuracy >= 90 else ("⚠️" if accuracy >= 70 else "❌")
    
    results.append((effect, len(matches), total, accuracy, status, mismatches[:3]))
    
print(f"\n{'Effect Type':<20} {'Match':>6} {'Total':>6} {'Accuracy':>10} Status")
print("-" * 52)
for effect, matches, total, acc, status, _ in results:
    print(f"{effect:<20} {matches:>6} {total:>6} {acc:>9.1f}% {status}")

# Show any mismatches
print("\n--- Sample Mismatches (may need parser update) ---")
for effect, _, _, _, _, mismatches in results:
    for card_no, name, text in mismatches:
        print(f"\n{effect}: {card_no} ({name})")
        print(f"  Text: {text}...")
