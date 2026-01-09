--- START OF FILE ability.py ---
"""
Ability and Effect System for Love Live Card Game.
Provides detailed modeling of game rules, triggers, costs, and complex resolution logic.
"""

from enum import IntEnum, auto
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field
import re

# ==========================================
# 1. Trigger Definitions
# ==========================================

class TriggerType(IntEnum):
    NONE = 0
    ON_PLAY = 1             # {{toujyou}} / 登場
    ON_LIVE_START = 2       # {{live_start}} / ライブ開始時
    ON_LIVE_SUCCESS = 3     # {{live_success}} / ライブ成功時
    CONSTANT = 4            # {{jyouji}} / 常時
    AUTO = 5                # {{jidou}} / 自動 (General state triggers)
    ACTIVATED = 6           # {{kidou}} / 起動
    TURN_START = 7          # ターン開始時
    TURN_END = 8            # ターン終了時
    ON_MOVE = 9             # エリアを移動したとき
    ON_OPPONENT_WAIT = 10   # 相手のメンバーがウェイトしたとき

# ==========================================
# 2. Targeting & Zones
# ==========================================

class ZoneType(IntEnum):
    NONE = 0
    HAND = 1
    STAGE = 2
    DISCARD = 3         # 控え室
    DECK = 4
    ENERGY = 5
    LIVE_ZONE = 6       # Live Card placement area
    SUCCESS_ZONE = 7    # Successful Lives
    REMOVED = 8

class TargetArea(IntEnum):
    ANY = 0
    CENTER = 1
    SIDE = 2            # Left or Right
    LEFT = 3
    RIGHT = 4
    ALL_AREAS = 5

class TargetPlayer(IntEnum):
    YOU = 0
    OPPONENT = 1
    BOTH = 2

# ==========================================
# 3. Effect Types (Granular)
# ==========================================

class EffectType(IntEnum):
    # --- Drawing & Resources ---
    DRAW = 1
    DISCARD_HAND = 2            # Effect forcing discard (not cost)
    RECOVER_TO_HAND = 3         # From Discard/Energy to Hand
    SEARCH_DECK = 4             # Look at top N, add X to hand
    CHARGE_ENERGY = 5           # Add card to energy
    
    # --- Stage Manipulation ---
    PLAY_MEMBER = 10            # Summon from Hand/Discard
    MOVE_MEMBER = 11            # Move within stage
    SWAP_MEMBER = 12            # Switch positions (Formation change)
    RETURN_TO_HAND = 13         # Bounce member
    SEND_TO_DISCARD = 14        # Removal / Sacrifice
    PLACE_UNDER = 15            # Put card under member (Yuigooka mechanics)
    
    # --- State Changes ---
    ACTIVATE = 20               # Untap
    WAIT = 21                   # Tap
    
    # --- Buffs / Debuffs ---
    BUFF_POWER = 30             # Generic power (rare in LL, mostly hearts/blades)
    GAIN_BLADE = 31             # Gain Blade icon
    GAIN_HEART = 32             # Gain Heart icon
    CHANGE_BASE_HEARTS = 33     # "Original hearts become X"
    MODIFY_COST = 34            # Reduce/Increase cost
    GRANT_ABILITY = 35          # Give [Trigger] text to a member
    NEGATE_ABILITY = 36         # Nullify abilities
    
    # --- Live Mechanics ---
    MODIFY_LIVE_SCORE = 40      # +Score
    MODIFY_LIVE_REQ = 41        # Reduce/Increase heart requirements
    SET_LIVE_REQ_TYPE = 42      # "Treat ALL blades as any color", etc.
    FORCE_LIVE_FAILURE = 43     # Cannot place in success zone
    LIVE_AUTO_WIN = 44          # Win ties
    
    # --- Deck Manipulation ---
    LOOK_AND_TOPDECK = 50       # Look top X, place back
    LOOK_AND_BOTTOMDECK = 51    # Look top X, place bottom
    RECYCLE_TO_DECK = 52        # Shuffle from discard to deck
    
    # --- Game Rules / Meta ---
    RESTRICTION_PLAY = 90       # Cannot play/summon
    RESTRICTION_LIVE = 91       # Cannot perform Live
    RESTRICTION_ACTIVATE = 92   # Cannot untap
    MODIFY_CHEER_COUNT = 93     # Wien Margarete (-8 cards revealed)
    FLAVOR_QUESTION = 94        # "Ask opponent what they like"
    
    # --- Flow Control ---
    SELECT_OPTION = 99          # Choose 1 of the following

# ==========================================
# 4. Conditions (for If/Then logic)
# ==========================================

class ConditionType(IntEnum):
    ALWAYS = 0
    
    # Counts
    COUNT_HAND = 1
    COUNT_STAGE = 2
    COUNT_ENERGY = 3
    COUNT_DISCARD = 4
    COUNT_SUCCESS_LIVE = 5
    COUNT_LIVE_ZONE = 6         # Current live cards
    
    # Attributes
    HAS_GROUP = 10              # Specific group on stage (u's, Aqours, etc)
    HAS_UNIT = 11               # Specific unit (Printemps, etc)
    HAS_NAME = 12               # Specific member name
    HAS_COST = 13               # Cost comparison (>=, <=)
    HAS_COLOR = 14              # Specific heart color present
    HAS_BLADE_COUNT = 15        # Member has X blades
    
    # State
    IS_ACTIVE = 20
    IS_WAITING = 21
    IS_CENTER = 22
    IS_SIDE = 23
    
    # History / Meta
    ENTERED_THIS_TURN = 30
    ENTERED_VIA_BATON = 31
    MOVED_THIS_TURN = 32
    IS_TURN_PLAYER = 33
    IS_FIRST_TURN = 34
    
    # Comparisons
    COMPARE_SCORE = 40          # Score vs Opponent
    COMPARE_ENERGY = 41         # Energy vs Opponent
    COMPARE_HAND = 42           # Hand vs Opponent
    COMPARE_HEARTS = 43         # Total hearts vs Opponent
    
    # Specifics
    CHEER_HAS_TYPE = 50         # Cheer revealed specific card type
    CHEER_HAS_NO_BLADE = 51     # Cheer revealed NO blades
    
    # Modal
    USER_CHOICE = 99            # Used for modal branches

# ==========================================
# 5. Data Structures
# ==========================================

@dataclass
class Condition:
    type: ConditionType
    target: TargetPlayer = TargetPlayer.YOU
    # Params: 'min', 'max', 'value', 'group', 'name', 'color', 'zone'
    params: Dict[str, Any] = field(default_factory=dict)
    negated: bool = False

@dataclass
class Cost:
    # Costs are mandatory actions to activate an ability
    raw_text: str
    energy_cost: int = 0
    tap_self: bool = False
    discard_card_count: int = 0
    discard_card_type: Optional[str] = None # 'LIVE', 'MEMBER', 'GROUP_X'
    return_to_hand: bool = False
    sacrifice_self: bool = False
    shuffle_discard_count: int = 0 # e.g. Shuffle 6 specific cards to deck bottom

@dataclass
class Effect:
    type: EffectType
    target_player: TargetPlayer = TargetPlayer.YOU
    target_zone: ZoneType = ZoneType.NONE
    value: int = 0
    
    # 'group', 'unit', 'name', 'max_cost', 'color'
    filters: Dict[str, Any] = field(default_factory=dict)
    
    # For conditional effects ("If X, then +1")
    sub_conditions: List[Condition] = field(default_factory=list)
    
    # "Up to", "Optional"
    is_optional: bool = False
    is_up_to: bool = False
    
    # Duration: 'turn', 'live', 'permanent'
    duration: str = 'permanent'

@dataclass
class Ability:
    raw_text: str
    trigger: TriggerType
    costs: List[Cost]
    conditions: List[Condition] # Requirements to play/trigger
    effects: List[Effect]
    is_once_per_turn: bool = False
    area_restriction: Optional[TargetArea] = None # e.g. Center Only

    def __repr__(self):
        return f"<Ability: [{self.trigger.name}] {self.raw_text[:30]}...>"

# ==========================================
# 6. Parser Implementation
# ==========================================

class AbilityParser:
    
    @staticmethod
    def parse(text: str) -> List[Ability]:
        clean_text = text.replace('\\n', '\n').replace('\r', '')
        # Split by distinct abilities using the Trigger tags as delimiters
        # We look for {{...}} patterns to start a new block
        parts = re.split(r'(\{\{.*?\}\})', clean_text)
        
        abilities = []
        current_trigger = TriggerType.CONSTANT # Default if no tag
        current_text = ""
        
        # Initial pass to reconstruct blocks
        blocks = []
        
        # If text doesn't start with a tag, handle preamble
        if parts and not re.match(r'\{\{.*?\}\}', parts[0]):
            if parts[0].strip():
                blocks.append((TriggerType.CONSTANT, parts[0].strip()))
            parts = parts[1:]
            
        i = 0
        while i < len(parts):
            tag = parts[i]
            content = parts[i+1] if i+1 < len(parts) else ""
            
            trigger = AbilityParser._map_trigger(tag)
            blocks.append((trigger, content.strip()))
            i += 2
            
        for trig, content in blocks:
            if not content: continue
            
            # Handle multiple sentences within one block (split by 。)
            # However, some sentences belong together "Do X. If you do, Do Y."
            # For this simplified parser, we treat the block as one Ability with multiple effects
            parsed_ability = AbilityParser._parse_block(trig, content)
            abilities.append(parsed_ability)
            
        return abilities

    @staticmethod
    def _map_trigger(tag: str) -> TriggerType:
        if 'toujyou' in tag or '登場' in tag: return TriggerType.ON_PLAY
        if 'live_start' in tag or 'ライブ開始' in tag: return TriggerType.ON_LIVE_START
        if 'live_success' in tag or 'ライブ成功' in tag: return TriggerType.ON_LIVE_SUCCESS
        if 'jyouji' in tag or '常時' in tag: return TriggerType.CONSTANT
        if 'jidou' in tag or '自動' in tag: return TriggerType.AUTO
        if 'kidou' in tag or '起動' in tag: return TriggerType.ACTIVATED
        if 'turn_start' in tag: return TriggerType.TURN_START
        return TriggerType.CONSTANT

    @staticmethod
    def _parse_block(trigger: TriggerType, text: str) -> Ability:
        costs = []
        conditions = []
        effects = []
        
        # 1. Separation of Cost/Condition vs Effect
        # Japanese syntax usually uses "：" (full width colon) for Activation Costs
        # Conditions often end in "場合、" (if ...)
        
        # Check specific Center restriction
        area_restrict = None
        if '{{center' in text or 'センターエリア' in text:
            if 'のみ発動' in text or 'のみ起動' in text:
                area_restrict = TargetArea.CENTER
            text = re.sub(r'\{\{.*?\}\}', '', text) # Remove inner tags
        
        activation_part = ""
        effect_part = text
        
        if '：' in text:
            parts = text.split('：', 1)
            activation_part = parts[0]
            effect_part = parts[1]
        elif ':' in text:
            parts = text.split(':', 1)
            activation_part = parts[0]
            effect_part = parts[1]
            
        # 2. Parse Activation (Costs & Activation Conditions)
        if activation_part:
            AbilityParser._parse_activation(activation_part, costs, conditions)
            
        # 3. Parse Effects (and conditional effects)
        AbilityParser._parse_effects(effect_part, effects, conditions)
        
        # 4. Global Flags
        once = 'ターン1回' in text or 'Turn 1' in text
        
        return Ability(
            raw_text=text,
            trigger=trigger,
            costs=costs,
            conditions=conditions,
            effects=effects,
            is_once_per_turn=once,
            area_restriction=area_restrict
        )

    @staticmethod
    def _parse_activation(text: str, costs: List[Cost], conditions: List[Condition]):
        # --- COSTS ---
        
        # Energy
        e_count = text.count('icon_energy')
        if e_count > 0:
            costs.append(Cost(f"Pay {e_count} Energy", energy_cost=e_count))
            
        # Tap Self
        if 'このメンバーをウェイト' in text:
            costs.append(Cost("Tap Self", tap_self=True))
            
        # Discard Hand
        discard_match = re.search(r'手札を(\d+)枚.*?控え室', text)
        if discard_match:
            cnt = int(discard_match.group(1))
            c_type = 'ANY'
            if 'ライブカード' in text: c_type = 'LIVE'
            if 'メンバー' in text: c_type = 'MEMBER'
            costs.append(Cost(f"Discard {cnt} {c_type}", discard_card_count=cnt, discard_card_type=c_type))
            
        # Shuffle Discard (LL-bp3-001-R+ type)
        if '控え室にある' in text and 'デッキの一番下' in text:
             num_match = re.search(r'合計(\d+)枚', text)
             count = int(num_match.group(1)) if num_match else 0
             costs.append(Cost(f"Shuffle {count} from discard", shuffle_discard_count=count))

        # --- CONDITIONS (Pre-effect) ---
        # "If X is on stage"
        
        # Check specific card names
        name_match = re.search(r'「(.*?)」', text)
        if name_match and 'いる場合' in text:
            conditions.append(Condition(ConditionType.HAS_NAME, params={'name': name_match.group(1)}))
            
        # Check counts
        count_match = re.search(r'(\d+)枚以上', text)
        if count_match and 'エネルギー' in text:
            conditions.append(Condition(ConditionType.COUNT_ENERGY, params={'min': int(count_match.group(1))}))

    @staticmethod
    def _parse_effects(text: str, effects: List[Effect], global_conditions: List[Condition]):
        # Sentences
        sentences = re.split(r'[。.]', text)
        
        current_condition = None # For "If X, then Y" flow
        
        for s in sentences:
            s = s.strip()
            if not s: continue
            
            # --- Inline Conditions (If X, Y) ---
            if '場合、' in s:
                cond_text, eff_text = s.split('場合、', 1)
                
                # Parse the condition part
                cond_params = {}
                c_type = ConditionType.ALWAYS
                
                if 'スコア' in cond_text and ('高い' in cond_text or '多い' in cond_text):
                    c_type = ConditionType.COMPARE_SCORE
                    cond_params['op'] = 'gt'
                elif 'スコア' in cond_text and '以上' in cond_text:
                     num = re.search(r'(\d+|[０-９]+)', cond_text)
                     if num: 
                         c_type = ConditionType.COUNT_SUCCESS_LIVE # Approx
                         cond_params['score_min'] = int(num.group(1).replace('６','6').replace('３','3')) # dirty hack for wide chars
                elif '手札' in cond_text and '多い' in cond_text:
                    c_type = ConditionType.COMPARE_HAND
                    cond_params['op'] = 'gt'
                elif 'エネルギー' in cond_text and '枚以上' in cond_text:
                    c_type = ConditionType.COUNT_ENERGY
                    num = re.search(r'(\d+)', cond_text)
                    if num: cond_params['min'] = int(num.group(1))
                    
                # Store this condition to apply to effects in the second half
                current_condition = Condition(c_type, params=cond_params)
                
                # Recursively parse the effect part
                temp_effects = []
                AbilityParser._parse_effects_logic(eff_text, temp_effects)
                for eff in temp_effects:
                    eff.sub_conditions.append(current_condition)
                    effects.append(eff)
                
                continue
            
            # Direct parsing if no "If" clause
            AbilityParser._parse_effects_logic(s, effects)

    @staticmethod
    def _parse_effects_logic(text: str, effects: List[Effect]):
        # Flag checks
        is_optional = 'てもよい' in text
        is_up_to = 'まで' in text
        
        # Duration check
        duration = 'permanent'
        if 'ライブ終了時まで' in text: duration = 'live'
        elif 'ターン終了時まで' in text: duration = 'turn'
        
        # 1. DRAW
        if '引く' in text:
            count_match = re.search(r'(\d+)枚', text)
            val = int(count_match.group(1)) if count_match else 1
            effects.append(Effect(EffectType.DRAW, value=val, is_optional=is_optional))
            
        # 2. DISCARD / HAND DROP
        if '手札' in text and ('控え室' in text or '捨てる' in text):
            count_match = re.search(r'(\d+)枚', text)
            val = int(count_match.group(1)) if count_match else 1
            effects.append(Effect(EffectType.DISCARD_HAND, value=val, is_optional=is_optional))

        # 3. SEARCH / LOOK TOP
        if 'デッキの上' in text and '見る' in text:
            count_match = re.search(r'(\d+)枚', text)
            val = int(count_match.group(1)) if count_match else 1
            
            # Determine follow-up (Add to hand?)
            if '手札' in text:
                # This is a Search effect
                params = {}
                if 'コスト' in text:
                    cost_m = re.search(r'コスト(\d+)以下', text)
                    if cost_m: params['max_cost'] = int(cost_m.group(1))
                if 'ライブカード' in text: params['type'] = 'LIVE'
                if 'メンバー' in text: params['type'] = 'MEMBER'
                
                # Check for group extraction
                group_match = re.search(r'『(.*?)』', text)
                if group_match: params['group'] = group_match.group(1)
                
                effects.append(Effect(EffectType.SEARCH_DECK, value=val, filters=params, is_optional=is_optional))
            else:
                # Just Look
                effects.append(Effect(EffectType.LOOK_AND_TOPDECK, value=val))

        # 4. RECOVER (Salvage)
        if '控え室' in text and '手札' in text and ('加える' in text or '戻す' in text):
            # Ensure it's not the discard cost or search result
            if 'デッキ' not in text:
                params = {}
                if 'ライブカード' in text: params['type'] = 'LIVE'
                effects.append(Effect(EffectType.RECOVER_TO_HAND, value=1, filters=params, is_optional=is_optional))
                
        # 5. BUFFS (Heart / Blade / Score)
        if '得る' in text or 'プラス' in text or '＋' in text:
            # Score
            score_m = re.search(r'スコア.*?(\d+|[０-９])', text)
            if score_m:
                 val = int(score_m.group(1).replace('１','1').replace('２','2')) # Normalize
                 effects.append(Effect(EffectType.MODIFY_LIVE_SCORE, value=val, duration=duration))
            
            # Blade
            if 'ブレード' in text:
                cnt = text.count('icon_blade') or 1
                target = TargetType.SELF
                if '全員' in text: target = TargetType.ALL_PLAYERS
                effects.append(Effect(EffectType.GAIN_BLADE, value=cnt, duration=duration))
                
            # Heart
            if 'ハート' in text or 'heart' in text:
                # Very specific parsing for heart colors usually required here
                # Simplified for this example
                effects.append(Effect(EffectType.GAIN_HEART, value=1, duration=duration))
        
        # 6. ACTIVATE (Untap)
        if 'アクティブ' in text:
            target_zone = ZoneType.STAGE
            if 'エネルギー' in text: target_zone = ZoneType.ENERGY
            
            count_m = re.search(r'(\d+)', text)
            val = int(count_m.group(1)) if count_m else 1
            
            effects.append(Effect(EffectType.ACTIVATE, target_zone=target_zone, value=val))
            
        # 7. POSITION CHANGE
        if 'ポジションチェンジ' in text:
            effects.append(Effect(EffectType.POSITION_CHANGE))
            
        # 8. PLAY MEMBER (Summon)
        if '登場させる' in text:
            params = {}
            if '控え室' in text: params['source'] = 'DISCARD'
            if '手札' in text: params['source'] = 'HAND'
            if 'ウェイト状態' in text: params['status'] = 'WAIT'
            
            cost_m = re.search(r'コスト(\d+)以下', text)
            if cost_m: params['max_cost'] = int(cost_m.group(1))
            
            effects.append(Effect(EffectType.PLAY_MEMBER, filters=params))
            
        # 9. CHEER MOD (Wien)
        if 'エール' in text and '減る' in text:
             num_m = re.search(r'(\d+)', text)
             val = int(num_m.group(1)) if num_m else 0
             effects.append(Effect(EffectType.MODIFY_CHEER_COUNT, value=-val, duration=duration))

