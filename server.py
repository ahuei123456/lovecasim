"""
Flask Backend for Love Live Card Game Web UI
"""
import os
import sys
import random
import json
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, request, send_from_directory
from game.game_state import GameState, Phase
from game.data_loader import CardDataLoader
from headless_runner import RandomAgent, create_easy_cards

app = Flask(__name__, static_folder='web_ui')
ai_agent = RandomAgent()

# Global game state
game_state = None
member_db = {}
live_db = {}
energy_db = {}

def init_game(deck_type='normal'):
    global game_state, member_db, live_db, energy_db
    loader = CardDataLoader("data/cards.json")
    member_db, live_db, energy_db = loader.load()
    
    # CRITICAL: Populate GameState static DBs so validations work
    GameState.member_db = member_db
    GameState.live_db = live_db
    
    # Pre-calculate Start Deck card IDs
    start_deck_m = []
    start_deck_l = []
    
    # Load raw JSON to check product field for filtering
    with open("data/cards.json", 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    for cid, m in member_db.items():
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
    
    if deck_type == 'easy':
        easy_m, easy_l = create_easy_cards()
        member_db[easy_m.card_id] = easy_m
        live_db[easy_l.card_id] = easy_l
        
    game_state = GameState()
    
    # Setup players
    for p in game_state.players:
        if deck_type == 'easy':
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
                    if len(member_bucket) >= 150: # Optimization: Don't build massive list
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
                    if len(live_bucket) >= 50: break
                
                if len(live_bucket) < 12:
                     while len(live_bucket) < 12:
                         live_bucket.extend(available_lives)
                         
                p.main_deck.extend(live_bucket[:12])
            
            random.shuffle(p.main_deck)
        
        # Energy Deck (12 cards)
        # Use actual Energy Card ID if available (2000+)
        if energy_db:
            eid = list(energy_db.keys())[0] # Take first energy card type found
            p.energy_deck = [eid] * 12
        else:
            p.energy_deck = [200] * 12 # Fallback
        
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

def serialize_card(cid):
    if cid in member_db:
        m = member_db[cid]
        return {
            'id': int(cid), 
            'name': m.name, 
            'cost': int(m.cost), 
            'type': 'member', 
            'img': m.img_path,
            'hp': int(m.total_hearts()),
            'blade': int(m.blades),
            'hearts': m.hearts.tolist(),  # Array of 6 colors
            'blade_hearts': m.blade_hearts.tolist(),  # Yell contribution
            'text': getattr(m, 'ability_text', '')
        }
    elif cid in live_db:
        l = live_db[cid]
        return {
            'id': int(cid), 
            'name': l.name, 
            'cost': int(l.total_required()), 
            'type': 'live', 
            'img': l.img_path,
            'score': int(l.score),
            'required_hearts': l.required_hearts.tolist(),  # Array of 7 (6 colors + any)
            'text': getattr(l, 'ability_text', '')
        }
    elif cid in energy_db:
        e = energy_db[cid]
        return {
            'id': int(cid),
            'name': e.name,
            'type': 'energy',
            'img': e.img_path
        }
    else:
        # Fallback for special IDs or unknown cards
        if cid == 888:
            return {'id': 888, 'name': 'Member (Easy)', 'cost': 1, 'img': 'img/cards/PLSD01/PL!-sd1-001-SD.png', 'type': 'member', 'hp': 1, 'blade': 1, 'hearts': [1,0,0,0,0,0], 'blade_hearts': [0,0,0,0,0,0], 'text': ''}
        if cid == 999:
            return {'id': 999, 'name': 'Live (Easy)', 'score': 1, 'img': 'img/cards/PLSD01/PL!-pb1-019-SD.png', 'type': 'live', 'cost': 1, 'required_hearts': [0,0,0,0,0,0,1], 'text': ''}
        return {'id': int(cid), 'name': f'Card {cid}', 'type': 'unknown', 'img': None}

def serialize_player(p, is_human):
    legal_mask = game_state.get_legal_actions()
    
    hand = []
    if is_human:
        for i, cid in enumerate(p.hand):
            c = serialize_card(cid)
            # Find legal actions for this card index (i)
            # Logic from game_state.get_legal_actions:
            # Play Member: 1 + i*3 + area (0,1,2)
            # Set Live: 64 + i (if phase is LIVE_SET)
            # Mulligan: 181 + i
            
            valid_actions = []
            
            # Check Play Member actions
            for area in range(3):
                aid = 1 + i * 3 + area
                if aid < len(legal_mask) and legal_mask[aid]:
                    valid_actions.append(aid)
            
            # Check Live Set action
            aid_live = 64 + i
            if aid_live < len(legal_mask) and legal_mask[aid_live]:
                valid_actions.append(aid_live)
                
            c['valid_actions'] = valid_actions
            hand.append(c)
    else:
        hand = [{'hidden': True, 'type': 'unknown'}] * len(p.hand)
    
    stage = []
    for i in range(3):
        cid = int(p.stage[i])
        if cid >= 0:
            c = serialize_card(cid)
            c['tapped'] = bool(p.tapped_members[i])
            c['energy'] = len(p.stage_energy[i])
            stage.append(c)
        else:
            stage.append(None)
    
    discard = [serialize_card(cid) for cid in p.discard]
    energy = [{'id': i, 'tapped': bool(p.tapped_energy[i]) if i < len(p.tapped_energy) else False} for i, _ in enumerate(p.energy_zone)]
    live_zone = [serialize_card(cid) for cid in p.live_zone]
    success_lives = [serialize_card(cid) for cid in p.success_lives]
    
    return {
        'player_id': p.player_id,
        'is_active': is_human,
        'hand': hand,
        'hand_count': len(p.hand),
        'mulligan_selection': list(getattr(p, 'mulligan_selection', [])) if is_human else [],
        'deck_count': len(p.main_deck),
        'energy_deck_count': len(p.energy_deck), # NEW
        'discard': discard,
        'discard_count': len(p.discard),
        'energy': energy,
        'energy_count': len(p.energy_zone),
        'energy_untapped': int(p.count_untapped_energy()),
        'live_zone': live_zone,
        'live_zone_count': len(p.live_zone), # Useful for AI
        'success_lives': success_lives,
        'score': len(p.success_lives),
        'stage': stage
    }

def serialize_state():
    global game_state
    active_idx = game_state.current_player
    
    legal_mask = game_state.get_legal_actions()
    legal_actions = []
    for i, v in enumerate(legal_mask):
        if v:
            desc = get_action_desc(i, game_state)
            
            # Create rich metadata for hover effects
            meta = {'id': i, 'desc': desc}
            
            p = game_state.active_player
            # 1. Play Member (1-180)
            if 1 <= i <= 180:
                idx = (i - 1) // 3
                area = (i - 1) % 3
                meta['type'] = 'PLAY'
                meta['hand_idx'] = idx
                meta['area_idx'] = area
                
                # Check baton touch for cost info
                cost = 0
                if idx < len(p.hand) and p.hand[idx] in game_state.member_db:
                    cost = game_state.member_db[p.hand[idx]].cost
                
                if p.stage[area] >= 0 and p.stage[area] in game_state.member_db:
                    prev = game_state.member_db[p.stage[area]]
                    meta['is_baton'] = True
                    meta['prev_cost'] = prev.cost
                    meta['final_cost'] = max(0, cost - prev.cost)
                else:
                    meta['final_cost'] = cost

            # 2. Mulligan (181-240)
            elif 181 <= i <= 240:
                idx = i - 181
                meta['type'] = 'MULLIGAN'
                meta['hand_idx'] = idx
            
            # 3. Live Set (64-123)
            elif 64 <= i <= 123:
                idx = i - 64
                meta['type'] = 'LIVE_SET'
                meta['hand_idx'] = idx
            
            # 4. Ability (200-202)
            elif 200 <= i <= 202:
                area = i - 200
                meta['type'] = 'ABILITY'
                meta['area_idx'] = area

            legal_actions.append(meta)
    
    return {
        'turn': game_state.turn_number,
        'phase': int(game_state.phase),  # Return numeric phase, not string name
        'active_player': int(active_idx),
        'players': [
            serialize_player(game_state.players[0], True), # P0 is ALWAYS human-viewable
            serialize_player(game_state.players[1], False) # P1 is ALWAYS hidden (AI)
        ],
        'legal_actions': legal_actions,
        'resolution_zone': [serialize_card(cid) for cid in game_state.yell_cards],
        'pending_choice': game_state.pending_choices[0] if game_state.pending_choices else None,
        'rule_log': game_state.rule_log[-10:] # Last 10 rules for display
    }

def get_action_desc(a, gs):
    if gs is None: return f"Action {a}"
    p = gs.active_player
    
    if a == 0: 
        if gs.phase == Phase.MAIN: return "メインフェイズ終了 (パス)"
        if gs.phase == Phase.LIVE_SET: return "ライブセット完了 (確定)"
        return "パス / 確定"
        
    elif 1 <= a <= 180:
        idx = (a - 1) // 3
        area_idx = (a - 1) % 3
        areas = ["左", "中", "右"]
        area_name = areas[area_idx]
        
        card_name = f"手札[{idx}]"
        if idx < len(p.hand):
            cid = p.hand[idx]
            if cid in gs.member_db:
                card_name = gs.member_db[cid].name
        
        # Check for Baton Touch (Stacking on existing member)
        suffix = ""
        if p.stage[area_idx] >= 0:
            if p.stage[area_idx] in gs.member_db:
                prev_cost = gs.member_db[p.stage[area_idx]].cost
                suffix = f" (バトンタッチ: -{prev_cost}コスト)"
        
        return f"{card_name}を{area_name}に置く{suffix}"
        
    elif 181 <= a <= 240:
        idx = a - 181
        card_name = f"手札[{idx}]"
        if idx < len(p.hand):
            cid = p.hand[idx]
            if cid in gs.member_db: card_name = gs.member_db[cid].name
            elif cid in gs.live_db: card_name = gs.live_db[cid].name
            
        return f"{card_name}をマリガン対象にする/外す"
        
    elif 64 <= a <= 123:
        idx = a - 64
        card_name = f"Hand[{idx}]"
        card_name = f"手札[{idx}]"
        if idx < len(p.hand):
            cid = p.hand[idx]
            if cid in gs.live_db: card_name = gs.live_db[cid].name
        return f"{card_name}をライブとしてセット"
        
    elif 200 <= a <= 202:
        areas = ["左", "中", "右"]
        area_name = areas[a - 200]
        cid = p.stage[a - 200]
        card_name = "メンバー"
        if cid in gs.member_db: card_name = gs.member_db[cid].name
        return f"{card_name}のスキル発動 ({area_name})"
        
    elif 270 <= a <= 279:
        return f"モード選択 {a - 270}"
    elif 280 <= a <= 285:
        colors = ["赤", "青", "緑", "黄", "紫", "ピンク"]
        return f"色選択: {colors[a-280]}"
    return f"Action {a}"

@app.route('/')
def index():
    return send_from_directory('web_ui', 'index.html')

@app.route('/board')
def game_board():
    return send_from_directory('web_ui', 'game_board.html')

@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('img', filename)

@app.route('/api/state')
def get_state():
    if game_state is None:
        init_game()
    return jsonify(serialize_state())

@app.route('/api/action', methods=['POST'])
def do_action():
    global game_state
    # Re-import Phase locally to prevent NameError if module scope is borked
    from game.game_state import Phase
    
    data = request.json
    action_id = data.get('action_id', 0)
    force = data.get('force', False)
    
    legal_mask = game_state.get_legal_actions()
    is_legal = legal_mask[action_id]
    print(f"DEBUG do_action: action={action_id}, force={force}, is_legal={is_legal}, phase={game_state.phase}, player={game_state.current_player}")
    
    if force or is_legal:
        game_state = game_state.step(action_id)
        
        # AUTO-ADVANCE LOOP
        # Advance through automatic phases AND AI turns
        max_safety = 100
        while not game_state.is_terminal() and max_safety > 0:
            max_safety -= 1
            
            # 1. Automatic phases (phases that don't need real human interaction beyond a 'confirm' or 'auto')
            if game_state.phase in (Phase.ACTIVE, Phase.ENERGY, Phase.DRAW, 
                                   Phase.PERFORMANCE_P1, Phase.PERFORMANCE_P2, Phase.LIVE_RESULT):
                game_state = game_state.step(0)
                continue
            
            # 2. AI Turn (P1 is always the AI)
            if game_state.current_player == 1:
                aid = ai_agent.choose_action(game_state, 1)
                print(f"DEBUG AI Move: action={aid}, phase={game_state.phase}")
                game_state = game_state.step(aid)
                continue
                
            # If it's P0's turn and not an automatic phase, wait for user
            break
            
        return jsonify({'success': True, 'state': serialize_state()})
    else:
        return jsonify({'success': False, 'error': f'Illegal action {action_id} in {game_state.phase}'})

@app.route('/api/exec', methods=['POST'])
def god_mode():
    global game_state
    code = request.json.get('code', '')
    try:
        p = game_state.active_player
        exec(code, {'state': game_state, 'p': p, 'np': np})
        return jsonify({'success': True, 'state': serialize_state()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/reset', methods=['POST'])
def reset():
    global game_state
    try:
        # Re-import Phase for safety
        from game.game_state import Phase
        import time
        random.seed(time.time()) # Ensure fresh seed
        print("DEBUG: Reset called")

        data = request.json or {}
        deck_type = data.get('deck_type', 'normal')
        print(f"DEBUG: Initializing game with {deck_type}")
        init_game(deck_type)
        print(f"DEBUG: Game initialized. Phase is {game_state.phase}")
        print(f"DEBUG: P0 Energy: {len(game_state.players[0].energy_zone)}")
        
        # Check if AI goes first or automatic phase
        # Run the same auto-advance loop as do_action to get to P0's turn or terminal
        max_safety = 100
        while not game_state.is_terminal() and max_safety > 0:
            max_safety -= 1
            
            # 1. Automatic phases (NOT including Mulligan)
            if game_state.phase in (Phase.ACTIVE, Phase.ENERGY, Phase.DRAW, 
                                   Phase.PERFORMANCE_P1, Phase.PERFORMANCE_P2, Phase.LIVE_RESULT):
                print(f"DEBUG: Auto-advancing Phase {game_state.phase}")
                game_state = game_state.step(0)
                continue
            
            # 2. AI Turn (P1)
            if game_state.current_player == 1:
                aid = ai_agent.choose_action(game_state, 1)
                print(f"DEBUG AI Move (Reset): action={aid}, phase={game_state.phase}")
                game_state = game_state.step(aid)
                continue
                
            # P0 turn
            print("DEBUG: Player 0 Turn Reached")
            break
             
        return jsonify({'success': True, 'state': serialize_state()})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    init_game()
    print("Starting server at http://localhost:5000")
    app.run(debug=True, port=5000)
