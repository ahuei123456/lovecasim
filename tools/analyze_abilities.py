"""
Analyze ability coverage across all cards.
Counts effect types and condition types to prioritize testing.
"""

import json
import os
import sys
from typing import Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.parser import AbilityParser
from engine.models.ability import ConditionType, EffectType, TriggerType

# Define what is currently implemented in game_state.py
SUPPORTED_TRIGGERS = {
    TriggerType.ON_PLAY,
    TriggerType.ON_LIVE_START,
    TriggerType.CONSTANT,
    # ON_LIVE_SUCCESS / TURN_START / TURN_END are stubs or partially there, allow for now
    TriggerType.ON_LIVE_SUCCESS,
}

SUPPORTED_EFFECTS = {
    EffectType.DRAW,
    EffectType.ADD_BLADES,
    EffectType.ADD_HEARTS,
    EffectType.BOOST_SCORE,
    EffectType.BUFF_POWER,
    # FLAVOR_ACTION was essentially a "do nothing" or modal wrapper, consider supported if modal used
}

SUPPORTED_CONDITIONS = {
    ConditionType.NONE,
    ConditionType.COUNT_GROUP,
    ConditionType.HAS_COLOR,
    ConditionType.COUNT_ENERGY,
    ConditionType.HAS_LIVE_CARD,
}


def analyze_coverage():
    try:
        # Use compiled data if available, or fall back to raw
        path = "engine/data/cards_compiled.json"
        if not os.path.exists(path):
            path = "data/cards.json"

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # If compiled, data is {member_db: {}, live_db: {}}
            if "member_db" in data:
                # Flask compiled structure to flat dict for analysis
                flat_data = {}
                flat_data.update(data["member_db"])
                flat_data.update(data["live_db"])
                data = flat_data

    except FileNotFoundError:
        print(f"Error: {path} not found")
        return

    total_cards = 0
    fully_supported = 0
    partially_supported = 0
    parse_failures = 0

    unsupported_effects: Dict[str, int] = {}
    unsupported_conditions: Dict[str, int] = {}

    print(f"Analyzing {len(data)} cards...")

    for _cid, card in data.items():
        # Handle both raw and compiled formats
        # Compiled: 'type' might be missing if inferred from DB, check keys
        # Raw: 'type' is strict

        # If compiled, struct is different. Let's assume raw text is preserved or reconstructable?
        # Actually compiled data has 'ability_text' preserved.

        raw_text = card.get("ability_text", card.get("ability", ""))

        # Filter types if raw
        ctype = card.get("type", "")
        if ctype and ctype not in ("メンバー", "ライブ") and not card.get("card_no"):
            continue

        total_cards += 1

        if not raw_text:
            fully_supported += 1  # No ability = supported
            continue

        try:
            abilities = AbilityParser.parse_ability_text(raw_text)
            if not abilities:
                # If text exists but no abilities parsed, likely flavor text or unparseable
                # Check directly if it looks like an ability (contains ":")
                if "：" in raw_text or ":" in raw_text:
                    parse_failures += 1
                else:
                    fully_supported += 1
                continue

            is_full = True

            for ab in abilities:
                if ab.trigger not in SUPPORTED_TRIGGERS:
                    is_full = False
                    # missing_features.append(f"Trigger: {ab.trigger.name}")

                for eff in ab.effects:
                    if eff.effect_type not in SUPPORTED_EFFECTS:
                        is_full = False
                        ename = eff.effect_type.name
                        unsupported_effects[ename] = unsupported_effects.get(ename, 0) + 1

                for cond in ab.conditions:
                    if cond.type not in SUPPORTED_CONDITIONS:
                        is_full = False
                        cname = cond.type.name
                        unsupported_conditions[cname] = unsupported_conditions.get(cname, 0) + 1

            if is_full:
                fully_supported += 1
            else:
                partially_supported += 1

        except Exception:
            parse_failures += 1
            # print(f"Parse error for {cid}: {e}")

    print("\n=== Coverage Report ===")
    print(f"Total Cards: {total_cards}")
    if total_cards > 0:
        print(f"Fully Supported: {fully_supported} ({fully_supported / total_cards * 100:.1f}%)")
        print(
            f"Partially Supported (Need Handlers): {partially_supported} ({partially_supported / total_cards * 100:.1f}%)"
        )
        print(f"Parse Failures: {parse_failures} ({parse_failures / total_cards * 100:.1f}%)")

    print("\n--- Top Missing Effects (Need Implementation) ---")
    for k, v in sorted(unsupported_effects.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{k}: {v}")

    print("\n--- Top Missing Conditions ---")
    for k, v in sorted(unsupported_conditions.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{k}: {v}")

    # Write detailed log
    with open("coverage_report.txt", "w", encoding="utf-8") as f:
        f.write(
            f"Coverage Report\nTotal: {total_cards}\nSupported: {fully_supported}\nPartial: {partially_supported}\nFailures: {parse_failures}\n"
        )
        f.write("\nMissing Effects:\n")
        for k, v in sorted(unsupported_effects.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{k}: {v}\n")


if __name__ == "__main__":
    analyze_coverage()
