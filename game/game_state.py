"""
Love Live Card Game - AlphaZero Compatible Game State

This module implements the game state representation for the Love Live
Official Card Game, designed for fast self-play with AlphaZero-style training.

Key Design Decisions:
- Numpy arrays for vectorized operations
- Immutable state with state copying for MCTS
- Action space encoded as integers for neural network output
- Observation tensors suitable for CNN input
"""

# Love Live! Card Game - Comprehensive Rules v1.04 Implementation
# Rule 1: Overview
# Rule 2: Card Information
# Rule 3: Players (Owner/Master)
# Rule 4: Zones

import numpy as np
from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Tuple, Optional, Dict, Any
import copy
try:
    from game.ability import Ability, TriggerType, Effect, EffectType, TargetType, AbilityCostType
except ImportError:
    from ability import Ability, TriggerType, Effect, EffectType, TargetType, AbilityCostType


class Phase(IntEnum):
    """Game phases within a turn"""
    SETUP = -2          # Initial setup (deck shuffle, energy placement)
    MULLIGAN_P1 = -1    # First player mulligan
    MULLIGAN_P2 = 0     # Second player mulligan (note: reusing 0 OK if we renumber)
    ACTIVE = 1          # Untap all cards
    ENERGY = 2          # Draw energy
    DRAW = 3            # Draw card
    MAIN = 4            # Play members, use abilities
    LIVE_SET = 5        # Set live cards face-down
    PERFORMANCE_P1 = 6  # First player's performance
    PERFORMANCE_P2 = 7  # Second player's performance
    LIVE_RESULT = 8     # Determine live winner


class CardType(IntEnum):
    """Card types in the game"""
    MEMBER = 0
    LIVE = 1
    ENERGY = 2


class HeartColor(IntEnum):
    """Heart/color types (6 colors + any + rainbow)"""
    PINK = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    PURPLE = 5
    ANY = 6      # Colorless requirement
    RAINBOW = 7  # Can be any color


class Area(IntEnum):
    """Member areas on stage"""
    LEFT = 0
    CENTER = 1
    RIGHT = 2


@dataclass
class MemberCard:
    """Represents a member card with all attributes"""
    card_id: int
    name: str
    cost: int
    hearts: np.ndarray  # Shape (6,) for each color count
    blade_hearts: np.ndarray  # Shape (6,) blade hearts by color
    blades: int
    group: str = ""
    unit: str = ""
    abilities: List[Ability] = field(default_factory=list)
    img_path: str = ""
    ability_text: str = ""
    volume_icons: int = 0
    draw_icons: int = 0
    
    def total_hearts(self) -> int:
        return int(np.sum(self.hearts))
    
    def total_blade_hearts(self) -> int:
        return int(np.sum(self.blade_hearts))


@dataclass 
class LiveCard:
    """Represents a live/song card"""
    card_id: int
    name: str
    score: int
    required_hearts: np.ndarray  # Shape (7,) required hearts by color (6 colors + any)
    abilities: List[Ability] = field(default_factory=list)
    img_path: str = ""
    ability_text: str = ""
    volume_icons: int = 0
    draw_icons: int = 0
    
    def total_required(self) -> int:
        return int(np.sum(self.required_hearts))


@dataclass
class EnergyCard:
    """Simple energy card"""
    card_id: int


class PlayerState:
    """State for one player - uses numpy arrays for efficiency (Rule 3)"""
    
    def __init__(self, player_id: int):
        self.player_id = player_id
        
        # Zones (Rule 4)
        self.hand: List[int] = []            # Rule 4.11 (Hand)
        self.main_deck: List[int] = []       # Rule 4.8 (Main Deck)
        self.energy_deck: List[int] = []     # Rule 4.9 (Energy Deck)
        self.discard: List[int] = []         # Rule 4.12 (Discard)
        self.energy_zone: List[int] = []     # Rule 4.7 (Energy Zone)
        self.success_lives: List[int] = []   # Rule 4.10 (Success Zone)
        self.live_zone: List[int] = []       # Rule 4.6 (Live Zone)
        self.live_zone_revealed: bool = False
        
        # Stage - 3 areas, each can have one member
        # -1 means empty, otherwise card_id
        self.stage: np.ndarray = np.full(3, -1, dtype=np.int32)
        
        # Energy under members (for each area, list of energy card_ids)
        self.stage_energy: List[List[int]] = [[], [], []]
        
        # Card states
        self.tapped_energy: np.ndarray = np.zeros(50, dtype=bool)  # Which energy are tapped
        self.tapped_members: np.ndarray = np.zeros(3, dtype=bool)  # Which stage areas are tapped
        
        # Turn tracking
        self.members_played_this_turn: np.ndarray = np.zeros(3, dtype=bool)  # Areas that got new members
        
        # Mulligan tracking
        self.mulligan_selection: set = set()  # Card indices selected for mulligan
        
        # Live Phase Tracking
        self.live_score_bonus: int = 0
        self.passed_lives: List[int] = [] # Cards that cleared the heart check (Rule 8.3.15)
        
    def copy(self) -> 'PlayerState':
        """Deep copy for MCTS simulation"""
        new = PlayerState(self.player_id)
        new.hand = self.hand.copy()
        new.main_deck = self.main_deck.copy()
        new.energy_deck = self.energy_deck.copy()
        new.discard = self.discard.copy()
        new.energy_zone = self.energy_zone.copy()
        new.success_lives = self.success_lives.copy()
        new.live_zone = self.live_zone.copy()
        new.live_zone_revealed = self.live_zone_revealed
        new.stage = self.stage.copy()
        new.stage_energy = [e.copy() for e in self.stage_energy]
        new.tapped_energy = self.tapped_energy.copy()
        new.tapped_members = self.tapped_members.copy()
        new.members_played_this_turn = self.members_played_this_turn.copy()
        new.mulligan_selection = self.mulligan_selection.copy()
        new.live_score_bonus = self.live_score_bonus
        new.passed_lives = self.passed_lives.copy()
        return new
    
    def count_untapped_energy(self) -> int:
        """Count available energy"""
        return len(self.energy_zone) - np.sum(self.tapped_energy[:len(self.energy_zone)])
    
    def get_total_blades(self, card_db: Dict[int, MemberCard]) -> int:
        """Sum blades from all untapped members"""
        total = 0
        for i, card_id in enumerate(self.stage):
            if card_id >= 0 and not self.tapped_members[i]:
                if card_id in card_db:
                    total += card_db[card_id].blades
        return total
    
    def get_total_hearts(self, card_db: Dict[int, MemberCard]) -> np.ndarray:
        """Sum hearts from all untapped members on stage"""
        total = np.zeros(6, dtype=np.int32)
        for i, card_id in enumerate(self.stage):
            if card_id >= 0 and not self.tapped_members[i] and card_id in card_db:
                total += card_db[card_id].hearts
        return total


class GameState:
    """
    Full game state (Rule 1)
    
    Features:
    - Rule 4.14: Resolution Zone (yell_cards)
    - Rule 1.2: Victory Detection
    - MCTS / AlphaZero support
    """
    
    # Class-level card database (Rule 2)
    member_db: Dict[int, MemberCard] = {}
    live_db: Dict[int, LiveCard] = {}
    
    def __init__(self):
        self.players = [PlayerState(0), PlayerState(1)]
        self.current_player = 0  # Who is acting now
        self.first_player = 0    # Who goes first this turn
        self.phase = Phase.ACTIVE
        self.turn_number = 1
        self.game_over = False
        self.winner = -1  # -1 = ongoing, 0/1 = player won, 2 = draw
        
        # For yell phase tracking
        self.yell_cards: List[int] = [] # Shared Resolution Zone (Rule 4.14)
        self.pending_effects: List[Effect] = []  # Stack of effects to resolve
        self.pending_choices: List[dict] = []
        self.rule_log: List[str] = [] # Real-time rule application log
        
        # Static caches (for performance and accessibility)
        # Should be set from server or data loader
        
        # Loop Detection (Rule 12.1)
        # Using a simple hash of the serialization for history
        self.state_history: List[int] = []
        self.loop_draw = False
    
    def log_rule(self, rule_id: str, description: str):
        """Append a rule application entry to the log."""
        entry = f"[{rule_id}] {description}"
        self.rule_log.append(entry)
        # Also print to stdout for server console debugging
        print(f"RULE_LOG: {entry}")
        
    def copy(self) -> 'GameState':
        """Deep copy for MCTS simulation"""
        new = GameState()
        new.players = [p.copy() for p in self.players]
        new.current_player = self.current_player
        new.first_player = self.first_player
        new.phase = self.phase
        new.turn_number = self.turn_number
        new.game_over = self.game_over
        new.winner = self.winner
        new.yell_cards = self.yell_cards.copy()
        new.pending_effects = copy.deepcopy(self.pending_effects)
        new.pending_choices = self.pending_choices.copy()
        new.rule_log = self.rule_log.copy()
        new.state_history = self.state_history.copy()
        return new
    
    @property
    def active_player(self) -> PlayerState:
        return self.players[self.current_player]
    
    @property  
    def inactive_player(self) -> PlayerState:
        return self.players[1 - self.current_player]
    
    def is_terminal(self) -> bool:
        """Check if game has ended"""
        return self.game_over
    
    def get_winner(self) -> int:
        """Returns winner (0 or 1) or -1 if not terminal, 2 if draw"""
        return self.winner
    
    def check_win_condition(self) -> None:
        """Check if anyone has won (3+ successful lives)"""
        p0_lives = len(self.players[0].success_lives)
        p1_lives = len(self.players[1].success_lives)
        
        if p0_lives >= 3 and p1_lives >= 3:
            self.game_over = True
            self.winner = 2  # Draw
        elif p0_lives >= 3:
            self.game_over = True
            self.winner = 0
        elif p1_lives >= 3:
            self.game_over = True
            self.winner = 1
    
    def get_legal_actions(self) -> np.ndarray:
        """
        Returns a mask of legal actions.
        
        Action space encoding:
        0: Pass/End phase
        1-180: Play member card from hand to area (card index 0-59 * 3 areas)
        64-123: Set live card (card index 0-59)
        124: Confirm live set
        
        Expanded for Complexity:
        200-202: Activate ability of member in Area (LEFT, CENTER, RIGHT)
        203-262: Choose card in hand (index 0-59) for effect target
        263-265: Choose member on stage (Area 0-2) for effect target
        """
        mask = np.zeros(300, dtype=bool)  # Increased size to 300
        
        if self.game_over:
            return mask
        
        p = self.active_player
        
        # Priority: If there are choices to be made for a pending effect
        if self.pending_choices:
            choice_type, params = self.pending_choices[0]
            if choice_type == "TARGET_HAND":
                for i in range(len(p.hand)):
                    mask[203 + i] = True
            elif choice_type == "TARGET_MEMBER":
                 for i in range(3):
                     if p.stage[i] >= 0:
                         mask[263 + i] = True
            elif choice_type == "MODAL":
                # params['options'] is a list of strings
                options = params.get('options', [])
                for i in range(len(options)):
                    mask[270 + i] = True
            elif choice_type == "COLOR_SELECT":
                # 280: Red, 281: Blue, 282: Green, 283: Yellow, 284: Purple, 285: Pink
                for i in range(6):
                    mask[280 + i] = True
            return mask

        # MULLIGAN phases: Select cards to return or confirm mulligan
        if self.phase in (Phase.MULLIGAN_P1, Phase.MULLIGAN_P2):
            mask[0] = True  # Confirm mulligan (done selecting)
            # Actions 181-240: Toggle card for mulligan (card index 0-59)
            for i in range(len(p.hand)):
                mask[181 + i] = True
            return mask

        if self.phase == Phase.MAIN:
            # Can always pass
            mask[0] = True
            
            # Can play members from hand if we have energy
            available_energy = p.count_untapped_energy()
            for i, card_id in enumerate(p.hand):
                # Play to stage
                # Action: 1 + i*3 + area
                # Requires: 
                # 1. Card is member (should be if i is hand index)
                # 2. Hand index valid
                # 3. Energy >= Cost
                # 4. Stage slot available OR Baton Touch
                
                if card_id not in self.member_db:
                    # print(f"DEBUG: Hand[{i}] is not a member card ({card_id})")
                    continue
                
                member = self.member_db[card_id]
                
                # Check slots
                for area in range(3):
                    action_id = 1 + i * 3 + area
                    
                    # Rule 9.6.2.1.2.1: Cannot specify an area that received a member THIS turn
                    if self.players[p.player_id].members_played_this_turn[area]:
                         # print(f"DEBUG: Hand[{i}] -> Area {area}: Already played to this slot this turn")
                         continue

                    
                    # Check slot availability / Baton Touch
                    active_cost = member.cost
                    if p.stage[area] >= 0:
                         if p.stage[area] in self.member_db:
                             baton_mem = self.member_db[p.stage[area]]
                             active_cost = max(0, active_cost - baton_mem.cost)
                    
                    if active_cost <= available_energy:
                         mask[action_id] = True
                    else:
                         print(f"DEBUG: Hand[{i}] ({member.name}) -> Area {area}: Cost {active_cost} > Energy {available_energy} (Slots: {p.stage}, EnergyZone: {len(p.energy_zone)}, Tapped: {np.sum(p.tapped_energy[:len(p.energy_zone)])})")
            
            # Can activate abilities of members on stage
            for i, card_id in enumerate(p.stage):
                if card_id >= 0 and card_id in self.member_db and not p.tapped_members[i]:
                    member = self.member_db[card_id]
                    for ab in member.abilities:
                        if ab.trigger == TriggerType.ACTIVATED:
                            # Check costs - simplified: check if energy available if cost is energy
                            can_pay = True
                            for cost in ab.costs:
                                if cost.type == AbilityCostType.ENERGY:
                                    if p.count_untapped_energy() < cost.value:
                                        can_pay = False
                                        break
                            # Check conditions (Rule 11 / Rule 9.6.2.2)
                            conditions_met = True
                            for cond in ab.conditions:
                                if not self._check_condition(p, cond, context={'area': i}):
                                    conditions_met = False
                                    break
                            
                            if can_pay and conditions_met:
                                mask[200 + i] = True
                                break # Currently only support one activated ability per card for selection simplicity
                                
        elif self.phase == Phase.LIVE_SET:
            # Can set up to 3 LIVE cards from hand face-down
            mask[0] = True  # Done setting cards
            if len(p.live_zone) < 3:
                for i, card_id in enumerate(p.hand):
                    # Only allow Live cards to be set (not Members)
                    if card_id in self.live_db:
                        mask[64 + i] = True
                    
        elif self.phase in (Phase.PERFORMANCE_P1, Phase.PERFORMANCE_P2):
            # During performance, mostly automatic but may have ability choices
            mask[0] = True  # Continue/confirm
            
        else:
            # Other phases are automatic
            mask[0] = True
            
        return mask
    
    def step(self, action_id: int) -> 'GameState':
        """
        Executes one step in the game (Rule 9).
        """
        self.log_rule("Rule 9.5", f"Processing action {action_id} in {self.phase.name} phase.")
        
        # Check rule conditions before acting (Rule 9.5.1 / 10.1.2)
        self._process_rule_checks()
        
        new_state = self.copy()
        
        # Rule 9.5.4.1: Check timing occurs before play timing
        new_state._process_rule_checks()
        
        # Priority: If waiting for a choice (like targeting), handles that action
        if new_state.pending_choices:
            new_state._handle_choice(action_id)
        # Otherwise, if resolving a complex effect stack
        elif new_state.pending_effects:
            new_state._resolve_pending_effect(0) # 0 is dummy action for auto-res
        # Normal action execution
        else:
            new_state._execute_action(action_id)
            
        # After any action, automatically process non-choice effects
        while new_state.pending_effects and not new_state.pending_choices:
            new_state._resolve_pending_effect(0) # 0 is dummy action for auto-res
            
        # Rule 9.5.1: Final check timing after action resolution
        new_state._process_rule_checks()
        
        # Rule 12.1: Infinite Loop Detection
        # Skip for Mulligan phases
        if new_state.phase not in (Phase.MULLIGAN_P1, Phase.MULLIGAN_P2):
            try:
                # Capture key state tuple
                state_tuple = (
                    new_state.phase,
                    new_state.current_player,
                    tuple(sorted(new_state.players[0].hand)),
                    tuple(new_state.players[0].stage),
                    tuple(tuple(x) for x in new_state.players[0].stage_energy),
                    tuple(new_state.players[0].energy_zone),
                    tuple(sorted(new_state.players[1].hand)),
                    tuple(new_state.players[1].stage),
                    tuple(tuple(x) for x in new_state.players[1].stage_energy),
                    tuple(new_state.players[1].energy_zone),
                )
                state_hash = hash(state_tuple)
                new_state.state_history.append(state_hash)
                
                if new_state.state_history.count(state_hash) >= 4:
                     new_state.log_rule("Rule 12.1", "Infinite Loop detected. Draw.")
                     new_state.game_over = True
                     new_state.winner = 2 # Draw
                     new_state.loop_draw = True
            except Exception as e:
                # If hashing fails, just ignore for now to prevent crash
                pass

        return new_state

    def _process_rule_checks(self) -> None:
        """
        Rule 10: Rule Processing.
        Checks game conditions and executes required cleanup automatically.
        """
        # Rule 10.1.2: Check timings loop until no more rules need processing
        rules_applied = True
        while rules_applied:
            rules_applied = False
            
            for p in self.players:
                # Rule 10.2: Refresh
                if not p.main_deck and p.discard:
                    self.log_rule("Rule 10.2", f"Player {p.player_id} Main Deck is empty. Shuffling discard into deck.")
                    p.main_deck = p.discard[:]
                    p.discard = []
                    random.shuffle(p.main_deck)
                    rules_applied = True
                
                # Rule 10.5.1: Illegal Live Card
                # Face-up cards in Live Zone that aren't LiveCards move to discard
                if p.live_zone:
                    corrected_live = []
                    for cid in p.live_zone:
                        if cid not in self.live_db:
                            self.log_rule("Rule 10.5.1", f"Non-live card {cid} removed from Live Zone.")
                            p.discard.append(cid)
                            rules_applied = True
                        else:
                            corrected_live.append(cid)
                    p.live_zone = corrected_live

                # Rule 10.5.2: Illegal Energy
                for cid in p.energy_zone[:]:
                    # cards in energy_zone are usually IDs. 
                    # If we accidentally have a non-card ID here, cleanup.
                    pass

                # Rule 10.5.3: Floating Energy
                for i in range(3):
                    if p.stage[i] < 0 and p.stage_energy[i]:
                        self.log_rule("Rule 10.5.3", f"Floating energy at slot {i} returned to energy deck.")
                        p.energy_deck.extend(p.stage_energy[i])
                        p.stage_energy[i] = []
                        rules_applied = True
                
                # Rule 10.6.1: Illegal Resolution Card
                # Resolution zone should be empty outside of Yell/Direct Effect resolution
                if self.yell_cards and not (self.phase in [Phase.PERFORMANCE_P1, Phase.PERFORMANCE_P2]):
                    self.log_rule("Rule 10.6.1", "Cleaning up illegal cards in Resolution Zone.")
                    for cid in self.yell_cards:
                        self.players[self.active_player_idx].discard.append(cid)
                    self.yell_cards = []
                    rules_applied = True

                # Rule 10.3: Victory Check
                if len(p.success_lives) >= 3 and not self.game_over:
                    self.log_rule("Rule 10.3", f"Player {p.player_id} has 3+ success lives. Game Over.")
                    self.game_over = True
                    self.winner = p.player_id
                    rules_applied = True

    def _resolve_pending_effect(self, action: int) -> None:
        """Resolve top effect from stack"""
        if not self.pending_effects:
            return
            
        effect = self.pending_effects.pop(0)
        p = self.active_player
        
        # Check if effect requires targeting
        if effect.target == TargetType.CARD_HAND:
             self.pending_choices.append(("TARGET_HAND", {"effect": "discard" if effect.effect_type == EffectType.SWAP_CARDS else "select"}))
             return
        elif effect.target == TargetType.MEMBER_SELECT:
             self.pending_choices.append(("TARGET_MEMBER", {"effect": "buff"}))
             return
        
        if effect.effect_type == EffectType.SELECT_MODE:
             # This requires the Ability to have modal_options populated
             # For now, we assume the effect is resolved in context of an ability
             # In a full engine, we might pass the ability object or options directly in the Effect params
             options = effect.params.get('options', [])
             self.pending_choices.append(("SELECT_MODE", {"options": options}))
             return
        elif effect.effect_type == EffectType.COLOR_SELECT:
             self.pending_choices.append(("COLOR_SELECT", {}))
             return

        if effect.effect_type == EffectType.DRAW:
            self._draw_cards(p, effect.value)
            
        elif effect.effect_type == EffectType.TAP_OPPONENT:
            # Target opponent member (Demo: first active member)
            opp = self.inactive_player
            block = False
            for i in range(3):
                if opp.stage[i] >= 0 and not opp.tapped_members[i]:
                     # Check immunity?
                     opp.tapped_members[i] = True
                     print(f"Effect: Tapped opponent member at area {i}")
                     break
                     
        elif effect.effect_type == EffectType.ORDER_DECK:
             # Just shuffle specific card to top/bottom? 
             # Parser says "Move from discard to Top".
             pass # Logic handled in dedicated MOVE_TO_DECK type?
             
        elif effect.effect_type == EffectType.MOVE_TO_DECK:
             pos = effect.params.get('position', 'top')
             # Demo: move top discard to deck
             if p.discard:
                 card = p.discard.pop()
                 if pos == 'top':
                     p.main_deck.insert(0, card)
                 else:
                     p.main_deck.append(card)
                 print(f"Effect: Moved card {card} from Discard to Deck {pos}")

        elif effect.effect_type == EffectType.PLACE_UNDER:
             # Move energy to member (Demo: current member)
             # Logic needs target. Demo: assumes triggering member or just logs.
             if p.energy_zone:
                 card = p.energy_zone.pop()
                 # Find where member is? Assume Area 0 for demo
                 p.stage_energy[0].append(card)
                 print(f"Effect: Placed energy {card} under member")

        elif effect.effect_type == EffectType.MOVE_MEMBER:
              # Rule 11.9: Move Member
              # We trigger a choice for moving.
              self.pending_choices.append(("TARGET_MEMBER_SLOT", {"reason": "position_change", "count": 1}))
              print("Triggered Position Change choice")

        elif effect.effect_type == EffectType.SWAP_ZONE:
             # Success Live <-> Hand
             pass

        elif effect.effect_type == EffectType.ADD_BLADES:
            # Add temp buff - this requires state tracking for buffs
            pass 
        elif effect.effect_type == EffectType.LOOK_DECK:
            # Reveal top N, add to pending choices
            pass
            
        elif effect.effect_type == EffectType.ADD_HEARTS:
             # Implementation for heart buffs
             pass
        
        elif effect.effect_type == EffectType.ADD_TO_HAND:
             # Basic implementation
             if effect.params.get('from') == 'discard' and p.discard:
                  p.hand.append(p.discard.pop())

        elif effect.effect_type == EffectType.FLAVOR_ACTION:
             # For PR-004: "What do you like?"
             if "何が好き？" in effect.params.get('text', ''):
                  self.pending_choices.append(("MODAL", {
                      "text": "何が好き？",
                      "options": ["チョコミント", "あなた", "その他"]
                  }))
    
        # After resolution, check triggers again?
        pass
    
    def _check_condition(self, player: PlayerState, cond: Condition, context: Dict[str, Any] = {}) -> bool:
        """
        Check if a specific condition (Rule 9.6.2.2/Rule 11) is met.
        """
        met = False
        if cond.type == ConditionType.NONE:
            met = True
        elif cond.type == ConditionType.TURN_1:
            met = (self.turn_number == 1)
        elif cond.type == ConditionType.IS_CENTER:
            # Context must provide 'area'
            met = (context.get('area') == 1) # 1 is Center
        elif cond.type == ConditionType.HAS_MEMBER:
            # Check if player stage has specific member
            name = cond.params.get('name')
            area = cond.params.get('area') # 'LEFT_STAGE' etc.
            
            found = False
            for i, cid in enumerate(player.stage):
                if cid >= 0 and cid in self.member_db:
                    m = self.member_db[cid]
                    if name in m.name: # Logic: substring match or exact?
                         # Area check
                         if area == 'CENTER_STAGE' and i != 1: continue
                         if area == 'LEFT_STAGE' and i != 0: continue
                         if area == 'RIGHT_STAGE' and i != 2: continue
                         found = True
                         break
            met = found
        elif cond.type == ConditionType.COUNT_STAGE:
            count = 0
            for cid in player.stage:
                if cid >= 0: count += 1
            met = (count >= cond.params.get('min', 0))
        elif cond.type == ConditionType.LIFE_LEAD:
            my_life = len(player.success_lives)
            opp_life = len(self.players[1 - player.player_id].success_lives)
            met = (my_life > opp_life)
        # TODO: Implement other condition types (HAS_COLOR, etc)
        else:
            met = True # Default lenient for now

        if cond.is_negated:
            return not met
        return met

    def _move_member(self, player: PlayerState, from_idx: int, to_idx: int) -> None:
        """
        Execute Position Change (Rule 11.9).
        - Moves member from from_idx to to_idx.
        - If target has a member, they SWAP (Rule 11.9.2).
        - Energy moves WITH the member (Rule 4.5.5.3).
        """
        if from_idx == to_idx:
            return

        # Swap logic
        # 1. Card IDs
        player.stage[from_idx], player.stage[to_idx] = player.stage[to_idx], player.stage[from_idx]
        
        # 2. Energy (Rule 4.5.5.3)
        player.stage_energy[from_idx], player.stage_energy[to_idx] = player.stage_energy[to_idx], player.stage_energy[from_idx]
        
        # 3. Tapped status (preserves state of the MEMBER, so we swap tapped status too)
        # Rule 4.5.4: Members have orientation. Moving preserves it unless specified.
        player.tapped_members[from_idx], player.tapped_members[to_idx] = player.tapped_members[to_idx], player.tapped_members[from_idx]
        
        self.log_rule("Rule 11.9", f"Position Change: Swapped slot {from_idx} and {to_idx}.")

    def _execute_action(self, action: int) -> None:
        """Internal: execute action on this state (mutates self)"""
        p = self.active_player
        
        # Handle MULLIGAN phases
        if self.phase in (Phase.MULLIGAN_P1, Phase.MULLIGAN_P2):
            if action == 0:
                # Confirm mulligan - execute the mulligan and move to next phase
                print(f"DEBUG: Player {self.current_player} confirming mulligan. Selection: {p.mulligan_selection}")
                self._execute_mulligan()
                print(f"DEBUG: After mulligan. Phase: {self.phase}, Current Player: {self.current_player}, P0 Hand: {len(self.players[0].hand)}, P1 Hand: {len(self.players[1].hand)}")
            elif 181 <= action <= 240:
                # Toggle card for mulligan selection
                card_idx = action - 181
                if card_idx < len(p.hand):
                    if not hasattr(p, 'mulligan_selection'):
                        p.mulligan_selection = set()
                    if card_idx in p.mulligan_selection:
                        p.mulligan_selection.remove(card_idx)
                        print(f"DEBUG: Player {self.current_player} deselected card {card_idx}. Selection: {p.mulligan_selection}")
                    else:
                        p.mulligan_selection.add(card_idx)
                        print(f"DEBUG: Player {self.current_player} selected card {card_idx}. Selection: {p.mulligan_selection}")
            return
        
        if self.phase == Phase.ACTIVE:
            self._do_active_phase()
            
        elif self.phase == Phase.ENERGY:
            self._do_energy_phase()
            
        elif self.phase == Phase.DRAW:
            self._do_draw_phase()
            
        elif self.phase == Phase.MAIN:
            if action == 0:
                # Pass - end main phase
                self._end_main_phase()
            elif 1 <= action <= 180:
                # Play member: action encodes card_index * 3 + area
                adjusted = action - 1
                card_idx = adjusted // 3
                area = adjusted % 3
                self._play_member(card_idx, area)
            elif 200 <= action <= 202:
                # Activate member ability
                area = action - 200
                self._activate_member_ability(area)
                
        elif self.phase == Phase.LIVE_SET:
            if action == 0:
                self._end_live_set()
            elif 64 <= action <= 123:
                card_idx = action - 64
                self._set_live_card(card_idx)
                
        elif self.phase == Phase.PERFORMANCE_P1:
            self._do_performance(0)
            
        elif self.phase == Phase.PERFORMANCE_P2:
            self._do_performance(1)
            
        elif self.phase == Phase.LIVE_RESULT:
            self._do_live_result()
    
    def _activate_member_ability(self, area: int) -> None:
        """Activate an ability of a member on stage"""
        p = self.active_player
        card_id = p.stage[area]
        if card_id < 0 or card_id not in self.member_db:
            return
            
        member = self.member_db[card_id]
        # For now, find first activated ability
        ability = None
        for ab in member.abilities:
            if ab.trigger == TriggerType.ACTIVATED:
                ability = ab
                break
        
        if not ability:
            return
            
        # Apply Condition Checks (Rule 11)
        conditions_met = True
        for cond in ability.conditions:
             if not self._check_condition(p, cond, context={'area': area}):
                 conditions_met = False
                 break
        
        if not conditions_met:
             print(f"Ability of {member.name} failed condition check.")
             return

        # Pay costs (pass area for TAP_SELF/SACRIFICE_SELF)
        if not self._pay_costs(p, ability.costs, source_area=area):
            return
            
        # Add effects to pending stack
        for effect in ability.effects:
            self.pending_effects.append(effect)
            
        print(f"Player {p.player_id} activated ability of {member.name} in Area {area}")
        
    def _pay_costs(self, player: PlayerState, costs: List[Cost], source_area: int = -1) -> bool:
        """Attempt to pay all costs for an ability"""
        # First verify they can all be paid
        can_pay = True
        for cost in costs:
            if cost.type == AbilityCostType.ENERGY:
                if player.count_untapped_energy() < cost.value:
                    can_pay = False
            elif cost.type == AbilityCostType.TAP_SELF:
                if source_area < 0 or player.tapped_members[source_area]:
                    can_pay = False
            elif cost.type == AbilityCostType.SACRIFICE_SELF:
                if source_area < 0:
                     can_pay = False
            
        if not can_pay:
            return False
            
        # Execute payments
        for cost in costs:
            if cost.type == AbilityCostType.ENERGY:
                paid = 0
                for i in range(len(player.energy_zone)):
                    if not player.tapped_energy[i] and paid < cost.value:
                        player.tapped_energy[i] = True
                        paid += 1
            elif cost.type == AbilityCostType.TAP_SELF:
                if source_area >= 0:
                    player.tapped_members[source_area] = True
                    
            elif cost.type == AbilityCostType.SACRIFICE_SELF:
                 if source_area >= 0:
                     card_id = player.stage[source_area]
                     player.discard.append(card_id)
                     player.stage[source_area] = -1 # Clear the stage slot
                     
                     # Move energy back to DECK (Rule 10.5.3)
                     for e in player.stage_energy[source_area]:
                        player.energy_deck.append(e)
                     player.stage_energy[source_area] = [] # Clear energy under sacrificed member
                     
                     player.tapped_members[source_area] = False # Reset state
                    
        return True

    def _handle_choice(self, action: int) -> None:
        """Handle target selection from pending choices"""
        if not self.pending_choices:
            return
            
        choice_type, params = self.pending_choices.pop(0)
        p = self.active_player
        opp = self.inactive_player
        
        if choice_type == "TARGET_HAND":
            hand_idx = action - 203
            if 0 <= hand_idx < len(p.hand):
                card_id = p.hand.pop(hand_idx)
                # Apply effect to card_id or move to target zone
                if params.get('effect') == 'discard':
                    p.discard.append(card_id)
                    print(f"Player {p.player_id} discarded card {card_id} from hand")
                    
        elif choice_type == "TARGET_MEMBER" or choice_type == "TARGET_MEMBER_SLOT":
            area = action - 263
            if 0 <= area < 3:
                # Check target valid?
                # params might have 'filter', etc.
                
                # Logic for Position Change (Rule 11.9)
                if params.get('reason') == 'position_change':
                    step = params.get('step', 'source')
                    if step == 'source':
                        # Valid source? Must have member?
                        if p.stage[area] >= 0:
                            # Push next step: Select Destination
                            self.pending_choices.insert(0, ("TARGET_MEMBER_SLOT", {
                                "reason": "position_change", 
                                "step": "dest", 
                                "source": area
                            }))
                            print(f"Position Change: Selected source area {area}")
                        else:
                             # Invalid source, retry?
                             print("Invalid source for move (empty)")
                             self.pending_choices.insert(0, (choice_type, params))
                    elif step == 'dest':
                        source = params.get('source')
                        if source is not None and source != area:
                            self._move_member(p, source, area)
                        else:
                            print("Invalid move (same area or missing source)")
                
                # Logic for Buffs
                elif params.get('effect') == 'buff':
                     # Apply buff to p.stage[area]
                     pass

        elif choice_type == "MODAL":
            option_idx = action - 270
            options = params.get('options', [])
            if 0 <= option_idx < len(options):
                choice = options[option_idx]
                print(f"Modal Choice: {choice}")
                
                if choice == "チョコミント":
                     # Both players discard 1
                     self.pending_choices.insert(0, ("TARGET_HAND", {"effect": "discard", "player": "active"}))
                     # We need a way to target opponent in pending choices too.
                     # Simplified: for now just process active player discard.
                     # In full game, would add TARGET_HAND for both.
                     pass
                elif choice == "あなた":
                     # Both draw 1
                     self._draw_cards(p, 1)
                     self._draw_cards(opp, 1)
                     print("Effect: Both players draw 1 card")
                elif choice == "その他":
                     # Both get Blade
                     # Implementation for temporary blades
                     pass

        elif choice_type == "SELECT_MODE":
            option_idx = action - 270
            options = params.get('options', []) # List of List[Effect]
            if 0 <= option_idx < len(options):
                chosen_effects = options[option_idx]
                # Push chosen effects to the front of the stack
                for effect in reversed(chosen_effects):
                    self.pending_effects.insert(0, effect)
                print(f"Selected Mode {option_idx} with {len(chosen_effects)} effects.")

        elif choice_type == "COLOR_SELECT":
            color_idx = action - 280
            colors = ["赤", "青", "緑", "黄", "紫", "ピンク"]
            if 0 <= color_idx < len(colors):
                color = colors[color_idx]
                print(f"Player {p.player_id} selected color: {color}")
                # For basic implementation, we store this in metadata or applies immediately
                # Example: PR-003 might need to store this color for the turn.
                pass
    
    def _do_active_phase(self) -> None:
        p = self.active_player
        self.log_rule("Rule 7.1", f"Active Phase: Untapping all members and energy for Player {p.player_id}.")
        p.members_played_this_turn[:] = False
        p.untap_all()
        self.phase = Phase.ENERGY
    
    def _do_energy_phase(self) -> None:
        p = self.active_player
        self.log_rule("Rule 7.2", f"Energy Phase: Player {p.player_id} moves 1 card from Energy Deck to Energy Zone.")
        if p.energy_deck:
            p.energy_zone.append(p.energy_deck.pop(0))
        self.phase = Phase.DRAW
    
    def _do_draw_phase(self) -> None:
        p = self.active_player
        self.log_rule("Rule 7.4", f"Draw Phase: Player {p.player_id} draws 1 card.")
        self._draw_cards(p, 1)
        self.phase = Phase.MAIN
    
    def _execute_mulligan(self) -> None:
        """Execute mulligan for current player: return selected cards, draw new ones, shuffle"""
        p = self.active_player
        
        if p.mulligan_selection:
            # Get cards to return (in reverse order to preserve indices)
            cards_to_return = []
            indices = sorted(p.mulligan_selection, reverse=True)
            for idx in indices:
                if idx < len(p.hand):
                    cards_to_return.append(p.hand.pop(idx))
            
            # Draw same number of replacement cards
            for _ in range(len(cards_to_return)):
                if p.main_deck:
                    p.hand.append(p.main_deck.pop(0))
            
            # Shuffle returned cards back into deck
            p.main_deck.extend(cards_to_return)
            np.random.shuffle(p.main_deck)
            
        # Clear selection
        p.mulligan_selection = set()
        
        # Transition to next phase
        if self.phase == Phase.MULLIGAN_P1:
            self.current_player = 1 - self.first_player
            self.phase = Phase.MULLIGAN_P2
        else:  # MULLIGAN_P2
            # Both mulligans done, start the actual game
            self.current_player = self.first_player
            self.phase = Phase.ACTIVE
    
    def _draw_cards(self, player: PlayerState, count: int) -> None:
        """Draw cards. Rule 10.2 (Refresh) is handled by _process_rule_checks."""
        for _ in range(count):
            self._process_rule_checks() # Ensure deck is ready
            if player.main_deck:
                player.hand.append(player.main_deck.pop(0))
            self._process_rule_checks() # Cleanup after change
    
    def _play_member(self, hand_idx: int, area_idx: int) -> None:
        p = self.active_player
        card_id = p.hand.pop(hand_idx)
        card = self.member_db[card_id]
        
        # Rule 9.6.2.1.2.1: Slot Cooldown check is in get_legal_actions, 
        # but we log the success here.
        self.log_rule("Rule 9.6.2", f"Player {p.player_id} plays {card.name} from hand to slot {area_idx}.")
        
        # Determine cost (Rule 9.6.2.1.1.2 - Baton Touch cost reduction)
        cost = card.cost
        is_baton = False
        if p.stage[area_idx] >= 0:
            prev_card = self.member_db[p.stage[area_idx]]
            cost = max(0, cost - prev_card.cost)
            is_baton = True
            self.log_rule("Rule 9.6.2.1.1.2", f"Baton Touch applied. Cost reduced from {card.cost} to {cost} by {prev_card.name}.")
            # Discard previous member
            p.discard.append(p.stage[area_idx])
            
            # Rule 4.5.5.4: When member leaves stage, energy under it goes to Energy Deck
            if p.stage_energy[area_idx]:
                 self.log_rule("Rule 4.5.5.4", f"Energy cards under {prev_card.name} returned to Energy Deck.")
                 p.energy_deck.extend(p.stage_energy[area_idx])
                 p.stage_energy[area_idx] = []
        
        # Pay cost (Rule 9.4)
        untapped = [i for i, tapped in enumerate(p.tapped_energy) if not tapped]
        for i in range(cost):
            p.tapped_energy[untapped[i]] = True
        
        # Move to stage
        p.stage[area_idx] = card_id
        p.members_played_this_turn[area_idx] = True
        
        # Check ON_PLAY triggers
        for ability in card.abilities: # Changed member to card here
            if ability.trigger == TriggerType.ON_PLAY:
                # Add effects to pending
                for effect in ability.effects:
                    self.pending_effects.append(effect)
    
    def _end_main_phase(self) -> None:
        """End main phase, enter live set phase"""
        print(f"DEBUG _end_main_phase: Current Player={self.current_player}, First Player={self.first_player}, Current Phase={self.phase}")
    
        # Switch to other player's main phase if this was first player
        if self.current_player == self.first_player:
            p2 = 1 - self.first_player
            print(f"DEBUG _end_main_phase: Switching to Player {p2}'s Main Phase")
            
            # Reset turn-based state for P2
            self.players[p2].tapped_energy[:] = False
            self.players[p2].tapped_members[:] = False
            self.players[p2].members_played_this_turn[:] = False
            
            # Switch player BEFORE executing phases
            self.current_player = p2
            
            # Transitions for P2: ACTIVE -> ENERGY -> DRAW -> MAIN
            self.phase = Phase.ACTIVE
            self._do_active_phase()
            self.phase = Phase.ENERGY
            self._do_energy_phase()
            self.phase = Phase.DRAW
            self._do_draw_phase()
            
            # Finally land in MAIN phase for P2
            self.phase = Phase.MAIN
        else:
            # Both players done with main, enter live set
            print("DEBUG _end_main_phase: Both players done. Transitioning to LIVE_SET")
            self.phase = Phase.LIVE_SET
            self.current_player = self.first_player
    
    def _set_live_card(self, hand_idx: int) -> None:
        """Set a card face-down in live zone"""
        p = self.active_player
        if hand_idx < 0 or hand_idx >= len(p.hand) or len(p.live_zone) >= 3:
            return
        card_id = p.hand.pop(hand_idx)
        p.live_zone.append(card_id)
        # Draw replacement
        self._draw_cards(p, 1)
    
    def _end_live_set(self) -> None:
        """End live card setting for current player"""
        if self.current_player == self.first_player:
            self.current_player = 1 - self.first_player
        else:
            self.phase = Phase.PERFORMANCE_P1
            self.current_player = self.first_player
    
    def _do_performance(self, player_idx: int) -> None:
        """Execute performance phase for a player"""
        p = self.players[player_idx]
        p.live_zone_revealed = True
        
        # Filter for live cards only
        valid_lives = []
        for card_id in p.live_zone:
            if card_id in self.live_db:
                valid_lives.append(card_id)
            else:
                p.discard.append(card_id)
        p.live_zone = valid_lives

        # Trigger ON_LIVE_START abilities of the live cards
        for card_id in p.live_zone:
            live = self.live_db[card_id]
            for ab in live.abilities:
                if ab.trigger == TriggerType.ON_LIVE_START:
                    for effect in ab.effects:
                        self.pending_effects.append(effect)
        
        # Trigger ON_LIVE_START abilities of members on stage (untapped)
        for i, card_id in enumerate(p.stage):
            if card_id >= 0 and not p.tapped_members[i] and card_id in self.member_db:
                member = self.member_db[card_id]
                for ab in member.abilities:
                    if ab.trigger == TriggerType.ON_LIVE_START:
                        for effect in ab.effects:
                            self.pending_effects.append(effect)
        
        if not p.live_zone:
            # No live cards, skip to next
            self._advance_performance()
            return
        
        # Yell: draw cards equal to total blades
        total_blades = p.get_total_blades(self.member_db)
        print(f"DEBUG: Player {player_idx} is yelling! Total blades: {total_blades}")
        self.yell_cards = []
        for _ in range(total_blades):
            if not p.main_deck:
                if p.discard:
                    self.log_rule("Rule 10.2", f"Player {player_idx}'s deck is empty, refreshing from discard.")
                    np.random.shuffle(p.discard)
                    p.main_deck = p.discard
                    p.discard = []
            if p.main_deck:
                card = p.main_deck.pop(0)
                self.yell_cards.append(card)
        
        self.log_rule("Rule 8.3.11", f"Yell Phase: Player {player_idx} reveals {len(self.yell_cards)} cards.")
        
        # Count icons for yell bonus (Rule 8.3.12 and Rule 8.4.2)
        draw_bonus = 0
        yell_score_bonus = 0
        for card_id in self.yell_cards:
            # Check both Member and Live DBs
            card = self.member_db.get(card_id) or self.live_db.get(card_id)
            if card:
                if hasattr(card, 'total_blade_hearts'):
                    draw_bonus += card.total_blade_hearts()
                draw_bonus += card.draw_icons
                yell_score_bonus += card.volume_icons
                
        self.log_rule("Rule 8.3.12.1", f"Yell Draw Bonus: +{draw_bonus} cards.")
        self._draw_cards(p, draw_bonus)
        
        # Calculate total hearts
        total_hearts = p.get_total_hearts(self.member_db).copy()
        self.log_rule("Rule 8.3.13", f"Hearts from stage: {total_hearts}.")
        
        # Add blade hearts from yell cards
        for card_id in self.yell_cards:
            if card_id in self.member_db:
                total_hearts += self.member_db[card_id].blade_hearts
        
        self.log_rule("Rule 8.3.14", f"Total Hearts (Stage + Yell): {total_hearts}.")
        
        # Rule 8.3.15: Check if requirements met for each live card
        remaining_hearts = total_hearts.copy()
        temp_passed = []
        all_passed = True
        
        for live_id in p.live_zone:
            if live_id not in self.live_db:
                continue # Safety
            live = self.live_db[live_id]
            
            if self._check_hearts_meet_requirement(remaining_hearts, live.required_hearts):
                self._consume_hearts(remaining_hearts, live.required_hearts)
                temp_passed.append(live_id)
                self.log_rule("Rule 8.3.15.1", f"Live card {live.name} passed heart check. Remaining hearts: {remaining_hearts}.")
            else:
                all_passed = False
                self.log_rule("Rule 8.3.15.2", f"Live card {live.name} failed heart check. Required: {live.required_hearts}, Available: {remaining_hearts}.")
                break
        
        # Rule 8.3.16: All or Nothing
        if all_passed:
            p.passed_lives = temp_passed
            self.log_rule("Rule 8.3.16.1", f"Player {player_idx} cleared all {len(temp_passed)} live cards.")
        else:
            # All go to discard
            self.log_rule("Rule 8.3.16.2", f"Player {player_idx} failed a heart requirement. All live cards discarded.")
            for live_id in p.live_zone:
                p.discard.append(live_id)
            p.passed_lives = []
        
        # Clear live zone as cards are now in passed_lives or discard
        p.live_zone = []

        # Rule 8.3.17: Apply Yell Score Bonus
        p.live_score_bonus = yell_score_bonus
        self.log_rule("Rule 8.3.17", f"Player {player_idx} Live Score Bonus (Yell): +{yell_score_bonus}.")
        
        # Rule 8.3.18: Move yell cards to discard
        for card_id in self.yell_cards:
            p.discard.append(card_id)
        self.yell_cards = []
        self.log_rule("Rule 8.3.18", f"Yell cards moved to discard pile.")
        
        # Rule 8.3.19: Members that performed now enter "Wait" state (Tapped)
        p.tapped_members[:] = True
        self.log_rule("Rule 8.3.19", f"Player {player_idx}'s members are now in Wait state (tapped).")
        
        self._advance_performance()
    
    def _check_hearts_meet_requirement(self, have: np.ndarray, need: np.ndarray) -> bool:
        """Check if hearts meet live card requirements"""
        # need[0:6] are color requirements, need[6] is "any" requirement
        remaining = have.copy()
        total_needed = 0
        
        # First satisfy color requirements
        for i in range(6):
            if need[i] > remaining[i]:
                return False
            remaining[i] -= need[i]
            total_needed += need[i]
        
        # "Any" requirement can be satisfied by remaining hearts
        total_needed += need[6] if len(need) > 6 else 0
        if np.sum(have) < total_needed:
            return False
            
        return True
    
    def _consume_hearts(self, have: np.ndarray, need: np.ndarray) -> None:
        """Destructively consume hearts from 'have' based on 'need'"""
        # 1. Colors
        for i in range(6):
            if need[i] > 0:
                have[i] -= need[i]
        
        # 2. 'Any' requirement (index 6, if exists)
        if len(need) > 6 and need[6] > 0:
            any_needed = need[6]
            # Naive consumption strategy: consume from first available colors
            # In a real solver we might want to save specific colors for next card, 
            # but standard Love Live rules usually verify total capacity.
            # However, since we process cards efficiently, just taking from first available is defined behavior?
            # Actually, players usually choose. But for auto-logic, greedy is fine for now.
            for i in range(6):
                if any_needed <= 0:
                    break
                if have[i] > 0:
                    take = min(have[i], any_needed)
                    have[i] -= take
                    any_needed -= take
    
    def _advance_performance(self) -> None:
        """Move to next performance phase or result"""
        if self.phase == Phase.PERFORMANCE_P1:
            self.phase = Phase.PERFORMANCE_P2
            self.current_player = 1 - self.first_player
        else:
            self.phase = Phase.LIVE_RESULT
    
    def _do_live_result(self) -> None:
        """Determine live winner and handle success (Rule 8.4)"""
        self.log_rule("Rule 8.4", "Live Winner Determination Phase starts.")
        p0 = self.players[0]
        p1 = self.players[1]
        
        # Rule 8.4.2: Calculate scores (Base Success + Yell Bonus)
        p0_base = sum(self.live_db[c].score for c in p0.passed_lives if c in self.live_db)
        p1_base = sum(self.live_db[c].score for c in p1.passed_lives if c in self.live_db)
        
        p0_total = p0_base + p0.live_score_bonus
        p1_total = p1_base + p1.live_score_bonus
        
        self.log_rule("Rule 8.4.2", f"Score Calculation: P0={p0_total} ({p0_base}+{p0.live_score_bonus}), P1={p1_total} ({p1_base}+{p1.live_score_bonus})")
        
        # Rule 8.4.6: Determine Winner(s)
        winners = []
        if p0_total > 0 or p1_total > 0:
            if p0_total > p1_total: winners = [0]
            elif p1_total > p0_total: winners = [1]
            else: winners = [0, 1]
        
        if not winners:
            self.log_rule("Rule 8.4.6.1", "No winners (both scores 0 or no cards).")
        else:
            self.log_rule("Rule 8.4.6.2", f"Winner(s): {' and '.join(['P'+str(w) for w in winners])}")
            
        # Rule 8.4.7: Winner(s) choose 1 card to Successful Zone
        # (AI logic: pick highest scoring card)
        for w_idx in winners:
            p = self.players[w_idx]
            if p.passed_lives:
                best_cid = max(p.passed_lives, key=lambda c: self.live_db[c].score if c in self.live_db else 0)
                p.success_lives.append(best_cid)
                p.passed_lives.remove(best_cid)
                self.log_rule("Rule 8.4.7", f"Player {w_idx} moves {self.live_db[best_cid].name} to Success Zone.")
        
        # Rule 8.4.8: Remainder to Discard
        for p in self.players:
            if p.passed_lives:
                self.log_rule("Rule 8.4.8", f"Discarding {len(p.passed_lives)} extra success cards for P{p.player_id}.")
                p.discard.extend(p.passed_lives)
                p.passed_lives = []
            p.live_score_bonus = 0
            
        # Rule 8.4.13: First Player Update
        old_first = self.first_player
        if len(winners) == 1:
            self.first_player = winners[0]
            if self.first_player != old_first:
                self.log_rule("Rule 8.4.13", f"Player {winners[0]} is now First Player.")
        
        # Phase Advancement
        self.log_rule("Rule 8.4.14", f"Turn {self.turn_number} finished.")
        self.turn_number += 1
        self.current_player = self.first_player
        self.phase = Phase.ACTIVE
        
        # Discard remaining live cards (from live_zone, not passed_lives)
        for p in self.players:
            for card_id in p.live_zone: # This should be empty if logic is correct, but for safety
                p.discard.append(card_id)
            p.live_zone = []
            p.live_zone_revealed = False
        
        # Check win condition
        self.check_win_condition()
        
        # Next turn
        if not self.game_over:
            self.turn_number += 1
            # Winner of live becomes first player
            self.current_player = self.first_player
            self.phase = Phase.ACTIVE
    
    def _live_success(self, player_idx: int) -> None:
        """Handle a successful live for player"""
        p = self.players[player_idx]
        if p.live_zone:
            # Move one live card to success pile (player can choose - take first for simplicity)
            card = p.live_zone.pop(0)
            p.success_lives.append(card)
            # Winner becomes first player next turn
            self.first_player = player_idx
    
    def get_observation(self) -> np.ndarray:
        """
        Return observation tensor for neural network.
        
        Shape: (channels, height, width) suitable for CNN
        Encodes:
        - Hand cards
        - Stage members
        - Live zone
        - Energy
        - Success piles
        - Game state (phase, turn, etc.)
        
        For simplicity, returns a flattened feature vector.
        A full implementation would use proper spatial encoding.
        """
        features = []
        
        for p_idx in range(2):
            p = self.players[p_idx]
            # Relative to current player
            is_current = 1.0 if p_idx == self.current_player else 0.0
            features.append(is_current)
            
            # Hand size (normalized)
            features.append(len(p.hand) / 20.0)
            
            # Deck size
            features.append(len(p.main_deck) / 60.0)
            
            # Energy count
            features.append(len(p.energy_zone) / 12.0)
            features.append(p.count_untapped_energy() / 12.0)
            
            # Success lives
            features.append(len(p.success_lives) / 3.0)
            
            # Stage - encode each area
            for area in range(3):
                has_member = 1.0 if p.stage[area] >= 0 else 0.0
                features.append(has_member)
                if p.stage[area] >= 0 and p.stage[area] in self.member_db:
                    m = self.member_db[p.stage[area]]
                    features.append(m.cost / 15.0)
                    features.append(m.blades / 6.0)
                    features.append(m.total_hearts() / 10.0)
                else:
                    features.extend([0.0, 0.0, 0.0])
        
        # Phase encoding (one-hot)
        for phase in Phase:
            features.append(1.0 if self.phase == phase else 0.0)
        
        # Turn number
        features.append(min(self.turn_number / 20.0, 1.0))
        
        return np.array(features, dtype=np.float32)
    
    def get_reward(self, player_idx: int) -> float:
        """Get reward for player (1 for win, -1 for loss, 0 otherwise)"""
        if not self.game_over:
            return 0.0
        if self.winner == 2:
            return 0.0  # Draw
        return 1.0 if self.winner == player_idx else -1.0


def create_sample_cards() -> Tuple[Dict[int, MemberCard], Dict[int, LiveCard]]:
    """Create sample cards for testing"""
    members = {}
    lives = {}
    
    # Create 48 sample members with varying stats
    for i in range(48):
        cost = 2 + (i % 14)  # Costs 2-15
        blades = 1 + (i % 6)  # Blades 1-6
        hearts = np.zeros(6, dtype=np.int32)
        hearts[i % 6] = 1 + (i // 6 % 3)  # 1-3 hearts of one color
        if i >= 24:
            hearts[(i + 1) % 6] = 1  # Second color for higher cost cards
        
        blade_hearts = np.zeros(6, dtype=np.int32)
        if i % 3 == 0:
            blade_hearts[i % 6] = 1
            
        members[i] = MemberCard(
            card_id=i,
            name=f"Member_{i}",
            cost=cost,
            hearts=hearts,
            blade_hearts=blade_hearts,
            blades=blades
        )
    
    # Create 12 sample live cards
    for i in range(12):
        score = 1 + (i % 3)  # Score 1-3
        required = np.zeros(7, dtype=np.int32)
        required[i % 6] = 2 + (i // 6)  # 2-3 of one color required
        required[6] = 1 + (i % 4)  # 1-4 "any" hearts required
        
        lives[100 + i] = LiveCard(
            card_id=100 + i,
            name=f"Live_{i}",
            score=score,
            required_hearts=required
        )
    
    return members, lives


def initialize_game(use_real_data: bool = True) -> GameState:
    """Create initial game state with shuffled decks"""
    
    # Try loading real data
    if use_real_data and not GameState.member_db:
        try:
            try:
                from game.data_loader import CardDataLoader
            except ImportError:
                from data_loader import CardDataLoader
                
            # Assuming path relative to execution or fixed
            loader = CardDataLoader("c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/data/cards.json")
            m, l, _ = loader.load()
            if m:
                GameState.member_db = m
                GameState.live_db = l
                print(f"Loaded {len(m)} members and {len(l)} lives from JSON")
        except Exception as e:
            print(f"Failed to load real data: {e}")
            
    if not GameState.member_db:
        # Fallback to sample
        members, lives = create_sample_cards()
        GameState.member_db = members
        GameState.live_db = lives
    
    
    state = GameState()
    
    for p_idx in range(2):
        p = state.players[p_idx]
        
        # Build decks
        # Build decks from available IDs
        member_ids = list(GameState.member_db.keys())
        live_ids = list(GameState.live_db.keys())
        
        # Filter if too many? For now just take random subset if huge
        if len(member_ids) > 48:
             member_ids = list(np.random.choice(member_ids, 48, replace=False))
        if len(live_ids) > 12:
             live_ids = list(np.random.choice(live_ids, 12, replace=False))
        energy_ids = list(range(200, 212))
        
        np.random.shuffle(member_ids)
        np.random.shuffle(live_ids)
        np.random.shuffle(energy_ids)
        
        p.main_deck = member_ids + live_ids
        np.random.shuffle(p.main_deck)
        p.energy_deck = energy_ids
        
        # Initial draw: 6 cards
        for _ in range(6):
            if p.main_deck:
                p.hand.append(p.main_deck.pop(0))
        
        # Initial energy: 0 (gain 3 at start of turn)
    
    # Set initial phase to Mulligan
    state.phase = Phase.MULLIGAN_P1
    
    # Randomly determine first player
    state.first_player = np.random.randint(2)
    state.current_player = state.first_player
    
    # Rule 6.2.1.7: Both players place top 3 cards of Energy Deck into Energy Zone
    for p in state.players:
        p.energy_zone = []
        for _ in range(3):
            if p.energy_deck:
                p.energy_zone.append(p.energy_deck.pop(0))
    
    return state


if __name__ == "__main__":
    # Test game creation and basic flow
    game = initialize_game()
    print(f"Game initialized. First player: {game.first_player}")
    print(f"P0 hand: {len(game.players[0].hand)} cards")
    print(f"P1 hand: {len(game.players[1].hand)} cards")
    print(f"Phase: {game.phase.name}")
    
    # Run a few random actions
    for step in range(20):
        if game.is_terminal():
            print(f"Game over! Winner: {game.get_winner()}")
            break
            
        legal = game.get_legal_actions()
        legal_indices = np.where(legal)[0]
        
        if len(legal_indices) == 0:
            print("No legal actions!")
            break
            
        action = np.random.choice(legal_indices)
        game = game.step(action)
        print(f"Step {step}: Action {action}, Phase {game.phase.name}, "
              f"Player {game.current_player}, "
              f"P0 lives: {len(game.players[0].success_lives)}, "
              f"P1 lives: {len(game.players[1].success_lives)}")
