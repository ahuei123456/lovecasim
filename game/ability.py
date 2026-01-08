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
    SET_BLADES = 31      # Layer 4: Set blades to fixed value
    SET_HEARTS = 32      # Layer 4: Set hearts to fixed value
    FORMATION_CHANGE = 33 # Rule 11.10: Rearrange all members
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
    REPLACE_EFFECT = 34  # Replacement effect (代わりに)
    TRIGGER_REMOTE = 35  # Trigger ability from another zone (Cluster 5)
    REDUCE_HEART_REQ = 36 # Need hearts reduced

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
    COST_CHECK = 16      # コストがX以下/以上
    RARITY_CHECK = 17    # Rarity filter
    HAND_HAS_NO_LIVE = 18 # Hand contains no live cards (usually paired with reveal cost)
    COUNT_SUCCESS_LIVE = 19 # 成功ライブカード置き場にX枚以上

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
    REVEAL_HAND_ALL = 6 # 手札をすべて公開する
    SACRIFICE_UNDER = 7 # 下に置かれているカードを控え室に置く
    DISCARD_ENERGY = 8   # エネルギーを控え室に置く

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
        
        # Split by newlines (blocks)
        blocks = text.split('\\n')
        if len(blocks) == 1:
            blocks = text.split('\n')
        
        last_ability = None
        for block in blocks:
            block = block.strip()
            if not block:
                continue
                
            # Split block into sentences
            sentences = [s for s in block.split('。') if s.strip()]
            
            for i, line in enumerate(sentences):
                line = line.strip()
                if not line:
                    continue
                    
                trigger = TriggerType.NONE
                conditions = []
                effects = []
                costs = []
                
                # --- Trigger Parsing ---
                if 'toujyou' in line or '登場' in line: trigger = TriggerType.ON_PLAY
                elif 'jidou' in line or '自動' in line: trigger = TriggerType.ON_LEAVES
                elif 'jyouji' in line or '常時' in line: trigger = TriggerType.CONSTANT
                elif 'live_success' in line or 'ライブ成功' in line: trigger = TriggerType.ON_LIVE_SUCCESS
                elif 'live_start' in line or 'ライブ開始' in line: trigger = TriggerType.ON_LIVE_START
                elif 'kidou' in line or '起動' in line: trigger = TriggerType.ACTIVATED
                elif 'ターン開始' in line: trigger = TriggerType.TURN_START
                elif 'ターン終了' in line: trigger = TriggerType.TURN_END
                
                # Double trigger check (e.g. {{toujyou.png|登場}}/{{live_start.png|ライブ開始時}})
                triggers = []
                if trigger != TriggerType.NONE:
                    triggers.append(trigger)
                else:
                    # Check for multiple triggers in the line
                    if 'toujyou' in line or '登場' in line: triggers.append(TriggerType.ON_PLAY)
                    if 'live_start' in line or 'ライブ開始' in line: triggers.append(TriggerType.ON_LIVE_START)
                    if 'toujyou' in line and 'live_start' in line: # Explicit double trigger line
                         pass # handled by append above, but we need to ensure we don't overwrite if it was detected as one
                
                # If multiple triggers found and it looks like a slash separated trigger line
                if len(triggers) > 1 and '/' in line:
                    # We will handle this by creating multiple abilities later or flagging it
                    # For now, let's pick the first one and store the second one in a temporary way 
                    # OR better: The parser loop creates ONE ability object. We might need to change return type or struct.
                    # A better approach for this engine: Clone the ability at the end for each trigger.
                    pass
                
                if not triggers and trigger == TriggerType.NONE:
                     pass # Normal continuation logic
                elif triggers:
                    trigger = triggers[0] # primary trigger
                
                # Continuation context
                is_continuation = (
                    line.startswith('・') or 
                    line.startswith('-') or 
                    line.startswith('－') or
                    any(line.startswith(kw) for kw in ['回答が', '選んだ場合', '条件が', 'それ以外', 'その', 'それら', '残り', 'そし', 'その後', 'そこから', 'もよい', 'を自分', '（', '('])
                )
                
                # Explicit trigger check
                has_explicit_trigger = '{{' in line 
                
                # Fallback trigger for first sentence
                if trigger == TriggerType.NONE and i == 0 and not is_continuation and not has_explicit_trigger:
                    if any(kw in line for kw in ['引', 'スコア', 'プラス', '＋', 'ブレード', 'ハート', '控', '戻', 'エネ', 'デッキ', '山札', '見る', '公開', '選ぶ', '選ぶ。']):
                        trigger = TriggerType.ACTIVATED
                
                content = line
                
                # --- Once per turn ---
                is_once_per_turn = any(kw in line for kw in [
                    '1ターンに1回', 'ターン終了時まで1回', 'に限る', 'ターン1回', '［ターン1回］', '【ターン1回】'
                ])

                if '[Turn 1]' in line or 'ターン1' in line: 
                    conditions.append(Condition(ConditionType.TURN_1))
                
                # --- Zone Context ---
                context_zone = None
                zone_map = {
                    '右サイドエリア': 'RIGHT_STAGE', '左サイドエリア': 'LEFT_STAGE', 'センターエリア': 'CENTER_STAGE',
                    '成功ライブカード置き場': 'SUCCESS_LIVE', 'ライブ成功カード置き場': 'SUCCESS_LIVE',
                    'エネルギー置き場': 'ENERGY', 'ライブカード置き場': 'LIVE_ZONE', 'ライブエリア': 'LIVE_AREA',
                    '控え室': 'DISCARD', '手札': 'HAND', 'ステージ': 'STAGE', '山札': 'DECK', 'デッキ': 'DECK'
                }
                for keyword, zone_id in zone_map.items():
                    if keyword in content:
                        context_zone = zone_id
                        if '相手' in content: context_zone = 'OPPONENT_' + context_zone
                        break

                # Success Live Count: 成功ライブカード置き場にカードがX枚以上ある場合
                if '成功ライブカード置き場' in content and '枚以上' in content:
                    match = re.search(r'(\d+)枚以上', content)
                    if match:
                        conditions.append(Condition(ConditionType.COUNT_SUCCESS_LIVE, {'min': int(match.group(1))}))

                # ALL Blade Rule (Meta Rule)
                if 'ALLブレード' in content and any(kw in content for kw in ['ハートとして扱う', 'ハートとして内容を確認', 'いずれかの色のハート']):
                    trigger = TriggerType.CONSTANT
                    effects.append(Effect(EffectType.META_RULE, target=TargetType.PLAYER, params={'type': 'heart_rule'}))

                # --- Condition Parsing ---
                # Group count
                if match := re.search(r'『(.*?)』.*?(\d+)(枚|人)以上', content):
                    params = {'group': match.group(1), 'min': int(match.group(2))}
                    if context_zone: params['zone'] = context_zone
                    conditions.append(Condition(ConditionType.COUNT_GROUP, params))
                # Zone count
                elif context_zone and (match := re.search(r'(\d+)(枚|人)以上', content)):
                    params = {'count': int(match.group(1)), 'zone': context_zone}
                    conditions.append(Condition(ConditionType.COUNT_DISCARD if context_zone == 'DISCARD' else ConditionType.COUNT_STAGE, params))
                
                # Generic count
                if (match := re.search(r'(\d+)枚以上ある場合', content)) and not conditions:
                    params = {'min': int(match.group(1))}
                    if context_zone: params['zone'] = context_zone
                    conditions.append(Condition(ConditionType.COUNT_STAGE, params))
                
                # "If all are X"
                if match := re.search(r'それらがすべて(.*?)の場合', content):
                     conditions.append(Condition(ConditionType.GROUP_FILTER, {'group': match.group(1), 'context': 'revealed'}))
                
                # Group filter 『...』
                for g in re.findall(r'『(.*?)』', content):
                    if not any(c.type == ConditionType.COUNT_GROUP and c.params.get('group') == g for c in conditions):
                        params = {'group': g}
                        if '名前の異なる' in content: params['distinct_names'] = True
                        if context_zone: params['zone'] = context_zone
                        if match := re.search(r'(\d+)(人|枚)以上', content):
                            params['count'] = int(match.group(1))
                            conditions.append(Condition(ConditionType.COUNT_GROUP, params))
                        else:
                            conditions.append(Condition(ConditionType.GROUP_FILTER, params))
                
                # Specific Member names 「...」
                if any(kw in content for kw in ['がある場合', 'がいる場合', '登場している場合']):
                    found_names = set()
                    for area_name, member_name in re.findall(r'([左中右センター].*?エリア)に「(.*?)」', content):
                        area_id = 'LEFT_STAGE' if '左' in area_name else 'RIGHT_STAGE' if '右' in area_name else 'CENTER_STAGE'
                        conditions.append(Condition(ConditionType.HAS_MEMBER, {'name': member_name, 'area': area_id, 'zone': 'STAGE'}))
                        found_names.add(member_name)
                    for n in re.findall(r'「(.*?)」', content):
                        if n not in found_names:
                            params = {'name': n}
                            if context_zone: params['zone'] = context_zone
                            conditions.append(Condition(ConditionType.HAS_MEMBER, params))
                
                # Colors
                for eng, jpn in {'red': '赤', 'blue': '青', 'green': '緑', 'yellow': '黄', 'purple': '紫', 'pink': 'ピンク'}.items():
                    if f'icon_{eng}' in line: conditions.append(Condition(ConditionType.HAS_COLOR, {'color': jpn}))
                
                # Negation
                if any(kw in content for kw in ['以外', 'でない場合', 'ではない場合']) and conditions:
                    conditions[-1].is_negated = True
                
                # center, life lead, score lead, opponent has, modal answer
                if 'センターエリア' in content and '場合' in content and not any(c.params.get('area') == 'CENTER_STAGE' for c in conditions):
                    conditions.append(Condition(ConditionType.IS_CENTER))
                if any(kw in content for kw in ['ライフが相手より多い', 'ライフが相手より少ない']): conditions.append(Condition(ConditionType.LIFE_LEAD))
                if 'スコア' in content and '相手より高い' in content: conditions.append(Condition(ConditionType.LIFE_LEAD, {'type': 'score'}))
                if '相手' in content and any(kw in content for kw in ['ある場合', 'いる場合']): conditions.append(Condition(ConditionType.OPPONENT_HAS))
                if match := re.search(r'回答が(.*?)の場合', content): conditions.append(Condition(ConditionType.MODAL_ANSWER, {'answer': match.group(1)}))
                
                # Cost filter: コスト(\d+)(以下|以上)
                if match := re.search(r'コスト(\d+)(以下|以上)', content):
                    conditions.append(Condition(ConditionType.COST_CHECK, {
                        'value': int(match.group(1)),
                        'comparison': 'LE' if match.group(2) == '以下' else 'GE'
                    }))
                
                # --- Cost Parsing ---
                if 'このメンバーをウェイトにし' in content or 'このメンバーをウェイトにする' in content: costs.append(Cost(AbilityCostType.TAP_SELF))
                if any(kw in content for kw in ['手札を1枚控え室に置', '手札を1枚捨て']): costs.append(Cost(AbilityCostType.DISCARD_HAND, 1))
                if match := re.search(r'手札を(\d+)枚控え室に置', content): costs.append(Cost(AbilityCostType.DISCARD_HAND, int(match.group(1))))
                if '手札をすべて公開する' in content: costs.append(Cost(AbilityCostType.REVEAL_HAND_ALL))
                if 'このメンバーを' in content and '控え室に置く' in content: costs.append(Cost(AbilityCostType.SACRIFICE_SELF))
                if '下に置かれているカードを' in content and '控え室に置く' in content: costs.append(Cost(AbilityCostType.SACRIFICE_UNDER))
                if 'エネルギーを' in content and '控え室に置く' in content: costs.append(Cost(AbilityCostType.DISCARD_ENERGY, 1))
                if '手札に戻す' in content and 'このメンバー' in content: costs.append(Cost(AbilityCostType.RETURN_HAND))
                if energy_icons := len(re.findall(r'\{\{icon_energy.*?\}\}', line)): costs.append(Cost(AbilityCostType.ENERGY, energy_icons))
                if match := re.search(r'エネルギーが(\d+)枚以上', content): conditions.append(Condition(ConditionType.COUNT_ENERGY, {'min': int(match.group(1))}))
                
                # Live card present condition: ライブカードがある場合
                if 'ライブカードがある場合' in content:
                    conditions.append(Condition(ConditionType.HAS_LIVE_CARD))
                
                 # Hand check: 公開した手札の中にライブカードがない場合
                if '公開した手札' in content and 'ライブカードがない' in content:
                     conditions.append(Condition(ConditionType.HAND_HAS_NO_LIVE))
                


                # --- Effect Parsing ---
                if match := re.search(r'(\d+)枚.*?引', content): effects.append(Effect(EffectType.DRAW, int(match.group(1)), TargetType.PLAYER))
                elif '引' in content: effects.append(Effect(EffectType.DRAW, 1, TargetType.PLAYER))
                
                if match := re.search(r'(?:デッキ|山札).*?(\d+)枚.*?(?:見る|見て)', content): effects.append(Effect(EffectType.LOOK_DECK, int(match.group(1))))
                if any(kw in content for kw in ['その中から', 'その中']): effects.append(Effect(EffectType.LOOK_AND_CHOOSE, 1, params={'source': 'looked'}))
                if match := re.search(r'(\d+)枚.*?公開', content): effects.append(Effect(EffectType.REVEAL_CARDS, int(match.group(1))))
                elif '公開' in content and 'エール' not in content: effects.append(Effect(EffectType.REVEAL_CARDS, 1))
                
                # Recovery/Add
                if '控え室から' in content and '手札に加え' in content:
                    filters = {}
                    if match := re.search(r'『(.*?)』', content): filters['group'] = match.group(1)
                    if match := re.search(r'コスト(\d+)以下', content): filters['cost_max'] = int(match.group(1))
                    eff_type = EffectType.RECOVER_LIVE if 'ライブカード' in content else EffectType.RECOVER_MEMBER
                    effects.append(Effect(eff_type, 1, TargetType.CARD_DISCARD, params={'to': 'hand', **filters}))
                    if any(kw in content for kw in ['ハート', 'heart']): effects[-1].params['filter'] = 'heart_req'
                elif '手札に加え' in content:
                    params = {'to': 'hand'}
                    if 'デッキ' in content: params['from'] = 'deck'
                    elif '成功ライブカード' in content: params['from'] = 'success_live'
                    elif 'ライブカード置き場' in content: params['from'] = 'live_zone'
                    elif '控え室' in content: params['from'] = 'discard'
                    if match := re.search(r'『(.*?)』', content): params['group'] = match.group(1)
                    if match := re.search(r'コスト(\d+)以下', content): params['cost_max'] = int(match.group(1))
                    effects.append(Effect(EffectType.ADD_TO_HAND, 1, params=params))
                
                if any(kw in content for kw in ['エールにより公開', 'エールで公開']): effects.append(Effect(EffectType.CHEER_REVEAL, 1))
                if 'デッキ' in content and any(kw in content for kw in ['探', 'サーチ']): effects.append(Effect(EffectType.SEARCH_DECK, 1))
                
                # Buffs
                target = TargetType.MEMBER_NAMED if (match := re.search(r'「(.*?)」.*?は', content)) else TargetType.OPPONENT if '相手' in content else TargetType.ALL_PLAYERS if '全員' in content else TargetType.MEMBER_SELF
                target_params = {'target_name': match.group(1)} if target == TargetType.MEMBER_NAMED else {}
                
                if 'ブレード' in content and '得る' in content:
                    count = int(match.group(1)) if (match := re.search(r'ブレード.*?(\d+)', content)) else 1
                    if 'ALLブレード' in content: target_params['all_blade'] = True
                    effects.append(Effect(EffectType.ADD_BLADES, count, target, params=target_params))
                if any(kw in content for kw in ['ハート', 'heart']) and any(kw in content for kw in ['得る', '加える', '増える']):
                    count = int(match.group(1)) if (match := re.search(r'[+＋](\d+)', content)) else len(re.findall(r'heart_\d+\.png', content)) or 1
                    effects.append(Effect(EffectType.ADD_HEARTS, count, target, params=target_params))
                elif any(kw in content for kw in ['必要ハート', 'heart']) and any(kw in content for kw in ['減らす', '少なくなる', '減る']):
                    count = int(match.group(1)) if (match := re.search(r'[-－](\d+)', content)) else len(re.findall(r'heart_00\.png', content)) or 1
                    effects.append(Effect(EffectType.REDUCE_HEART_REQ, count, TargetType.PLAYER, params=target_params))
                
                if 'エネルギー' in content and any(kw in content for kw in ['置く', '加える']):
                    effects.append(Effect(EffectType.ENERGY_CHARGE, 1, params={'from': 'deck'} if 'デッキ' in content else {}))
                
                if any(kw in content for kw in ['につき', '枚数', '1人につき', '人につき']):
                    eff_params = {'multiplier': True}
                    if '成功ライブカード' in content or 'ライブカード' in content: eff_params['per_live'] = True
                    elif 'エネ' in content: eff_params['per_energy'] = True
                    elif 'メンバー' in content or '人につき' in content: eff_params['per_member'] = True
                    # Attach to the LAST effect if applicable
                    if effects and effects[-1].effect_type in (EffectType.ADD_BLADES, EffectType.ADD_HEARTS, EffectType.BUFF_POWER):
                        effects[-1].params.update(eff_params)
                    else:
                        effects.append(Effect(EffectType.BUFF_POWER, 1, params=eff_params))
                
                if (match := re.search(r'[+＋](\d+)', content)) and not any(kw in content for kw in ['ブレード', 'ハート', 'スコア']):
                    effects.append(Effect(EffectType.BUFF_POWER, int(match.group(1))))
                
                if 'エリア' in content and '移動' in content: effects.append(Effect(EffectType.MOVE_MEMBER, 1))
                if 'アクティブに' in content:
                    count = int(match.group(1)) if (match := re.search(r'(\d+)枚', content)) else 1
                    target_type = TargetType.MEMBER_SELF if 'このメンバー' in content else TargetType.MEMBER_SELECT
                    effects.append(Effect(EffectType.ACTIVATE_MEMBER, count, target_type, params={'target': 'energy'} if 'エネルギー' in content else {}))
                
                # Duration
                dur = {'until': 'live_end'} if 'ライブ終了時まで' in content else {'until': 'turn_end'} if any(kw in content for kw in ['ターン終了まで', '終了時まで']) else {}
                if dur:
                    if not effects: effects.append(Effect(EffectType.BUFF_POWER, 1, params={**dur, 'temporary': True}))
                    else:
                        for eff in effects: eff.params.update(dur)
                
                if '必要ハート' in content and any(kw in content for kw in ['扱う', '確認']): effects.append(Effect(EffectType.META_RULE, 0, params={'type': 'heart_rule'}))
                if 'スコア' in content and any(kw in content for kw in ['加算', '合算']): effects.append(Effect(EffectType.META_RULE, 0, params={'type': 'score_rule'}))
                if any(kw in content for kw in ['選ばれない', '選べない', '置けない']): effects.append(Effect(EffectType.IMMUNITY, 1))
                
                if '登場させる' in content:
                    count = int(match.group(1)) if (match := re.search(r'(\d+)枚', content)) else 1
                    src = 'hand' if '手札' in content else 'discard'
                    effects.append(Effect(EffectType.RECOVER_MEMBER, count, TargetType.CARD_DISCARD, {'auto_play': True, 'from': src}))
                
                # Cluster 5: Remote Ability Triggering
                if '能力' in content and any(kw in content for kw in ['発動させる', '発動する']):
                    zone = 'discard' if '控え室' in content else 'stage'
                    effects.append(Effect(EffectType.TRIGGER_REMOTE, 1, params={'from': zone}))

                if '控' in content and any(kw in content for kw in ['置', '送']):
                    # Prevent parsing "Sacrifice Self" as generic discard effect
                    if 'このメンバー' not in content:
                        count = int(match.group(1)) if (match := re.search(r'(?:手札|から).*?(\d+)枚', content)) else int(match.group(1)) if (match := re.search(r'(\d+)枚', content)) else 1
                        src = 'deck' if 'デッキ' in content else 'hand' if '手札' in content else None
                        effects.append(Effect(EffectType.SWAP_CARDS, count, params={'target': 'discard', 'from': src} if src else {'target': 'discard'}))
                
                if '相手' in content and any(kw in content for kw in ['ウェイト', '休み']):
                    count = int(match.group(1)) if (match := re.search(r'(\d+)人', content)) else 1
                    effects.append(Effect(EffectType.TAP_OPPONENT, count, TargetType.OPPONENT, {'all': True} if 'すべて' in content else {}))
                
                if match := re.search(r'スコア.*?[+＋](\d+)', content): effects.append(Effect(EffectType.BOOST_SCORE, int(match.group(1))))
                elif 'スコア' in content and any(kw in content for kw in ['得る', '＋']): effects.append(Effect(EffectType.BOOST_SCORE, 1))
                
                if 'コスト' in content and any(kw in content for kw in ['減', '-']): effects.append(Effect(EffectType.REDUCE_COST, 1))
                if any(kw in content for kw in ['無効', 'キャンセル']): effects.append(Effect(EffectType.NEGATE_EFFECT, 1))
                
                if 'デッキ' in content:
                    if '順番' in content: effects.append(Effect(EffectType.ORDER_DECK, 1))
                    elif ('一番上' in content or '一番下' in content) and 'シャッフル' in content and '合計' in content:
                        count = int(match.group(1)) if (match := re.search(r'合計(\d+)枚', content)) else 0
                        params = {'shuffle': True, 'position': 'bottom' if '一番下' in content else 'top', 'target_zone': 'discard' if '控え室' in content else None}
                        if names := re.findall(r'「(.*?)」', content): params['target_names'] = names
                        effects.append(Effect(EffectType.ORDER_DECK, count, params=params))
                    elif '一番上' in content: effects.append(Effect(EffectType.MOVE_TO_DECK, 1, params={'position': 'top'}))
                    elif '一番下' in content: effects.append(Effect(EffectType.MOVE_TO_DECK, 1, params={'position': 'bottom'}))
                    if effects and effects[-1].effect_type in (EffectType.ORDER_DECK, EffectType.LOOK_AND_CHOOSE):
                        if 'メンバー' in content: effects[-1].params['filter'] = 'member'
                        if 'ライブ' in content: effects[-1].params['filter'] = 'live'
                
                if match := re.search(r'以下から(\d+|１|２|３|４|５|一|二|三|四|五)(つ|枚|回)を選ぶ', content):
                    val_str = match.group(1)
                    # Simple mapping for common Japanese numerals
                    val_map = {'１': 1, '２': 2, '３': 3, '４': 4, '５': 5, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5}
                    val = int(val_map.get(val_str, val_str)) if not val_str.isdigit() else int(val_str)
                    effects.append(Effect(EffectType.SELECT_MODE, val))
                elif '以下から1つを選ぶ' in content: effects.append(Effect(EffectType.SELECT_MODE, 1))
                if any(kw in content for kw in ['ハートの色を1つ指定', '好きなハートの色を']): effects.append(Effect(EffectType.COLOR_SELECT, 1))
                if 'メンバーの下に' in content and '置' in content: effects.append(Effect(EffectType.PLACE_UNDER, 1))
                if '聞く' in content: effects.append(Effect(EffectType.FLAVOR_ACTION, 1))
                if 'ライブできない' in content: effects.append(Effect(EffectType.RESTRICTION, 1, params={'type': 'live'}))
                if '置くことができない' in content: effects.append(Effect(EffectType.RESTRICTION, 1, params={'type': 'placement'}))
                if 'なる' in content and 'すべて' in content and (match := re.search(r'すべて\[(.*?)\]になる', content)): effects.append(Effect(EffectType.TRANSFORM_COLOR, 1, params={'target_color': match.group(1)}))
                if 'バトンタッチ' in content and '2人' in content: effects.append(Effect(EffectType.BATON_TOUCH_MOD, 2))
                if match := re.search(r'スコアは([0-9０-９]+)になる', content): effects.append(Effect(EffectType.SET_SCORE, int(match.group(1).replace('４','4'))))
                if '公開' in content and any(kw in content for kw in ['置き場', '加える']): effects.append(Effect(EffectType.SWAP_ZONE, 1))
                if '手札に加える' in content and not effects: effects.append(Effect(EffectType.DRAW, 1, params={'generic_add': True}))
                
                # Replacement Effects (代わりに - Cluster 4)
                if '代わりに' in content:
                    # Find the replacement value (e.g., 'スコアを＋２' -> 2)
                    match = re.search(r'代わりに.*?[+＋](\d+)', content)
                    if match:
                        effects.append(Effect(EffectType.REPLACE_EFFECT, int(match.group(1)), params={'replaces': 'score_boost'}))

                if (content.startswith('（') and content.endswith('）')) or (content.startswith('(') and content.endswith(')')):
                     # If the whole sentence is in parens, it's often reminder text
                     if not effects:
                         effects.append(Effect(EffectType.META_RULE, 1))
                         trigger = TriggerType.CONSTANT
                     else:
                         # Ensure reminder text within a block doesn't add accidental effects
                         pass 

                # Final touches
                is_opt = 'てもよい' in content
                is_glob = 'すべての' in content
                is_opp_hand = '相手の手札' in content
                for eff in effects:
                    eff.is_optional = is_opt
                    if is_glob: eff.params['all'] = True
                    if is_opp_hand: eff.target = TargetType.OPPONENT_HAND
                # Also mark costs as optional when pattern detected
                for cost in costs:
                    if is_opt:
                        cost.is_optional = True
                
                # --- Construct Ability ---
                if trigger != TriggerType.NONE:
                    # Handle multiple triggers (lazy way: create one ability, caller might need to dup if we want perfection, 
                    # but actually we can just return a list of abilities from this function, so we can append multiple)
                    # For now, let's keep it simple: if we detected the slash, we append multiple
                    
                    base_ability = Ability(raw_text=content.strip(), trigger=trigger, effects=effects, conditions=conditions, costs=costs, is_once_per_turn=is_once_per_turn)
                    abilities.append(base_ability)
                    last_ability = base_ability
                    
                    # Dual trigger hack for PL!-PR-009-PR
                    if 'toujyou' in line and (('live_start' in line) or ('live_success' in line)) and '/' in line:
                         second_trigger = TriggerType.ON_LIVE_START if 'live_start' in line else TriggerType.ON_LIVE_SUCCESS
                         # Clone it effectively
                         abilities.append(Ability(
                             raw_text=content.strip(), 
                             trigger=second_trigger, 
                             effects=[Effect(e.effect_type, e.value, e.target, e.params.copy(), e.is_optional) for e in effects], 
                             conditions=[Condition(c.type, c.params.copy(), c.is_negated) for c in conditions], 
                             costs=[Cost(c.type, c.value, c.params.copy(), c.is_optional) for c in costs],
                             is_once_per_turn=base_ability.is_once_per_turn
                         ))
                         
                elif effects or conditions or costs:
                    if last_ability:
                        if (line.startswith('・') or line.startswith('-') or line.startswith('－')) and any(e.effect_type == EffectType.SELECT_MODE for e in last_ability.effects):
                            last_ability.modal_options.append(effects)
                        else:
                            last_ability.effects.extend(effects)
                            last_ability.conditions.extend(conditions)
                            last_ability.costs.extend(costs)
                        last_ability.raw_text += " " + content.strip()
                        if is_once_per_turn: last_ability.is_once_per_turn = True
                    elif not is_continuation:
                        last_ability = Ability(raw_text=content.strip(), trigger=TriggerType.CONSTANT, effects=effects, conditions=conditions, costs=costs, is_once_per_turn=is_once_per_turn)
                        abilities.append(last_ability)
                        
        return abilities
