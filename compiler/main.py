import os
import sys

# Add project root to path to allow imports if running as script
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import json

import numpy as np
from pydantic import TypeAdapter

from compiler.parser import AbilityParser
from engine.models.card import EnergyCard, LiveCard, MemberCard


def compile_cards(input_path: str, output_path: str):
    print(f"Loading raw cards from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    compiled_data = {"member_db": {}, "live_db": {}, "energy_db": {}, "meta": {"version": "1.0", "source": input_path}}

    sorted_keys = sorted(raw_data.keys())
    m_idx = 0
    l_idx = 1000
    e_idx = 2000

    success_count = 0
    errors = []

    # Pre-create adapters
    member_adapter = TypeAdapter(MemberCard)
    live_adapter = TypeAdapter(LiveCard)
    energy_adapter = TypeAdapter(EnergyCard)

    for key in sorted_keys:
        item = raw_data[key]
        ctype = item.get("type", "")

        try:
            if ctype == "メンバー":
                m_card = parse_member(m_idx, key, item)
                compiled_data["member_db"][str(m_idx)] = member_adapter.dump_python(m_card, mode="json")
                m_idx += 1
            elif ctype == "ライブ":
                l_card = parse_live(l_idx, key, item)
                compiled_data["live_db"][str(l_idx)] = live_adapter.dump_python(l_card, mode="json")
                l_idx += 1
            elif ctype == "エネルギー":
                e_card = parse_energy(e_idx, key, item)
                compiled_data["energy_db"][str(e_idx)] = energy_adapter.dump_python(e_card, mode="json")
                e_idx += 1

            success_count += 1

        except Exception as e:
            errors.append(f"Error parsing card {key} ({item.get('name')}): {e}")

    print(f"Compilation complete. Processed {success_count} cards.")
    if errors:
        print(f"Encountered {len(errors)} errors:")
        for err_msg in errors:
            print(f"  - {err_msg}")

    # Write output
    print(f"Writing compiled data to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(compiled_data, f, ensure_ascii=False, indent=2)
    print("Done.")


def _resolve_img_path(data: dict) -> str:
    # Logic copied/adapted from old data_loader to bake paths into the JSON
    img_path = str(data.get("_img", ""))
    if img_path:
        if img_path.startswith("img/"):
            return img_path[4:]
        return img_path

    raw_url = str(data.get("img", ""))
    if raw_url and "cardlist/" in raw_url:
        try:
            parts = raw_url.split("cardlist/")[-1].split("/")
            if len(parts) >= 2:
                product = parts[0]
                filename = parts[1]
                return f"cards/{product}/{filename}"
        except Exception:
            pass
    return raw_url


def parse_member(card_id: int, card_no: str, data: dict) -> MemberCard:
    spec = data.get("special_heart", {})
    raw_ability = str(data.get("ability", ""))

    # Parse helpers (duplicated from old loader logic, but using Pydantic validation now)
    # Actually Pydantic models will handle conversion if we pass correct types,
    # but for manual parsing like 'hearts' dict -> array we still need helper logic or Pydantic validators.
    # To keep it simple, we do the transformation here before instantiating.

    return MemberCard(
        card_id=card_id,
        card_no=card_no,
        name=str(data.get("name", "Unknown")),
        cost=data.get("cost", 0),
        hearts=parse_hearts(data.get("base_heart", {})),
        blade_hearts=parse_blade_hearts(data.get("blade_heart", {})),
        blades=data.get("blade", 0),
        groups=data.get("series", ""),  # Validator will handle string -> List[Group]
        units=data.get("unit", ""),  # Validator will handle string -> List[Unit]
        abilities=AbilityParser.parse_ability_text(raw_ability),
        img_path=_resolve_img_path(data),
        ability_text=raw_ability,
        volume_icons=spec.get("score", 0),
        draw_icons=spec.get("draw", 0),
    )


def parse_live(card_id: int, card_no: str, data: dict) -> LiveCard:
    spec = data.get("special_heart", {})
    raw_ability = str(data.get("ability", ""))

    return LiveCard(
        card_id=card_id,
        card_no=card_no,
        name=str(data.get("name", "Unknown")),
        score=data.get("score", 0),
        required_hearts=parse_live_reqs(data.get("need_heart", {})),
        abilities=AbilityParser.parse_ability_text(raw_ability),
        groups=data.get("series", ""),
        units=data.get("unit", ""),
        img_path=_resolve_img_path(data),
        ability_text=raw_ability,
        volume_icons=spec.get("score", 0),
        draw_icons=spec.get("draw", 0),
        blade_hearts=parse_blade_hearts(data.get("blade_heart", {})),
    )


def parse_energy(card_id: int, card_no: str, data: dict) -> EnergyCard:
    return EnergyCard(card_id=card_id)


def parse_hearts(heart_dict: dict) -> np.ndarray:
    hearts = np.zeros(6, dtype=np.int32)
    if not heart_dict:
        return hearts
    for k, v in heart_dict.items():
        if k.startswith("heart"):
            try:
                idx = int(k.replace("heart", "")) - 1
                if 0 <= idx < 6:
                    hearts[idx] = int(v)
            except ValueError:
                pass
    return hearts


def parse_blade_hearts(heart_dict: dict) -> np.ndarray:
    hearts = np.zeros(7, dtype=np.int32)
    if not heart_dict:
        return hearts
    for k, v in heart_dict.items():
        if k == "b_all":
            hearts[6] = int(v)
        elif k.startswith("b_heart"):
            try:
                idx = int(k.replace("b_heart", "")) - 1
                if 0 <= idx < 6:
                    hearts[idx] = int(v)
            except ValueError:
                pass
    return hearts


def parse_live_reqs(req_dict: dict) -> np.ndarray:
    reqs = np.zeros(7, dtype=np.int32)
    if not req_dict:
        return reqs
    base = parse_hearts(req_dict)
    reqs[:6] = base
    for k, v in req_dict.items():
        if k in ["star", "any", "common"]:
            reqs[6] = int(v)
    return reqs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="engine/data/cards.json", help="Path to raw cards.json")
    parser.add_argument("--output", default="engine/data/cards_compiled.json", help="Output path")
    args = parser.parse_args()

    # Resolve paths relative to cwd if needed, or assume running from root
    compile_cards(args.input, args.output)
