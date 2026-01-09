
import json
import numpy as np
from game.game_state import GameState, Phase
from game.ability import TriggerType

def serialize_card(cid, member_db, live_db, energy_db, is_viewable=True, peek=False):
    if not is_viewable and not peek:
        return {
            'id': int(cid),
            'name': '???',
            'type': 'unknown',
            'img': 'cards/back.png',
            'hidden': True
        }
    
    card_data = {}
    
    # Handle unknown/placeholder IDs
    if cid == 888:
        return {'id': 888, 'name': 'Member (Easy)', 'cost': 1, 'img': 'cards/PLSD01/PL!-sd1-001-SD.png', 'type': 'member', 'hp': 1, 'blade': 1, 'hearts': [1,0,0,0,0,0], 'blade_hearts': [0,0,0,0,0,0], 'text': ''}
    if cid == 999:
        return {'id': 999, 'name': 'Live (Easy)', 'score': 1, 'img': 'cards/PLSD01/PL!-pb1-019-SD.png', 'type': 'live', 'cost': 1, 'required_hearts': [0,0,0,0,0,0,1], 'text': ''}

    if cid in member_db:
        m = member_db[cid]
        ability_text = getattr(m, 'ability_text', '')
        if hasattr(m, 'abilities') and m.abilities:
            ability_lines = []
            for ab in m.abilities:
                trigger_icon = {
                    TriggerType.ACTIVATED: '【起動】',
                    TriggerType.ON_PLAY: '【登場】',
                    TriggerType.CONSTANT: '【常時】',
                    TriggerType.ON_LIVE_START: '【ライブ開始】',
                    TriggerType.ON_LIVE_SUCCESS: '【ライブ成功時】'
                }.get(ab.trigger, '【自動】')
                ability_lines.append(f"{trigger_icon} {ab.raw_text}")
            ability_text = "\n".join(ability_lines)

        card_data = {
            'id': int(cid),
            'name': m.name,
            'type': 'member',
            'cost': m.cost,
            'hp': 1, 
            'blade': m.blades, 
            'img': m.img_path,
            'hearts': m.hearts.tolist(),
            'blade_hearts': m.blade_hearts.tolist(),
            'color': 'Unknown',
            'text': ability_text
        }
    elif cid in live_db:
        l = live_db[cid]
        ability_text = getattr(l, 'ability_text', '')
        if hasattr(l, 'abilities') and l.abilities:
             ability_lines = []
             for ab in l.abilities:
                 trigger_icon = {
                    TriggerType.ON_LIVE_START: '【ライブ開始】'
                 }.get(ab.trigger, '【自動】')
                 ability_lines.append(f"{trigger_icon} {ab.raw_text}")
             ability_text = "\n".join(ability_lines)

        card_data = {
            'id': int(cid),
            'name': l.name,
            'type': 'live',
            'score': l.score,
            'img': l.img_path,
            'required_hearts': l.required_hearts.tolist(),
            'text': ability_text
        }
    elif cid in energy_db:
        e = energy_db[cid]
        card_data = {
            'id': int(cid),
            'name': e.name,
            'type': 'energy',
            'img': e.img_path
        }
    else:
        return {'id': cid, 'name': f'Card {cid}', 'type': 'unknown', 'img': None}
    
    if not is_viewable and peek:
        card_data['hidden'] = True
        card_data['face_down'] = True 
        
    return card_data

def serialize_player(p, game_state, player_idx, viewer_idx=0, is_viewable=True):
    # Calculate expected yell count based on total blades
    expected_yells = 0
    if hasattr(game_state, 'member_db'):
        for i, card_id in enumerate(p.stage):
            if card_id >= 0 and not p.tapped_members[i] and card_id in game_state.member_db:
                member = game_state.member_db[card_id]
                expected_yells += member.blades
    
    legal_mask = game_state.get_legal_actions()
    member_db = game_state.member_db
    live_db = game_state.live_db
    energy_db = getattr(game_state, 'energy_db', {})
    
    hand = []
    if is_viewable:
        for i, cid in enumerate(p.hand):
            c = serialize_card(cid, member_db, live_db, energy_db)
            valid_actions = []
            
            for area in range(3):
                aid = 1 + i * 3 + area
                if aid < len(legal_mask) and legal_mask[aid]:
                    valid_actions.append(aid)
            
            aid_live = 400 + i
            if aid_live < len(legal_mask) and legal_mask[aid_live]:
                valid_actions.append(aid_live)
            
            aid_mull = 300 + i
            if aid_mull < len(legal_mask) and legal_mask[aid_mull]:
                valid_actions.append(aid_mull)
                
            c['valid_actions'] = valid_actions
            hand.append(c)
    else:
        hand = [serialize_card(cid, member_db, live_db, energy_db, is_viewable=False) for cid in p.hand]
    
    stage = []
    for i in range(3):
        cid = int(p.stage[i])
        if cid >= 0:
            c = serialize_card(cid, member_db, live_db, energy_db)
            c['tapped'] = bool(p.tapped_members[i])
            c['energy'] = len(p.stage_energy[i])
            stage.append(c)
        else:
            stage.append(None)
    
    discard = [serialize_card(cid, member_db, live_db, energy_db, is_viewable=True) for cid in p.discard]
    
    energy = []
    for i, _ in enumerate(p.energy_zone):
        # Handle index out of bounds safe access for tapped array? No, numpy array is large enough (50)
        is_tapped = bool(p.tapped_energy[i]) if i < len(p.tapped_energy) else False
        energy.append({
            'id': i, 
            'tapped': is_tapped, 
            'card': serialize_card(p.energy_zone[i], member_db, live_db, energy_db, is_viewable=False)
        })

    live_zone = []
    for i, cid in enumerate(p.live_zone):
        is_revealed = False
        if i < len(p.live_zone_revealed):
             is_revealed = bool(p.live_zone_revealed[i])
        
        can_peek = (player_idx == viewer_idx)
        live_zone.append(serialize_card(cid, member_db, live_db, energy_db, is_viewable=is_revealed, peek=can_peek))

    score = 0
    for cid in p.success_lives:
        if cid in live_db:
            score += live_db[cid].score
    
    return {
        'player_id': p.player_id,
        'score': score,
        'is_active': is_viewable,
        'hand': hand,
        'hand_count': len(p.hand),
        'mulligan_selection': list(getattr(p, 'mulligan_selection', [])) if is_viewable else [],
        'deck_count': len(p.main_deck),
        'energy_deck_count': len(p.energy_deck),
        'discard': discard,
        'discard_count': len(p.discard),
        'energy': energy,
        'energy_count': len(p.energy_zone),
        'energy_untapped': int(p.count_untapped_energy()),
        'live_zone': live_zone,
        'live_zone_count': len(p.live_zone),
        'stage': stage,
        'success_lives': [serialize_card(cid, member_db, live_db, energy_db, is_viewable) for cid in p.success_lives],
        'restrictions': list(p.restrictions),
        'expected_yells': expected_yells
    }

def get_action_desc(a, gs):
    if gs is None: return f"Action {a}"
    p = gs.active_player
    member_db = gs.member_db
    live_db = gs.live_db
    
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
        new_card_cost = 0
        if idx < len(p.hand):
            cid = p.hand[idx]
            if cid in member_db:
                card_name = member_db[cid].name
                new_card_cost = member_db[cid].cost
        
        if p.stage[area_idx] >= 0 and p.stage[area_idx] in member_db:
            old_card = member_db[p.stage[area_idx]]
            actual_cost = max(0, new_card_cost - old_card.cost)
            return f"{card_name}を{area_name}に置く (バトンタッチ: {old_card.name}, コスト {actual_cost})"
        
        return f"{card_name}を{area_name}に置く (コスト {new_card_cost})"
        
    elif 300 <= a <= 359:
        idx = a - 300
        card_name = f"手札[{idx}]"
        if idx < len(p.hand):
            cid = p.hand[idx]
            if cid in member_db: card_name = member_db[cid].name
            elif cid in live_db: card_name = live_db[cid].name
            
        return f"{card_name}をマリガン対象にする/外す"
        
    elif 400 <= a <= 459:
        idx = a - 400
        card_name = f"手札[{idx}]"
        if idx < len(p.hand):
            cid = p.hand[idx]
            if cid in live_db: card_name = live_db[cid].name
        return f"{card_name}をライブとしてセット"
        
    elif 200 <= a <= 202:
        areas = ["左", "中", "右"]
        area_idx = a - 200
        area_name = areas[area_idx]
        cid = p.stage[area_idx]
        card_name = "メンバー"
        ability_summary = ""
        
        if cid >= 0 and cid in member_db:
            card_name = member_db[cid].name
            member = member_db[cid]
            if hasattr(member, 'abilities') and member.abilities:
                activated_abs = [ab for ab in member.abilities if ab.trigger == TriggerType.ACTIVATED]
                if activated_abs:
                    ability_summary = f" - {activated_abs[0].raw_text[:50]}..."
                    if len(activated_abs[0].raw_text) <= 50:
                        ability_summary = f" - {activated_abs[0].raw_text}"
        
        return f"{card_name}のスキル発動 ({area_name}){ability_summary}"
        
    elif 500 <= a <= 559:
        idx = a - 500
        if idx < len(p.hand):
            cid = p.hand[idx]
            name = "Card"
            if cid in member_db: name = member_db[cid].name
            elif cid in live_db: name = live_db[cid].name
            return f"{name}を選択"
        return f"手札のカード {idx} を選択"

    elif 560 <= a <= 562:
        idx = a - 560
        areas = ["左", "中", "右"]
        cid = p.stage[idx]
        name = "メンバー"
        if cid >= 0 and cid in member_db: name = member_db[cid].name
        return f"{areas[idx]}の{name}を選択"

    elif 570 <= a <= 579:
        return f"モード選択 {a - 570}"
    
    elif 580 <= a <= 585:
        colors = ["赤", "青", "緑", "黄", "紫", "ピンク"]
        return f"色選択: {colors[a-580]}"

    elif 590 <= a <= 599:
        idx = a - 590
        if idx < len(gs.triggered_abilities):
            return f"自動能力の解決 ({idx+1}/{len(gs.triggered_abilities)})"
        return f"自動能力の解決 {idx}"
        
    elif 600 <= a <= 659:
        idx = a - 600
        if gs.pending_choices:
            choice_type, params = gs.pending_choices[0]
            if choice_type == "SELECT_FROM_LIST":
                cards = params.get('cards', [])
                if idx < len(cards):
                    cid = cards[idx]
                    name = "Card"
                    if cid in member_db: name = member_db[cid].name
                    elif cid in live_db: name = live_db[cid].name
                    return f"{name}を選択"
            elif choice_type == "TARGET_OPPONENT_MEMBER":
                 if idx < 3:
                     areas = ["左", "中", "右"]
                     opp = gs.inactive_player
                     cid = opp.stage[idx]
                     name = "メンバー"
                     if cid >= 0 and cid in member_db: name = member_db[cid].name
                     return f"相手の{areas[idx]}の{name}を選択"
        return f"選択 {idx}"

    elif 660 <= a <= 719:
        idx = a - 660
        if gs.pending_choices:
            choice_type, params = gs.pending_choices[0]
            if choice_type == "SELECT_FROM_DISCARD":
                cards = params.get('cards', [])
                if idx < len(cards):
                    cid = cards[idx]
                    name = "Card"
                    if cid in member_db: name = member_db[cid].name
                    elif cid in live_db: name = live_db[cid].name
                    return f"{name}を選択"
        return f"控え室のカード {idx} を選択"

    return f"Action {a}"

def serialize_state(game_state):
    active_idx = game_state.current_player
    legal_mask = game_state.get_legal_actions()
    legal_actions = []
    p = game_state.active_player
    member_db = game_state.member_db
    
    for i, v in enumerate(legal_mask):
        if v:
            desc = get_action_desc(i, game_state)
            meta = {'id': i, 'desc': desc}
            
            if 1 <= i <= 180:
                meta['type'] = 'PLAY'
                meta['hand_idx'] = (i - 1) // 3
                meta['area_idx'] = (i - 1) % 3
                if meta['hand_idx'] < len(p.hand):
                    cid = p.hand[meta['hand_idx']]
                    c_data = serialize_card(cid, member_db, game_state.live_db, getattr(game_state, 'energy_db', {}))
                    meta['img'] = c_data['img']
                    meta['name'] = c_data['name']
                    meta['cost'] = c_data.get('cost', 0)
                    
            elif 200 <= i <= 202:
                meta['type'] = 'ABILITY'
                meta['area_idx'] = i - 200
                if p.stage[meta['area_idx']] >= 0:
                    cid = p.stage[meta['area_idx']]
                    c_data = serialize_card(cid, member_db, game_state.live_db, getattr(game_state, 'energy_db', {}))
                    meta['img'] = c_data['img']
                    meta['name'] = c_data['name']
                    
            elif 300 <= i <= 359:
                meta['type'] = 'MULLIGAN'
                meta['hand_idx'] = i - 300
                if meta['hand_idx'] < len(p.hand):
                    cid = p.hand[meta['hand_idx']]
                    c_data = serialize_card(cid, member_db, game_state.live_db, getattr(game_state, 'energy_db', {}))
                    meta['img'] = c_data['img']
                    meta['name'] = c_data['name']
                    
            elif 400 <= i <= 459:
                meta['type'] = 'LIVE_SET'
                meta['hand_idx'] = i - 400
                if meta['hand_idx'] < len(p.hand):
                    cid = p.hand[meta['hand_idx']]
                    c_data = serialize_card(cid, member_db, game_state.live_db, getattr(game_state, 'energy_db', {}))
                    meta['img'] = c_data['img']
                    meta['name'] = c_data['name']
            
            legal_actions.append(meta)
    
    pending_choice_info = None
    if game_state.pending_choices:
        choice_type, params = game_state.pending_choices[0]
        pending_choice_info = {
            'type': choice_type,
            'description': params.get('effect_description', ''),
            'source_ability': params.get('source_ability', ''),
            'source_member': params.get('source_member', ''),
            'is_optional': params.get('is_optional', False),
            'params': params
        }
    
    return {
        'turn': game_state.turn_number,
        'phase': int(game_state.phase),
        'active_player': int(active_idx),
        'game_over': game_state.game_over,
        'winner': game_state.winner,
        'players': [
            serialize_player(game_state.players[0], game_state, player_idx=0, viewer_idx=0, is_viewable=True),
            serialize_player(game_state.players[1], game_state, player_idx=1, viewer_idx=0, is_viewable=False)
        ],
        'legal_actions': legal_actions,
        'pending_choice': pending_choice_info,
        'performance_results': getattr(game_state, 'performance_results', {}),
        'rule_log': game_state.rule_log
    }
