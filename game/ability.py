"""
Ability and Effect System for Love Live Card Game.
Handles triggers, effect stack, and ability resolution.
"""

from enum import IntEnum, auto
from typing import List, Optional, Callable, Dict, Any, Union
from dataclasses import dataclass, field
import re

class TriggerType(IntEnum):
    NONE = 0
    ON_PLAY = 1           # 登場時
    ON_LIVE_START = 2     # ライブ開始時
    ON_LIVE_SUCCESS = 3   # ライブ成功時
    TURN_START = 4        
    TURN_END = 5
    CONSTANT = 6          # 常時
    ACTIVATED = 7         # 起動
    ON_LEAVES = 8         # 自動 - when member leaves stage/is discarded

class TargetType(IntEnum):
    SELF = 0
    PLAYER = 1         
    OPPONENT = 2       
    ALL_PLAYERS = 3
    MEMBER_SELF = 4    
    MEMBER_OTHER = 5   
    CARD_HAND = 6      
    CARD_DISCARD = 7   
    CARD_DECK_TOP = 8
    OPPONENT_HAND = 9  # 相手の手札
    MEMBER_SELECT = 10 # Select manual target
    MEMBER_NAMED = 11  # Specific named member implementation

class EffectType(IntEnum):
    DRAW = 0             
    ADD_BLADES = 1       
    ADD_HEARTS = 2       
    REDUCE_COST = 3      
    LOOK_DECK = 4        
    RECOVER_LIVE = 5     # Recover Live from discard
    BOOST_SCORE = 6      
    RECOVER_MEMBER = 7   # Recover Member from discard
    BUFF_POWER = 8       # Generic power/heart buff
    IMMUNITY = 9         # Cannot be targeted/chosen
    MOVE_MEMBER = 10     # Move member to different area
    SWAP_CARDS = 11      # Swap cards between zones
    SEARCH_DECK = 12     # Search deck for specific card
    ENERGY_CHARGE = 13   # Add cards to energy zone
    NEGATE_EFFECT = 14   # Cancel/negate an effect
    ORDER_DECK = 15      # Reorder cards in deck
    META_RULE = 16       # Rule clarification text (no effect)
    SELECT_MODE = 17     # Choose one of the following effects
    MOVE_TO_DECK = 18    # Move card to top/bottom of deck
    TAP_OPPONENT = 19    # Tap opponent's member
    PLACE_UNDER = 20     # Place card under member
    FLAVOR_ACTION = 99   # "Ask opponent what they like", etc.
    RESTRICTION = 21     # Restriction on actions (Cannot Live, etc)
    BATON_TOUCH_MOD = 22 # Modify baton touch rules (e.g. 2 members)
    SET_SCORE = 23       # Set score to fixed value
    SWAP_ZONE = 24       # Swap between zones (e.g. Hand <-> Live)
    TRANSFORM_COLOR = 25 # Change all colors of type X to Y
    REVEAL_CARDS = 26    # 公開 - reveal cards from zone
    LOOK_AND_CHOOSE = 27 # 見る、その中から - look at cards, choose from them
    CHEER_REVEAL = 28    # エールにより公開 - cards revealed via cheer mechanic
    ACTIVATE_MEMBER = 29 # アクティブにする - untap/make active a member
    ADD_TO_HAND = 30     # 手札に加える - add card to hand (from any zone)
    COLOR_SELECT = 31    # Specify a heart color

class ConditionType(IntEnum):
    NONE = 0
    TURN_1 = 1           # Turn == 1
    HAS_MEMBER = 2       # Specific member on stage
    HAS_COLOR = 3        # Specific color on stage
    COUNT_STAGE = 4      # Count members >= X
    COUNT_HAND = 5
    COUNT_DISCARD = 6
    IS_CENTER = 7
    LIFE_LEAD = 8
    COUNT_GROUP = 9      # "3+ Aqours members"
    GROUP_FILTER = 10    # Filter by group name
    OPPONENT_HAS = 11    # Opponent has X
    SELF_IS_GROUP = 12   # This card is from group X
    MODAL_ANSWER = 13    # Choice/Answer branch (e.g. LL-PR-004-PR)
    COUNT_ENERGY = 14    # エネルギーがX枚以上
    HAS_LIVE_CARD = 15   # ライブカードがある場合

@dataclass
class Condition:
    type: ConditionType
    params: Dict[str, Any] = field(default_factory=dict)
    is_negated: bool = False  # "If NOT X" / "Except X"
    
@dataclass
class Effect:
    effect_type: EffectType
    value: int = 0
    target: TargetType = TargetType.SELF
    params: Dict[str, Any] = field(default_factory=dict)
    is_optional: bool = False  # ～てもよい

class AbilityCostType(IntEnum):
    NONE = 0
    ENERGY = 1
    TAP_SELF = 2        # ウェイトにする
    DISCARD_HAND = 3    # 手札を捨てる
    RETURN_HAND = 4     # 手札に戻す (Self bounce)
    SACRIFICE_SELF = 5  # このメンバーを控え室に置く

@dataclass
class Cost:
    type: AbilityCostType
    value: int = 0
    params: Dict[str, Any] = field(default_factory=dict)
    is_optional: bool = False

@dataclass
class Ability:
    raw_text: str
    trigger: TriggerType
    effects: List[Effect]
    conditions: List[Condition] = field(default_factory=list)
    costs: List[Cost] = field(default_factory=list)
    modal_options: List[List[Effect]] = field(default_factory=list) # For SELECT_MODE
    is_once_per_turn: bool = False
    
    def __str__(self):
        c_str = f" [Cond:{len(self.conditions)}]" if self.conditions else ""
        cost_str = f" [Cost:{len(self.costs)}]" if self.costs else ""
        return f"[{self.trigger.name}]{c_str}{cost_str} {self.raw_text[:30]}..."

class AbilityParser:
    @staticmethod
    def parse_ability_text(text: str) -> List[Ability]:
        abilities = []
        
        # First split by newlines (each line is typically one ability)
        # Then within each line, identify the trigger tag at the start
        lines = text.split('\\n')  # Handle escaped newlines in JSON
        if len(lines) == 1:
            lines = text.split('\n')  # Handle real newlines
        
        # Further split by Japanese period '。' to isolate sentences
        # But keep the period or handle reconstruction? simpler to just flat map
        split_lines = []
        for l in lines:
            # removing empty strings from split
            split_lines.extend([s for s in l.split('。') if s.strip()])
        lines = split_lines
        
        last_ability = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            trigger = TriggerType.NONE
            conditions = []
            effects = []
            costs = []
            
            # --- Trigger Parsing ---
            # Handle both text-based and icon-based triggers
            # Common patterns: {{toujyou.png|登場}}, {{jidou.png|自動}}, {{kidou.png|起動}}
            if '登場' in line or '{{toujyou' in line: trigger = TriggerType.ON_PLAY
            elif '自動' in line or '{{jidou' in line: trigger = TriggerType.ON_LEAVES  # "Automatic" trigger on state change
            elif '常時' in line or '{{jyouji' in line: trigger = TriggerType.CONSTANT
            elif 'ライブ成功' in line or '{{live_success' in line: trigger = TriggerType.ON_LIVE_SUCCESS
            elif 'ライブ開始' in line or '{{live_start' in line: trigger = TriggerType.ON_LIVE_START
            elif '起動' in line or '{{kidou' in line: trigger = TriggerType.ACTIVATED
            elif 'ターン開始' in line: trigger = TriggerType.TURN_START
            elif 'ターン終了' in line: trigger = TriggerType.TURN_END
            
            # Continuation context
            is_continuation = (
                line.startswith('・') or 
                line.startswith('-') or 
                any(line.startswith(kw) for kw in ['回答が', '選んだ場合', '条件が', 'それ以外', '（', '('])
            )
            
            # Explicit trigger detection (existence of {{...}})
            has_explicit_trigger = '{{' in line and (
                'toujyou' in line or 'jidou' in line or 'jyouji' in line or 
                'live_success' in line or 'live_start' in line or 'kidou' in line or 
                'ターン開始' in line or 'ターン終了' in line or
                '登場' in line or '常時' in line or '起動' in line or '自動' in line
            )
            
            # Fallback: if no trigger but has effect keywords, default to ACTIVATED
            # Only do this if it's NOT a continuation AND doesn't have an explicit trigger tag
            if trigger == TriggerType.NONE and not is_continuation and not has_explicit_trigger:
                if any(kw in line for kw in ['引', 'スコア', 'プラス', '＋', 'ブレード', 'ハート', '控', '戻', 'エネ', 'デッキ', '山札']):
                    trigger = TriggerType.ACTIVATED
            
            content = re.sub(r'\{\{.*?\|(.*?)\}\}', r'\1', line)
            
            # --- Condition Parsing ---
            # [Turn 1]
            # Once per turn check
            if '1ターンに1回' in line or 'ターン終了時まで1回' in line or 'に限る' in line:
                is_once_per_turn = True
            else:
                is_once_per_turn = False

            if '[Turn 1]' in line or 'ターン1' in line: 
                conditions.append(Condition(ConditionType.TURN_1))
            
            # Zone context detection for subsequent conditions
            context_zone = None
            zone_map = {
                '右サイドエリア': 'RIGHT_STAGE',
                '左サイドエリア': 'LEFT_STAGE',
                'センターエリア': 'CENTER_STAGE',
                '成功ライブカード置き場': 'SUCCESS_LIVE',
                'ライブ成功カード置き場': 'SUCCESS_LIVE',
                'エネルギー置き場': 'ENERGY',
                'ライブカード置き場': 'LIVE_ZONE',
                'ライブエリア': 'LIVE_AREA',
                '控え室': 'DISCARD',
                '手札': 'HAND',
                'ステージ': 'STAGE',
                '山札': 'DECK',
                'デッキ': 'DECK'
            }
            
            for keyword, zone_id in zone_map.items():
                if keyword in content:
                    context_zone = zone_id
                    # Shift to Opponent if "相手" is near the zone keyword
                    # Simple heuristic: if '相手' is in the line at all for these checks
                    if '相手' in content:
                        context_zone = 'OPPONENT_' + context_zone
                    break

            # Group count: "『Aqours』のメンバーが3枚以上" or "3枚以上のメンバー" or "成功ライブカード置き場にカードが2枚以上"
            # Also handle zone-specific counts like "控え室に...枚以上"
            match_group_count = re.search(r'『(.*?)』.*?(\d+)(枚|人)以上', content)
            if match_group_count:
                params = {
                    'group': match_group_count.group(1),
                    'min': int(match_group_count.group(2))
                }
                if context_zone: params['zone'] = context_zone
                conditions.append(Condition(ConditionType.COUNT_GROUP, params))
            
            # Zone count without group (e.g. "成功ライブカード置き場にカードが2枚以上")
            elif re.search(r'(\d+)(枚|人)以上', content) and context_zone:
                match_zone_count = re.search(r'(\d+)(枚|人)以上', content)
                if match_zone_count:
                    params = {
                        'count': int(match_zone_count.group(1)),
                        'zone': context_zone
                    }
                    conditions.append(Condition(ConditionType.COUNT_DISCARD if context_zone == 'DISCARD' else ConditionType.COUNT_STAGE, params))
            
            # "If all are X" (Reveal/Check condition) - e.g. それらがすべてメンバーカードの場合
            match_all_check = re.search(r'それらがすべて(.*?)の場合', content)
            if match_all_check:
                 conditions.append(Condition(ConditionType.GROUP_FILTER, {'group': match_all_check.group(1), 'context': 'revealed'}))
            
            # Generic count: "N枚以上ある場合"
            match_count = re.search(r'(\d+)枚以上ある場合', content)
            if match_count and not match_group_count:
                params = {'min': int(match_count.group(1))}
                if context_zone: params['zone'] = context_zone
                conditions.append(Condition(ConditionType.COUNT_STAGE, params))
            
            # Group filter: "『μ's』" or "『Aqours』"
            match_groups = re.findall(r'『(.*?)』', content)
            for g in match_groups:
                if g not in [c.params.get('group') for c in conditions if c.type == ConditionType.COUNT_GROUP]:
                    # Check for "distinct names" (名前の異なる)
                    distinct_names = '名前の異なる' in content
                    
                    # Check for count (X人以上/X枚以上)
                    count_match = re.search(r'(\d+)(人|枚)以上', content)
                    if count_match:
                         params = {'group': g, 'count': int(count_match.group(1))}
                         if distinct_names: params['distinct_names'] = True
                         if context_zone: params['zone'] = context_zone
                         conditions.append(Condition(ConditionType.COUNT_GROUP, params))
                    else:
                         # Filter logic
                         params = {'group': g}
                         if context_zone: params['zone'] = context_zone
                         conditions.append(Condition(ConditionType.GROUP_FILTER, params))
            
            # Specific Member names (multiple) with area detection
            if 'がある場合' in content or 'がいる場合' in content or '登場している場合' in content:
                # Try to find area-name pairs first
                pairs = re.findall(r'([左中右センター].*?エリア)に「(.*?)」', content)
                found_names = set()
                for area_name, member_name in pairs:
                    area_id = None
                    if '左' in area_name: area_id = 'LEFT_STAGE'
                    elif '右' in area_name: area_id = 'RIGHT_STAGE'
                    elif 'センター' in area_name or '中' in area_name: area_id = 'CENTER_STAGE'
                    
                    conditions.append(Condition(ConditionType.HAS_MEMBER, {
                        'name': member_name,
                        'area': area_id,
                        'zone': 'STAGE'
                    }))
                    found_names.add(member_name)
                
                # Fallback for names without explicit area in same clause
                names = re.findall(r'「(.*?)」', content)
                for n in names:
                    if n not in found_names:
                        params = {'name': n}
                        if context_zone: params['zone'] = context_zone
                        conditions.append(Condition(ConditionType.HAS_MEMBER, params))
            
            # Color Icon detection
            color_map = {
                'red': '赤', 'blue': '青', 'green': '緑', 'yellow': '黄', 'purple': '紫', 'pink': 'ピンク'
            }
            for eng, jpn in color_map.items():
                if f'icon_{eng}' in line:
                    conditions.append(Condition(ConditionType.HAS_COLOR, {'color': jpn}))
            
            # Negation detection for conditions
            if '以外' in content or 'でない場合' in content or 'ではない場合' in content:
                if conditions:
                    conditions[-1].is_negated = True
            
            # Center position check (Avoid redundant if center-area member was already matched)
            if 'センターエリア' in content and '場合' in content:
                if not any(c.type == ConditionType.HAS_MEMBER and c.params.get('area') == 'CENTER_STAGE' for c in conditions):
                    conditions.append(Condition(ConditionType.IS_CENTER))
            
            # Life Lead Condition
            if 'ライフが相手より多い' in content or 'ライフが相手より少ない' in content:
                conditions.append(Condition(ConditionType.LIFE_LEAD))
            
            # Score Lead Condition ("score is higher than opponent")
            if 'スコア' in content and '相手より高い' in content:
                # Reuse LIFE_LEAD for now or create new type, report implies reuse
                conditions.append(Condition(ConditionType.LIFE_LEAD, {'type': 'score'}))
            
            # Opponent has condition
            if '相手' in content and ('ある場合' in content or 'いる場合' in content):
                conditions.append(Condition(ConditionType.OPPONENT_HAS))
                
            # Modal Answer Branch (e.g. LL-PR-004-PR)
            match_modal = re.search(r'回答が(.*?)の場合', content)
            if match_modal:
                conditions.append(Condition(ConditionType.MODAL_ANSWER, {'answer': match_modal.group(1)}))
                
            # --- Cost Parsing ---
            if 'このメンバーをウェイトにし' in content:
                costs.append(Cost(AbilityCostType.TAP_SELF))
            
            if '手札を1枚控え室に置' in content:
                costs.append(Cost(AbilityCostType.DISCARD_HAND, 1))
            
            # Sacrifice self: このメンバーをステージから控え室に置く
            if 'このメンバーを' in content and '控え室に置く' in content:
                costs.append(Cost(AbilityCostType.SACRIFICE_SELF))
            
            # Energy condition: エネルギーがX枚以上ある場合
            match_energy_cond = re.search(r'エネルギーが(\d+)枚以上', content)
            if match_energy_cond:
                conditions.append(Condition(ConditionType.COUNT_ENERGY, {'min': int(match_energy_cond.group(1))}))
            
            # Live card present condition: ライブカードがある場合
            if 'ライブカードがある場合' in content:
                conditions.append(Condition(ConditionType.HAS_LIVE_CARD))

            # --- Effect Parsing ---
            
            # Draw (with quantity extraction)
            match_draw = re.search(r'(\d+)枚.*?引', content)
            if match_draw:
                effects.append(Effect(EffectType.DRAW, int(match_draw.group(1)), TargetType.PLAYER))
            elif '引' in content:
                effects.append(Effect(EffectType.DRAW, 1, TargetType.PLAYER))
                
            # Look at Deck
            match_look = re.search(r'デッキ.*?(\d+)枚.*?見る', content)
            if match_look:
                count = int(match_look.group(1))
                effects.append(Effect(EffectType.LOOK_DECK, count))
            
            # Choose from looked cards / revealed cards (Independent check)
            if 'その中から' in content or 'その中' in content:
                effects.append(Effect(EffectType.LOOK_AND_CHOOSE, 1, params={'source': 'looked'}))
            
            # Reveal cards (公開)
            match_reveal = re.search(r'(\d+)枚.*?公開', content)
            if match_reveal:
                effects.append(Effect(EffectType.REVEAL_CARDS, int(match_reveal.group(1))))
            elif '公開' in content and 'エール' not in content:
                effects.append(Effect(EffectType.REVEAL_CARDS, 1))

            # Recover (Discard to Hand) checking strict "from discard"
            # NOTE: Use 'if' not 'elif' here to allow multiple effects in one line unless mutually exclusive
            if '控え室から' in content and '手札に加え' in content:
                source_zone = 'discard'
                if 'ライブカード' in content:
                    effects.append(Effect(EffectType.RECOVER_LIVE, 1, TargetType.CARD_DISCARD, params={'to': 'hand'}))
                else:
                    effects.append(Effect(EffectType.RECOVER_MEMBER, 1, TargetType.CARD_DISCARD, params={'to': 'hand'}))
                
                # Check for Heart filter
                if 'ハート' in content or 'heart' in content:
                    effects[-1].params['filter'] = 'heart_req'
            
            # Generic Add to Hand (from any zone)
            # Use 'if' here too, but check if we already added a Recover effect to avoid duplication?
            # Actually, "Recover" matches "Add to hand", so we should use elif logic ONLY if we found Recover.
            # But since we unchained everything... let's be careful.
            # If line is "Discard 1 card. Add 1 to hand." -> Both effects.
            # If line is "Recover from discard to hand" -> Just Recover.
            # "Recover" check consumes the "Add to hand" part because of the 'and' condition.
            # So we use `elif` relative to Recover, but independent of Reveal/Look.
            elif '手札に加え' in content:
                params = {'to': 'hand'}
                # Determine source zone
                if 'デッキ' in content: params['from'] = 'deck'
                elif '成功ライブカード' in content: params['from'] = 'success_live'
                elif 'ライブカード置き場' in content: params['from'] = 'live_zone'
                elif '控え室' in content and 'から' in content: params['from'] = 'discard' 
                effects.append(Effect(EffectType.ADD_TO_HAND, 1, params=params))
            
            # Cheer/Yell reveal (エールにより公開)
            if 'エールにより公開' in content or 'エールで公開' in content:
                effects.append(Effect(EffectType.CHEER_REVEAL, 1))
            
            # Search deck
            if 'デッキ' in content and ('探' in content or 'サーチ' in content):
                effects.append(Effect(EffectType.SEARCH_DECK, 1))
            
            # Blade/Heart Buff - multiple patterns
            # Blade/Heart Buff - Handling Named Targets (e.g. Tiny Stars)
            # Check for patterns like '「Name」...は...を得る'
            # We strip the line to check context
            target = TargetType.MEMBER_SELF
            target_params = {}
            
            fullname_match = re.search(r'「(.*?)」.*?は', content)
            if fullname_match:
                target = TargetType.MEMBER_NAMED
                target_params['target_name'] = fullname_match.group(1)
            elif '相手' in content: target = TargetType.OPPONENT
            elif '全員' in content: target = TargetType.ALL_PLAYERS
            
             # Heart / Blade Gain
            # Handle cases where both are gained: "Heart and Blade gain"
            # Logic: Check for Blade gain, Check for Heart gain independently
            
            # Blade gain
            if 'ブレード' in content and '得る' in content:
                blade_match = re.search(r'ブレード.*?(\d+)', content)
                count = int(blade_match.group(1)) if blade_match else 1
                # Check for "ALL Blade"
                if 'ALLブレード' in content:
                    target_params['all_blade'] = True
                effects.append(Effect(EffectType.ADD_BLADES, count, target, params=target_params))
            
            # Heart gain
            if ('ハート' in content or 'heart' in content) and '得る' in content:
                heart_match = re.search(r'\+(\d+)', content)
                if heart_match:
                    effects.append(Effect(EffectType.ADD_HEARTS, int(heart_match.group(1)), target, params=target_params))
                elif re.search(r'heart\d+', content):
                    # Count specific heart icons
                    count = len(re.findall(r'heart_\d+\.png', content)) or 1
                    effects.append(Effect(EffectType.ADD_HEARTS, count, target, params=target_params))
                # If just "Gain Heart" without explicit +Number (e.g. from template text)
                elif 'ハート' in content:
                     effects.append(Effect(EffectType.ADD_HEARTS, 1, target, params=target_params))
            
            # Energy charge
            if 'エネルギー' in content and ('置く' in content or '加える' in content):
                e_params = {}
                if 'デッキ' in content: e_params['from'] = 'deck'
                effects.append(Effect(EffectType.ENERGY_CHARGE, 1, params=e_params))
            
            # Per-card multiplier ("1枚につき" = for each card)
            if '1枚につき' in content or '枚数' in content:
                # This modifies value of other effects, but we note it as a buff
                effects.append(Effect(EffectType.BUFF_POWER, 1, params={'multiplier': True}))
            
            # Per-member multiplier ("1人につき" = for each member)
            if '1人につき' in content or '人につき' in content:
                effects.append(Effect(EffectType.BUFF_POWER, 1, params={'multiplier': True, 'per_member': True}))
            
            # Generic power buff ("+X" or "＋X" without specific type)
            match_power = re.search(r'[+＋](\d+)', content)
            if match_power and not any(kw in content for kw in ['ブレード', 'ハート', 'スコア']):
                effects.append(Effect(EffectType.BUFF_POWER, int(match_power.group(1))))
                
            # Move member
            if 'エリア' in content and '移動' in content:
                effects.append(Effect(EffectType.MOVE_MEMBER, 1))
            
            # Untap / Make Active (アクティブに)
            if 'アクティブに' in content:
                # Check for Energy target
                if 'エネルギー' in content:
                    # Match count
                    match_count = re.search(r'(\d+)枚', content)
                    count = int(match_count.group(1)) if match_count else 1
                    effects.append(Effect(EffectType.ACTIVATE_MEMBER, count, TargetType.MEMBER_SELECT, params={'target': 'energy'}))
                else:
                    # Match count if present
                    match_count = re.search(r'(メンバー|\d+人)', content)
                    count = 1
                    if match_count:
                        m = re.search(r'(\d+)', match_count.group(0))
                        if m: count = int(m.group(1))
                    effects.append(Effect(EffectType.ACTIVATE_MEMBER, count, TargetType.MEMBER_SELECT))
            
            # Temporary effects ("until end of X") - add duration params
            duration_params = {}
            if 'ライブ終了時まで' in content:
                duration_params['until'] = 'live_end'
            elif 'ターン終了まで' in content or '終了時まで' in content:
                duration_params['until'] = 'turn_end'
            
            # If duration but no effects yet, add a buff placeholder
            if duration_params:
                if not effects:
                    effects.append(Effect(EffectType.BUFF_POWER, 1, params={**duration_params, 'temporary': True}))
                else:
                    for eff in effects:
                        eff.params.update(duration_params)
            
            # META_RULE: Heart requirement clarifications (parenthetical rules)
            if '必要ハート' in content and ('扱う' in content or '確認' in content):
                effects.append(Effect(EffectType.META_RULE, 0, params={'type': 'heart_rule'}))
            
            # META_RULE: Score calculation rules (parenthetical)
            if 'スコア' in content and ('加算' in content or '合算' in content):
                 effects.append(Effect(EffectType.META_RULE, 0, params={'type': 'score_rule'}))
            
            # Immunity / Cannot be chosen
            if '選ばれない' in content or '選べない' in content or '置けない' in content:
                effects.append(Effect(EffectType.IMMUNITY, 1))
            
            # Play/Summon Member
            if '登場させる' in content:
                count = 1
                match_count_play = re.search(r'(\d+)枚', content)
                if match_count_play: count = int(match_count_play.group(1))
                
                play_params = {'auto_play': True, 'from': 'discard'} # Default to discard if unspecified, or 'zone'
                if '手札' in content: play_params['from'] = 'hand'
                elif '控え室' in content: play_params['from'] = 'discard'
                
                effects.append(Effect(EffectType.RECOVER_MEMBER, count, TargetType.CARD_DISCARD, play_params))
            
            # Forced discard / send to waiting room
            if '控' in content and ('置' in content or '送' in content):
                count = 1
                match_discard_count = re.search(r'(\d+)枚', content)
                if match_discard_count: count = int(match_discard_count.group(1))
                
                discard_params = {'target': 'discard'}
                if 'デッキ' in content: discard_params['from'] = 'deck'
                elif '手札' in content: discard_params['from'] = 'hand'
                
                effects.append(Effect(EffectType.SWAP_CARDS, count, params=discard_params))
            
            # Opponent Member Effects (相手のメンバーをウェイトにする, 相手のステージにいるメンバー)
            if '相手' in content and ('ウェイト' in content or '休み' in content):
                # Match count if present
                match_count = re.search(r'(\d+)人', content)
                count = int(match_count.group(1)) if match_count else 1
                
                # Determine if it's all or specific
                if 'すべて' in content:
                    effects.append(Effect(EffectType.TAP_OPPONENT, count, TargetType.OPPONENT, params={'all': True}))
                else:
                    effects.append(Effect(EffectType.TAP_OPPONENT, count, TargetType.OPPONENT))
            
            # Score boost (handle both + and ＋)
            match_score = re.search(r'スコア.*?[+＋](\d+)', content)
            if match_score:
                effects.append(Effect(EffectType.BOOST_SCORE, int(match_score.group(1))))
            elif 'スコア' in content and '得る' in content:
                effects.append(Effect(EffectType.BOOST_SCORE, 1))
            elif 'スコア' in content and '＋' in content:
                effects.append(Effect(EffectType.BOOST_SCORE, 1))
            
            # Cost reduction
            if 'コスト' in content and ('減' in content or '-' in content):
                effects.append(Effect(EffectType.REDUCE_COST, 1))
            
            # Negate / Cancel
            if '無効' in content or 'キャンセル' in content:
                effects.append(Effect(EffectType.NEGATE_EFFECT, 1))
            
            # Deck Ordering / Moving to Deck
            if 'デッキ' in content:
                if '順番' in content:
                    effects.append(Effect(EffectType.ORDER_DECK, 1))
                elif ('一番上' in content or '一番下' in content) and 'シャッフル' in content and '合計' in content:
                    # Triple Trio Shuffle Sum
                    match_count = re.search(r'合計(\d+)枚', content)
                    count = int(match_count.group(1)) if match_count else 0
                    params = {
                        'shuffle': True, 
                        'position': 'bottom' if '一番下' in content else 'top',
                        'target_zone': 'discard' if '控え室' in content else None
                    }
                    # Capture specific names if Present
                    names = re.findall(r'「(.*?)」', content)
                    if names:
                        params['target_names'] = names
                        
                    effects.append(Effect(EffectType.ORDER_DECK, count, params=params))
                elif '一番上' in content:
                    effects.append(Effect(EffectType.MOVE_TO_DECK, 1, params={'position': 'top'}))
                elif '一番下' in content:
                    effects.append(Effect(EffectType.MOVE_TO_DECK, 1, params={'position': 'bottom'}))
                
                # Add member/live filter to any ORDER_DECK effect if present
                if effects and effects[-1].effect_type == EffectType.ORDER_DECK:
                    if 'メンバー' in content: effects[-1].params['filter'] = 'member'
                    if 'ライブ' in content: effects[-1].params['filter'] = 'live'
            
            # Select Mode ("Choose 1 from below")
            if '以下から1つを選ぶ' in content:
                effects.append(Effect(EffectType.SELECT_MODE, 1))

            # Color Selection
            if 'ハートの色を1つ指定' in content or '好きなハートの色を' in content:
                effects.append(Effect(EffectType.COLOR_SELECT, 1))
            
            # Tap Opponent
            if '相手' in content and ('ウェイト' in content or '休み' in content):
                effects.append(Effect(EffectType.TAP_OPPONENT, 1))
            
            # Place Under Member (handle "may place")
            if 'メンバーの下に' in content and '置' in content:
                effects.append(Effect(EffectType.PLACE_UNDER, 1))
            
            # Flavor Action
            if '聞く' in content: # Ask
                effects.append(Effect(EffectType.FLAVOR_ACTION, 1))
            
            # Restrictions (Cannot Live, Cannot Place)
            if 'ライブできない' in content:
                effects.append(Effect(EffectType.RESTRICTION, 1, params={'type': 'live'}))
            if '置くことができない' in content:
                effects.append(Effect(EffectType.RESTRICTION, 1, params={'type': 'placement'}))
            
            # TRANSFORM_COLOR (all blades become X)
            if 'なる' in content and 'すべて' in content and (match := re.search(r'すべて\[(.*?)\]になる', content)):
                effects.append(Effect(EffectType.TRANSFORM_COLOR, 1, params={'target_color': match.group(1)}))
            
            # Baton Touch Mod
            if 'バトンタッチ' in content and '2人' in content:
                 effects.append(Effect(EffectType.BATON_TOUCH_MOD, 2))
            
            # Set Score
            match_set_score = re.search(r'スコアは([0-9０-９]+)になる', content)
            if match_set_score:
                 val = int(match_set_score.group(1).replace('４','4')) # Handle full width 4 if needed
                 effects.append(Effect(EffectType.SET_SCORE, val))
            
            # Swap / Exchange (Reveal from hand... put in zone)
            if '公開' in content and ('置き場' in content or '加える' in content):
                 effects.append(Effect(EffectType.SWAP_ZONE, 1))
            
            # Generic Add to Hand fallback (if nothing else matched but we see "Add to hand")
            if '手札に加える' in content and not effects:
                 effects.append(Effect(EffectType.DRAW, 1, params={'generic_add': True}))
            
            # Meta Rule Text (Parenthetical rules)
            
            # Meta Rule Text (Parenthetical rules)
            if content.startswith('（') and content.endswith('）'):
                 effects.append(Effect(EffectType.META_RULE, 1))
                 trigger = TriggerType.CONSTANT
            if content.startswith('(') and content.endswith(')'): # Half-width parens too
                 effects.append(Effect(EffectType.META_RULE, 1))
                 trigger = TriggerType.CONSTANT
            
            # --- Construct Ability ---
            
            # --- Construct Ability ---

            # Final touches on effects
            is_optional = 'てもよい' in content
            is_global = 'すべての' in content
            is_opponent_hand = '相手の手札' in content
            
            for eff in effects:
                eff.is_optional = is_optional
                if is_global:
                    eff.params['all'] = True
                if is_opponent_hand:
                    eff.target = TargetType.OPPONENT_HAND
                
            # --- Construct Ability ---
            # If we have trigger
            # --- Construct Ability ---
            if trigger != TriggerType.NONE:
                last_ability = Ability(
                    raw_text=content.strip(),
                    trigger=trigger,
                    effects=effects,
                    conditions=conditions,
                    costs=costs,
                    is_once_per_turn=is_once_per_turn
                )
                abilities.append(last_ability)
            elif effects or conditions or costs:
                if last_ability:
                    # SELECT_MODE logic: if line starts with bullet, it's a modal option
                    if line.startswith('・') and any(e.effect_type == EffectType.SELECT_MODE for e in last_ability.effects):
                         last_ability.modal_options.append(effects)
                    else:
                         # Continuation - Merge into last ability
                         last_ability.effects.extend(effects)
                         last_ability.conditions.extend(conditions)
                         last_ability.costs.extend(costs)
                    
                    last_ability.raw_text += " " + content.strip()
                    if is_once_per_turn:
                        last_ability.is_once_per_turn = True
                else:
                    # No trigger detected but has effects loop - Default to CONSTANT (safe fallback)
                    # This captures parenthesized rules and flavor text
                    last_ability = Ability(
                        raw_text=content.strip(),
                        trigger=TriggerType.CONSTANT,
                        effects=effects,
                        conditions=conditions,
                        costs=costs,
                        is_once_per_turn=is_once_per_turn
                    )
                    abilities.append(last_ability)

                
        return abilities
