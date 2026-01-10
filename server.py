"""
Flask Backend for Love Live Card Game Web UI
"""

import json
import os
import random
import sys
from datetime import datetime
from typing import Any

import numpy as np
from flask import Flask, jsonify, request, send_from_directory

from ai.headless_runner import SmartHeuristicAgent, create_easy_cards
from game.data_loader import CardDataLoader
from game.game_state import GameState, Phase

# --- PATH SETUP ---
# Define directories for locating assets and data
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = CURRENT_DIR # Engine is now merged into root
AI_DIR = os.path.join(CURRENT_DIR, "ai")
TOOLS_DIR = os.path.join(CURRENT_DIR, "tools")

# Tools imports (optional)
try:
    from tools.deck_extractor import extract_deck_data
except ImportError:
    print("Warning: Could not import deck_extractor from tools.")

    def extract_deck_data(content, db):
        return [], [], {}, ["Importer not found"]


# Static folder is now in frontend/web_ui
# Static folder is now in frontend/web_ui
FRONTEND_DIR = os.path.join(CURRENT_DIR, "frontend")
WEB_UI_DIR = os.path.join(FRONTEND_DIR, "web_ui")
IMG_DIR = os.path.join(FRONTEND_DIR, "img")  # Images seem to be in frontend/img
# Note: frontend/web_ui has its own js/css folders which index.html likely uses

app = Flask(__name__, static_folder=WEB_UI_DIR)
ai_agent = SmartHeuristicAgent()

# Global game state
game_state: GameState | None = None
# Use Any to avoid circular imports or strict union issues for now
member_db: dict[int, Any] = {}
live_db: dict[int, Any] = {}
energy_db: dict[int, Any] = {}
game_history: list[dict] = []  # For replay recording

# Custom deck storage (list of card_no strings like "PL!-sd1-001-SD")
custom_deck_p0: list[str] | None = None  # Player 0 (Human)
custom_deck_p1: list[str] | None = None  # Player 1 (AI)
custom_energy_deck_p0: list[str] | None = None
custom_energy_deck_p1: list[str] | None = None

# Reverse mapping: card_no string -> internal integer ID
card_no_to_id: dict[str, int] = {}


def build_card_no_mapping():
    """Build reverse lookup from card_no string to internal ID.

    Replicates the ID assignment logic from data_loader.py:
    - Members: 0-999
    - Lives: 1000-1999
    - Energy: 2000+
    """
    global card_no_to_id
    card_no_to_id = {}

    # Load raw JSON to get the original card_no strings
    try:
        cards_path = os.path.join(ENGINE_DIR, "data", "cards.json")
        with open(cards_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"Error loading cards.json for mapping: {e}")
        return

    # Replicate the exact ID assignment from CardDataLoader.load()
    sorted_keys = sorted(raw_data.keys())

    m_idx = 0
    l_idx = 1000
    e_idx = 2000

    for key in sorted_keys:
        card_data = raw_data[key]
        ctype = card_data.get("type")

        if ctype == "メンバー":
            card_no_to_id[key] = m_idx
            m_idx += 1
        elif ctype == "ライブ":
            card_no_to_id[key] = l_idx
            l_idx += 1
        elif ctype == "エネルギー":
            card_no_to_id[key] = e_idx
            e_idx += 1

    print(f"Built card_no_to_id mapping: {len(card_no_to_id)} entries")


def convert_deck_strings_to_ids(deck_strings):
    """Convert list of card_no strings to internal IDs."""
    ids = []
    for card_no in deck_strings:
        if card_no in card_no_to_id:
            ids.append(card_no_to_id[card_no])
        else:
            print(f"Warning: Unknown card_no '{card_no}', skipping.")
    return ids


def save_replay():
    """Save the current game history to a file."""
    if not game_history:
        return

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("replays", exist_ok=True)
        filename = f"replays/replay_{timestamp}.json"

        # Structure matches what web_ui expects (based on current UI code)
        data = {
            "game_id": 0,
            "timestamp": timestamp,
            "winner": game_state.winner if game_state else -1,
            "states": game_history,
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"Replay saved to {filename}")
    except Exception as e:
        print(f"Failed to save replay: {e}")


game_history = []  # For replay recording


def init_game(deck_type="normal"):
    global game_state, member_db, live_db, energy_db, game_history

    # Ensure true randomness for each game
    import time

    random.seed(int(time.time() * 1000) % (2**31))

    # DATA PATH: ../engine/data/cards.json
    cards_path = os.path.join(ENGINE_DIR, "data", "cards.json")
    loader = CardDataLoader(cards_path)
    member_db, live_db, energy_db = loader.load()

    # CRITICAL: Populate GameState static DBs so validations work
    GameState.member_db = member_db
    GameState.live_db = live_db

    # Initialize JIT arrays for performance
    GameState._init_jit_arrays()

    # Build reverse mapping for custom deck support
    build_card_no_mapping()

    # Pre-calculate Start Deck card IDs

    # Load raw JSON to check product field for filtering
    cards_path = os.path.join(ENGINE_DIR, "data", "cards.json")
    with open(cards_path, "r", encoding="utf-8") as f:
        json.load(f)

    for _cid, _m in member_db.items():
        # Find raw key by matching name/cost/type? Or better, DataLoader should store product.
        # Since DataLoader doesn't verify product yet, we'll try to guess or just use ALL valid cards
        # that are from Start Deck (usually ID < 100 for this mock loader or by string ID).
        # Actually, let's just use ALL loaded members/lives for 'normal' and specific ones for 'starter'.
        # For 'start_deck', we can filter by card string ID prefix 'PL!-sd1' or 'LL-E'.

        # But 'member_db' keys are integers 0..N. We need a way to link back.
        # The loader assigns IDs sequentially.
        # Let's just build a random valid deck from ALL cards for now,
        # unless 'easy' mode.
        pass

    # If deck_type is 'easy', we use the simple mock cards for logic testing.
    # If deck_type is 'normal' or 'starter', we use REAL cards.

    if deck_type == "easy":
        easy_m, easy_l = create_easy_cards()
        member_db[easy_m.card_id] = easy_m
        live_db[easy_l.card_id] = easy_l

    game_state = GameState()

    # Setup players
    for pidx, p in enumerate(game_state.players):
        # Check for custom deck first
        custom_deck = custom_deck_p0 if pidx == 0 else custom_deck_p1

        if custom_deck:
            # Use custom deck
            p.main_deck = convert_deck_strings_to_ids(custom_deck)
            random.shuffle(p.main_deck)  # Shuffle custom deck for variety
            print(f"Player {pidx}: Using custom deck ({len(p.main_deck)} cards, shuffled)")
        elif deck_type == "easy":
            # Use Easy Cards (888/999) but mapped to real images
            p.main_deck = [888] * 48 + [999] * 12
        else:
            # NORMAL / STARTER MODE: Build a valid deck
            # Rule: Max 4 copies of same card number.
            # Total: 48 Members + 12 Lives (Total 60 in main deck per game_state spec)

            p.main_deck = []

            # 1. Select Members (48)
            available_members = list(member_db.keys())
            if available_members:
                # Shuffle availability to vary decks
                random.shuffle(available_members)

                member_bucket = []
                for mid in available_members:
                    # Add 4 copies of each until we have enough
                    count = 4
                    member_bucket.extend([mid] * count)
                    if len(member_bucket) >= 150:  # Optimization: Don't build massive list
                        break

                # Pick 48 from the bucket
                if len(member_bucket) < 48:
                    # Fallback if DB too small
                    while len(member_bucket) < 48:
                        member_bucket.extend(available_members)

                # Ensure we don't accidentally pick >4 if we just slice
                # Actually, simply taking the first 48 from our constructed bucket (which has 4 of each distinct card)
                # guarantees validity if we shuffle the CARDS/TYPES, not the final list.
                # Steps:
                # 1. Shuffle types.
                # 2. Add 4 of Type A, 4 of Type B...
                # 3. Take first 48 cards.

                p.main_deck.extend(member_bucket[:48])

            # 2. Select Lives (12)
            available_lives = list(live_db.keys())
            if available_lives:
                random.shuffle(available_lives)
                live_bucket = []
                for lid in available_lives:
                    live_bucket.extend([lid] * 4)
                    if len(live_bucket) >= 50:
                        break

                if len(live_bucket) < 12:
                    while len(live_bucket) < 12:
                        live_bucket.extend(available_lives)

                p.main_deck.extend(live_bucket[:12])

            random.shuffle(p.main_deck)

        # Energy Deck (12 cards)
        # Use actual Energy Card ID if available (2000+)
        if energy_db:
            eid = list(energy_db.keys())[0]  # Take first energy card type found
            p.energy_deck = [eid] * 12
        else:
            p.energy_deck = [200] * 12  # Fallback

        # Custom Energy Deck Override
        custom_energy = custom_energy_deck_p0 if pidx == 0 else custom_energy_deck_p1
        if custom_energy:
            p.energy_deck = convert_deck_strings_to_ids(custom_energy)
            print(f"Player {pidx}: Using custom energy deck ({len(p.energy_deck)} cards)")

        # Explicit shuffle before drawing
        random.shuffle(p.main_deck)
        if game_state.players.index(p) == 0:
            print(f"DEBUG: P0 Deck Shuffled. Top 5: {p.main_deck[-5:]}")

        # Initial draw (6 cards - standard Mulligan start)
        for _ in range(6):
            if p.main_deck:
                p.hand.append(p.main_deck.pop())

        # Initial energy: 3 cards (Rule 6.2.1.7)
        for _ in range(3):
            if p.energy_deck:
                p.energy_zone.append(p.energy_deck.pop(0))

    # Randomly determine first player
    game_state.first_player = random.randint(0, 1)
    game_state.current_player = game_state.first_player

    # Start in MULLIGAN phase
    game_state.phase = Phase.MULLIGAN_P1

    # Initialize history with starting state
    game_history = [serialize_state()]

    # Initialize history with starting state
    game_history = [serialize_state()]


def serialize_card(cid, is_viewable=True, peek=False):
    if not is_viewable and not peek:
        return {"id": int(cid), "name": "???", "type": "unknown", "img": "cards/back.png", "hidden": True}

    card_data = {}
    if cid in member_db:
        m = member_db[cid]
        # ... (rest of member serialization) ...
        # We need to construct the full object or call a helper if we want to avoid code duplication.
        # However, to minimize changes, let's just grab the object if it was already resolved or rebuild it.
        # Actually, let's restructure slightly to allow fall-through.
        pass  # Handle below
    elif cid in live_db:
        pass  # Handle below
    else:
        # Fallback for truly unknown ID if that happens, or just return hidden
        return {"id": cid, "name": "Unknown", "img": "cards/back.png"}

    # Re-implementing the logic below to handle flow correctly
    if cid in member_db:
        m = member_db[cid]
        ability_text = getattr(m, "ability_text", "")
        if hasattr(m, "abilities") and m.abilities:
            ability_lines = []
            from game.ability import TriggerType

            for ab in m.abilities:
                trigger_icon = {
                    TriggerType.ACTIVATED: "【起動】",
                    TriggerType.ON_PLAY: "【登場】",
                    TriggerType.CONSTANT: "【常時】",
                    TriggerType.ON_LIVE_START: "【ライブ開始】",
                    TriggerType.ON_LIVE_SUCCESS: "【ライブ成功時】",
                }.get(ab.trigger, "【自動】")
                ability_lines.append(f"{trigger_icon} {ab.raw_text}")
            ability_text = "\n".join(ability_lines)

        card_data = {
            "id": int(cid),
            "card_no": m.card_no,
            "name": m.name,
            "type": "member",
            "cost": m.cost,
            "hp": 1,  # Default HP/Life for members if tracked, or just omit if not in model
            "blade": m.blades,  # Corrected from .blade to .blades
            "img": m.img_path,
            "hearts": m.hearts.tolist(),
            "blade_hearts": m.blade_hearts.tolist(),
            "color": "Unknown",  # Could derive from hearts
            "text": ability_text,
        }
    elif cid in live_db:
        l = live_db[cid]
        ability_text = getattr(l, "ability_text", "")
        if hasattr(l, "abilities") and l.abilities:
            ability_lines = []
            from game.ability import TriggerType

            for ab in l.abilities:
                trigger_icon = {TriggerType.ON_LIVE_START: "【ライブ開始】"}.get(ab.trigger, "【自動】")
                ability_lines.append(f"{trigger_icon} {ab.raw_text}")
            ability_text = "\n".join(ability_lines)

        card_data = {
            "id": int(cid),
            "card_no": l.card_no,
            "name": l.name,
            "type": "live",
            "score": l.score,
            "img": l.img_path,
            "required_hearts": l.required_hearts.tolist(),
            "text": ability_text,
        }

    if not is_viewable and peek:
        card_data["hidden"] = True  # Mark as hidden generally
        card_data["face_down"] = True  # Explicit flag for UI to show "peek" state

    return card_data

    if cid in member_db:
        m = member_db[cid]

        # Format ability text for display
        ability_text = getattr(m, "ability_text", "")
        if hasattr(m, "abilities") and m.abilities:
            # Concatenate all ability descriptions
            ability_lines = []
            from game.ability import TriggerType

            for ab in m.abilities:
                trigger_icon = {
                    TriggerType.ACTIVATED: "【起動】",
                    TriggerType.ON_PLAY: "【登場】",
                    TriggerType.CONSTANT: "【常時】",
                    TriggerType.ON_LIVE_START: "【ライブ開始】",
                    TriggerType.ON_LIVE_SUCCESS: "【ライブ成功】",
                }.get(ab.trigger, "【能力】")
                ability_lines.append(f"{trigger_icon} {ab.raw_text}")
            ability_text = "\\n".join(ability_lines)

        return {
            "id": int(cid),
            "name": m.name,
            "cost": int(m.cost),
            "type": "member",
            "img": m.img_path,
            "hp": int(m.total_hearts()),
            "blade": int(m.blades),
            "hearts": m.hearts.tolist(),  # Array of 6 colors
            "blade_hearts": m.blade_hearts.tolist(),  # Yell contribution
            "text": ability_text,
        }
    elif cid in live_db:
        l = live_db[cid]
        return {
            "id": int(cid),
            "name": l.name,
            "cost": int(l.total_required()),
            "type": "live",
            "img": l.img_path,
            "score": int(l.score),
            "required_hearts": l.required_hearts.tolist(),  # Array of 7 (6 colors + any)
            "text": getattr(l, "ability_text", ""),
        }
    elif cid in energy_db:
        e = energy_db[cid]
        return {"id": int(cid), "name": e.name, "type": "energy", "img": e.img_path}
    else:
        # Fallback for special IDs or unknown cards
        if cid == 888:
            return {
                "id": 888,
                "name": "Member (Easy)",
                "cost": 1,
                "img": "cards/PLSD01/PL!-sd1-001-SD.png",
                "type": "member",
                "hp": 1,
                "blade": 1,
                "hearts": [1, 0, 0, 0, 0, 0],
                "blade_hearts": [0, 0, 0, 0, 0, 0],
                "text": "",
            }
        if cid == 999:
            return {
                "id": 999,
                "name": "Live (Easy)",
                "score": 1,
                "img": "cards/PLSD01/PL!-pb1-019-SD.png",
                "type": "live",
                "cost": 1,
                "required_hearts": [0, 0, 0, 0, 0, 0, 1],
                "text": "",
            }
        return {"id": int(cid), "name": f"Card {cid}", "type": "unknown", "img": None}


def serialize_player(p, player_idx, viewer_idx=0, is_viewable=True):
    """Serialize one player's state."""

    # Calculate expected yell count based on total blades
    expected_yells = 0
    if game_state and hasattr(game_state, "member_db"):
        for i, card_id in enumerate(p.stage):
            if card_id >= 0 and not p.tapped_members[i] and card_id in game_state.member_db:
                member = game_state.member_db[card_id]
                expected_yells += member.blades

    legal_mask = game_state.get_legal_actions() if game_state else [False] * 1024

    hand = []
    if is_viewable:
        for i, cid in enumerate(p.hand):
            c = serialize_card(cid)
            # Find legal actions for this card index (i)
            # Logic from game.game_state.get_legal_actions:
            # Play Member: 1 + i*3 + area (0,1,2)
            valid_actions = []

            # Check Play Member actions
            for area in range(3):
                aid = 1 + i * 3 + area
                if aid < len(legal_mask) and legal_mask[aid]:
                    valid_actions.append(aid)

            # Check Live Set action
            aid_live = 400 + i
            if aid_live < len(legal_mask) and legal_mask[aid_live]:
                valid_actions.append(aid_live)

            # Check Mulligan toggle
            aid_mull = 300 + i
            if aid_mull < len(legal_mask) and legal_mask[aid_mull]:
                valid_actions.append(aid_mull)

            c["valid_actions"] = valid_actions
            hand.append(c)
    else:
        hand = [serialize_card(cid, is_viewable=False) for cid in p.hand]

    stage = []
    for i in range(3):
        cid = int(p.stage[i])
        if cid >= 0:
            c = serialize_card(cid)
            c["tapped"] = bool(p.tapped_members[i])
            c["energy"] = len(p.stage_energy[i])
            stage.append(c)
        else:
            stage.append(None)

    discard = [serialize_card(cid, is_viewable=True) for cid in p.discard]
    energy = [
        {
            "id": i,
            "tapped": bool(p.tapped_energy[i]) if i < len(p.tapped_energy) else False,
            "card": serialize_card(p.energy_zone[i], is_viewable=False),
        }
        for i, _ in enumerate(p.energy_zone)
    ]
    live_zone = []
    for i, cid in enumerate(p.live_zone):
        is_revealed = False
        if i < len(p.live_zone_revealed):
            is_revealed = bool(p.live_zone_revealed[i])

        # Rule: Owner can peek at their own live cards (Rule 4.9.2)
        # Use passed viewer_idx context
        can_peek = player_idx == viewer_idx

        # Serialization:
        # If open info (revealed): viewable=True
        # If hidden info but owner: viewable=False, peek=True
        # If hidden info and opp: viewable=False, peek=False

        live_zone.append(serialize_card(cid, is_viewable=is_revealed, peek=can_peek))

    # Score is the NUMBER of successful lives (win condition: 3)
    score = len(p.success_lives)

    return {
        "player_id": p.player_id,
        "score": score,  # Added score field
        "is_active": is_viewable,  # Changed from is_human
        "hand": hand,
        "hand_count": len(p.hand),
        "mulligan_selection": list(getattr(p, "mulligan_selection", [])) if is_viewable else [],
        "deck_count": len(p.main_deck),
        "energy_deck_count": len(p.energy_deck),  # NEW
        "discard": discard,
        "discard_count": len(p.discard),
        "energy": energy,
        "energy_count": len(p.energy_zone),
        "energy_untapped": int(p.count_untapped_energy()),
        "live_zone": live_zone,
        "live_zone_count": len(p.live_zone),  # Useful for AI
        "stage": stage,
        "success_lives": [serialize_card(cid, is_viewable) for cid in p.success_lives],
        "restrictions": list(p.restrictions),
        "expected_yells": expected_yells,  # New field
    }


def serialize_state():
    global game_state
    if game_state is None:
        return {
            "turn": 0,
            "phase": 0,
            "active_player": 0,
            "game_over": False,
            "winner": -1,
            "players": [],
            "legal_actions": [],
            "pending_choice": None,
            "performance_results": {},
            "rule_log": [],
        }

    active_idx = game_state.current_player

    legal_mask = game_state.get_legal_actions()
    legal_actions = []
    p = game_state.active_player
    # Only reveal card details in actions if it's the viewer's (P0) turn/actions
    # This prevents P1 (AI/Opponent) actions from leaking info via legal_actions list
    actions_viewable = game_state.current_player == 0

    for i, v in enumerate(legal_mask):
        if v:
            desc = get_action_desc(i, game_state)
            meta = {"id": i, "desc": desc}

            # Add rich metadata for highlighting and UI display

            if 1 <= i <= 180:
                meta["type"] = "PLAY"
                meta["hand_idx"] = (i - 1) // 3
                meta["area_idx"] = (i - 1) % 3
                if meta["hand_idx"] < len(p.hand):
                    cid = p.hand[meta["hand_idx"]]
                    c_data = serialize_card(cid, is_viewable=actions_viewable)
                    meta["img"] = c_data["img"]
                    meta["name"] = c_data["name"]
                    meta["cost"] = c_data.get("cost", 0)
                    meta["card_id"] = int(cid) if actions_viewable else -1

            elif 200 <= i <= 202:
                meta["type"] = "ABILITY"
                meta["area_idx"] = i - 200
                if p.stage[meta["area_idx"]] >= 0:
                    cid = p.stage[meta["area_idx"]]
                    # Stage cards are public, so viewable is True
                    c_data = serialize_card(cid, is_viewable=True)
                    meta["img"] = c_data["img"]
                    meta["name"] = c_data["name"]
                    meta["card_id"] = int(cid)

            elif 300 <= i <= 359:
                meta["type"] = "MULLIGAN"
                meta["hand_idx"] = i - 300
                if meta["hand_idx"] < len(p.hand):
                    cid = p.hand[meta["hand_idx"]]
                    c_data = serialize_card(cid, is_viewable=actions_viewable)
                    meta["img"] = c_data["img"]
                    meta["name"] = c_data["name"]
                    meta["card_id"] = int(cid) if actions_viewable else -1

            elif 400 <= i <= 459:
                meta["type"] = "LIVE_SET"
                meta["hand_idx"] = i - 400
                if meta["hand_idx"] < len(p.hand):
                    cid = p.hand[meta["hand_idx"]]
                    c_data = serialize_card(cid, is_viewable=actions_viewable)
                    meta["img"] = c_data["img"]
                    meta["name"] = c_data["name"]
                    meta["card_id"] = int(cid) if actions_viewable else -1

            elif 600 <= i <= 659:
                meta["type"] = "SELECT"
                # For SELECT_FROM_LIST, the ID is often the index in the list
                meta["index"] = i - 600
                # If we have looked_cards, we can find the exact card
                if (
                    hasattr(game_state, "looked_cards")
                    and game_state.looked_cards
                    and meta["index"] < len(game_state.looked_cards)
                ):
                    cid = game_state.looked_cards[meta["index"]]
                    # Looked cards are privately visible to the active player
                    c_data = serialize_card(cid, is_viewable=actions_viewable)
                    meta["img"] = c_data["img"]
                    meta["name"] = c_data["name"]
                    meta["card_id"] = int(cid)
                # Check for pending choices generic list
                elif game_state.pending_choices:
                    choice_type, params = game_state.pending_choices[0]
                    if choice_type in ("SELECT_FROM_LIST", "TARGET_OPPONENT_MEMBER", "SELECT_SWAP_SOURCE"):
                        cards = params.get("cards", [])
                        # For opponent member target, cards might not be populated directly as list of IDs but derived
                        if choice_type == "TARGET_OPPONENT_MEMBER":
                            opp = game_state.inactive_player
                            if meta["index"] < 3 and opp.stage[meta["index"]] >= 0:
                                meta["card_id"] = int(opp.stage[meta["index"]])
                        elif meta["index"] < len(cards):
                            meta["card_id"] = int(cards[meta["index"]])

            elif 660 <= i <= 719:
                # Discard Select
                meta["type"] = "SELECT_DISCARD"
                meta["index"] = i - 660
                if game_state.pending_choices:
                    choice_type, params = game_state.pending_choices[0]
                    if choice_type == "SELECT_FROM_DISCARD":
                        cards = params.get("cards", [])
                        if meta["index"] < len(cards):
                            meta["card_id"] = int(cards[meta["index"]])

            elif 500 <= i <= 559:
                # Hand Select (Target/Discard)
                meta["type"] = "SELECT_HAND"
                meta["hand_idx"] = i - 500
                if meta["hand_idx"] < len(p.hand):
                    meta["card_id"] = int(p.hand[meta["hand_idx"]])

            elif 560 <= i <= 562:
                # Stage Select
                meta["type"] = "SELECT_STAGE"
                meta["area_idx"] = i - 560
                if p.stage[meta["area_idx"]] >= 0:
                    meta["card_id"] = int(p.stage[meta["area_idx"]])

            legal_actions.append(meta)

    # CRITICAL: If it's the opponent's turn (P1), hide the legal actions list entirely
    # to prevent the user from seeing/making decisions for the AI.
    if game_state.current_player != 0:
        legal_actions = []

    # Serialize pending choice with metadata
    pending_choice_info = None
    if game_state.pending_choices:
        choice_type, params = game_state.pending_choices[0]
        pending_choice_info = {
            "type": choice_type,
            "description": params.get("effect_description", ""),
            "source_ability": params.get("source_ability", ""),
            "source_member": params.get("source_member", ""),
            "is_optional": params.get("is_optional", False),
            "params": params,  # Include all original params
        }

        # Enrich params with serialized cards if it's a list choice
        if choice_type in ("SELECT_FROM_LIST", "LOOK_AND_CHOOSE", "SELECT_FROM_DISCARD"):
            cards = params.get("cards", [])
            if cards:
                params["serialized_cards"] = [serialize_card(cid) for cid in cards]

    return {
        "turn": game_state.turn_number,
        "phase": int(game_state.phase),  # Return numeric phase, not string name
        "active_player": int(active_idx),
        "game_over": game_state.game_over,
        "winner": game_state.winner,
        "players": [
            serialize_player(
                game_state.players[0], player_idx=0, viewer_idx=0, is_viewable=True
            ),  # P0 is human (viewer)
            serialize_player(
                game_state.players[1], player_idx=1, viewer_idx=0, is_viewable=False
            ),  # P1 is AI (opponent)
        ],
        "legal_actions": legal_actions,
        "pending_choice": pending_choice_info,
        "performance_results": getattr(game_state, "performance_results", {}),
        "rule_log": game_state.rule_log,  # Full history
    }


def get_action_desc(a, gs):
    """
    Generate clear, informative Japanese action descriptions.
    Shows card names, costs, and ability sources for better user understanding.
    """
    if gs is None:
        return f"アクション {a}"
    p = gs.active_player

    # Helper to get card name from any db
    def get_card_name(cid):
        if cid in gs.member_db:
            return gs.member_db[cid].name
        if cid in gs.live_db:
            return gs.live_db[cid].name
        return f"カード#{cid}"

    if a == 0:
        if gs.phase == Phase.MAIN:
            return "【終了】メインフェイズを終了する"
        if gs.phase == Phase.LIVE_SET:
            return "【確定】ライブカードをセットして続行"
        if gs.phase in (Phase.MULLIGAN_P1, Phase.MULLIGAN_P2):
            return "【確定】マリガンを実行"
        return "【パス】何もせず続行"

    elif 1 <= a <= 180:
        idx = (a - 1) // 3
        area_idx = (a - 1) % 3
        areas = ["左サイド", "センター", "右サイド"]
        area_name = areas[area_idx]

        card_name = f"手札[{idx}]"
        new_card_cost = 0
        if gs.current_player == 0:  # Only show details for P0 (human)
            if idx < len(p.hand):
                cid = p.hand[idx]
                if cid in gs.member_db:
                    card_name = gs.member_db[cid].name
                    new_card_cost = gs.member_db[cid].cost

            # Check if Baton Touch applies (slot is occupied)
            if p.stage[area_idx] >= 0 and p.stage[area_idx] in gs.member_db:
                old_card = gs.member_db[p.stage[area_idx]]
                actual_cost = max(0, new_card_cost - old_card.cost)
                return f"【登場】{card_name} → {area_name} (バトンタッチ: {old_card.name}を控え室、実質コスト{actual_cost})"
            else:
                return f"【登場】{card_name} → {area_name} (コスト{new_card_cost})"

        return f"【登場】{card_name} → {area_name}"

    elif 300 <= a <= 359:
        idx = a - 300
        card_name = f"手札[{idx}]"

        is_human_turn = gs.current_player == 0

        if is_human_turn and idx < len(p.hand):
            cid = p.hand[idx]
            card_name = get_card_name(cid)
            # Check if already selected
            is_selected = idx in p.mulligan_selection
            status = "★選択中" if is_selected else ""
            return f"【マリガン】{card_name} {status}".strip()
        elif not is_human_turn:
            return "【マリガン】相手のカード"

        return f"【マリガン】{card_name}"

    elif 400 <= a <= 459:
        idx = a - 400
        card_name = f"手札[{idx}]"
        score = ""
        if idx < len(p.hand):
            cid = p.hand[idx]
            if cid in gs.live_db:
                live = gs.live_db[cid]
                card_name = live.name
                score = f" (スコア{live.score})"
        return f"【ライブセット】{card_name}{score}"

    elif 200 <= a <= 202:
        areas = ["左サイド", "センター", "右サイド"]
        area_idx = a - 200
        area_name = areas[area_idx]
        cid = p.stage[area_idx]
        card_name = "メンバー"
        ability_text = ""

        if cid >= 0 and cid in gs.member_db:
            card_name = gs.member_db[cid].name
            member = gs.member_db[cid]

            # Get ability text if available
            if hasattr(member, "abilities") and member.abilities:
                from game.ability import TriggerType

                activated_abs = [ab for ab in member.abilities if ab.trigger == TriggerType.ACTIVATED]

                if activated_abs:
                    raw = activated_abs[0].raw_text
                    # Truncate but keep meaningful text
                    if len(raw) > 40:
                        ability_text = f"\n　効果: {raw[:40]}…"
                    else:
                        ability_text = f"\n　効果: {raw}"

        return f"【起動】{card_name} ({area_name}){ability_text}"

    elif 500 <= a <= 559:
        idx = a - 500
        if idx < len(p.hand):
            cid = p.hand[idx]
            name = get_card_name(cid)
            return f"【選択】手札から: {name}"
        return "【選択】手札から選択"

    elif 560 <= a <= 562:
        idx = a - 560
        areas = ["左サイド", "センター", "右サイド"]
        cid = p.stage[idx]
        name = "空きエリア"
        if cid >= 0 and cid in gs.member_db:
            name = gs.member_db[cid].name
        return f"【選択】{areas[idx]}: {name}"

    elif 570 <= a <= 579:
        mode_num = a - 570 + 1
        return f"【モード{mode_num}】を選択"

    elif 580 <= a <= 585:
        colors = ["赤", "青", "緑", "黄", "紫", "ピンク"]
        color = colors[a - 580]
        return f"【色選択】{color}ハート"

    elif 590 <= a <= 599:
        idx = a - 590
        ability_info = ""
        if idx < len(gs.triggered_abilities):
            trigger_info = gs.triggered_abilities[idx]
            # Try to get source card name
            if isinstance(trigger_info, tuple) and len(trigger_info) >= 2:
                source_cid = trigger_info[0] if isinstance(trigger_info[0], int) else None
                if source_cid is not None:
                    ability_info = f": {get_card_name(source_cid)}"
            return f"【自動能力】解決 ({idx + 1}/{len(gs.triggered_abilities)}){ability_info}"
        return "【自動能力】解決"

    elif 600 <= a <= 659:
        idx = a - 600
        if gs.pending_choices:
            choice_type, params = gs.pending_choices[0]
            source_name = params.get("source_card_name", "")
            source_prefix = f"【{source_name}】" if source_name else "【選択】"

            if choice_type == "SELECT_FROM_LIST":
                cards = params.get("cards", [])
                if idx < len(cards):
                    cid = cards[idx]
                    name = get_card_name(cid)
                    return f"{source_prefix}{name}"
            elif choice_type == "TARGET_OPPONENT_MEMBER":
                if idx < 3:
                    areas = ["左サイド", "センター", "右サイド"]
                    opp = gs.inactive_player
                    cid = opp.stage[idx]
                    name = "空きエリア"
                    if cid >= 0 and cid in gs.member_db:
                        name = gs.member_db[cid].name
                    return f"{source_prefix}相手の{areas[idx]}: {name}"
            elif choice_type == "SELECT_SUCCESS_LIVE":
                cards = params.get("cards", [])
                if idx < len(cards):
                    cid = cards[idx]
                    name = get_card_name(cid)
                    return f"【成功ライブ選択】{name}を成功置き場へ"
        return "【選択】対象を選んでください"

    elif 660 <= a <= 719:
        idx = a - 660
        if gs.pending_choices:
            choice_type, params = gs.pending_choices[0]
            source_name = params.get("source_card_name", "")
            source_prefix = f"【{source_name}】" if source_name else "【控え室】"

            if choice_type == "SELECT_FROM_DISCARD":
                cards = params.get("cards", [])
                if idx < len(cards):
                    cid = cards[idx]
                    name = get_card_name(cid)
                    return f"{source_prefix}{name}を回収"
        return "【控え室】カードを選択"

    return "アクション"


@app.route("/")
def index():
    return send_from_directory(WEB_UI_DIR, "index.html")


@app.route("/board")
def game_board():
    return send_from_directory(WEB_UI_DIR, "game_board.html")  # Assuming it exists there


@app.route("/img/<path:filename>")
def serve_img(filename):
    return send_from_directory(IMG_DIR, filename)


@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(os.path.join(WEB_UI_DIR, "js"), filename)


@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(os.path.join(WEB_UI_DIR, "css"), filename)


@app.route("/icon_blade.png")
def serve_icon():
    # If icon is in root or img, adjust. Assuming img for now or checking existence.
    # Fallback to IMG_DIR or WEB_UI_DIR
    return send_from_directory(IMG_DIR, "icon_blade.png")


@app.route("/api/state")
def get_state():
    global game_state
    from game.game_state import Phase

    gs = game_state
    if gs is None:
        init_game()
        gs = game_state  # Update local from global after init
        if gs is None:  # Should technically be impossible if init_game works
            return jsonify(serialize_state())  # Or error

        # Auto-advance if AI goes first or phase is automatic
        max_safety = 100
        while not gs.is_terminal() and max_safety > 0:
            max_safety -= 1

            if gs.phase in (
                Phase.ACTIVE,
                Phase.ENERGY,
                Phase.DRAW,
                Phase.PERFORMANCE_P1,
                Phase.PERFORMANCE_P2,
                Phase.LIVE_RESULT,
            ):
                gs = gs.step(0)
                game_state = gs
                continue

            if gs.current_player == 1:
                if gs.phase in (Phase.MULLIGAN_P1, Phase.MULLIGAN_P2):
                    aid = 0
                else:
                    aid = ai_agent.choose_action(gs, 1)
                gs = gs.step(aid)
                game_state = gs
                continue

            break

    return jsonify(serialize_state())


@app.route("/api/set_deck", methods=["POST"])
def set_deck():
    """Accept a custom deck for a player."""
    global custom_deck_p0, custom_deck_p1, custom_energy_deck_p0, custom_energy_deck_p1
    data = request.json
    player_id = data.get("player", 0)
    deck_ids = data.get("deck", [])  # List of card_no strings
    energy_ids = data.get("energy_deck", [])

    if player_id == 0:
        custom_deck_p0 = deck_ids
        custom_energy_deck_p0 = energy_ids
    else:
        custom_deck_p1 = deck_ids
        custom_energy_deck_p1 = energy_ids

    return jsonify(
        {
            "status": "ok",
            "player": player_id,
            "deck_size": len(deck_ids),
            "message": f"Deck set for Player {player_id + 1}. Reset game to apply.",
        }
    )


@app.route("/api/upload_deck", methods=["POST"])
def upload_deck():
    """Accept a raw deck file content (decktest.txt style) and load it."""
    global custom_deck_p0, custom_deck_p1, custom_energy_deck_p0, custom_energy_deck_p1

    data = request.json
    content = data.get("content", "")
    player_id = data.get("player", 0)

    card_db = {}
    try:
        with open("data/cards.json", "r", encoding="utf-8") as f:
            card_db = json.load(f)
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to load card DB: {e}"})

    main_deck, energy_deck, _, errors = extract_deck_data(content, card_db)

    if errors:
        return jsonify({"success": False, "error": "Validation Errors:\n" + "\n".join(errors)})

    if not main_deck and not energy_deck:
        return jsonify({"success": False, "error": "No cards found in file."})

    # Set Decks
    if player_id == 0:
        custom_deck_p0 = main_deck
        custom_energy_deck_p0 = energy_deck
    else:
        custom_deck_p1 = main_deck
        custom_energy_deck_p1 = energy_deck

    # Reset Game
    init_game(deck_type="custom")

    return jsonify(
        {
            "success": True,
            "main_count": len(main_deck),
            "energy_count": len(energy_deck),
            "message": f"Deck Loaded! ({len(main_deck)} Main, {len(energy_deck)} Energy)",
        }
    )


@app.route("/api/validate_cards", methods=["POST"])
def validate_cards():
    """Validate card IDs against the database and provide type breakdown."""
    data = request.json
    card_ids = data.get("card_ids", [])
    card_counts = data.get("card_counts", {})  # Optional: {card_id: quantity}

    known = []
    unknown = []
    card_info = {}  # card_id -> {type, name, internal_id}

    # Type counters
    member_count = 0
    live_count = 0
    energy_count = 0

    for card_id in card_ids:
        qty = card_counts.get(card_id, 1)
        if card_id in card_no_to_id:
            internal_id = card_no_to_id[card_id]
            known.append(card_id)

            # Determine type and get name
            if internal_id in member_db:
                card_info[card_id] = {"type": "Member", "name": member_db[internal_id].name}
                member_count += qty
            elif internal_id in live_db:
                card_info[card_id] = {"type": "Live", "name": live_db[internal_id].name}
                live_count += qty
            elif internal_id in energy_db:
                card_info[card_id] = {"type": "Energy", "name": energy_db[internal_id].name}
                energy_count += qty
        else:
            unknown.append(card_id)

    return jsonify(
        {
            "known": known,
            "unknown": unknown,
            "known_count": len(known),
            "unknown_count": len(unknown),
            "card_info": card_info,
            "breakdown": {"member": member_count, "live": live_count, "energy": energy_count},
        }
    )


@app.route("/api/clear_performance", methods=["POST"])
def clear_performance():
    global game_state
    if game_state:
        # Check attribute existence for safety (mypy complaint)
        if hasattr(game_state, "last_performance_result"):
            game_state.last_performance_result = None
    return jsonify({"status": "ok"})


@app.route("/api/action", methods=["POST"])
def do_action():
    global game_state
    gs = game_state
    if gs is None:
        return jsonify({"success": False, "error": "Game not initialized"}), 400

    # Re-import Phase locally to prevent NameError if module scope is borked
    from game.game_state import Phase

    data = request.json
    action_id = data.get("action_id", 0)
    force = data.get("force", False)

    legal_mask = gs.get_legal_actions()
    is_legal = legal_mask[action_id]
    print(
        f"DEBUG do_action: action={action_id}, force={force}, is_legal={is_legal}, phase={gs.phase}, player={gs.current_player}"
    )

    if force or is_legal:
        try:
            gs = gs.step(action_id)
            game_state = gs

            # AUTO-ADVANCE LOOP
            # Advance through automatic phases AND AI turns
            max_safety = 100

            # Record state after the user's initial action
            game_history.append(serialize_state())

            while not gs.is_terminal() and max_safety > 0:
                max_safety -= 1

                # 1. Automatic phases (phases that don't need real human interaction beyond a 'confirm' or 'auto')
                if gs.phase in (
                    Phase.ACTIVE,
                    Phase.ENERGY,
                    Phase.DRAW,
                    Phase.PERFORMANCE_P1,
                    Phase.PERFORMANCE_P2,
                    Phase.LIVE_RESULT,
                ):
                    gs = gs.step(0)
                    game_state = gs
                    game_history.append(serialize_state())
                    continue

                # 2. AI Turn (P1 is always the AI)
                if gs.current_player == 1:
                    if gs.phase in (Phase.MULLIGAN_P1, Phase.MULLIGAN_P2):
                        # Force-confirm AI mulligan to speed up and prevent info leak
                        aid = 0
                    else:
                        aid = ai_agent.choose_action(gs, 1)
                    print(f"DEBUG AI Move: action={aid}, phase={gs.phase}")
                    gs = gs.step(aid)
                    game_state = gs
                    game_history.append(serialize_state())
                    continue

                # If it's P0's turn and not an automatic phase, wait for user
                break

            if gs.is_terminal():
                save_replay()

            return jsonify({"success": True, "state": serialize_state()})
        except Exception as e:
            import traceback

            traceback.print_exc()
            return jsonify({"success": False, "error": str(e), "trace": traceback.format_exc()}), 500
    else:
        return jsonify({"success": False, "error": f"Illegal action {action_id} in {gs.phase}"})


@app.route("/api/exec", methods=["POST"])
@app.route("/api/exec", methods=["POST"])
def god_mode():
    global game_state
    if game_state is None:
        return jsonify({"success": False, "error": "Game not initialized"})
    code = request.json.get("code", "")
    try:
        p = game_state.active_player
        exec(code, {"state": game_state, "p": p, "np": np})
        return jsonify({"success": True, "state": serialize_state()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/reset", methods=["POST"])
def reset():
    global game_state
    try:
        # Re-import Phase for safety
        import time

        from game.game_state import Phase

        random.seed(time.time())  # Ensure fresh seed
        print("DEBUG: Reset called")

        data = request.json or {}
        deck_type = data.get("deck_type", "normal")
        print(f"DEBUG: Initializing game with {deck_type}")
        init_game(deck_type)
        gs = game_state
        if gs:
            print(f"DEBUG: Game initialized. Phase is {gs.phase}")
            print(f"DEBUG: P0 Energy: {len(gs.players[0].energy_zone)}")
        else:
            print("DEBUG: Game init failed (gs is None)")
            return jsonify({"success": False, "error": "Init failed"}), 500

        # Check if AI goes first or automatic phase
        # Run the same auto-advance loop as do_action to get to P0's turn or terminal
        max_safety = 100
        # Use local variable for type narrowing
        gs = game_state
        if gs is None:  # Should be initialized by init_game above, but for safety
            return jsonify({"success": False, "error": "Game init failed"}), 500

        while not gs.is_terminal() and max_safety > 0:
            max_safety -= 1

            # 1. Automatic phases (NOT including Mulligan)
            if gs.phase in (
                Phase.ACTIVE,
                Phase.ENERGY,
                Phase.DRAW,
                Phase.PERFORMANCE_P1,
                Phase.PERFORMANCE_P2,
                Phase.LIVE_RESULT,
            ):
                print(f"DEBUG: Auto-advancing Phase {gs.phase}")
                gs = gs.step(0)
                game_state = gs
                continue

            # 2. AI Turn (P1)
            if gs.current_player == 1:
                if gs.phase in (Phase.MULLIGAN_P1, Phase.MULLIGAN_P2):
                    aid = 0
                else:
                    aid = ai_agent.choose_action(gs, 1)
                print(f"DEBUG AI Move (Reset): action={aid}, phase={gs.phase}")
                gs = gs.step(aid)
                game_state = gs
                continue

            # P0 turn
            print("DEBUG: Player 0 Turn Reached")
            break

        return jsonify({"success": True, "state": serialize_state()})
    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/replay/<filename>")
def get_replay(filename):
    """Serve replay JSON files"""
    replay_path = f"replays/{filename}"
    if os.path.exists(replay_path):
        with open(replay_path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"error": "Replay not found"}), 404


@app.route("/api/advance", methods=["POST"])
def advance():
    global game_state
    gs = game_state
    if gs is None:
        return jsonify({"success": False, "error": "Game not initialized"})
    from game.game_state import Phase

    # Run auto-advance loop
    max_safety = 50
    while not gs.is_terminal() and max_safety > 0:
        max_safety -= 1
        # Advance if in an automatic phase OR if it's the AI's turn
        if gs.phase in (
            Phase.ACTIVE,
            Phase.ENERGY,
            Phase.DRAW,
            Phase.PERFORMANCE_P1,
            Phase.PERFORMANCE_P2,
            Phase.LIVE_RESULT,
        ):
            gs = gs.step(0)
            game_state = gs
            continue

        # If it's the AI's turn (P1), let it act immediately
        if gs.current_player == 1 and not gs.is_terminal():
            aid = ai_agent.choose_action(gs, 1)
            gs = gs.step(aid)
            game_state = gs
            continue

        break

    return jsonify({"success": True, "state": serialize_state()})


@app.route("/api/full_log", methods=["GET"])
def get_full_log():
    """Return the complete rule log without truncation."""
    gs = game_state
    if gs is None:
        return jsonify({"log": [], "total_entries": 0})
    return jsonify({"log": gs.rule_log, "total_entries": len(gs.rule_log)})


@app.route("/api/report_issue", methods=["POST"])
def report_issue():
    """Save the current game state and user explanation to a report file."""
    try:
        data = request.json
        explanation = data.get("explanation", "")
        # We can take the current state from the request or just use our global game_state
        # Providing it in the request is safer if the user is looking at a specific frame (e.g. in replay mode)
        # But for now, let's use the provided state if it exists, otherwise capture the current one.
        state_to_save = data.get("state") or serialize_state()
        history = data.get("history", [])  # Optionally capture action history if UI has it

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("reports", exist_ok=True)

        filename = f"reports/report_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "timestamp": timestamp,
                    "explanation": explanation,
                    "state": state_to_save,
                    "history": history,
                    "action_desc": get_action_desc(state_to_save.get("last_action", 0), game_state)
                    if "last_action" in state_to_save
                    else "N/A",
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        return jsonify({"success": True, "filename": filename})
    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    # PyInstaller Bundle Check
    if getattr(sys, "frozen", False):
        # If frozen, we might need to adjust static folder or templates folder depending on how flask finds them.
        # However, we added paths with --add-data, so they should be in sys._MEIPASS.
        # Flask's root_path defaults to __main__ directory, which in onefile mode is temporary.
        # We need to explicitly point static_folder to the MEIPASS location.
        bundle_dir = getattr(sys, "_MEIPASS", ".")  # type: ignore
        app.static_folder = os.path.join(bundle_dir, "web_ui")
        # app.template_folder = os.path.join(bundle_dir, 'templates') # if we used templates

        # Also need to make sure data loader finds 'data/cards.json'
        # CardDataLoader expects relative path. We might need to chdir or patch it.
        # Easiest is to chdir to the bundle dir so relative paths work?
        # BUT 'replays' need to be written to writable cwd, not temp dir.
        # So we should NOT chdir globally.
        # Instead, we should update filenames to be absolute paths based on bundle_dir if read-only.

        # Monkey patch the loader path just for this instance if needed,
        # but CardDataLoader takes a path arg.
        # We need to ensure 'init_game' calls it with the correct absolute path.
        pass

    # Patched init_game for Frozen state to find data
    original_init_game = init_game

    def frozen_init_game(deck_type="normal"):
        if getattr(sys, "frozen", False):
            bundle_dir = getattr(sys, "_MEIPASS", ".")  # type: ignore
            os.path.join(bundle_dir, "data", "cards.json")

            # We need to temporarily force the loader to use this path
            # But init_game hardcodes "data/cards.json" in correct logic?
            # actually checking init_game source:
            #   loader = CardDataLoader("data/cards.json")
            # We need to change that line or intercept.

            # Use os.chdir to temp dir for READS? No, we need writes to real dir.
            # Best way: Just ensure data/cards.json exists in CWD? No, user won't have it.

            # HACK: We can't easily change the hardcoded string inside init_game without rewriting it.
            # However, we can patch CardDataLoader class to fix the path!
            # Assuming CardDataLoader is imported from game.data_loader
            from game.data_loader import CardDataLoader

            ops_init = CardDataLoader.__init__

            def new_init(self, filepath):
                if not os.path.exists(filepath) and getattr(sys, "frozen", False):
                    # Try bundle path
                    bundle_path = os.path.join(sys._MEIPASS, filepath)  # type: ignore
                    if os.path.exists(bundle_path):
                        filepath = bundle_path
                ops_init(self, filepath)

            CardDataLoader.__init__ = new_init  # type: ignore[method-assign]

        original_init_game(deck_type)

    init_game = frozen_init_game

    # Auto-open browser
    import webbrowser
    from threading import Timer

    def open_browser():
        webbrowser.open_new("http://localhost:8000/")

    Timer(1.5, open_browser).start()

    # Run Server
    # use_reloader=False is crucial for PyInstaller to implicit avoid spawning subprocesses incorrectly
    app.run(host="0.0.0.0", port=8000, debug=False, use_reloader=False)
