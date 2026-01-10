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
# Rule 1: ゲームの概要 (General Overview)
# Rule 2: カードの情報 (Card Information)
# Rule 3: プレイヤーに関する情報 (Player Info)
# Rule 4: 領域 (Zones)

# Rule 1.3: ゲームの大原則 (Fundamental Principles)
# Rule 1.3.1: Card text overrides rules.
# Rule 1.3.2: Impossible actions are simply not performed.
# Rule 1.3.3: "Cannot" effects take priority over "Can" effects.
# Rule 1.3.4: Active player chooses first when multiple choices occur.
# Rule 1.3.5: Numerical selections must be non-negative integers.

import random
from enum import IntEnum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from engine.models.ability import (
    Ability,
    AbilityCostType,
    Condition,
    ConditionType,
    Cost,
    Effect,
    EffectType,
    TargetType,
    TriggerType,
)
from engine.models.card import LiveCard, MemberCard
from engine.models.enums import Group, Unit

# Import Numba utils
# Import Numba utils
try:
    from engine.game.numba_utils import JIT_AVAILABLE, calc_main_phase_masks
except ImportError:
    JIT_AVAILABLE = False

    def calc_main_phase_masks(*args):
        pass


# =============================================================================
# OBJECT POOLING FOR PERFORMANCE
# =============================================================================


class StatePool:
    """
    Object pool for PlayerState and GameState to avoid allocation overhead.
    Thread-local pools for multiprocessing compatibility.
    """

    _player_pool: List["PlayerState"] = []
    _game_pool: List["GameState"] = []
    _max_pool_size: int = 100

    @classmethod
    def get_player_state(cls, player_id: int) -> "PlayerState":
        """Get a PlayerState from the pool or create a new one."""
        if cls._player_pool:
            ps = cls._player_pool.pop()
            ps._reset(player_id)
            return ps
        return PlayerState(player_id)

    @classmethod
    def get_game_state(cls) -> "GameState":
        """Get a GameState from the pool or create a new one."""
        if cls._game_pool:
            gs = cls._game_pool.pop()
            gs._reset()
            return gs
        return GameState()

    @classmethod
    def return_player_state(cls, ps: "PlayerState") -> None:
        """Return a PlayerState to the pool for reuse."""
        if len(cls._player_pool) < cls._max_pool_size:
            cls._player_pool.append(ps)

    @classmethod
    def return_game_state(cls, gs: "GameState") -> None:
        """Return a GameState to the pool for reuse."""
        if len(cls._game_pool) < cls._max_pool_size:
            cls._game_pool.append(gs)


class Phase(IntEnum):
    """Game phases within a turn"""

    SETUP = -2  # Initial setup (deck shuffle, energy placement)
    MULLIGAN_P1 = -1  # First player mulligan
    MULLIGAN_P2 = 0  # Second player mulligan (note: reusing 0 OK if we renumber)
    ACTIVE = 1  # Untap all cards
    ENERGY = 2  # Draw energy
    DRAW = 3  # Draw card
    MAIN = 4  # Play members, use abilities
    LIVE_SET = 5  # Set live cards face-down
    PERFORMANCE_P1 = 6  # First player's performance
    PERFORMANCE_P2 = 7  # Second player's performance
    LIVE_RESULT = 8  # Determine live winner


# Enums and Card Classes moved to engine.models
# Imported above


class PlayerState:
    """State for one player - uses numpy arrays for efficiency (Rule 3)"""

    __slots__ = (
        "player_id",
        "hand",
        "main_deck",
        "energy_deck",
        "discard",
        "energy_zone",
        "success_lives",
        "live_zone",
        "live_zone_revealed",
        "stage",
        "stage_energy",
        "tapped_energy",
        "tapped_members",
        "members_played_this_turn",
        "mulligan_selection",
        "baton_touch_limit",
        "baton_touch_count",
        "negate_next_effect",
        "restrictions",
        "live_score_bonus",
        "passed_lives",
        "cannot_live",
        "used_abilities",
        "continuous_effects",
        "hand_buffer",
        "meta_rules",
    )

    def __init__(self, player_id: int):
        self.player_id = player_id

        # Zones (Rule 4)
        self.hand: List[int] = []  # Rule 4.4 (手札)
        self.main_deck: List[int] = []  # Rule 4.2 (メインデッキ)
        self.energy_deck: List[int] = []  # Rule 4.3 (エネルギーデッキ)
        self.discard: List[int] = []  # Rule 4.7 (控え室)
        self.energy_zone: List[int] = []  # Rule 4.6 (エネルギー置き場)
        self.success_lives: List[int] = []  # Rule 4.10 (成功ライブカード置き場)
        self.live_zone: List[int] = []  # Rule 4.9 (ライブカード置き場)
        self.live_zone_revealed: List[bool] = []

        # Stage - 3 areas, each can have one member
        # -1 means empty, otherwise card_id
        self.stage: np.ndarray = np.full(3, -1, dtype=np.int32)

        # Energy under members (for each area, list of energy card_ids)
        self.stage_energy: List[List[int]] = [[], [], []]

        # Card states
        self.tapped_energy: np.ndarray = np.zeros(100, dtype=bool)  # Which energy are tapped
        self.tapped_members: np.ndarray = np.zeros(3, dtype=bool)  # Which stage areas are tapped

        # Turn tracking
        self.members_played_this_turn: np.ndarray = np.zeros(3, dtype=bool)  # Areas that got new members

        # Mulligan tracking
        self.mulligan_selection: set = set()  # Card indices selected for mulligan

        # New: Baton Touch
        # Rule 9.6.2.3.2: No explicit per-turn limit, only per-area placement limit
        self.baton_touch_limit: int = 99
        self.baton_touch_count: int = 0

        # New: Effect control
        self.negate_next_effect: bool = False
        self.restrictions: set[str] = set()  # "live", "placement", etc.

        # Live Phase Tracking
        self.live_score_bonus: int = 0
        self.passed_lives: List[int] = []  # Cards that cleared the heart check (Rule 8.3.15)

        # Rule 8.3.4.1: Live Restriction
        self.cannot_live: bool = False

        # Rule 11.2: Once per Turn tracking
        self.used_abilities: set[str] = set()  # "cid-ability_idx"

        # Rule 9.9: Continuous Effects tracking
        self.continuous_effects: List[Dict[str, Any]] = []

        # Meta-Rules (e.g., ALL Blade as Any)
        self.meta_rules: set[str] = set()

        # Pre-allocated buffer for JIT
        self.hand_buffer: np.ndarray = np.zeros(100, dtype=np.int32)

    def _reset(self, player_id: int) -> None:
        """Reset state for pool reuse - avoids object allocation."""
        self.player_id = player_id
        self.hand.clear()
        self.main_deck.clear()
        self.energy_deck.clear()
        self.discard.clear()
        self.energy_zone.clear()
        self.success_lives.clear()
        self.live_zone.clear()
        self.live_zone_revealed.clear()
        # Use in-place fill/copyto instead of full() if buffers exist
        if not hasattr(self, "stage"):
            self.stage = np.full(3, -1, dtype=np.int32)
            self.tapped_energy = np.zeros(100, dtype=bool)
            self.tapped_members = np.zeros(3, dtype=bool)
            self.members_played_this_turn = np.zeros(3, dtype=bool)
            self.hand_buffer = np.zeros(100, dtype=np.int32)
        else:
            self.stage.fill(-1)
            self.tapped_energy.fill(False)
            self.tapped_members.fill(False)
            self.members_played_this_turn.fill(False)
            self.hand_buffer.fill(0)
        self.mulligan_selection.clear()
        self.baton_touch_limit = 1
        self.baton_touch_count = 0
        self.negate_next_effect = False
        self.restrictions.clear()
        self.live_score_bonus = 0
        self.passed_lives.clear()
        self.cannot_live = False
        self.used_abilities.clear()
        self.continuous_effects.clear()
        self.meta_rules.clear()

    def copy(self) -> "PlayerState":
        """Optimized copy using object pool"""
        new = StatePool.get_player_state(self.player_id)
        self.copy_to(new)
        return new

    def copy_to(self, new: "PlayerState") -> None:
        """In-place copy to an existing object to avoid allocation"""
        new.hand = list(self.hand)
        new.main_deck = list(self.main_deck)
        new.energy_deck = list(self.energy_deck)
        new.discard = list(self.discard)
        new.energy_zone[:] = self.energy_zone
        new.success_lives[:] = self.success_lives
        new.live_zone[:] = self.live_zone
        new.live_zone_revealed[:] = self.live_zone_revealed

        # Use np.copyto for in-place copy to pooled buffers
        np.copyto(new.stage, self.stage)
        for i, e in enumerate(self.stage_energy):
            new.stage_energy[i] = e[:]
        np.copyto(new.tapped_energy, self.tapped_energy)
        np.copyto(new.tapped_members, self.tapped_members)
        np.copyto(new.members_played_this_turn, self.members_played_this_turn)
        new.mulligan_selection = self.mulligan_selection.copy()
        new.baton_touch_limit = self.baton_touch_limit
        new.baton_touch_count = self.baton_touch_count
        new.negate_next_effect = self.negate_next_effect
        new.restrictions = self.restrictions.copy()
        new.live_score_bonus = self.live_score_bonus
        new.passed_lives[:] = self.passed_lives
        new.cannot_live = self.cannot_live
        new.used_abilities = self.used_abilities.copy()
        new.continuous_effects[:] = [e.copy() for e in self.continuous_effects]

    def untap_all(self) -> None:
        """Rule 7.4: Untap all cards in Energy Zone and Member Area"""
        self.tapped_energy[:] = False
        self.tapped_members[:] = False

    def count_untapped_energy(self) -> int:
        """Count available energy (vectorized)"""
        return int(np.count_nonzero(~self.tapped_energy[: len(self.energy_zone)]))

    def get_effective_blades(self, slot_idx: int, card_db: Dict[int, MemberCard]) -> int:
        """Rule 9.9: 継続効果の処理 (Calculating effective values via Layers)"""
        card_id = self.stage[slot_idx]
        if card_id < 0 or card_id not in card_db:
            return 0
        member = card_db[card_id]
        blades = member.blades

        # 1. Gather all active effects for this slot
        slot_effects = [e["effect"] for e in self.continuous_effects if e.get("target_slot") in (-1, slot_idx)]

        # 2. Add CONSTANT abilities from the member itself (Rule 9.1.1.3)
        for ab in member.abilities:
            if ab.trigger == TriggerType.CONSTANT:
                # Check conditions for constant ability
                if all(self._check_condition_for_constant(ab_cond, slot_idx) for ab_cond in ab.conditions):
                    slot_effects.extend(ab.effects)

        # Layer 4: Set to specific values
        for eff in slot_effects:
            if eff.effect_type == EffectType.SET_BLADES:
                blades = eff.value

        # Layer 5: Additive modifications
        for eff in slot_effects:
            val = eff.value
            if eff.params.get("multiplier"):
                if eff.params.get("per_live"):
                    val *= len(self.success_lives)
                elif eff.params.get("per_energy"):
                    val *= len(self.energy_zone)
                elif eff.params.get("per_member"):
                    val *= np.sum(self.stage >= 0)

            if eff.effect_type == EffectType.ADD_BLADES:
                blades += val
            elif eff.effect_type == EffectType.BUFF_POWER:
                blades += val  # BUFF_POWER adds to blades by default

        return max(0, blades)

    def _check_condition_for_constant(self, cond: Condition, slot_idx: int) -> bool:
        """Helper to check constant ability conditions without a full context object"""
        # Simplified version of _check_condition for internal state lookups
        if cond.type == ConditionType.NONE:
            return True
        # Add specific constant check logic if needed
        return True  # Default lenient

    def get_effective_hearts(self, slot_idx: int, card_db: Dict[int, MemberCard]) -> np.ndarray:
        """Rule 9.9: 継続効果の処理 (Calculating effective values via Layers)
        Returns shape (7,) array: [R, B, G, Y, P, Pi, Any=0]
        """
        card_id = self.stage[slot_idx]
        if card_id < 0 or card_id not in card_db:
            return np.zeros(7, dtype=np.int32)
        member = card_db[card_id]
        # Pad to 7 elements (6 colors + 1 "any" slot, always 0 for members)
        hearts = np.zeros(7, dtype=np.int32)
        # Safety: ensure we only copy 6 color hearts. Log if hearts has unexpected size.
        if len(member.hearts) != 6:
            print(
                f"[BUG] Card {member.name} (ID:{card_id}) has hearts size {len(member.hearts)}, expected 6. Data: {member.hearts}"
            )
        hearts[:6] = member.hearts[:6].copy()

        # 1. Gather all active effects for this slot
        slot_effects = [e["effect"] for e in self.continuous_effects if e.get("target_slot") in (-1, slot_idx)]

        # 2. Add CONSTANT abilities from the member itself
        for ab in member.abilities:
            if ab.trigger == TriggerType.CONSTANT:
                if all(self._check_condition_for_constant(ab_cond, slot_idx) for ab_cond in ab.conditions):
                    slot_effects.extend(ab.effects)

        # Layer 4 (Rule 9.9.1.4): Set to specific values
        for eff in slot_effects:
            if eff.effect_type == EffectType.SET_HEARTS:
                # Ensure effect value is padded to (7,)
                if isinstance(eff.value, np.ndarray):
                    if len(eff.value) == 6:
                        hearts[:6] = eff.value
                    else:
                        hearts = eff.value

        # Layer 5 (Rule 9.9.1.5): Additive/Subtractive modifications
        for eff in slot_effects:
            if eff.effect_type in (EffectType.ADD_HEARTS, EffectType.BUFF_POWER):
                # Buff power usually adds blades, but if it has heart value we add it
                if isinstance(eff.value, np.ndarray):
                    if len(eff.value) == 6:
                        hearts[:6] += eff.value
                    else:
                        hearts += eff.value
                elif isinstance(eff.value, (int, float)) and eff.effect_type == EffectType.ADD_HEARTS:
                    # Some effects might specify a single number for all colors? (Rare)
                    # For now assume value is array for heart effects.
                    pass
        return np.maximum(0, hearts)

    def get_total_blades(self, card_db: Dict[int, MemberCard]) -> int:
        """Sum blades from all untapped members using layers"""
        total = 0
        for i, card_id in enumerate(self.stage):
            if card_id >= 0 and not self.tapped_members[i]:
                total += self.get_effective_blades(i, card_db)
        return total

    def get_total_hearts(self, card_db: Dict[int, MemberCard]) -> np.ndarray:
        """Sum hearts from all untapped members on stage using layers
        Returns shape (7,) array: [R, B, G, Y, P, Pi, Any=0]
        """
        total = np.zeros(7, dtype=np.int32)
        for i, card_id in enumerate(self.stage):
            if card_id >= 0 and not self.tapped_members[i]:
                total += self.get_effective_hearts(i, card_db)
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

    # Numba Acceleration Arrays
    _jit_member_costs: Optional[np.ndarray] = None

    @classmethod
    def _init_jit_arrays(cls):
        """Initialize static arrays for Numba JIT"""
        if not cls.member_db:
            return

        # Find max ID
        max_id = max(max(cls.member_db.keys(), default=0), max(cls.live_db.keys(), default=0))
        # Create cost lookup array (default -1 for non-members)
        costs = np.full(max_id + 1, -1, dtype=np.int32)

        for cid, member in cls.member_db.items():
            costs[cid] = member.cost

        cls._jit_member_costs = costs

    __slots__ = (
        "verbose",
        "players",
        "current_player",
        "first_player",
        "phase",
        "turn_number",
        "game_over",
        "winner",
        "performance_results",
        "yell_cards",
        "pending_effects",
        "pending_choices",
        "rule_log",
        "current_resolving_ability",
        "current_resolving_member",
        "current_resolving_member_id",
        "looked_cards",
        "triggered_abilities",
        "state_history",
        "loop_draw",
    )

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.players = [PlayerState(0), PlayerState(1)]
        self.current_player = 0  # Who is acting now
        self.first_player = 0  # Who goes first this turn
        self.phase = Phase.ACTIVE
        self.turn_number: int = 1
        self.game_over: bool = False
        self.winner: int = -1  # -1 = ongoing, 0/1 = player won, 2 = draw

        # Performance Result Tracking (for UI popup)
        self.performance_results: Dict[int, Any] = {}

        # For yell phase tracking
        self.yell_cards: List[int] = []  # Shared Resolution Zone (Rule 4.14)
        self.pending_effects: List[Effect] = []  # Stack of effects to resolve
        self.pending_choices: List[Tuple[str, Dict[str, Any]]] = []  # (choice_type, params with metadata)
        self.rule_log: List[str] = []  # Real-time rule application log

        # Track currently resolving ability for context
        self.current_resolving_ability: Optional[Ability] = None
        self.current_resolving_member: Optional[str] = None  # Member name
        self.current_resolving_member_id: int = -1  # Member card ID

        # Temporary zone for LOOK_DECK
        self.looked_cards: List[int] = []

        # Rule 9.7: Automatic Abilities
        # List of (player_id, Ability, context) waiting to be played
        self.triggered_abilities: List[Tuple[int, Ability, Dict[str, Any]]] = []

        # Static caches (for performance and accessibility)
        # Should be set from server or data loader

        # Loop Detection (Rule 12.1)
        # Using a simple hash of the serialization for history
        self.state_history: List[int] = []
        self.loop_draw = False

    def log_rule(self, rule_id: str, description: str):
        """Append a rule application entry to the log."""
        # Add Turn and Phase context
        phase_name = self.phase.name if hasattr(self.phase, "name") else str(self.phase)
        entry = f"[Turn {self.turn_number}] [{phase_name}] [{rule_id}] {description}"
        self.rule_log.append(entry)
        # Also print to stdout for server console debugging
        if self.verbose:
            print(f"RULE_LOG: {entry}")

    def _reset(self) -> None:
        """Reset state for pool reuse - avoids object allocation."""
        self.verbose = False
        # Players get reset by PlayerState._reset or replaced
        self.current_player = 0
        self.first_player = 0
        self.phase = Phase.ACTIVE
        self.turn_number = 1
        self.game_over = False
        self.winner = -1
        self.performance_results.clear()
        self.yell_cards.clear()
        self.pending_effects.clear()
        self.pending_choices.clear()
        self.rule_log.clear()
        self.current_resolving_ability = None
        self.current_resolving_member = None
        self.current_resolving_member_id = -1
        self.looked_cards.clear()
        self.triggered_abilities.clear()
        self.state_history.clear()
        self.loop_draw = False

    def copy(self) -> "GameState":
        """Optimized copy using object pool and in-place player copy"""
        new = StatePool.get_game_state()
        self.copy_to(new)
        return new

    def copy_to(self, new: "GameState") -> None:
        """In-place copy to an existing object to avoid allocation"""
        new.verbose = self.verbose
        # Reuse existing PlayerState objects in the pooled GameState
        for i, p in enumerate(self.players):
            p.copy_to(new.players[i])

        new.current_player = self.current_player
        new.first_player = self.first_player
        new.phase = self.phase
        new.turn_number = self.turn_number
        new.game_over = self.game_over
        new.winner = self.winner
        new.yell_cards[:] = self.yell_cards
        new.pending_effects[:] = self.pending_effects
        new.pending_choices[:] = self.pending_choices
        new.rule_log[:] = self.rule_log
        new.current_resolving_ability = self.current_resolving_ability
        new.current_resolving_member = self.current_resolving_member
        new.current_resolving_member_id = self.current_resolving_member_id
        new.looked_cards[:] = self.looked_cards
        new.triggered_abilities[:] = self.triggered_abilities
        new.state_history[:] = self.state_history
        new.loop_draw = self.loop_draw

    def inject_card(self, player_idx: int, card_id: int, zone: str, position: int = -1) -> None:
        """Inject a card into a specific zone for testing purposes."""
        if player_idx < 0 or player_idx >= len(self.players):
            raise ValueError("Invalid player index")

        p = self.players[player_idx]

        if zone == "hand":
            if position == -1:
                p.hand.append(card_id)
            else:
                p.hand.insert(position, card_id)
        elif zone == "energy":
            if position == -1:
                p.energy_zone.append(card_id)
            else:
                p.energy_zone.insert(position, card_id)
        elif zone == "live":
            if position == -1:
                p.live_zone.append(card_id)
                p.live_zone_revealed.append(False)
            else:
                p.live_zone.insert(position, card_id)
                p.live_zone_revealed.insert(position, False)
        elif zone == "stage":
            if position < 0 or position >= 3:
                raise ValueError("Stage position must be 0-2")
            p.stage[position] = card_id
        else:
            raise ValueError(f"Invalid zone: {zone}")

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
            # Rule 1.2.1.1: 成功ライブカード 3枚以上で勝利
            self.game_over = True
            self.winner = 0
        elif p1_lives >= 3:
            # Rule 1.2.1.1: 成功ライブカード 3枚以上で勝利
            self.game_over = True
            self.winner = 1

    def get_legal_actions(self) -> np.ndarray:
        """
        Returns a mask of legal actions (Rule 9.5.4: プレイタイミング).

        Expanded for Complexity:
        200-202: Activate ability of member in Area (LEFT, CENTER, RIGHT)
        300-359: Mulligan toggle
        400-459: Live Set
        500-559: Choose card in hand (index 0-59) for effect target
        560-562: Choose member on stage (Area 0-2) for effect target
        590-599: Choose pending trigger to resolve
        """
        mask = np.zeros(1000, dtype=bool)

        if self.game_over:
            return mask

        p = self.active_player

        # Priority: If there are choices to be made for a pending effect
        if self.pending_choices:
            choice_type, params = self.pending_choices[0]
            if choice_type == "TARGET_HAND":
                # Allow skip for optional costs
                if params.get("is_optional"):
                    mask[0] = True
                if len(p.hand) > 0:
                    for i in range(len(p.hand)):
                        mask[500 + i] = True
                else:
                    mask[0] = True  # No valid targets, allow pass
            elif choice_type == "TARGET_MEMBER" or choice_type == "TARGET_MEMBER_SLOT":
                # 560-562: Selected member on stage
                found = False
                for i in range(3):
                    if p.stage[i] >= 0 or choice_type == "TARGET_MEMBER_SLOT":
                        # Filter: for 'activate', only tapped members are legal
                        if params.get("effect") == "activate" and not p.tapped_members[i]:
                            continue
                        mask[560 + i] = True
                        found = True
                if not found:
                    mask[0] = True  # No valid targets, allow pass
            elif choice_type == "DISCARD_SELECT":
                # 500-559: Select card in hand to discard
                # Allow skip for optional costs
                if params.get("is_optional"):
                    mask[0] = True
                if len(p.hand) > 0:
                    for i in range(len(p.hand)):
                        mask[500 + i] = True
                else:
                    mask[0] = True  # No cards to discard, allow pass
            elif choice_type == "MODAL" or choice_type == "SELECT_MODE":
                # params['options'] is a list of strings or list of lists
                options = params.get("options", [])
                for i in range(len(options)):
                    mask[570 + i] = True
            elif choice_type == "CHOOSE_FORMATION":
                # For now, just a dummy confirm? Or allow re-arranging?
                # Simplified: Action 0 to confirm current formation
                mask[0] = True
            elif choice_type == "COLOR_SELECT":
                # 580: Red, 581: Blue, 582: Green, 583: Yellow, 584: Purple, 585: Pink
                for i in range(6):
                    mask[580 + i] = True
            elif choice_type == "TARGET_OPPONENT_MEMBER":
                # Opponent Stage 0-2 -> Action 600-602
                opp = self.inactive_player
                found = False
                for i in range(3):
                    if opp.stage[i] >= 0:
                        mask[600 + i] = True
                        found = True
                if not found:
                    # If no valid targets but choice exists, softlock prevention:
                    # Ideally we should strictly check before pushing choice, but safe fallback:
                    mask[0] = True  # Pass/Cancel

            elif choice_type == "SELECT_FROM_LIST":
                # 600-659: List selection (up to 60 items)
                cards = params.get("cards", [])
                card_count = min(len(cards), 60)
                if card_count > 0:
                    mask[600 : 600 + card_count] = True
                else:
                    mask[0] = True  # Empty list, allow pass

            elif choice_type == "SELECT_FROM_DISCARD":
                # 660-719: Discard selection (up to 60 items)
                cards = params.get("cards", [])
                card_count = min(len(cards), 60)
                if card_count > 0:
                    mask[660 : 660 + card_count] = True
                else:
                    mask[0] = True  # Empty discard, allow pass

            elif choice_type == "SELECT_FORMATION_SLOT" or choice_type == "SELECT_ORDER":
                # 700-759: Item selection from a list
                cards = params.get("cards", params.get("available_members", []))
                card_count = min(len(cards), 60)
                if card_count > 0:
                    mask[700 : 700 + card_count] = True
                else:
                    mask[0] = True

            elif choice_type == "SELECT_SWAP_SOURCE":
                # 600-659: Reuse list selection range
                cards = params.get("cards", [])
                card_count = min(len(cards), 60)
                if card_count > 0:
                    mask[600 : 600 + card_count] = True
                else:
                    mask[0] = True

            elif choice_type == "SELECT_SWAP_TARGET":
                # 500-559: Target hand range
                if len(p.hand) > 0:
                    for i in range(len(p.hand)):
                        mask[500 + i] = True
                else:
                    mask[0] = True

            elif choice_type == "SELECT_SUCCESS_LIVE":
                # 600-659: Select from passed lives list
                cards = params.get("cards", [])
                card_count = min(len(cards), 60)
                if card_count > 0:
                    mask[600 : 600 + card_count] = True
                else:
                    mask[0] = True

        # MULLIGAN phases: Select cards to return or confirm mulligan
        elif self.phase in (Phase.MULLIGAN_P1, Phase.MULLIGAN_P2):
            mask[0] = True  # Confirm mulligan (done selecting)
            # Actions 300-359: Toggle card for mulligan (card index 0-59)
            for i in range(len(p.hand)):
                mask[300 + i] = True

        # Auto-advance phases: these phases process automatically in 'step' when any valid action is received
        # We allow Action 0 (Pass) to trigger the transition.
        elif self.phase in (
            Phase.ACTIVE,
            Phase.ENERGY,
            Phase.DRAW,
            Phase.PERFORMANCE_P1,
            Phase.PERFORMANCE_P2,
            Phase.LIVE_RESULT,
        ):
            mask[0] = True

        elif self.phase == Phase.MAIN:
            # Can always pass
            mask[0] = True

            # --- SHARED PRE-CALCULATIONS ---
            available_energy = p.count_untapped_energy()
            total_reduction = 0
            for ce in p.continuous_effects:
                if ce["effect"].effect_type == EffectType.REDUCE_COST:
                    total_reduction += ce["effect"].value

            # --- PLAY MEMBERS ---
            if "placement" not in p.restrictions:
                # JIT Optimization Path
                if JIT_AVAILABLE and self._jit_member_costs is not None:
                    # Use pre-allocated hand buffer to avoid reallocation
                    hand_len = len(p.hand)
                    if hand_len > 0:
                        p.hand_buffer[:hand_len] = p.hand

                    calc_main_phase_masks(
                        p.hand_buffer[:hand_len],
                        p.stage,
                        available_energy,
                        total_reduction,
                        True,  # Baton touch is always allowed if slot occupied
                        p.members_played_this_turn,
                        self._jit_member_costs,
                        mask,
                    )
                else:
                    # Python Fallback
                    for i, card_id in enumerate(p.hand):
                        if card_id not in self.member_db:
                            continue

                        member = self.member_db[card_id]

                        for area in range(3):
                            action_id = 1 + i * 3 + area

                            if p.members_played_this_turn[area]:
                                continue

                            active_cost = max(0, member.cost - total_reduction)
                            if p.stage[area] >= 0:
                                if p.stage[area] in self.member_db:
                                    baton_mem = self.member_db[p.stage[area]]
                                    active_cost = max(0, active_cost - baton_mem.cost)

                            if active_cost <= available_energy:
                                mask[action_id] = True

                            # DEBUG: Trace why specific cards fail
                            elif self.verbose and (member.cost >= 10 or card_id == 369):
                                print(
                                    f"DEBUG REJECT: Card {card_id} ({member.name}) Area {area}: Cost {active_cost} > Energy {available_energy}. Limit {p.baton_touch_limit}, Count {p.baton_touch_count}"
                                )

            # --- ACTIVATE ABILITIES ---
            # Uses same available_energy
            for i, card_id in enumerate(p.stage):
                if card_id >= 0 and card_id in self.member_db and not p.tapped_members[i]:
                    member = self.member_db[card_id]
                    for _abi_idx, ab in enumerate(member.abilities):
                        if ab.trigger == TriggerType.ACTIVATED:
                            # Action ID 200-202: Activate ability of member in Area 0-2
                            # Simplified check: Assuming sufficient energy/conditions if untapping is main cost
                            # For full strictness, we'd check ability cost here.
                            # But since ability logic is complex, we rely on JIT/Python check in _execute_action mostly
                            # or just allow it and let it fail if invalid cost?
                            # Standard practice: Check basic costs (tap, energy) if possible.

                            # For now, just mark legal if untaped.
                            mask[200 + i] = True
                            break  # Only one ability activation per member slot

        elif self.phase == Phase.LIVE_SET:
            mask[0] = True
            # Check live restriction (Rule 8.3.4.1 / Cluster 3)
            if "live" not in p.restrictions and len(p.live_zone) < 3:
                for i, card_id in enumerate(p.hand):
                    # Only allow Live cards to be set (not Members)
                    if card_id in self.live_db:
                        mask[400 + i] = True
        else:
            # Other phases are automatic
            mask[0] = True

        # Safety check: Ensure at least one action is legal to prevent softlocks
        if not np.any(mask):
            # Force action 0 (Pass) as legal
            mask[0] = True
            # print(f"WARNING: No legal actions found in phase {self.phase.name}, forcing Pass action")

        return mask

    def step(self, action_id: int) -> "GameState":
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
            new_state._resolve_pending_effect(0)  # 0 is dummy action for auto-res
        # Normal action execution
        else:
            new_state._execute_action(action_id)

        # After any action, automatically process non-choice effects
        while new_state.pending_effects and not new_state.pending_choices:
            new_state._resolve_pending_effect(0)  # 0 is dummy action for auto-res

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

                if new_state.state_history.count(state_hash) >= 20:
                    new_state.log_rule("Rule 12.1", "Infinite Loop detected. Terminating as Draw.")
                    new_state.game_over = True
                    new_state.winner = 2  # Draw
                    new_state.loop_draw = True
            except Exception:
                # If hashing fails, just ignore for now to prevent crash
                pass

        return new_state

    def _process_rule_checks(self) -> None:
        """
        Rule 10: Rule Processing & Check Timing (Rule 9.5.3).
        Checks game conditions and executes required cleanup automatically.
        Also handles Triggered Automatic Abilities.
        """
        looping = True
        while looping:
            looping = False

            # Step 1: Rule Processing (Rule 10)
            rules_applied = True
            while rules_applied:
                rules_applied = False
                for p in self.players:
                    # Update Meta Rules (Continuous Effects from Stage and Live Zone)
                    p.meta_rules.clear()
                    # 1. Members on stage
                    for cid in p.stage:
                        if cid >= 0 and cid in self.member_db:
                            m = self.member_db[cid]
                            for ab in m.abilities:
                                if ab.trigger == TriggerType.CONSTANT:
                                    for eff in ab.effects:
                                        if eff.effect_type == EffectType.META_RULE:
                                            p.meta_rules.add(str(eff.params.get("type", "")))

                    # 2. Cards in Live Zone and Success Lives (Some rules are on Live cards)
                    for zone in [p.live_zone, p.success_lives]:
                        for cid in zone:
                            if cid in self.live_db:
                                l = self.live_db[cid]
                                for ab in l.abilities:
                                    if ab.trigger == TriggerType.CONSTANT:
                                        for eff in ab.effects:
                                            if eff.effect_type == EffectType.META_RULE:
                                                p.meta_rules.add(str(eff.params.get("type", "")))

                    # Rule 10.2: Refresh
                    if not p.main_deck and p.discard:
                        self.log_rule("Rule 10.2", f"Player {p.player_id} Main Deck empty. Shuffling.")
                        p.main_deck = p.discard[:]
                        p.discard = []
                        random.shuffle(p.main_deck)
                        rules_applied = True

                    # Rule 10.5.1: Illegal Live Card
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

                    # Rule 10.5.3: Floating Energy
                    for i in range(3):
                        if p.stage[i] < 0 and p.stage_energy[i]:
                            self.log_rule("Rule 10.5.3", f"Floating energy at slot {i} returned to energy deck.")
                            p.energy_deck.extend(p.stage_energy[i])
                            p.stage_energy[i] = []
                            rules_applied = True

                    # Rule 10.6.1: Illegal Resolution Card
                    if self.yell_cards and self.phase not in [Phase.PERFORMANCE_P1, Phase.PERFORMANCE_P2]:
                        self.log_rule("Rule 10.6.1", "Cleaning up illegal cards in Resolution Zone.")
                        for cid in self.yell_cards:
                            # Use active player for cleanup as default
                            self.players[self.current_player].discard.append(cid)
                        self.yell_cards = []
                        rules_applied = True

                    # Rule 10.3: Victory Check
                    if len(p.success_lives) >= 3 and not self.game_over:
                        self.log_rule("Rule 10.3", f"Player {p.player_id} has 3+ success lives. Game Over.")
                        self.game_over = True

                        # Fix: Check for Draw if other player also won?
                        # Since we iterate sequentially, if P1 wins here, check if P0 already won.
                        # Actually, better to accumulate winners and decide at end of loop?
                        # Or check opponent's lives here.
                        opp = self.players[1 - p.player_id]
                        if len(opp.success_lives) >= 3:
                            self.winner = 2  # Draw
                        else:
                            self.winner = p.player_id

                        rules_applied = True

                if rules_applied:
                    looping = True

            # Step 2: Pick Triggered Ability (Rule 9.5.3.2 / 9.5.3.3)
            # Only pick if not currently waiting for a choice
            # AUTO-RESOLVE: Process ALL triggers automatically in FIFO order
            if self.triggered_abilities and not self.pending_choices:
                p_triggers: List[List[int]] = [[] for _ in range(2)]
                for i, (pid, _ab, _ctx) in enumerate(self.triggered_abilities):
                    p_triggers[pid].append(i)

                # Active player first (Rule 9.5.3.2)
                ap = self.current_player
                if p_triggers[ap]:
                    # Auto-resolve the FIRST trigger for active player
                    idx = p_triggers[ap][0]
                    pid, ab, ctx = self.triggered_abilities.pop(idx)
                    self._play_automatic_ability(pid, ab, ctx)
                    looping = True
                    continue  # Repeat the loop to process next trigger

                # Non-active player next (Rule 9.5.3.3)
                nap = 1 - ap
                if p_triggers[nap]:
                    # Auto-resolve the FIRST trigger for non-active player
                    idx = p_triggers[nap][0]
                    pid, ab, ctx = self.triggered_abilities.pop(idx)
                    self._play_automatic_ability(pid, ab, ctx)
                    looping = True
                    continue

    def _play_automatic_ability(self, player_id: int, ability: Ability, context: Dict[str, Any]) -> None:
        """Execute logic to 'play' an automatic ability (Rule 9.7)"""
        p = self.players[player_id]

        # Check conditions (Rule 11)
        if ability.conditions:
            for cond in ability.conditions:
                if not self._check_condition(p, cond, context):
                    # print(f"Automatic ability of {ability.effects[0].effect_type if ability.effects else 'unknown'} failed condition.")
                    return

        # Pay costs if any (Rule 9.7.3.1.1: Automatic abilities with costs are optional)
        # For now, we assume if they can't pay, it's skipped.
        # In a full UI, we'd ask "Pay cost to trigger?"
        if ability.costs:
            if not self._pay_costs(p, ability.costs):
                return

        # Resolve effects
        self.log_rule("Rule 9.7", f"Player {player_id} resolving automatic ability.")

        # Store ability context for pending_choices creation
        self.current_resolving_ability = ability
        # Try to get member name from context
        area = context.get("area", -1)
        if area >= 0 and p.stage[area] >= 0:
            card_id = p.stage[area]
            if card_id in self.member_db:
                self.current_resolving_member = self.member_db[card_id].name
                self.current_resolving_member_id = card_id

        # We process effects one by one. If an effect triggers a choice, we stop and let step() handle it.
        for effect in ability.effects:
            self.pending_effects.insert(0, effect)

        # Try to resolve non-choice effects immediately
        while self.pending_effects and not self.pending_choices:
            self._resolve_pending_effect(0, context=context)

        # Clear context when done (or when pending choice created)
        if not self.pending_choices:
            self.current_resolving_ability = None
            self.current_resolving_member = None
            self.current_resolving_member_id = -1

    def _resolve_pending_effect(self, action: int, context: Optional[Dict[str, Any]] = None) -> None:
        """Resolve top effect from stack"""
        if not self.pending_effects:
            return

        effect = self.pending_effects.pop(0)
        p = self.active_player
        ctx = context or {}

        self.log_rule("Rule 9.7", f"Resolving effect: {effect.effect_type.name} (Value: {effect.value})")

        # Check if effect requires targeting

        # FIX: Prioritize EffectType checks that might overlap with generic targets
        if p.negate_next_effect:
            p.negate_next_effect = False
            if self.verbose:
                print(f"Effect: Effect {effect.effect_type} negated by current effect mitigation.")
            return

        if effect.effect_type == EffectType.ACTIVATE_MEMBER:
            # Choose a member to untap (or self if target is self)
            if effect.target == TargetType.MEMBER_SELF:
                # If self, context should have it, or it implies active member
                area = ctx.get("area", -1)
                if area >= 0:
                    p.tapped_members[area] = False
                    if self.verbose:
                        print(f"Effect: Player {p.player_id} activated member at area {area} (Self)")
                else:
                    # If generic "activate self" but no context?
                    pass
            else:
                self.pending_choices.append(
                    (
                        "TARGET_MEMBER",
                        {
                            "effect": "activate",
                            "effect_description": "Select a member to untap",
                            "source_ability": self.current_resolving_ability.raw_text
                            if self.current_resolving_ability
                            else "",
                            "source_member": self.current_resolving_member or "Unknown",
                            "is_optional": False,
                        },
                    )
                )
            return

        if effect.target == TargetType.CARD_HAND:
            if len(p.hand) > 0:
                effect_desc = (
                    "Select a card to discard"
                    if effect.effect_type == EffectType.SWAP_CARDS
                    else "Select a card from hand"
                )
                self.pending_choices.append(
                    (
                        "TARGET_HAND",
                        {
                            "effect": "discard" if effect.effect_type == EffectType.SWAP_CARDS else "select",
                            "effect_description": effect_desc,
                            "source_ability": self.current_resolving_ability.raw_text
                            if self.current_resolving_ability
                            else "",
                            "source_member": self.current_resolving_member or "Unknown",
                            "is_optional": False,
                        },
                    )
                )
            else:
                print(f"Effect {effect.effect_type} skipped: No cards in hand to target.")
            return
        elif effect.target == TargetType.MEMBER_SELECT:
            # Check if there are any members on stage
            if any(cid >= 0 for cid in p.stage):
                self.pending_choices.append(
                    (
                        "TARGET_MEMBER",
                        {
                            "effect": "buff",
                            "target_effect": effect,
                            "effect_description": f"Select a member for {effect.effect_type.name}",
                            "source_ability": self.current_resolving_ability.raw_text
                            if self.current_resolving_ability
                            else "",
                            "source_member": self.current_resolving_member or "Unknown",
                            "is_optional": False,
                        },
                    )
                )
            else:
                pass  # print(f"Effect {effect.effect_type} skipped: No members on stage to target.")
            return

        if effect.effect_type == EffectType.SELECT_MODE:
            # This requires the Ability to have modal_options populated
            # For now, we assume the effect is resolved in context of an ability
            # In a full engine, we might pass the ability object or options directly in the Effect params
            options = effect.params.get("options", [])
            self.pending_choices.append(
                (
                    "SELECT_MODE",
                    {
                        "options": options,
                        "effect_description": "Choose one of the following",
                        "source_ability": self.current_resolving_ability.raw_text
                        if self.current_resolving_ability
                        else "",
                        "source_member": self.current_resolving_member or "Unknown",
                        "is_optional": False,
                    },
                )
            )
            return
        elif effect.effect_type == EffectType.COLOR_SELECT:
            self.pending_choices.append(
                (
                    "COLOR_SELECT",
                    {
                        "effect_description": "Select a heart color",
                        "source_ability": self.current_resolving_ability.raw_text
                        if self.current_resolving_ability
                        else "",
                        "source_member": self.current_resolving_member or "Unknown",
                        "is_optional": False,
                    },
                )
            )
            return

        if effect.effect_type == EffectType.REVEAL_CARDS:
            # Rule 5.7: 公開する
            count = effect.value
            source = effect.params.get("from", "deck")
            if source == "deck":
                self.looked_cards = []
                for _ in range(count):
                    if p.main_deck:
                        self.looked_cards.append(p.main_deck.pop(0))
                if self.verbose:
                    print(f"Effect: Player {p.player_id} revealed {len(self.looked_cards)} cards from deck")
            elif source == "hand":
                # Reveal all hand? Or specific?
                pass
            return

        if effect.effect_type == EffectType.CHEER_REVEAL:
            # specialized reveal for Cheer logic
            if p.main_deck:
                card = p.main_deck.pop(0)
                self.looked_cards = [card]
                # Logic for "If it is X, do Y" follows in next effects or conditions
                if self.verbose:
                    print(f"Effect: Cheer reveal: {card}")
            return

        if effect.target == TargetType.MEMBER_NAMED:
            # Rule 11.8: Target member by name
            name = effect.params.get("target_name", "")
            found_slot = -1
            for i, cid in enumerate(p.stage):
                if cid >= 0 and cid in self.member_db:
                    if name in self.member_db[cid].name:
                        found_slot = i
                        break
            if found_slot >= 0:
                ctx = ctx.copy() if ctx else {}
                ctx["area"] = found_slot
                # Convert target type effectively so target_slot logic works
                # but we use a local target variable to avoid mutating the effect object
                target_for_logic = TargetType.MEMBER_SELF
            else:
                if self.verbose:
                    print(f"Named target '{name}' not found on stage.")
                return
        else:
            target_for_logic = effect.target

        if effect.effect_type == EffectType.DRAW:
            self._draw_cards(p, effect.value)

        elif effect.effect_type == EffectType.TAP_OPPONENT:
            opp = self.inactive_player
            if any(cid >= 0 for cid in opp.stage):
                self.pending_choices.append(
                    (
                        "TARGET_OPPONENT_MEMBER",
                        {
                            "effect": "tap",
                            "effect_description": "Select an opponent's member to tap",
                            "source_ability": self.current_resolving_ability.raw_text
                            if self.current_resolving_ability
                            else "",
                            "source_member": self.current_resolving_member or "Unknown",
                            "is_optional": False,
                        },
                    )
                )
            else:
                pass

        elif effect.effect_type == EffectType.MOVE_TO_DECK:
            pos = effect.params.get("position", "top")
            # Demo: move top discard to deck
            if p.discard:
                card = p.discard.pop()
                if pos == "top":
                    p.main_deck.insert(0, card)
                else:
                    p.main_deck.append(card)

        elif effect.effect_type == EffectType.MOVE_MEMBER:
            # Rule 11.9: Move Member
            # We trigger a choice for moving.
            self.pending_choices.append(("TARGET_MEMBER_SLOT", {"reason": "position_change", "count": 1}))
            self.pending_choices.append(("TARGET_MEMBER_SLOT", {"reason": "position_change", "count": 1}))

        elif effect.effect_type == EffectType.SWAP_ZONE:
            # Success Live <-> Hand (Swap 1 card)
            # 1. Select card from Success Live (if any)
            live_cards = p.success_lives
            if not live_cards:
                if self.verbose:
                    print("SWAP_ZONE failed: No success live cards")
                return

            if not p.hand:
                if self.verbose:
                    print("SWAP_ZONE failed: Empty hand")
                return

            # Chain choices: Select from Success Live -> Select from Hand -> Swap
            self.pending_choices.append(("SELECT_SWAP_SOURCE", {"cards": live_cards.copy(), "source": "success_live"}))

        elif effect.effect_type == EffectType.ADD_BLADES:
            # Rule 9.9: 継続効果の登録
            val = effect.value
            if effect.params.get("multiplier"):
                if effect.params.get("per_live"):
                    val *= len(p.success_lives)
                elif effect.params.get("per_energy"):
                    val *= len(p.energy_zone)
                elif effect.params.get("per_member"):
                    val *= int(np.sum(p.stage >= 0))
            p.continuous_effects.append(
                {
                    "effect": Effect(EffectType.ADD_BLADES, val, effect.target, effect.params),
                    "target_slot": ctx.get("area", -1) if target_for_logic == TargetType.MEMBER_SELF else -1,
                    "expiry": effect.params.get("until", "turn_end").upper(),
                }
            )
        elif effect.effect_type == EffectType.LOOK_DECK:
            # Rule 5.7: 山札のカードを上から見る
            count = effect.value
            if len(p.main_deck) < count:
                count = len(p.main_deck)

            # Draw from top (index 0)
            self.looked_cards = []
            for _ in range(count):
                if p.main_deck:
                    self.looked_cards.append(p.main_deck.pop(0))

        elif effect.effect_type == EffectType.LOOK_AND_CHOOSE:
            # Create choice from looked cards
            if self.looked_cards:
                self.pending_choices.append(
                    ("SELECT_FROM_LIST", {"cards": self.looked_cards.copy(), "reason": "look_and_choose"})
                )

        elif effect.effect_type == EffectType.RECOVER_LIVE:
            # Retrieve live card from discard to hand
            live_cards_in_discard = [cid for cid in p.discard if cid in self.live_db]

            # Apply filters
            group_filter = effect.params.get("group")
            if group_filter:
                live_cards_in_discard = [
                    cid for cid in live_cards_in_discard if group_filter in self.live_db[cid].groups
                ]

            if live_cards_in_discard:
                # Create choice to select which live card to recover
                self.pending_choices.append(
                    (
                        "SELECT_FROM_DISCARD",
                        {
                            "cards": live_cards_in_discard,
                            "count": effect.value,
                            "filter": "live",
                            "destination": "hand",
                        },
                    )
                )

        elif effect.effect_type == EffectType.RECOVER_MEMBER:
            # Retrieve member card from discard to hand
            member_cards_in_discard = [cid for cid in p.discard if cid in self.member_db]

            # Apply filters
            group_filter = effect.params.get("group")
            if group_filter:
                target_group = Group.from_japanese_name(group_filter)
                member_cards_in_discard = [
                    cid for cid in member_cards_in_discard if target_group in self.member_db[cid].groups
                ]

            cost_max = effect.params.get("cost_max")
            if cost_max is not None:
                member_cards_in_discard = [
                    cid for cid in member_cards_in_discard if self.member_db[cid].cost <= cost_max
                ]

            if member_cards_in_discard:
                # Create choice to select which member card to recover
                self.pending_choices.append(
                    (
                        "SELECT_FROM_DISCARD",
                        {
                            "cards": member_cards_in_discard,
                            "count": effect.value,
                            "filter": "member",
                            "destination": effect.params.get("to", "hand"),
                        },
                    )
                )

        elif effect.effect_type == EffectType.SWAP_CARDS:
            # Rule 5.8: カードを入れ替える
            # Typically "Draw X, Discard Y" or just "Discard Y"
            # Parser seems to separate Draw and Discard(Swap)
            if effect.params.get("target") == "discard" and effect.params.get("from") in ("hand", None):
                count = effect.value
                # If hand has fewer cards than count? Rule usually implies discard as much as possible or cannot activate?
                # Assuming simple "discard N" choice
                self.pending_choices.append(("DISCARD_SELECT", {"count": count}))

        elif effect.effect_type == EffectType.ADD_HEARTS:
            # Rule 9.9: 継続効果の登録
            val = effect.value
            if effect.params.get("multiplier"):
                if effect.params.get("per_live"):
                    val *= len(p.success_lives)
                elif effect.params.get("per_energy"):
                    val *= len(p.energy_zone)
                elif effect.params.get("per_member"):
                    val *= int(np.sum(p.stage >= 0))
            p.continuous_effects.append(
                {
                    "effect": Effect(EffectType.ADD_HEARTS, val, effect.target, effect.params),
                    "target_slot": ctx.get("area", -1) if target_for_logic == TargetType.MEMBER_SELF else -1,
                    "expiry": effect.params.get("until", "turn_end").upper(),
                }
            )

        elif effect.effect_type == EffectType.BUFF_POWER:
            # Generic buff (often used with multipliers)
            val = effect.value
            if effect.params.get("multiplier"):
                if effect.params.get("per_live"):
                    val *= len(p.success_lives)
                elif effect.params.get("per_energy"):
                    val *= len(p.energy_zone)
                elif effect.params.get("per_member"):
                    val *= int(np.sum(p.stage >= 0))

            p.continuous_effects.append(
                {
                    "effect": Effect(
                        EffectType.ADD_BLADES, val, target_for_logic, effect.params
                    ),  # Treat as blade buff for now
                    "target_slot": ctx.get("area", -1) if target_for_logic == TargetType.MEMBER_SELF else -1,
                    "expiry": effect.params.get("until", "turn_end").upper(),
                }
            )

        elif effect.effect_type == EffectType.BOOST_SCORE:
            # Rule 11.8: スコアの上昇
            # Check for replacement effects (Cluster 4)
            final_val = effect.value
            for ce in p.continuous_effects:
                if (
                    ce["effect"].effect_type == EffectType.REPLACE_EFFECT
                    and ce["effect"].params.get("replaces") == "score_boost"
                ):
                    final_val = ce["effect"].value
                    if self.verbose:
                        print(f"REPLACE: Score boost replaced to {final_val}")
                    break
            p.live_score_bonus += int(final_val)

        elif effect.effect_type == EffectType.REPLACE_EFFECT:
            # Cluster 4: Store replacement effect for later use
            p.continuous_effects.append({"effect": effect, "expiry": effect.params.get("until", "live_end").upper()})

        elif effect.effect_type == EffectType.SET_SCORE:
            # Set absolute score
            p.live_score_bonus = effect.value - 0  # Assuming score is bonus? No, usually it's base score.
            # If this is used, it often overrides the calculated score.
            ctx["set_score_override"] = effect.value

        elif effect.effect_type == EffectType.BATON_TOUCH_MOD:
            p.baton_touch_limit = effect.value
            if self.verbose:
                print(f"Effect: Baton touch limit set to {effect.value}")

        elif effect.effect_type == EffectType.REDUCE_COST:
            # Add continuous effect for cost reduction
            p.continuous_effects.append({"effect": effect, "expiry": effect.params.get("until", "turn_end").upper()})

        elif effect.effect_type == EffectType.REDUCE_HEART_REQ:
            # Rule 8.3.15: Reduce heart requirement for live
            p.continuous_effects.append({"effect": effect, "expiry": effect.params.get("until", "live_end").upper()})

        elif effect.effect_type == EffectType.NEGATE_EFFECT:
            # Target opponent and negate their next effect
            self.inactive_player.negate_next_effect = True
            if self.verbose:
                print(f"Effect: Next effect of Player {self.inactive_player.player_id} will be negated.")

        elif effect.effect_type == EffectType.RESTRICTION:
            res_type = effect.params.get("type")
            if res_type:
                p.restrictions.add(res_type)
                if self.verbose:
                    print(f"Effect: Restriction added: {res_type}")

        elif effect.effect_type == EffectType.IMMUNITY:
            p.restrictions.add("immunity")  # Simple implementation
            if self.verbose:
                print("Effect: Immunity granted.")

        elif effect.effect_type == EffectType.ADD_TO_HAND:
            # Basic implementation
            if effect.params.get("from") == "discard" and p.discard:
                p.hand.append(p.discard.pop())

        elif effect.effect_type == EffectType.TRIGGER_REMOTE:
            # Cluster 5: Remote Ability Triggering
            zone = effect.params.get("from", "discard")
            if zone == "discard":
                # Create choice to select a card from discard
                members_in_discard = [cid for cid in p.discard if cid in self.member_db]
                if members_in_discard:
                    self.pending_choices.append(
                        (
                            "SELECT_FROM_DISCARD",
                            {
                                "cards": members_in_discard,
                                "count": 1,
                                "filter": "member_with_ability",
                                "destination": "trigger_ability",
                            },
                        )
                    )
                    if self.verbose:
                        print("TRIGGER_REMOTE: Select member from discard to trigger ability.")

        elif effect.effect_type == EffectType.ENERGY_CHARGE:
            # Rule 4.10: エネルギー置き場にカードを置く
            source = effect.params.get("from", "deck")
            count = effect.value
            if source == "deck":
                for _ in range(count):
                    if p.main_deck:
                        current_card = p.main_deck.pop(0)
                        p.energy_zone.append(current_card)
                        # tapped_energy is pre-allocated False in __init__ (size 100)
                        p.tapped_energy[len(p.energy_zone) - 1] = False
            elif source == "hand":
                self.pending_choices.append(("TARGET_HAND", {"effect": "energy_charge", "count": count}))
                if self.verbose:
                    print(f"Player {p.player_id} must choose {count} card(s) from hand to charge energy")

        elif effect.effect_type == EffectType.FLAVOR_ACTION:
            # For PR-004: "What do you like?"
            if "何が好き？" in effect.params.get("text", ""):
                self.pending_choices.append(
                    ("MODAL", {"text": "何が好き？", "options": ["チョコミント", "あなた", "その他"]})
                )

            # Rule 11.10: Re-arrange all members
            # We trigger a choice for the new ordering
            self.pending_choices.append(("CHOOSE_FORMATION", {}))

        elif effect.effect_type == EffectType.TAP_OPPONENT:
            # Rule: Tap opponent member(s)
            opp = self.inactive_player
            if effect.params.get("all"):
                for i in range(3):
                    if opp.stage[i] >= 0:
                        opp.tapped_members[i] = True
                if self.verbose:
                    print("Effect: All opponent members tapped.")
            else:
                count = effect.value
                # Create choice for active player to choose opponent member
                # We need a new choice type TARGET_OPPONENT_MEMBER
                # If opponent has no members, skip
                has_member = any(cid >= 0 for cid in opp.stage)
                if has_member:
                    for _ in range(count):
                        self.pending_choices.append(("TARGET_OPPONENT_MEMBER", {"effect": "tap"}))

        elif effect.effect_type == EffectType.ORDER_DECK:
            # Sort or Move to Bottom/Top
            position = effect.params.get("position", "top")
            shuffle = effect.params.get("shuffle", False)
            count = effect.value
            if self.verbose:
                print(f"DEBUG: ORDER_DECK pos={position} shuf={shuffle} cnt={count}")

            # Take top N cards (index 0 is TOP)
            top_cards = []
            for _ in range(min(count, len(p.main_deck))):
                top_cards.append(p.main_deck.pop(0))

            if not top_cards:
                return

            if shuffle:
                # Shuffle and put back
                random.shuffle(top_cards)

                if position == "bottom":
                    # Put at bottom (extend adds to end)
                    p.main_deck.extend(top_cards)
                else:
                    # Put back on top (insert in reverse order to preserve [0, 1, 2] -> 0=Top)
                    for c in reversed(top_cards):
                        p.main_deck.insert(0, c)
            else:
                # Manual Reorder -> Prompt User
                self.pending_choices.append(("SELECT_ORDER", {"cards": top_cards, "ordered": [], "position": position}))

        elif effect.effect_type == EffectType.PLACE_UNDER:
            # "Place under member"
            target_area = ctx.get("area", -1)

            # If target was MEMBER_SELECT, we might need logic to pass that selection here?
            # For now, assume context has area (from MEMBER_SELF or forwarded)

            if effect.params.get("from", "hand") == "hand" and target_area >= 0:
                self.pending_choices.append(
                    ("TARGET_HAND", {"effect": "place_under", "target_area": target_area, "count": effect.value})
                )
            else:
                if self.verbose:
                    print(f"PLACE_UNDER failed: invalid target area {target_area} or source")

        elif effect.effect_type == EffectType.SEARCH_DECK:
            # Rule 5.7: 山札からカードを選ぶ
            group = effect.params.get("group")
            cost_max = effect.params.get("cost_max")

            targets = []
            for cid in p.main_deck:
                if cid in self.member_db:
                    m = self.member_db[cid]
                    if group:
                        target_group = Group.from_japanese_name(group)
                        if target_group not in m.groups:
                            continue
                    if cost_max is not None and m.cost > cost_max:
                        continue
                    targets.append(cid)
                elif cid in self.live_db:
                    l = self.live_db[cid]
                    if group:
                        target_group = Group.from_japanese_name(group)
                        if target_group not in l.groups:
                            continue
                    targets.append(cid)

            if targets:
                self.pending_choices.append(
                    (
                        "SELECT_FROM_LIST",
                        {
                            "cards": targets,
                            "reason": "search_deck",
                            "shuffle": True,  # Standard rule
                        },
                    )
                )
            else:
                # Search failed, but usually we still shuffle?
                # Comprehensive rules 5.7.1: 山札をシャッフルする
                random.shuffle(p.main_deck)
                if self.verbose:
                    print(f"Search failed: No matching cards for {group}. Deck shuffled.")

        elif effect.effect_type == EffectType.FORMATION_CHANGE:
            # Rule 11.10: Re-arrange all members
            members = []
            for i in range(3):
                if p.stage[i] >= 0:
                    members.append((i, p.stage[i]))

            if members:
                self.pending_choices.append(
                    (
                        "SELECT_FORMATION_SLOT",
                        {"slot_index": 0, "available_members": members, "new_stage": [-1, -1, -1]},
                    )
                )
            else:
                if self.verbose:
                    print("No members to rearrange.")

        # After resolution, check triggers again?
        pass

    def _check_condition(self, player: PlayerState, cond: Condition, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if a specific condition (Rule 9.6.2.2/Rule 11) is met.
        """
        if context is None:
            context = {}
        met = False
        if cond.type == ConditionType.NONE:
            met = True
        elif cond.type == ConditionType.TURN_1:
            met = self.turn_number == 1
        elif cond.type == ConditionType.IS_CENTER:
            # Context must provide 'area'
            met = context.get("area") == 1  # 1 is Center
        elif cond.type == ConditionType.HAS_MEMBER:
            # Check if player stage has specific member
            name = cond.params.get("name")
            area = cond.params.get("area")  # 'LEFT_STAGE' etc.

            found = False
            for i, cid in enumerate(player.stage):
                if cid >= 0 and cid in self.member_db:
                    m = self.member_db[cid]
                    if name and name in m.name:  # Logic: substring match or exact?
                        # Area check
                        if area == "CENTER_STAGE" and i != 1:
                            continue
                        if area == "LEFT_STAGE" and i != 0:
                            continue
                        if area == "RIGHT_STAGE" and i != 2:
                            continue
                        found = True
                        break
            met = found
        elif cond.type == ConditionType.COUNT_STAGE:
            count = 0
            for cid in player.stage:
                if cid >= 0:
                    count += 1
            met = count >= cond.params.get("min", 0)
        elif cond.type == ConditionType.LIFE_LEAD:
            my_life = len(player.success_lives)
            opp_life = len(self.players[1 - player.player_id].success_lives)
            met = my_life > opp_life
        elif cond.type in (ConditionType.COUNT_GROUP, ConditionType.GROUP_FILTER):
            # Count members of group in zone
            group_str = cond.params.get("group", "").strip("『』")
            zone = cond.params.get("zone", "STAGE")
            min_count = cond.params.get(
                "count", cond.params.get("min", 1 if cond.type == ConditionType.GROUP_FILTER else 0)
            )

            if not group_str:
                return False

            target_group = Group.from_japanese_name(group_str)
            target_unit = Unit.from_japanese_name(group_str)

            count = 0
            cards_to_check = []
            if cond.params.get("context") == "revealed":
                cards_to_check = self.looked_cards
            elif zone == "STAGE":
                for cid in player.stage:
                    if cid >= 0:
                        cards_to_check.append(cid)
            elif zone == "DISCARD":
                cards_to_check = player.discard
            elif zone == "HAND":
                cards_to_check = player.hand
            elif zone == "DECK":
                cards_to_check = player.main_deck

                cards_to_check = self.looked_cards

            for cid in cards_to_check:
                if cid in self.member_db:
                    m = self.member_db[cid]
                    # Check both group (series) and unit
                    match_group = target_group != Group.OTHER and target_group in m.groups
                    match_unit = target_unit != Unit.OTHER and target_unit in m.units

                    if match_group or match_unit:
                        count += 1
                elif cid in self.live_db:
                    l = self.live_db[cid]
                    match_group = target_group != Group.OTHER and target_group in l.groups
                    match_unit = target_unit != Unit.OTHER and target_unit in l.units
                    if match_group or match_unit:
                        count += 1

            met = count >= min_count
        elif cond.type == ConditionType.HAS_COLOR:
            color = cond.params.get("color")
            # Check if any member has this heart color or if stage has color
            # Simplified: check the combined untap hearts
            active_hearts = player.get_total_hearts(self.member_db)
            color_map = {"赤": 1, "青": 4, "緑": 3, "黄": 2, "紫": 5, "ピンク": 0}
            color = str(cond.params.get("color", ""))
            idx = color_map.get(color)
            if idx is not None:
                met = active_hearts[idx] > 0

        elif cond.type == ConditionType.OPPONENT_HAND_DIFF:
            diff_needed = cond.params.get("diff", 0)
            opp_id = 1 - player.player_id
            opp_hand = len(self.players[opp_id].hand)
            my_hand = len(player.hand)
            met = (opp_hand - my_hand) >= diff_needed
        elif cond.type == ConditionType.COUNT_ENERGY:
            met = len(player.energy_zone) >= cond.params.get("min", 0)
        elif cond.type == ConditionType.HAS_LIVE_CARD:
            met = len(player.live_zone) > 0
        elif cond.type == ConditionType.COUNT_HAND:
            met = len(player.hand) >= cond.params.get("min", 0)
        elif cond.type == ConditionType.COUNT_DISCARD:
            met = len(player.discard) >= cond.params.get("min", 0)
        elif cond.type == ConditionType.SELF_IS_GROUP:
            # Check if self (triggering card) is from group
            # Usually self is looked up from context["card_id"] or context["member_id"]
            cid = context.get("card_id")
            req_group_str = cond.params.get("group", "")
            if not req_group_str:
                met = False
            else:
                target_group_enum = Group.from_japanese_name(req_group_str)
                if cid is not None:
                    if cid in self.member_db:
                        m_card = self.member_db[cid]
                        met = target_group_enum in m_card.groups
                    elif cid in self.live_db:
                        l_card = self.live_db[cid]
                        met = target_group_enum in l_card.groups
                    else:
                        met = False
                else:
                    met = False
        elif cond.type == ConditionType.MODAL_ANSWER:
            met = context.get("answer") == cond.params.get("answer")
        elif cond.type == ConditionType.HAND_HAS_NO_LIVE:
            has_live = any(cid in self.live_db for cid in player.hand)
            met = not has_live
        elif cond.type == ConditionType.COUNT_SUCCESS_LIVE:
            count = len(player.success_lives)
            met = count >= cond.params.get("min", 0)
        elif cond.type == ConditionType.GROUP_FILTER:
            group_str = cond.params.get("group", "")
            if not group_str:
                met = False
            else:
                target_group = Group.from_japanese_name(group_str)
                target_unit = Unit.from_japanese_name(group_str)

                context_cards = []
                if cond.params.get("context") == "revealed":
                    context_cards = self.looked_cards
                else:
                    cid = context.get("card_id")
                    if cid is not None:
                        context_cards = [cid]

                if not context_cards:
                    met = False
                else:
                    match_count = 0
                    for cid in context_cards:
                        if cid in self.member_db:
                            m = self.member_db[cid]
                            match_group = target_group != Group.OTHER and target_group in m.groups
                            match_unit = target_unit != Unit.OTHER and target_unit in m.units
                            if match_group or match_unit:
                                match_count += 1
                        elif cid in self.live_db:
                            l = self.live_db[cid]
                            match_group = target_group != Group.OTHER and target_group in l.groups
                            match_unit = target_unit != Unit.OTHER and target_unit in l.units
                            if match_group or match_unit:
                                match_count += 1

                    met = (match_count == len(context_cards)) if context_cards else False
        elif cond.type == ConditionType.COST_CHECK:
            cid = context.get("card_id")
            if cid is not None and cid in self.member_db:
                val = self.member_db[cid].cost
                target_val = cond.params.get("value", 0)
                comparison = cond.params.get("comparison", "LE")
                if comparison == "LE":
                    met = val <= target_val
                else:
                    met = val >= target_val
        elif cond.type == ConditionType.OPPONENT_HAS:
            opp = self.players[1 - player.player_id]
            # Simple check: does opponent have any member on stage?
            # In a more complex engine, we'd check for specific names/groups in params
            met = any(cid >= 0 for cid in opp.stage)
        # TODO: Implement other condition types (RARITY_CHECK, etc)
        else:
            met = True  # Default lenient for now

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
        player.stage_energy[from_idx], player.stage_energy[to_idx] = (
            player.stage_energy[to_idx],
            player.stage_energy[from_idx],
        )

        # 3. Tapped status (preserves state of the MEMBER, so we swap tapped status too)
        # Rule 4.5.4: Members have orientation. Moving preserves it unless specified.
        player.tapped_members[from_idx], player.tapped_members[to_idx] = (
            player.tapped_members[to_idx],
            player.tapped_members[from_idx],
        )

        self.log_rule("Rule 11.9", f"Position Change: Swapped slot {from_idx} and {to_idx}.")

    def _execute_action(self, action: int) -> None:
        """Internal: execute action on this state (mutates self)"""
        p = self.active_player

        # Handle MULLIGAN phases
        if self.phase in (Phase.MULLIGAN_P1, Phase.MULLIGAN_P2):
            if action == 0:
                # Confirm mulligan - execute the mulligan and move to next phase
                self._execute_mulligan()
            elif 300 <= action <= 359:
                # Toggle card for mulligan selection
                card_idx = action - 300
                if card_idx < len(p.hand):
                    if not hasattr(p, "mulligan_selection"):
                        p.mulligan_selection = set()
                    if card_idx in p.mulligan_selection:
                        p.mulligan_selection.remove(card_idx)
                    else:
                        p.mulligan_selection.add(card_idx)
            return

        # Handle Pending Choices (Prioritize over Phase logic)
        # Actions 500+ are generally reserved for choices
        if self.pending_choices:
            # Handle Optional Skip (Action 0)
            if action == 0:
                choice_type, params = self.pending_choices[0]
                if params.get("is_optional"):
                    if self.verbose:
                        print("Player chose to skip optional action.")
                    # Clear this choice
                    self.pending_choices.pop(0)
                    # If this was a cost for an ability, we might need to cancel the ability?
                    # If pending_effects are queued, clear them?
                    # Rule: cancelling cost cancels execution.
                    if params.get("reason") == "cost":
                        if self.verbose:
                            print("Optional cost skipped -> Cancelling pending effects.")
                        self.pending_effects.clear()
                        # Also clear any remaining choices (e.g. if cost was discard 2 and we skipped 1st)
                        self.pending_choices.clear()
                    return

            if action >= 500:
                self._handle_choice(action)
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
            elif 400 <= action <= 459:
                card_idx = action - 400
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
        ability = None
        # Rule 11.2: Once per Turn
        for abi_idx, ab in enumerate(member.abilities):
            if ab.trigger == TriggerType.ACTIVATED:
                abi_key = f"{card_id}-{abi_idx}"
                if ab.is_once_per_turn and abi_key in p.used_abilities:
                    continue
                ability = ab
                ability_idx = abi_idx
                break

        if not ability:
            if self.verbose:
                print(f"No usable activated ability found for {member.name} (maybe already used?)")
            return

        # Apply Condition Checks (Rule 11)
        conditions_met = True
        for cond in ability.conditions:
            if not self._check_condition(p, cond, context={"area": area}):
                conditions_met = False
                break

        if not conditions_met:
            if self.verbose:
                print(f"Ability of {member.name} failed condition check.")
            return

        # Pay costs (pass area for TAP_SELF/SACRIFICE_SELF)
        if not self._pay_costs(p, ability.costs, source_area=area):
            return

        # Add effects to pending stack
        for effect in ability.effects:
            self.pending_effects.append(effect)

        # Mark as used (Rule 11.2)
        if ability.is_once_per_turn:
            p.used_abilities.add(f"{card_id}-{ability_idx}")

        self.log_rule(
            "Rule 11.3", f"Player {p.player_id} activates ability of {member.name}: {ability.raw_text[:60]}..."
        )

        # Resolve effects immediately (Rule 9.7 logic applied to Manual Activation)
        while self.pending_effects and not self.pending_choices:
            self._resolve_pending_effect(0, context={"area": area, "card_id": card_id})

    def _pay_costs(self, player: PlayerState, costs: List[Cost], source_area: int = -1) -> bool:
        """Attempt to pay all costs for an ability (Rule 5.9 / Rule 9.4)"""
        # First verify they can all be paid (Rule 9.4.2.2)
        can_pay = True

        # Calculate cost reduction
        total_reduction = 0
        for ce in player.continuous_effects:
            if ce["effect"].effect_type == EffectType.REDUCE_COST:
                total_reduction += ce["effect"].value

        for cost in costs:
            if cost.type == AbilityCostType.ENERGY:
                actual_cost = max(0, cost.value - total_reduction)
                if player.count_untapped_energy() < actual_cost:
                    can_pay = False
            elif cost.type == AbilityCostType.TAP_SELF:
                if source_area < 0 or player.tapped_members[source_area]:
                    can_pay = False
            elif cost.type == AbilityCostType.SACRIFICE_SELF:
                if source_area < 0 or player.stage[source_area] < 0:
                    can_pay = False
            elif cost.type == AbilityCostType.DISCARD_HAND:
                if len(player.hand) < cost.value:
                    can_pay = False
            elif cost.type == AbilityCostType.REVEAL_HAND_ALL:
                # Can always reveal if you have a hand? Even if empty? Usually yes.
                pass
            elif cost.type == AbilityCostType.SACRIFICE_UNDER:
                if source_area < 0 or not player.stage_energy[source_area]:
                    can_pay = False
            elif cost.type == AbilityCostType.DISCARD_ENERGY:
                if player.count_untapped_energy() < 1:
                    can_pay = False
            elif cost.type == AbilityCostType.RETURN_HAND:
                if source_area < 0 or player.stage[source_area] < 0:
                    can_pay = False

        if not can_pay:
            return False

        # If all costs can be paid, now actually pay them
        for cost in costs:
            if cost.type == AbilityCostType.ENERGY:
                # Tap energy
                actual_cost = max(0, cost.value - total_reduction)
                tapped_count = 0
                for i in range(len(player.energy_zone) - 1, -1, -1):  # Tap from right to left
                    if tapped_count >= actual_cost:
                        break  # Break if enough energy is tapped
                    if not player.tapped_energy[i]:
                        player.tapped_energy[i] = True
                        tapped_count += 1
            elif cost.type == AbilityCostType.TAP_SELF:
                if source_area >= 0:
                    player.tapped_members[source_area] = True
            elif cost.type == AbilityCostType.SACRIFICE_SELF:
                if source_area >= 0 and player.stage[source_area] >= 0:
                    self.log_rule("Rule 9.4", f"Player {player.player_id} sacrificing member at area {source_area}.")
                    player.discard.append(player.stage[source_area])
                    player.stage[source_area] = -1  # Clear the stage slot

                    # Move energy back to DECK (Rule 10.5.3)
                    for e in player.stage_energy[source_area]:
                        player.energy_deck.append(e)
                    player.stage_energy[source_area] = []  # Clear energy under sacrificed member

                    player.tapped_members[source_area] = False  # Reset state
                    # FAQ Q79: If member is sacrificed, the slot becomes available again for play this turn
                    player.members_played_this_turn[source_area] = False

            elif cost.type == AbilityCostType.REVEAL_HAND_ALL:
                # Log the reveal. Since there's no UI for "reveal" in this backend state (it's perfect info or logged),
                # we just log it.
                hand_names = []
                for cid in player.hand:
                    if cid in self.member_db:
                        hand_names.append(self.member_db[cid].name)
                    elif cid in self.live_db:
                        hand_names.append(self.live_db[cid].name)
                self.log_rule(
                    "Rule 9.4", f"Player {player.player_id} pays cost: Reveals Hand [{', '.join(hand_names)}]"
                )

            elif cost.type == AbilityCostType.SACRIFICE_UNDER:
                if source_area >= 0 and player.stage_energy[source_area]:
                    self.log_rule(
                        "Rule 9.4",
                        f"Player {player.player_id} pays cost: Sacrificing energy under member at {source_area}.",
                    )
                    player.energy_deck.extend(player.stage_energy[source_area])
                    player.stage_energy[source_area] = []

            elif cost.type == AbilityCostType.DISCARD_ENERGY:
                # Tap 1 energy as cost
                for i in range(len(player.energy_zone) - 1, -1, -1):
                    if not player.tapped_energy[i]:
                        player.tapped_energy[i] = True
                        break

            elif cost.type == AbilityCostType.RETURN_HAND:
                if source_area >= 0 and player.stage[source_area] >= 0:
                    self.log_rule(
                        "Rule 9.4", f"Player {player.player_id} pays cost: Returning member at {source_area} to hand."
                    )
                    player.hand.append(player.stage[source_area])
                    player.stage[source_area] = -1
                    player.energy_deck.extend(player.stage_energy[source_area])
                    player.stage_energy[source_area] = []

            elif cost.type == AbilityCostType.DISCARD_HAND:
                # Rule 9.2: Discard card(s) as cost
                # Create choice to discard
                # Determine how many? cost.value.
                # If value > 1, we might need multiple choices or a multi-select.
                # Current system seems to queue individual choices?
                # or TARGET_HAND with count?
                # _handle_choice pops ONE pending choice.
                # So we should append 'cost.value' choices?
                # Or TARGET_HAND logic handles 'count'?
                # View _handle_choice (line 2059):
                # if choice_type == "TARGET_HAND":
                #    hand_idx = action - 500
                #    card_id = p.hand.pop(hand_idx)
                #    if params.get('effect') == 'discard': ...
                # It handles ONE card.
                # So we need to loop cost.value times.
                for _ in range(cost.value):
                    self.pending_choices.append(
                        (
                            "TARGET_HAND",
                            {"reason": "cost", "effect": "discard", "is_optional": cost.is_optional},
                        )
                    )

        return True

    def _handle_choice(self, action: int) -> None:
        """Handle target selection from pending choices"""
        if not self.pending_choices:
            return

        choice_type, params = self.pending_choices.pop(0)
        p = self.active_player
        opp = self.inactive_player

        if choice_type == "TARGET_HAND":
            hand_idx = action - 500
            if 0 <= hand_idx < len(p.hand):
                card_id = p.hand.pop(hand_idx)
                # Apply effect to card_id or move to target zone
                if params.get("effect") == "discard":
                    p.discard.append(card_id)
                elif params.get("effect") == "energy_charge":
                    p.energy_zone.append(card_id)
                    # Use index assignment instead of append for numpy array
                    p.tapped_energy[len(p.energy_zone) - 1] = False
                elif params.get("effect") == "place_under":
                    target_area = params.get("target_area", -1)
                    if target_area >= 0:
                        p.stage_energy[target_area].append(card_id)
                        if self.verbose:
                            print(f"Player {p.player_id} placed card {card_id} under member at {target_area}")

        elif choice_type == "TARGET_MEMBER" or choice_type == "TARGET_MEMBER_SLOT":
            area = action - 560
            if 0 <= area < 3:
                # Rule 9.9: If this was a buff effect choice
                if params.get("effect") == "buff":
                    target_effect = params.get("target_effect")
                    if target_effect:
                        p.continuous_effects.append(
                            {
                                "effect": target_effect,
                                "target_slot": area,
                                "expiry": "TURN_END",  # Default duration
                            }
                        )
                        if self.verbose:
                            print(f"Player {p.player_id} targeted slot {area} with {target_effect.effect_type.name}")

                elif params.get("effect") == "activate":
                    # Rule 11.2: Activate (Untap) member
                    p.tapped_members[area] = False
                    if self.verbose:
                        print(f"Effect: Player {p.player_id} activated member at area {area}")

                # Rule 11.9: If this was Position Change
                elif params.get("reason") == "position_change":
                    step = params.get("step", "source")
                    if step == "source":
                        # Valid source? Must have member?
                        if p.stage[area] >= 0:
                            # Push next step: Select Destination
                            self.pending_choices.insert(
                                0, ("TARGET_MEMBER_SLOT", {"reason": "position_change", "step": "dest", "source": area})
                            )
                            if self.verbose:
                                print(f"Position Change: Selected source area {area}")
                        else:
                            # Invalid source, retry?
                            if self.verbose:
                                print("Invalid source for move (empty)")
                            self.pending_choices.insert(0, (choice_type, params))
                    elif step == "dest":
                        source = params.get("source")
                        if source is not None and source != area:
                            self._move_member(p, source, area)
                        else:
                            if self.verbose:
                                print("Invalid move (same area or missing source)")

                # Logic for Buffs
                elif params.get("effect") == "buff":
                    # Apply buff to p.stage[area]
                    pass

        elif choice_type == "DISCARD_SELECT":
            count = params.get("count", 1)
            card_idx = action - 500

            p = self.active_player
            if 0 <= card_idx < len(p.hand):
                card_id = p.hand.pop(card_idx)
                p.discard.append(card_id)
                if self.verbose:
                    print(f"Player {p.player_id} discarded {card_id}")

                if count > 1:
                    params["count"] = count - 1
                    self.pending_choices.insert(0, ("DISCARD_SELECT", params))

        elif choice_type == "MODAL":
            option_idx = action - 570
            options = params.get("options", [])
            if 0 <= option_idx < len(options):
                choice = options[option_idx]
                if self.verbose:
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
                    if self.verbose:
                        print("Effect: Both players draw 1 card")
                elif choice == "その他":
                    # Formation Change (PR-004)
                    self.pending_choices.append(("CHOOSE_FORMATION", {}))

        elif choice_type == "TARGET_OPPONENT_MEMBER":
            area = action - 600
            # Opponent stage is 0-2 (same indices, but relative to them)
            # Just store the area, apply effect
            opp = self.inactive_player
            if 0 <= area < 3 and opp.stage[area] >= 0:
                effect_type = params.get("effect")
                if effect_type == "tap":
                    opp.tapped_members[area] = True
                    if self.verbose:
                        print(f"Effect: Opponent's member at area {area} was tapped.")

        elif choice_type == "SELECT_MODE":
            option_idx = action - 570
            options = params.get("options", [])  # List of List[Effect]
            if 0 <= option_idx < len(options):
                chosen_effects = options[option_idx]
                # Push chosen effects to the front of the stack
                for effect in reversed(chosen_effects):
                    self.pending_effects.insert(0, effect)
                if self.verbose:
                    print(f"Selected Mode {option_idx} with {len(chosen_effects)} effects.")

        elif choice_type == "COLOR_SELECT":
            color_idx = action - 580
            colors = ["赤", "青", "緑", "黄", "紫", "ピンク"]
            if 0 <= color_idx < len(colors):
                color = colors[color_idx]
                if self.verbose:
                    print(f"Player {p.player_id} selected color: {color}")

        elif choice_type == "SELECT_FROM_LIST":
            cards = params.get("cards", [])
            idx = action - 600

            if 0 <= idx < len(cards):
                selected = cards.pop(idx)
                p.hand.append(selected)
                if self.verbose:
                    print(f"Player {p.player_id} selected {selected} from looked/list")

                # Assume single choice for now.
                if self.looked_cards:
                    # Move unchosen cards to discard (breakroom) instead of deck bottom
                    for c in cards:  # 'cards' now contains only the unchosen cards
                        p.discard.append(c)
                    self.looked_cards = []
                    if self.verbose:
                        print(f"Moved {len(cards)} cards to discard (breakroom).")
                # For basic implementation, we store this in metadata or applies immediately
                # Example: PR-003 might need to store this color for the turn.

                if params.get("reason") == "search_deck":
                    # Rule 5.7.1: Remove card from deck, then shuffle
                    # selected is already added to p.hand in 1957
                    # We must find and remove it from p.main_deck
                    if selected in p.main_deck:
                        p.main_deck.remove(selected)

                    if params.get("shuffle", False):
                        random.shuffle(p.main_deck)
                        if self.verbose:
                            print("Deck shuffled after search.")

                pass

        elif choice_type == "SELECT_FROM_DISCARD":
            # Player selects card(s) from discard pile to recover
            cards = params.get("cards", [])
            count = params.get("count", 1)
            destination = params.get("destination", "hand")
            idx = action - 660

            if 0 <= idx < len(cards):
                selected_card = cards[idx]
                # Remove from discard
                if selected_card in p.discard:
                    p.discard.remove(selected_card)

                    # Add to destination
                    if destination == "hand":
                        p.hand.append(selected_card)
                        if self.verbose:
                            print(f"Player {p.player_id} recovered card {selected_card} to hand")
                    elif destination == "stage":
                        # Find empty slot
                        area = -1
                        for i in range(3):
                            if p.stage[i] < 0:
                                area = i
                                break
                        if area >= 0:
                            p.stage[area] = selected_card
                            if self.verbose:
                                print(f"Player {p.player_id} recovered card {selected_card} to Stage Area {area}")
                        else:
                            p.hand.append(selected_card)  # Fallback to hand if full
                            if self.verbose:
                                print(f"Player {p.player_id} recovered card {selected_card} to hand (Stage Full)")

                    # If need to select more, re-queue the choice
                    if count > 1:
                        remaining_cards = [c for c in cards if c != selected_card and c in p.discard]
                        if remaining_cards:
                            params["cards"] = remaining_cards
                            params["count"] = count - 1
                            self.pending_choices.insert(0, ("SELECT_FROM_DISCARD", params))

        elif choice_type == "TARGET_OPPONENT_MEMBER":
            idx = action - 600
            opp = self.inactive_player
            if 0 <= idx < 3 and opp.stage[idx] >= 0:
                if params.get("effect") == "tap":
                    opp.tapped_members[idx] = True
                    if self.verbose:
                        print(f"Effect: Player {p.player_id} tapped opponent member at area {idx}")

        elif choice_type == "CHOOSE_FORMATION":
            if self.verbose:
                print(f"Player {p.player_id} initializing formation change.")
            # Collect current members
            members = []  # (original_index, card_id)
            for i in range(3):
                if p.stage[i] >= 0:
                    members.append((i, p.stage[i]))

            if not members:
                if self.verbose:
                    print("No members to rearrange.")
            else:
                if self.verbose:
                    print(f"Formation Change: members to rearrange: {members}")
                # Start selection for Slot 0 (Left)
                # We pass the list of 'available' members (by their current/original index or id)
                self.pending_choices.append(
                    (
                        "SELECT_FORMATION_SLOT",
                        {
                            "slot_index": 0,
                            "available_members": members,  # List of (orig_idx, cid)
                            "new_stage": [-1, -1, -1],
                        },
                    )
                )

        elif choice_type == "SELECT_FORMATION_SLOT":
            # User selects which member goes into 'slot_index'
            # Action maps to index in 'available_members'
            slot_index = params.get("slot_index", 0)
            available = params.get("available_members", [])
            new_stage = params.get("new_stage", [-1, -1, -1])

            idx = action - 700

            if 0 <= idx < len(available):
                selected = available.pop(idx)  # (orig_idx, cid)
                new_stage[slot_index] = selected[1]
                if self.verbose:
                    print(f"Formation: Puts member {selected[1]} into slot {slot_index}. Remaining: {len(available)}")

                # Next slot?
                next_slot = slot_index + 1
                if next_slot < 3 and available:
                    self.pending_choices.insert(
                        0,
                        (
                            "SELECT_FORMATION_SLOT",
                            {"slot_index": next_slot, "available_members": available, "new_stage": new_stage},
                        ),
                    )
                else:
                    # All slots filled or no more members
                    # Fill remaining slots with -1 if any
                    for k in range(next_slot, 3):
                        new_stage[k] = -1
                    np.copyto(p.stage, new_stage)
                    if self.verbose:
                        print(f"Formation Change Complete. New Stage: {p.stage}")

        elif choice_type == "SELECT_SWAP_SOURCE":
            # Select card from Success Live to return to hand
            cards = params.get("cards", [])
            idx = action - 600
            if 0 <= idx < len(cards):
                card_to_hand = cards[idx]
                # Second step: Select card from hand to send to Success Live
                # Tricky: we need to ensure we don't pick the *same* card if we just added it?
                # Actually, logically we first pick from Live, put in Hand, then pick from Hand put in Live?
                # Or Simultaneous? "Swap" implies simultaneous.
                # Let's do: Store choice 1, ask choice 2, then execute.
                self.pending_choices.insert(0, ("SELECT_SWAP_TARGET", {"card_to_hand": card_to_hand}))

        elif choice_type == "SELECT_SWAP_TARGET":
            # Select card from Hand to send to Success Live
            # Action - 600? Or TARGET_HAND (500)?
            # TARGET_HAND uses 500
            idx = action - 500  # Use target hand range
            if 0 <= idx < len(p.hand):
                card_to_live = p.hand[idx]  # Don't pop yet

                card_to_hand = params.get("card_to_hand")

                # Execute Swap
                if card_to_hand in p.success_lives:
                    p.success_lives.remove(card_to_hand)
                    p.hand.append(card_to_hand)

                if card_to_live in p.hand:
                    p.hand.remove(card_to_live)
                    p.success_lives.append(card_to_live)

                if self.verbose:
                    print(f"Swapped {card_to_hand} (from Live) with {card_to_live} (from Hand)")

        elif choice_type == "SELECT_SUCCESS_LIVE":
            # Player selects which passed live card to move to success zone
            cards = params.get("cards", [])
            player_id = params.get("player_id", 0)
            idx = action - 600

            if 0 <= idx < len(cards):
                selected_cid = cards[idx]
                target_player = self.players[player_id]
                if selected_cid in target_player.passed_lives:
                    target_player.success_lives.append(selected_cid)
                    target_player.passed_lives.remove(selected_cid)
                    self.log_rule(
                        "Rule 8.4.7",
                        f"Player {player_id} chose to move {self.live_db[selected_cid].name} to Success Zone.",
                    )
                    if self.verbose:
                        print(f"SELECT_SUCCESS_LIVE: Player {player_id} selected {selected_cid}")

        elif choice_type == "CHOOSE_TRIGGER":
            trigger_choice_idx = action - 590
            indices = params.get("indices", [])
            if 0 <= trigger_choice_idx < len(indices):
                trigger_idx = indices[trigger_choice_idx]
                pid, ab, ctx = self.triggered_abilities.pop(trigger_idx)
                self._play_automatic_ability(pid, ab, ctx)
                if self.verbose:
                    print(f"Player {pid} chose to resolve trigger index {trigger_idx}")

        elif choice_type == "SELECT_ORDER":
            idx = action - 700
            cards = params.get("cards", [])
            ordered = params.get("ordered", [])
            position = params.get("position", "top")

            if 0 <= idx < len(cards):
                selected = cards.pop(idx)
                ordered.append(selected)
                if self.verbose:
                    print(f"Player {p.player_id} selected {selected} for order position {len(ordered)}")

                if cards:
                    # Continue selecting
                    self.pending_choices.insert(0, ("SELECT_ORDER", params))
                else:
                    # Done. Place ordered cards.
                    if position == "top":
                        # Put back on top (Reverse insert)
                        for c in reversed(ordered):
                            p.main_deck.insert(0, c)
                    else:
                        # Put at bottom
                        p.main_deck.extend(ordered)

        # After choice is handled, resume pending effects if any
        # This handles the case where a choice interrupted a chain of effects (e.g. Test Ability: Order -> Tap(Choice) -> Draw)
        if self.pending_effects and not self.pending_choices:
            # Basic context, might be missing original card info but sufficient for context-free effects
            self._resolve_pending_effect(0, context={})

    def _do_active_phase(self) -> None:
        p = self.active_player
        # Rule 7.4: アクティブフェイズ (Active Phase)
        self.log_rule("Rule 7.4", f"Active Phase: Untapping all members and energy for Player {p.player_id}.")
        p.members_played_this_turn[:] = False
        p.untap_all()
        self.phase = Phase.ENERGY

    def _do_energy_phase(self) -> None:
        p = self.active_player
        # Rule 7.5: エネルギーフェイズ (Energy Phase)
        self.log_rule("Rule 7.5", f"Energy Phase: Player {p.player_id} moves 1 card from Energy Deck to Energy Zone.")
        if p.energy_deck:
            p.energy_zone.append(p.energy_deck.pop(0))
        self.phase = Phase.DRAW

    def _do_draw_phase(self) -> None:
        p = self.active_player
        # Rule 7.6: ドローフェイズ (Draw Phase)
        self.log_rule("Rule 7.6", f"Draw Phase: Player {p.player_id} draws 1 card.")
        self._draw_cards(p, 1)
        self.phase = Phase.MAIN

    def _clear_expired_effects(self, expiry_type: str) -> None:
        """Rule 9.9.2: Cleanup temporary effects"""
        for p in self.players:
            p.continuous_effects = [e for e in p.continuous_effects if e.get("expiry") != expiry_type]
            if expiry_type == "LIVE_END":
                p.cannot_live = False  # Reset live restriction
                p.live_score_bonus = 0  # Reset score bonus

    def _execute_mulligan(self) -> None:
        """Execute mulligan for current player (Rule 6.2.1.6)"""
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
        """Draw cards (Rule 5.6). Rule 10.2 (Refresh) is handled by _process_rule_checks."""
        for _ in range(count):
            # Rule 10.2: リフレッシュ (Refresh check before each draw)
            self._process_rule_checks()
            if player.main_deck:
                player.hand.append(player.main_deck.pop(0))
            self._process_rule_checks()  # Rule maintenance

    def _play_member(self, hand_idx: int, area_idx: int) -> None:
        p = self.active_player

        # Check restrictions
        if "placement" in p.restrictions:
            if self.verbose:
                print(f"Player {p.player_id} cannot play members due to restriction.")
            # This should ideally be caught by get_legal_actions, but safe guard:
            p.hand.insert(hand_idx, p.hand.pop(hand_idx))  # Return to hand or just fail
            return

        card_id = p.hand.pop(hand_idx)
        card = self.member_db[card_id]

        # Rule 9.6.2.1.2.1: Slot Cooldown check is in get_legal_actions,
        # but we log the success here.
        self.log_rule("Rule 9.6.2", f"Player {p.player_id} plays {card.name} from hand to slot {area_idx}.")

        # Calculate cost reduction from continuous effects
        total_reduction = 0
        for ce in p.continuous_effects:
            if ce["effect"].effect_type == EffectType.REDUCE_COST:
                total_reduction += ce["effect"].value

        # Determine cost (Rule 9.6.2.1.1.2 - Baton Touch cost reduction)
        base_cost = max(0, card.cost - total_reduction)
        cost = base_cost
        if p.stage[area_idx] >= 0:
            prev_card = self.member_db[p.stage[area_idx]]
            cost = max(0, cost - prev_card.cost)
            p.baton_touch_count += 1
            self.log_rule(
                "Rule 9.6.2.1.1.2", f"Baton Touch applied. Cost reduced from {base_cost} to {cost} by {prev_card.name}."
            )
            # Discard previous member
            p.discard.append(p.stage[area_idx])

            # Rule 4.5.5.4: When member leaves stage, energy under it goes to Energy Deck
            if p.stage_energy[area_idx]:
                self.log_rule("Rule 4.5.5.4", f"Energy cards under {prev_card.name} returned to Energy Deck.")
                p.energy_deck.extend(p.stage_energy[area_idx])
                p.stage_energy[area_idx] = []

        # Pay cost (Rule 9.4)
        untapped = [i for i, tapped in enumerate(p.tapped_energy) if not tapped]
        if len(untapped) < cost:
            # Should not happen if get_legal_actions is correct
            print(f"Error: Not enough energy to pay cost {cost}")
            p.hand.insert(hand_idx, card_id)
            return

        for i in range(cost):
            p.tapped_energy[untapped[i]] = True

        # Move to stage
        p.stage[area_idx] = card_id
        p.members_played_this_turn[area_idx] = True

        # Rule 11.3: Trigger Enter Stage abilities (登場)
        for ability in card.abilities:
            if ability.trigger == TriggerType.ON_PLAY:
                self.triggered_abilities.append((p.player_id, ability, {"area": area_idx}))
                # print(f"Queued ON_PLAY trigger for {card.name}")

    def _end_main_phase(self) -> None:
        """End main phase, enter live set phase"""
        # Switch to other player's main phase if this was first player
        if self.current_player == self.first_player:
            p2 = 1 - self.first_player

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
            self.phase = Phase.LIVE_SET
            self.current_player = self.first_player

    def _set_live_card(self, hand_idx: int) -> None:
        """Set a card face-down in live zone"""
        p = self.active_player
        if hand_idx < 0 or hand_idx >= len(p.hand) or len(p.live_zone) >= 3:
            return
        card_id = p.hand.pop(hand_idx)
        p.live_zone.append(card_id)
        p.live_zone_revealed.append(False)
        # Draw replacement
        self._draw_cards(p, 1)

    def _end_live_set(self) -> None:
        """End live card setting for current player"""
        if self.current_player == self.first_player:
            self.current_player = 1 - self.first_player
        else:
            # Both done. Start Performance Phase.
            # Reset performance results for the new sequence
            self.performance_results = {}

            # Rule 8.3.2: First Player performs first.
            if self.first_player == 0:
                self.phase = Phase.PERFORMANCE_P1
                self.current_player = 0
            else:
                self.phase = Phase.PERFORMANCE_P2
                self.current_player = 1

    def _do_performance(self, player_idx: int) -> None:
        """Execute performance phase for a player"""
        p = self.players[player_idx]

        # Rule 8.3.4.1: Cannot Live status
        if p.cannot_live:
            self.log_rule("Rule 8.3.4.1", f"Player {player_idx} cannot live. Discarding all live cards.")
            for card_id in p.live_zone:
                p.discard.append(card_id)
            p.live_zone = []
            self._advance_performance()
            return

        p.live_zone_revealed = [True] * len(p.live_zone)

        # Filter for live cards only
        valid_lives = []
        for card_id in p.live_zone:
            if card_id in self.live_db:
                valid_lives.append(card_id)
            else:
                p.discard.append(card_id)
        p.live_zone = valid_lives

        # Rule 11.4: Trigger ON_LIVE_START abilities of the live cards
        for card_id in p.live_zone:
            live = self.live_db[card_id]
            for ab in live.abilities:
                if ab.trigger == TriggerType.ON_LIVE_START:
                    self.triggered_abilities.append((player_idx, ab, {}))

        # Trigger ON_LIVE_START abilities of members on stage
        for i, card_id in enumerate(p.stage):
            if card_id >= 0 and not p.tapped_members[i] and card_id in self.member_db:
                member = self.member_db[card_id]
                for ab in member.abilities:
                    if ab.trigger == TriggerType.ON_LIVE_START:
                        self.triggered_abilities.append((player_idx, ab, {"area": i}))

        if not p.live_zone:
            # No live cards, skip to next
            self._advance_performance()
            return

        # Yell: draw cards equal to total blades
        total_blades = p.get_total_blades(self.member_db)
        self.log_rule(
            "Rule 8.3.10",
            f"🎺 YELL START: Player {player_idx} has {total_blades} total blades on stage → Revealing {total_blades} cards from deck",
        )

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

        # List the yelled card names for clarity
        yell_names = []
        for cid in self.yell_cards:
            card_obj = self.member_db.get(cid) or self.live_db.get(cid)
            if card_obj:
                yell_names.append(f"{card_obj.name} (ID:{cid})")

        self.log_rule(
            "Rule 8.3.11",
            f"Yell Zone: {len(self.yell_cards)} cards revealed: {', '.join(yell_names) if yell_names else 'None'}",
        )

        # Count icons for yell bonus (Rule 8.3.12 and Rule 8.4.2)
        draw_bonus = 0
        yell_score_bonus = 0
        total_hearts = np.zeros(7, dtype=np.int32)
        blade_hearts_padded = np.zeros(7, dtype=np.int32)  # Pre-init for Meta Rule

        for card_id in self.yell_cards:
            # Check both Member and Live DBs
            card_obj = self.member_db.get(card_id) or self.live_db.get(card_id)
            if card_obj:
                if hasattr(card_obj, "total_blade_hearts"):
                    # Standard: Add all blade hearts to draw
                    draw_bonus += card_obj.total_blade_hearts()

                    # META RULE: If heart_rule active, Convert ALL Blade (Index 6) to Any Heart
                    # b_all is mapped to index 6 by data_loader
                    if (
                        "heart_rule" in p.meta_rules
                        and hasattr(card_obj, "blade_hearts")
                        and card_obj.blade_hearts.size > 6
                    ):
                        all_blade_count = card_obj.blade_hearts[6]
                        if all_blade_count > 0:
                            draw_bonus -= all_blade_count  # Remove from draw
                            blade_hearts_padded[6] += all_blade_count  # Add to Any Heart
                            total_hearts[6] += (
                                all_blade_count  # CRITICAL: Also add to total hearts for requirement check
                            )
                            self.log_rule("Meta Rule", f"ALL Blade on {card_obj.name} treated as Any Heart.")

                draw_bonus += card_obj.draw_icons
                yell_score_bonus += card_obj.volume_icons

        self.log_rule("Rule 8.3.12.1", f"Yell Draw Bonus: +{draw_bonus} cards.")
        self._draw_cards(p, draw_bonus)

        # Calculate total hearts
        # (Variables initialized above)

        # Breakdown of member contributions
        self.log_rule("Rule 8.3.13", f"--- Heart Contribution Breakdown (Player {player_idx}) ---")

        for i in range(3):
            cid = p.stage[i]
            if cid >= 0 and cid in self.member_db:
                member = self.member_db[cid]
                # Pad get_effective_hearts result to shape (7,)
                m_hearts_raw = p.get_effective_hearts(i, self.member_db)
                m_hearts = np.zeros(7, dtype=np.int32)
                m_hearts[: len(m_hearts_raw)] = m_hearts_raw
                total_hearts += m_hearts

                # Log individual contribution - CORRECT COLOR ORDER: Pink=0, Red=1, Yellow=2, Green=3, Blue=4, Purple=5
                COLOR_NAMES = ["Pink", "Red", "Yellow", "Green", "Blue", "Purple", "Any"]
                h_str = ", ".join([f"{COLOR_NAMES[idx]}:{m_hearts[idx]}" for idx in range(7) if m_hearts[idx] > 0])
                self.log_rule("Rule 8.3.13", f"Slot {i} [{member.name} (ID:{cid})]: +[{h_str if h_str else 'None'}]")

        # Add blade hearts from yell cards
        if self.yell_cards:
            self.log_rule("Rule 8.3.14", "--- Yell Heart Contributions ---")
        for card_id in self.yell_cards:
            # Blade hearts only come from members
            if card_id in self.member_db:
                member = self.member_db[card_id]
                # Update total_hearts with color blade hearts
                card_blade_hearts = np.zeros(7, dtype=np.int32)
                card_blade_hearts[:6] = member.blade_hearts[:6]  # Only colors here, b_all handled above
                total_hearts += card_blade_hearts
                COLOR_NAMES = ["Pink", "Red", "Yellow", "Green", "Blue", "Purple", "Any"]
                h_str = ", ".join(
                    [
                        f"{COLOR_NAMES[idx]}:{member.blade_hearts[idx]}"
                        for idx in range(6)
                        if member.blade_hearts[idx] > 0
                    ]
                )
                if h_str:
                    self.log_rule("Rule 8.3.14", f"Yell [{member.name} (ID:{card_id})]: +[{h_str}] (Blade)")

        total_h_sum = np.sum(total_hearts)
        COLOR_NAMES = ["Pink", "Red", "Yellow", "Green", "Blue", "Purple", "Any"]
        total_hearts_str = ", ".join(
            [f"{COLOR_NAMES[idx]}:{total_hearts[idx]}" for idx in range(7) if total_hearts[idx] > 0]
        )
        self.log_rule(
            "Rule 8.3.14.S",
            f"--- TOTAL HEARTS AVAILABLE: [{total_hearts_str if total_hearts_str else 'None'}] (Total Vol: {total_h_sum}) ---",
        )

        # Rule 8.3.15: Check if requirements met for each live card
        remaining_hearts = total_hearts.copy()
        temp_passed = []
        all_passed = True

        for live_id in p.live_zone:
            if live_id not in self.live_db:
                continue  # Safety
            live = self.live_db[live_id]

            req = live.required_hearts.copy()  # Use copy as we might modify it

            # Apply requirement reductions (REDUCE_HEART_REQ)
            total_heart_reduction = 0
            for ce in p.continuous_effects:
                if ce["effect"].effect_type == EffectType.REDUCE_HEART_REQ:
                    total_heart_reduction += ce["effect"].value

            if total_heart_reduction > 0:
                req[6] = max(0, req[6] - total_heart_reduction)
                self.log_rule(
                    "Effect",
                    f"Heart requirement reduced by {total_heart_reduction} (Any). New 'Any' requirement: {req[6]}",
                )

            COLOR_NAMES = ["Pink", "Red", "Yellow", "Green", "Blue", "Purple"]

            # Create a combined string for "Have/Need" for only required colors
            have_need_list = []
            for i in range(6):
                if req[i] > 0:
                    have_need_list.append(f"{COLOR_NAMES[i]} {remaining_hearts[i]}/{int(req[i])}")

            # Handle "Any" separately
            if req[6] > 0:
                have_need_list.append(f"Any {np.sum(remaining_hearts)}/{int(req[6])}")

            have_need_str = ", ".join(have_need_list)

            if self._check_hearts_meet_requirement(remaining_hearts, req):
                self.log_rule("Rule 8.3.15.1", f"Checking '{live.name}' → [{have_need_str}]")

                old_remaining = remaining_hearts.copy()
                self._consume_hearts(remaining_hearts, req)
                consumed = old_remaining - remaining_hearts

                cons_str = ", ".join([f"{COLOR_NAMES[i]}:{consumed[i]}" for i in range(6) if consumed[i] > 0])

                temp_passed.append(live_id)
                self.log_rule("Rule 8.3.15.1", f"✅ PASSED: Fulfilled with [{cons_str}]")
            else:
                all_passed = False
                self.log_rule("Rule 8.3.15.2", f"❌ FAILED: '{live.name}' → [{have_need_str}]")
                break

        # Rule 8.3.16: All or Nothing
        if all_passed and temp_passed:
            p.passed_lives = temp_passed
            self.log_rule(
                "Rule 8.3.16.1", f"🎉 SUCCESS! Player {player_idx} cleared ALL {len(temp_passed)} live card(s)!"
            )
        else:
            # All go to discard
            if p.live_zone:
                self.log_rule(
                    "Rule 8.3.16.2",
                    f"💔 FAILURE! Player {player_idx} failed one or more requirements. All face-down live cards discarded.",
                )
            for live_id in p.live_zone:
                p.discard.append(live_id)
            p.passed_lives = []

        # --- Capture Performance Result for UI (Popup) ---
        member_contribs = []
        for i in range(3):
            if p.stage[i] >= 0 and p.stage[i] in self.member_db:
                member = self.member_db[p.stage[i]]
                m_hearts_raw = p.get_effective_hearts(i, self.member_db)
                m_hearts = np.zeros(7, dtype=np.int32)
                m_hearts[: len(m_hearts_raw)] = m_hearts_raw
                member_contribs.append({"name": member.name, "hearts": m_hearts.tolist(), "img": member.img_path})

        yell_contribs = []
        # yell_cards are still in self.yell_cards at this point
        for cid in self.yell_cards:
            if cid in self.member_db:
                m = self.member_db[cid]
                yell_contribs.append({"name": m.name, "blade_hearts": m.blade_hearts.tolist(), "img": m.img_path})
            elif cid in self.live_db:  # Yell cards can be lives (no hearts, but show them)
                l = self.live_db[cid]
                yell_contribs.append({"name": l.name, "blade_hearts": [0] * 7, "img": l.img_path, "is_live": True})

        final_lives_data = []
        for live_id in p.live_zone:
            if live_id in self.live_db:
                l = self.live_db[live_id]
                final_lives_data.append(
                    {
                        "name": l.name,
                        "required": l.required_hearts.tolist(),
                        "passed": live_id in temp_passed,
                        "img": l.img_path,
                    }
                )

        self.performance_results[player_idx] = {
            "player_idx": player_idx,
            "total_hearts": total_hearts.tolist(),
            "member_contributions": member_contribs,
            "yell_cards": yell_contribs,
            "lives": final_lives_data,
            "success": bool(all_passed and temp_passed),
        }
        if self.verbose:
            print(f"DEBUG: Performance Results set for P{player_idx}: {self.performance_results[player_idx].keys()}")
        # -----------------------------------------------

        # Clear live zone as cards are now in passed_lives or discard
        p.live_zone = []

        # Rule 8.3.17: Apply Yell Score Bonus
        p.live_score_bonus = yell_score_bonus
        self.log_rule("Rule 8.3.17", f"Player {player_idx} Live Score Bonus (Yell): +{yell_score_bonus}.")

        # Rule 8.3.18: Move yell cards to discard
        for card_id in self.yell_cards:
            p.discard.append(card_id)
        self.yell_cards = []
        self.log_rule("Rule 8.3.18", "Yell cards moved to discard pile.")

        # Rule 8.3.19: Members that performed now enter "Wait" state (Tapped)
        p.tapped_members[:] = True
        self.log_rule("Rule 8.3.19", f"Player {player_idx}'s members are now in Wait state (tapped).")

        # Performance Summary
        stage_hearts_total = sum([total_hearts[i] - blade_hearts_padded[i] for i in range(6)])  # Approximate
        yell_hearts_total = sum([blade_hearts_padded[i] for i in range(6)])  # Approximate
        success_str = "✓ SUCCESS" if all_passed and temp_passed else "✗ FAILURE"

        self.log_rule("PERF_SUMMARY", f"━━━ PERFORMANCE SUMMARY (Player {player_idx}) ━━━")
        self.log_rule("PERF_SUMMARY", f"  Yell Cards: {len(self.yell_cards)} cards revealed, +{draw_bonus} cards drawn")
        self.log_rule(
            "PERF_SUMMARY",
            f"  Hearts: {total_h_sum} total ({stage_hearts_total} from stage, ~{yell_hearts_total} from yells)",
        )
        self.log_rule(
            "PERF_SUMMARY",
            f"  Result: {success_str} - {len(temp_passed) if temp_passed else 0}/{len(p.live_zone)} lives cleared",
        )
        self.log_rule("PERF_SUMMARY", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        self._advance_performance()

    def _check_hearts_meet_requirement(self, have: np.ndarray, need: np.ndarray) -> bool:
        """Check if hearts meet live card requirements"""
        # need[0:6] are color requirements, need[6] is "any" requirement
        remaining = have.copy()
        total_needed = 0

        # First satisfy color requirements
        # First satisfy color requirements
        for i in range(6):
            # Safe access for need[i]
            n_val = need[i] if i < len(need) else 0

            if n_val > remaining[i]:
                return False
            remaining[i] -= n_val
            total_needed += n_val

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
        if self.first_player == 0:
            # Order: P0 (Phase 6) -> P1 (Phase 7) -> Result
            if self.phase == Phase.PERFORMANCE_P1:
                self.phase = Phase.PERFORMANCE_P2
                self.current_player = 1
            else:
                self.phase = Phase.LIVE_RESULT
        else:
            # Order: P1 (Phase 7) -> P0 (Phase 6) -> Result
            if self.phase == Phase.PERFORMANCE_P2:
                self.phase = Phase.PERFORMANCE_P1
                self.current_player = 0
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

        self.log_rule(
            "Rule 8.4.2",
            f"Score Calculation: P0={p0_total} ({p0_base}+{p0.live_score_bonus}), P1={p1_total} ({p1_base}+{p1.live_score_bonus})",
        )

        # Rule 8.4.6: Determine Winner(s)
        winners = []
        if p0_total > 0 or p1_total > 0:
            if p0_total > p1_total:
                winners = [0]
            elif p1_total > p0_total:
                winners = [1]
            else:
                winners = [0, 1]

        if not winners:
            # Rule 8.4.6.1: ライブに勝利したプレイヤーはいません
            self.log_rule("Rule 8.4.6.1", "No winners (both scores 0 or no cards).")
        else:
            # Rule 8.4.6.2: スコアが大きいプレイヤーがライブに勝利
            self.log_rule("Rule 8.4.6.2", f"Winner(s): {' and '.join(['P' + str(w) for w in winners])}")

        # Rule 8.4.4: Live Success event
        for pid in range(2):
            p = self.players[pid]
            if p.passed_lives:
                # Trigger ON_LIVE_SUCCESS abilities of members on stage
                for i, card_id in enumerate(p.stage):
                    if card_id >= 0 and card_id in self.member_db:
                        member = self.member_db[card_id]
                        for ab in member.abilities:
                            if ab.trigger == TriggerType.ON_LIVE_SUCCESS:
                                self.triggered_abilities.append((pid, ab, {"area": i}))
                                if self.verbose:
                                    print(f"Queued ON_LIVE_SUCCESS for {member.name}")

        # Rule 8.4.7: Winner(s) choose 1 card to Successful Zone
        for w_idx in winners:
            p = self.players[w_idx]
            if p.passed_lives:
                if len(p.passed_lives) == 1:
                    # Only one live passed - auto-select
                    cid = p.passed_lives[0]
                    p.success_lives.append(cid)
                    p.passed_lives.remove(cid)
                    self.log_rule("Rule 8.4.7", f"Player {w_idx} moves {self.live_db[cid].name} to Success Zone.")
                else:
                    # Multiple lives passed - player must choose (for P0) or AI auto-selects (for P1)
                    if w_idx == 0:
                        # Human player - create pending choice
                        self.pending_choices.append(
                            ("SELECT_SUCCESS_LIVE", {"cards": p.passed_lives.copy(), "player_id": w_idx})
                        )
                        self.log_rule("Rule 8.4.7", f"Player {w_idx} must choose which live to move to Success Zone.")
                    else:
                        # AI player - auto-select highest scoring
                        best_cid = max(p.passed_lives, key=lambda c: self.live_db[c].score if c in self.live_db else 0)
                        p.success_lives.append(best_cid)
                        p.passed_lives.remove(best_cid)
                        self.log_rule(
                            "Rule 8.4.7", f"Player {w_idx} moves {self.live_db[best_cid].name} to Success Zone."
                        )
                if self.verbose:
                    print(f"DEBUG: Player {w_idx} Success Lives: {len(p.success_lives)}")

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

        # Rule 8.4.11: Constant Effect Cleanup
        for p in self.players:
            p.continuous_effects = [e for e in p.continuous_effects if e.get("expiry") != "TURN_END"]
            p.cannot_live = False  # Reset Rule 8.3.4.1
            p.used_abilities.clear()  # Reset Rule 11.2
            self.log_rule("Rule 8.4.11", f"Cleaned up TURN_END effects for Player {p.player_id}.")

        # Phase Advancement
        self.log_rule("Rule 8.4.14", f"Turn {self.turn_number} finished.")
        self.turn_number += 1
        self.current_player = self.first_player
        self.phase = Phase.ACTIVE

        # Discard remaining live cards (from live_zone, not passed_lives)
        for p in self.players:
            for card_id in p.live_zone:  # This should be empty if logic is correct, but for safety
                p.discard.append(card_id)
            p.live_zone = []
            p.live_zone_revealed = []

        # Check win condition
        self.check_win_condition()

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
        # Get reward for player (1 for win, -1 for loss, 0 otherwise)
        if self.winner == player_idx:
            return 1.0
        elif self.winner >= 0:
            return -1.0
        return 0.0

    def take_action(self, action_id: int) -> None:
        """In-place version of step() for testing and direct manipulation."""
        if self.pending_choices:
            self._handle_choice(action_id)
        else:
            self._execute_action(action_id)

        # Process resulting effects
        while self.pending_effects and not self.pending_choices:
            self._resolve_pending_effect(0)


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
            card_no=f"SAMPLE-M-{i}",
            name=f"Member_{i}",
            cost=cost,
            hearts=hearts,
            blade_hearts=blade_hearts,
            blades=blades,
        )

    # Create 12 sample live cards
    for i in range(12):
        score = 1 + (i % 3)  # Score 1-3
        required = np.zeros(7, dtype=np.int32)
        required[i % 6] = 2 + (i // 6)  # 2-3 of one color required
        required[6] = 1 + (i % 4)  # 1-4 "any" hearts required

        lives[100 + i] = LiveCard(
            card_id=100 + i, card_no=f"SAMPLE-L-{i}", name=f"Live_{i}", score=score, required_hearts=required
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
        print(
            f"Step {step}: Action {action}, Phase {game.phase.name}, "
            f"Player {game.current_player}, "
            f"P0 lives: {len(game.players[0].success_lives)}, "
            f"P1 lives: {len(game.players[1].success_lives)}"
        )

# --- COMPREHENSIVE RULEBOOK INDEX (v1.04) ---
# This index ensures 100% searchability of all official rule identifiers.
#
# Rule 1: ゲームの概要
# Rule 1.1: ゲーム人数
# Rule 1.1.1: このゲームは原則2 名のプレイヤーにより対戦を
# Rule 1.2: ゲームの勝敗
# Rule 1.2.1: いずれかのプレイヤーが勝利した、または敗北した
# Rule 1.2.1.1: いずれかのプレイヤーの成功ライブカード置
# Rule 1.2.1.2: 両方のプレイヤーが同時に3 枚以上になっ
# Rule 1.2.2: すべてのプレイヤーが同時に敗北する場合、その
# Rule 1.2.3: すべてのプレイヤーは、ゲーム中の任意の時点で
# Rule 1.2.3.1: 投了を行う行為は、いかなるカードの影響も
# Rule 1.2.4: なんらかのカードにより、いずれかのプレイヤーが
# Rule 1.3: ゲームの大原則
# Rule 1.3.1: カードに書かれているテキストの内容が総合ルー
# Rule 1.3.2: なんらかの理由によりプレイヤーが実行不可能なこ
# Rule 1.3.2.1: すでにある状態にあるものを改めてその状
# Rule 1.3.2.2: ある行動を実行する際の単位数や回数が0
# Rule 1.3.2.3: ある行動を要求する効果が複数発生し、そ
# Rule 1.3.2.4: プレイヤーやカードが持つ数値情報は、特に
# Rule 1.3.3: あるカードの効果によりプレイヤーがなんらかの行
# Rule 1.3.4: 複数のプレイヤーが同時になんらかの選択を行う
# Rule 1.3.4.1: ある効果が複数のプレイヤーに適用され、
# Rule 1.3.4.2: 非公開領域のカードを同時に選択する場
# Rule 1.3.5: なんらかの数を選ぶ場合、0 以上の整数を選ぶ必
# Rule 1.3.5.1: カードやルールにより‘～まで’のように上限
# Rule 2: カードの情報
# Rule 2.1: ハートアイコン
# Rule 2.1.1: ハートアイコンは
# Rule 2.1.2: 同色のハートアイコンが複数重なって表記されてい
# Rule 2.1.3: ブレードハート（2.7）のハートアイコンはブレード
# Rule 2.2: カードタイプ
# Rule 2.2.1: カードの種類を表す情報です。
# Rule 2.2.2: カードタイプは、‘ライブ’‘メンバー’‘エネルギー’の
# Rule 2.2.2.1: カードタイプがライブであるカードは、ゲーム
# Rule 2.2.2.1.1: スコア（2.10）や必要ハート（2.11）を持つ
# Rule 2.2.2.2: カードタイプがメンバーであるカードは、ライ
# Rule 2.2.2.2.1: コスト（2.6）やハート（2.9）を持つカード
# Rule 2.2.2.3: カードタイプがエネルギーであるカードは、メ
# Rule 2.2.2.3.1: カード左下に‘エネルギーカード’と表記
# Rule 2.3: カード名
# Rule 2.3.1: このカードの持つ固有名称です。
# Rule 2.3.2: カード名は他の能力や効果で参照することがありま
# Rule 2.3.2.1: カード名に＆を含むメンバーカードは、＆で
# Rule 2.3.2.2: テキスト中、「」（かぎ括弧）で囲まれた名称
# Rule 2.4: グループ名
# Rule 2.4.1: カードが属するアイドルグループの名称です。
# Rule 2.4.2: グループ名はロゴで表記され、そのロゴに対応した
# Rule 2.4.2.1: カード名に＆を含むメンバーカードは、＆で
# Rule 2.4.2.2: メンバー名称とグループ名称の対応は、巻
# Rule 2.4.3: グループ名は他の能力や効果で参照することがあ
# Rule 2.4.3.1: テキスト中、『』（二重かぎ括弧）で囲まれた
# Rule 2.4.4: ロゴとグループ名称の対応は、巻末の付録を参照
# Rule 2.5: ユニット名
# Rule 2.5.1: カードが属するユニットの名称です。
# Rule 2.5.2: ユニット名はロゴで表記され、そのロゴに対応した
# Rule 2.5.3: ユニット名とロゴの対応は、巻末の付録を参照して
# Rule 2.6: コスト
# Rule 2.6.1: メンバーカードをプレイするためのコスト（9.6.2.3.1）
# Rule 2.7: ブレードハート
# Rule 2.7.1: エール（8.3.11）により実行する処理の内容を示すア
# Rule 2.7.2: アイコンとそれに対応する処理の内容に関しては、
# Rule 2.8: ブレード
# Rule 2.8.1: メンバーがエール（8.3.11）による処理で公開する
# Rule 2.8.2: ブレードの数値はブレードアイコン
# Rule 2.9: ハート
# Rule 2.9.1: ライブ成功判定（8.3.14）を行う際にプレイヤーが得
# Rule 2.9.2: ハートはハートアイコン（2.1）で示されます。
# Rule 2.9.3: メンバーのハート表記では、複数のハートアイコン
# Rule 2.10: スコア
# Rule 2.10.1: ライブが成功した場合にこのライブカードにより得
# Rule 2.11: 必要ハート
# Rule 2.11.1: ライブを成功させるために必要とするハートの数で
# Rule 2.11.2: 必要ハートは、ハート音符（右
# Rule 2.11.2.1: 各ハート音符は、縦に
# Rule 2.11.2.2: ハート音符が複数ある場合、その全てを同
# Rule 2.11.3: 与えられた数と種類のハートアイコンは、以下の
# Rule 2.12: カードテキスト
# Rule 2.12.1: このカードが持つ固有の能力を示す情報です。
# Rule 2.12.2: カードテキスト（2.12）で『』（二重かぎ括弧）で指定
# Rule 2.12.3: カードテキストで「」（かぎ括弧）で指定した名称を
# Rule 2.12.4: カードテキストの中に、（）（丸括弧）で囲まれた、能
# Rule 2.13: イラスト
# Rule 2.13.1: カードの内容をイメージしたイラストです。
# Rule 2.13.2: イラストは、ゲーム上は特に意味を持ちません。
# Rule 2.14: 付帯条項
# Rule 2.14.1: カードナンバー、イラストレーター表記、カードの著
# Rule 2.14.2: カードナンバーはデッキ構築の際に参照します。
# Rule 2.14.3: カードナンバー以外の付帯条項は、ゲーム上は特
# Rule 3: プレイヤーに関する情報
# Rule 3.1: オーナーとマスター
# Rule 3.1.1: オーナーとは、カードの物理的な所有者を指しま
# Rule 3.1.2: マスターとは、カードや能力や効果などを現在使用
# Rule 3.1.2.1: 常時能力のマスターとは、その能力を有する
# Rule 3.1.2.2: 起動能力のマスターとは、それをプレイした
# Rule 3.1.2.3: 自動能力のマスターとは、その能力を有する
# Rule 3.1.2.4: 効果のマスターとは、その効果を発生した能
# Rule 3.1.2.4.1: ある効果により特にプレイヤーが指定
# Rule 4: 領域
# Rule 4.1: 領域の基本
# Rule 4.1.1: 領域は、特に指定がない限り、各プレイヤーがそれ
# Rule 4.1.2: 領域によっては、そこに置かれているカードの内容
# Rule 4.1.2.1: 公開領域にカードが置かれる場合、その
# Rule 4.1.2.2: 領域が公開であるか非公開であるかにかか
# Rule 4.1.2.3: 非公開領域においては、その領域のカード
# Rule 4.1.3: 領域によっては、そこに置かれるカードの順番が管
# Rule 4.1.3.1: 順番を管理する領域のカードの順番は、
# Rule 4.1.4: カードがメンバーエリアからメンバーエリアあるいは
# Rule 4.1.4.1: あるカードによる効果内で、その効果が移動
# Rule 4.1.5: 複数のカードがある領域に同時に置かれる場合、
# Rule 4.1.5.1: 公開領域から非公開領域に複数のカードが
# Rule 4.1.6: あるカードが持つテキストや能力や効果において、
# Rule 4.1.7: あるカードがメンバーエリアやライブカード置き場以
# Rule 4.2: 領域の可視状態
# Rule 4.2.1: 領域内にあるカードは、公開状態か非公開状態か
# Rule 4.2.2: 公開状態とは、カードの内容や情報をすべてのプレ
# Rule 4.2.3: 非公開状態とは、一部または全部のプレイヤーが
# Rule 4.3: カードの配置状態
# Rule 4.3.1: 一部の領域において、カードの配置状態が指定さ
# Rule 4.3.2: 向きを表す状態は、‘アクティブ状態’、‘ウェイト状
# Rule 4.3.2.1: アクティブ状態のカードは、そのカードのマス
# Rule 4.3.2.2: ウェイト状態のカードは、そのカードのマス
# Rule 4.3.2.3: 配置状態が指定される領域にカードが置か
# Rule 4.3.3: 表示面を表す状態は、‘表向き’か‘裏向き’のいず
# Rule 4.3.3.1: 表向き状態のカードは、カードの情報が書か
# Rule 4.3.3.2: 裏向き状態のカードは、カードの情報が書か
# Rule 4.4: ステージ
# Rule 4.4.1: プレイヤーのメンバーエリアを統合した領域です。
# Rule 4.4.2: プレイヤーはステージ内に自身のメンバーエリア
# Rule 4.5: メンバーエリア
# Rule 4.5.1: プレイしたメンバーカードを置く領域です。
# Rule 4.5.1.1: テキスト等で単に‘エリア’と書かれている場
# Rule 4.5.2: プレイヤーはメンバーエリアを3 つ持ちます。
# Rule 4.5.2.1: 各メンバーエリアは、それぞれ‘左サイドエリ
# Rule 4.5.2.2: 同一プレイヤーに属する、左サイドエリアは
# Rule 4.5.2.3: 同一プレイヤーに属する、左サイドエリアと
# Rule 4.5.3: メンバーエリアはすべてのプレイヤーに対して公開
# Rule 4.5.4: メンバーエリアのメンバーカードは向きを示す配置
# Rule 4.5.5: メンバーエリアのメンバーカードの下に、エネル
# Rule 4.5.5.1: メンバーエリアのメンバーカードの下に重ね
# Rule 4.5.5.2: メンバーエリアのメンバーカードの下に重ね
# Rule 4.5.5.3: メンバーエリアのメンバーが他のメンバーエ
# Rule 4.5.5.4: メンバーエリアのメンバーがメンバーエリア
# Rule 4.5.6: テキスト等で、特に領域を指定せずに‘メンバー’を
# Rule 4.6: ライブカード置き場
# Rule 4.6.1: プレイヤーが実行するライブカードを置く領域です。
# Rule 4.6.2: ライブカード置き場はすべてのプレイヤーに対して
# Rule 4.7: エネルギー置き場
# Rule 4.7.1: エネルギーカードを置く領域です。
# Rule 4.7.2: エネルギー置き場はすべてのプレイヤーに対して
# Rule 4.7.3: エネルギー置き場のカードは向きを示す配置状態
# Rule 4.7.4: テキスト等で単に‘エネルギー’を参照する場合、そ
# Rule 4.8: メインデッキ置き場
# Rule 4.8.1: ゲーム開始時に自分のメインデッキを置く領域で
# Rule 4.8.2: メインデッキ置き場はすべてのプレイヤーに対して
# Rule 4.8.3: メインデッキ置き場のカードを他の領域に複数枚移
# Rule 4.8.4: テキスト等で単に‘デッキ’を参照する場合、それは
# Rule 4.9: エネルギーデッキ置き場
# Rule 4.9.1: ゲーム開始時に自分のエネルギーデッキを置く領
# Rule 4.9.2: エネルギーデッキ置き場はすべてのプレイヤーに
# Rule 4.9.3: エネルギーデッキ置き場のカードを他の領域に複
# Rule 4.9.4: テキスト等で単に‘エネルギーデッキ’を参照する場
# Rule 4.10: 成功ライブカード置き場
# Rule 4.10.1: ゲーム中に成功したライブのライブカードを置く領
# Rule 4.10.2: 成功ライブカード置き場はすべてのプレイヤーに
# Rule 4.11: 手札
# Rule 4.11.1: 各プレイヤーが未使用のカードを相手に見せずに
# Rule 4.11.2: 手札は非公開領域ですが、自分の手札のカード
# Rule 4.11.3: ‘手札にあるカードを（数値）枚’は、カードテキスト
# Rule 4.12: 控え室
# Rule 4.12.1: 各プレイヤーの使用済みのカードが置かれる領域
# Rule 4.12.2: 控え室は公開領域で、カードの順番は管理されま
# Rule 4.13: 除外領域
# Rule 4.13.1: ゲームから取り除かれたカードを置く領域です。
# Rule 4.13.2: 除外領域は原則として公開領域で、この領域の
# Rule 4.14: 解決領域
# Rule 4.14.1: ゲームの進行中に、能力やカードが一時的に置か
# Rule 4.14.2: 解決領域は公開領域で、カードの順番が管理され
# Rule 5: 特定行動
# Rule 5.1: 概要
# Rule 5.1.1: 特定行動とは、このゲームを行う際に特別な意味を
# Rule 5.2: アクティブにする/ウェイトにする
# Rule 5.2.1: カードを‘アクティブにする’または‘ウェイトにする’
# Rule 5.3: 表にする/裏にする
# Rule 5.3.1: カードを‘表にする’または‘裏にする’指示がある
# Rule 5.4: 置く
# Rule 5.4.1: カードを指定領域に‘置く’指示がある場合、その
# Rule 5.5: シャッフルする
# Rule 5.5.1: 指定されたカード群を‘シャッフルする’指示がある
# Rule 5.5.1.1: カード群として単に領域名が指定された場
# Rule 5.5.1.2: カード群のカードが0 枚または1 枚の状態
# Rule 5.6: 引く
# Rule 5.6.1: カードを‘1 枚引く’指示がある場合、指定プレイ
# Rule 5.6.2: カードを‘（数値）枚引く’指示がある場合、指定プレ
# Rule 5.6.3: カードを‘（数値）枚まで引く’指示がある場合、指定
# Rule 5.6.3.1: （数値）が0 以下である場合は、この指示を
# Rule 5.6.3.2: 指定プレイヤーはこの指示を終了することが
# Rule 5.6.3.3: 指定プレイヤーはカードを1 枚引きます。
# Rule 5.6.3.4: この指示により5.6.3.3 を実行した回数が（数
# Rule 5.7: 上から見る
# Rule 5.7.1: ‘メインデッキ置き場を上から（数値）枚見る’指示が
# Rule 5.7.2: ‘メインデッキ置き場を上から（数値）枚まで見る’指
# Rule 5.7.2.1: （数値）が0 以下である場合は、この指示を
# Rule 5.7.2.2: 枚数として1 を指定します。
# Rule 5.7.2.3: 指定プレイヤーはこの指示を終了することが
# Rule 5.7.2.4: 指定プレイヤーは、メインデッキ置き場の一
# Rule 5.7.2.5: この指示により5.7.2.4 を実行した回数が（数
# Rule 5.8: 入れ替える
# Rule 5.8.1: あるカードと別なカードを‘入れ替える’指示がある
# Rule 5.8.2: 何らかの理由で、入れ替える指示の実行時にいず
# Rule 5.9.1: あるプレイヤーが’
# Rule 5.9.1.1: ‘
# Rule 5.10: （エネルギーをメンバーの）下に置く
# Rule 5.10.1: あるエネルギーカードをあるメンバーの‘下に置く’
# Rule 6: ゲームの準備
# Rule 6.1: デッキの準備
# Rule 6.1.1: 各プレイヤーは、ゲームの開始前に自身のカードに
# Rule 6.1.1.1: メインデッキは、メンバーカード48 枚ちょうど
# Rule 6.1.1.2: メインデッキには、カードナンバーが同一で
# Rule 6.1.1.3: エネルギーデッキは、エネルギーカード12
# Rule 6.1.2: デッキの構築条件に関する常時能力は、上記の
# Rule 6.2: ゲーム前の手順
# Rule 6.2.1: ゲームの開始前に、各プレイヤーは以下の手順を
# Rule 6.2.1.1: このゲームで使用する自身のデッキを提示
# Rule 6.2.1.2: 各プレイヤーは自身のメインデッキを自身の
# Rule 6.2.1.3: 各プレイヤーは自身のエネルギーデッキを
# Rule 6.2.1.4: 各プレイヤーは無作為にどちらのプレイヤー
# Rule 6.2.1.5: 各プレイヤーは自身のメインデッキ置き場の
# Rule 6.2.1.6: 先攻プレイヤーから順に、各プレイヤーは自
# Rule 6.2.1.7: 各プレイヤーは自身のエネルギーデッキ置
# Rule 7: ゲームの進行
# Rule 7.1: 概要
# Rule 7.1.1: ゲームは‘ターン’と呼ばれる手順を繰り返すことで
# Rule 7.1.2: 各ターンは、‘先攻通常フェイズ’、‘後攻通常フェイ
# Rule 7.2: アクティブプレイヤー
# Rule 7.2.1: ゲーム中のフェイズにおいて、手番プレイヤーを指
# Rule 7.2.1.1: 手番プレイヤーを指定するフェイズ中は、手
# Rule 7.2.1.2: 手番プレイヤーを指定しないフェイズ中は、
# Rule 7.2.2: アクティブプレイヤーでないもう一方のプレイヤーは
# Rule 7.3: 通常フェイズ
# Rule 7.3.1: 通常フェイズとは、いずれかのプレイヤーが一連の
# Rule 7.3.2: 各通常フェイズでは手番プレイヤーを1 人指定し、
# Rule 7.3.2.1: 通常フェイズには、先攻プレイヤーが手番プ
# Rule 7.3.3: 通常フェイズでは、‘アクティブフェイズ’（7.4）、‘エ
# Rule 7.4: アクティブフェイズ
# Rule 7.4.1: 手番プレイヤーは、自身のエネルギー置き場とメン
# Rule 7.4.2: ‘ターンの始めに’および‘アクティブフェイズの始め
# Rule 7.4.3: チェックタイミングが発生します。このチェックタイミ
# Rule 7.5: エネルギーフェイズ
# Rule 7.5.1: ‘エネルギーフェイズの始めに’の誘発条件が発生
# Rule 7.5.2: 手番プレイヤーは、自身のエネルギーデッキの一
# Rule 7.5.3: チェックタイミングが発生します。このチェックタイミ
# Rule 7.6: ドローフェイズ
# Rule 7.6.1: ‘ドローフェイズの始めに’の誘発条件が発生し、
# Rule 7.6.2: 手番プレイヤーはカードを1 枚引きます。
# Rule 7.6.3: チェックタイミングが発生します。このチェックタイミ
# Rule 7.7: メインフェイズ
# Rule 7.7.1: ‘メインフェイズの始めに’の誘発条件が発生し、
# Rule 7.7.2: 手番プレイヤーにプレイタイミング（9.5.2）が与えら
# Rule 7.7.2.1: 自分のカードが持つ起動能力を1 つ選び、
# Rule 7.7.2.2: 自分の手札のメンバーカードを1 枚選び、そ
# Rule 7.7.3: メインフェイズが終了します。
# Rule 7.8: ライブフェイズ
# Rule 7.8.1: 両プレイヤーはライブフェイズを実行します。詳しく
# Rule 8: ライブフェイズ
# Rule 8.1: 概要
# Rule 8.1.1: ライブフェイズでは、両プレイヤーが手札のライブ
# Rule 8.1.2: ライブフェイズでは、‘ライブカードセットフェイズ’
# Rule 8.2: ライブカードセットフェイズ
# Rule 8.2.1: ‘ライブフェイズの始めに’および‘ライブカードセット
# Rule 8.2.2: 先攻プレイヤーは、自身の手札のカードを3 枚まで
# Rule 8.2.3: チェックタイミングが発生します。
# Rule 8.2.4: 後攻プレイヤーは、自身の手札のカードを3 枚まで
# Rule 8.2.5: チェックタイミングが発生します。このチェックタイミ
# Rule 8.3: パフォーマンスフェイズ
# Rule 8.3.1: パフォーマンスフェイズとは、いずれかのプレイ
# Rule 8.3.2: 各パフォーマンスフェイズでは手番プレイヤーを1
# Rule 8.3.2.1: パフォーマンスフェイズには、先攻プレイ
# Rule 8.3.3: 手番プレイヤーの自動能力の‘パフォーマンスフェ
# Rule 8.3.4: 手番プレイヤーは自身のライブカード置き場のカー
# Rule 8.3.4.1: 手番プレイヤーが‘ライブできない’状態であ
# Rule 8.3.5: チェックタイミングが発生します。
# Rule 8.3.6: この時点で手番プレイヤーのライブカード置き場に
# Rule 8.3.7: 手番プレイヤーのライブカード置き場にライブカード
# Rule 8.3.8: ‘ライブ開始時’の事象が発生します（11.4）。
# Rule 8.3.9: チェックタイミングが発生します。
# Rule 8.3.10: 手番プレイヤーは、自身のアクティブ状態なメン
# Rule 8.3.11: 手番プレイヤーは、自身のメインデッキの一番上
# Rule 8.3.12: 手番プレイヤーは解決領域に置かれているすべ
# Rule 8.3.13: チェックタイミングが発生します。
# Rule 8.3.14: 手番プレイヤーは自身のすべてのメンバーのハー
# Rule 8.3.15: 手番プレイヤーはライブカード置き場の各ライブ
# Rule 8.3.15.1: 現在のライブ所有ハートにより、そのライブ
# Rule 8.3.15.1.1: その際、各
# Rule 8.3.15.1.2: これによりそのライブカードの必要
# Rule 8.3.16: 前述の手順によりいずれかのライブカードの必要
# Rule 8.3.17: チェックタイミングが発生します。このチェックタイミ
# Rule 8.4: ライブ勝敗判定フェイズ
# Rule 8.4.1: ‘ライブ判定フェイズの始めに’の誘発条件が発生
# Rule 8.4.2: ライブカード置き場にカードがあるプレイヤーは、自
# Rule 8.4.2.1: その際、各プレイヤーは自身のエールの
# Rule 8.4.3: ライブの合計スコアを比較する場合、それは以下の
# Rule 8.4.3.1: 両方のプレイヤーのどちらのライブカード置
# Rule 8.4.3.2: 一方のプレイヤーのライブカード置き場に
# Rule 8.4.3.3: 両方のプレイヤーのライブカード置き場に
# Rule 8.4.4: ライブカード置き場にカードがあるプレイヤーは、ラ
# Rule 8.4.5: チェックタイミングが発生します。
# Rule 8.4.6: 合計スコアを比較し、ライブに勝利したプレイヤーを
# Rule 8.4.6.1: 両方のプレイヤーのどちらのライブカード置
# Rule 8.4.6.2: いずれかのプレイヤーのライブカード置き場
# Rule 8.4.7: ライブに勝利したプレイヤーは、自身のライブカード
# Rule 8.4.7.1: 両方のプレイヤーが勝利している場合
# Rule 8.4.8: 各プレイヤーは、自身のライブ置き場に残っている
# Rule 8.4.9: チェックタイミングが発生します。
# Rule 8.4.10: ‘ターンの終わりに’で示されている誘発条件のう
# Rule 8.4.11: チェックタイミングが発生します。このチェックタイミ
# Rule 8.4.12: この時点で、8.4.11 のチェックタイミングで自動能
# Rule 8.4.13: 8.4.7 において、一方のプレイヤーのみが成功ライ
# Rule 8.4.14: このターンを終了します。
# Rule 9: カードや能力のプレイと解決
# Rule 9.1: 能力の種別
# Rule 9.1.1: 能力は、起動能力、自動能力、常時能力の3 種類
# Rule 9.1.1.1: 起動能力とは、プレイタイミングが与えられ
# Rule 9.1.1.1.1: 起動能力は、カード上では‘
# Rule 9.1.1.2: 自動能力とは、その能力に示された事象が
# Rule 9.1.1.2.1: 自動能力は、カード上では‘
# Rule 9.1.1.3: 常時能力とは、その能力が有効な期間、常
# Rule 9.1.1.3.1: 常時能力は、カード上では‘
# Rule 9.2: 効果の種別
# Rule 9.2.1: 効果は‘単発効果’‘継続効果’‘置換効果’の3 種
# Rule 9.2.1.1: ‘単発効果’とは、解決中にその指示を実行
# Rule 9.2.1.2: ‘継続効果’とは、一定の期限の間（期間が
# Rule 9.2.1.3: ‘置換効果’とは、ゲーム中にある事象が発
# Rule 9.2.1.3.1: 能力に‘（行動A）する時、かわりに（行
# Rule 9.2.1.3.2: 能力に‘（行動A）する時、かわりに[選
# Rule 9.3: 有効な能力と無効な能力
# Rule 9.3.1: 何らかの効果により、特定の効果が‘有効’であっ
# Rule 9.3.2: 何らかの効果の一部あるいは全部が特定の条件
# Rule 9.3.3: 何らかの効果の一部あるいは全部が特定の条件
# Rule 9.3.4: 能力は原則として以下の条件で有効になります。
# Rule 9.3.4.1: 特定の領域や特定の状況でのプレイまたは
# Rule 9.3.4.1.1: あるカードのプレイ時やそのカードを特
# Rule 9.3.4.2: カードタイプがメンバーであるカードの能力
# Rule 9.3.4.3: カードタイプがライブであるカードの能力は、
# Rule 9.4: コストと支払い
# Rule 9.4.1: 起動能力や自動能力の先頭に、‘：’（コロン）の手
# Rule 9.4.2: ‘コストを支払う’とは’コストで示された行動を実行
# Rule 9.4.2.1: コストに複数の行動がある場合、テキストの
# Rule 9.4.2.2: コストのうち一部または全部を支払うことが
# Rule 9.4.3: コストのうち
# Rule 9.5: チェックタイミングとプレイタイミング
# Rule 9.5.1: チェックタイミングとは、ゲーム中で発生したルール
# Rule 9.5.1.1: チェックタイミングにおいては、まずルール処
# Rule 9.5.2: プレイタイミングとは、指定されたプレイヤーが能動
# Rule 9.5.3: チェックタイミングが発生した場合、ゲームは以下
# Rule 9.5.3.1: 現在処理を行うべきルール処理すべてを同
# Rule 9.5.3.2: プレイヤーがマスターであるいずれかの自
# Rule 9.5.3.3: 非アクティブプレイヤーがマスターであるい
# Rule 9.5.3.4: チェックタイミングを終了します。
# Rule 9.5.4: いずれかのプレイヤーにプレイタイミングが発生し
# Rule 9.5.4.1: チェックタイミングが発生します。チェックタイ
# Rule 9.5.4.2: プレイタイミングが実際にそのプレイヤーに
# Rule 9.5.4.3: プレイタイミングを与えられたプレイヤーが
# Rule 9.6: プレイと解決
# Rule 9.6.1: 起動能力や自動能力や手札のカードは、プレイす
# Rule 9.6.2: カードや能力をプレイする場合は、以下の手順に従
# Rule 9.6.2.1: プレイする能力や手札のカードを指定しま
# Rule 9.6.2.1.1: プレイするのがカードである場合、それ
# Rule 9.6.2.1.2: の処理を行います。
# Rule 9.6.2.1.2.1: その際、このターンにステージで
# Rule 9.6.2.1.3: プレイするのが能力である場合、その
# Rule 9.6.2.2: カードや能力に何らかの選択が必要である
# Rule 9.6.2.3: プレイするためのコストがある場合、そのコ
# Rule 9.6.2.3.1: プレイするのがメンバーのカードである
# Rule 9.6.2.3.2: メンバーをプレイする際、支払うべき
# Rule 9.6.2.3.2.1: これによりコストを減らす処理を
# Rule 9.6.2.4: カードや能力の解決を行います。
# Rule 9.6.2.4.1: プレイしたのがメンバーである場合、そ
# Rule 9.6.2.4.2: プレイしたのが起動能力や自動能力で
# Rule 9.6.2.4.2.1: 能力の解決によってメンバーカー
# Rule 9.6.3: カードや能力に’～選び’や’～選ぶ’と書かれてい
# Rule 9.6.3.1: 選ぶ数が指定されている場合、それが可能
# Rule 9.6.3.1.1: 選ぶ数が’～まで選び’や’～まで選
# Rule 9.6.3.1.2: 選ぶ数が指定されている場合に、指定
# Rule 9.6.3.1.3: 選ぶ数が指定されている場合に、目標
# Rule 9.6.3.1.4: 選ぶものが公開されていない非公開領
# Rule 9.7: 自動能力の処理
# Rule 9.7.1: 自動能力とは、特定の誘発条件が発生したときに、
# Rule 9.7.2: なんらかの自動能力の誘発条件が満たされた場
# Rule 9.7.2.1: 自動能力の誘発条件が複数回満たされた
# Rule 9.7.3: チェックタイミングが発生した段階で、自動能力のプ
# Rule 9.7.3.1: 待機状態の自動能力のプレイは強制で、プ
# Rule 9.7.3.1.1: 自動能力が任意でコストを支払うことに
# Rule 9.7.3.2: 選んだ待機状態の自動能力をプレイできな
# Rule 9.7.3.2.1: 自動能力が任意でコストを支払うことに
# Rule 9.7.4: あるカードが領域を移動することを誘発条件とする
# Rule 9.7.4.1: 領域移動誘発による自動能力が、その能力
# Rule 9.7.4.1.1: カードが公開領域から非公開領域、あ
# Rule 9.7.4.1.2: カードがステージからそれ以外の領域
# Rule 9.7.4.1.3: 上記に示された以外の、公開領域から
# Rule 9.7.4.2: あるカードが領域移動誘発能力を持ち、そ
# Rule 9.7.5: なんらかの効果により、以降の特定の時点で誘発
# Rule 9.7.5.1: 時限誘発は、特に期限が示されていないか
# Rule 9.7.6: 自動能力が、特定の事項が発生したことではなく、
# Rule 9.7.6.1: 状態誘発は、その状態が発生したときに1
# Rule 9.7.7: 待機状態の自動能力のプレイ時に、その自動能力
# Rule 9.8: 単発効果の処理
# Rule 9.8.1: 単発効果を実行するよう求められた場合、そこに指
# Rule 9.9: 継続効果の処理
# Rule 9.9.1: なんらかの継続効果が存在する状態でカードの情
# Rule 9.9.1.1: カード自身に表記されている情報が、常に基
# Rule 9.9.1.2: 次に、能力を与える/失わせる/有効にする/
# Rule 9.9.1.3: 次に、継続効果のうち情報の数値を変更す
# Rule 9.9.1.4: 次に、継続効果のうち情報の数値を特定の
# Rule 9.9.1.4.1: ハートやブレードの個数を特定の数に
# Rule 9.9.1.5: 次に、継続効果のうち情報の数値を変更す
# Rule 9.9.1.5.1: ハートやブレードの個数を加減算する
# Rule 9.9.1.6: 以上の9.9.1.2X-9.9.1.4 で適用順の前後が決
# Rule 9.9.1.7: 以上の9.9.1.2X-9.9.1.6 で適用順の前後が決
# Rule 9.9.1.7.1: 継続効果の発生源が常時能力である
# Rule 9.9.1.7.2: それ以外の能力の場合は、それがプレ
# Rule 9.9.2: 常時能力以外で発生している継続効果は、その能
# Rule 9.9.3: 特定の領域におけるカードの情報を変更する継続
# Rule 9.9.3.1: 特定の情報を持つカードが領域に入ることを
# Rule 9.10: 置換効果の処理
# Rule 9.10.1: 置換効果が発生している場合、その置換効果の
# Rule 9.10.1.1: これにより、置換された元の事象はまったく
# Rule 9.10.2: 同一の事象に対し複数の置換効果が発生してい
# Rule 9.10.2.1: 影響を受ける事象がカードや能力である場
# Rule 9.10.2.2: 影響を受ける事象がゲーム中の行動であ
# Rule 9.10.2.3: 同一の事象に対しては、各置換効果は最
# Rule 9.10.3: 置換効果が選択型置換効果（’～する時、かわり
# Rule 9.11: 最終情報
# Rule 9.11.1: ある効果が特定のカードの情報や状態を参照して
# Rule 9.12: 発生源
# Rule 9.12.1: 能力や効果により、ある効果の発生源を求めるこ
# Rule 9.12.2: 能力の発生源とは、その能力を持つカード、また
# Rule 10: ルール処理
# Rule 10.1: ルール処理の基本
# Rule 10.1.1: ルール処理とは、ゲームにおいて特定の事象が
# Rule 10.1.2: ルール処理は、リフレッシュ（10.2）を除き、チェック
# Rule 10.1.3: ルール処理が複数同時に実行を求められる場
# Rule 10.2: リフレッシュ
# Rule 10.2.1: リフレッシュはチェックタイミングにかぎらず、ゲー
# Rule 10.2.2: 以下のいずれかの条件を満たすとき、リフレッシュ
# Rule 10.2.2.1: いずれかのプレイヤーのメインデッキ置き
# Rule 10.2.2.2: メインデッキ置き場を上から見る指示があ
# Rule 10.2.3: リフレッシュを行うプレイヤーは、自身の控え室の
# Rule 10.2.4: 両方のプレイヤーが同時にリフレッシュを行う条件
# Rule 10.3: 勝利処理
# Rule 10.3.1: いずれかのプレイヤーの勝利ライブカード置き場
# Rule 10.4: 重複メンバー処理
# Rule 10.4.1: いずれかのプレイヤーの1 つのメンバーエリアに
# Rule 10.5: 不正カード処理
# Rule 10.5.1: いずれかのプレイヤーのライブカード置き場にライ
# Rule 10.5.2: いずれかのエネルギー置き場にエネルギーでない
# Rule 10.5.3: いずれかのメンバーエリアに、上に重なっているメ
# Rule 10.5.4: 上記のいずれかの処理において、控え室に置く
# Rule 10.6: 不正解決領域処理
# Rule 10.6.1: 解決領域に現在プレイ中または解決中であるまた
# Rule 11: キーワードとキーワード能力
# Rule 11.1: 概要
# Rule 11.1.1: キーワードとは、特定の処理を行う能力を簡略表
# Rule 11.1.2: 自動能力を意味するキーワード能力において、
# Rule 11.1.3: 能力の中には’
# Rule 11.2: ターン1 回
# Rule 11.2.2: キーワード
# Rule 11.2.3: ’
# Rule 11.3: 登場
# Rule 11.3.1: [Icon] は、メンバーがメンバーエリアに置かれた
# Rule 11.3.2: ‘
# Rule 11.4: ライブ開始時
# Rule 11.4.1: [Icon] は、ライブが開始されたことを誘
# Rule 11.4.2: ‘
# Rule 11.4.2.1: パフォーマンスフェイズ中、手番プレイヤー
# Rule 11.5: ライブ成功時
# Rule 11.5.1: [Icon] は、ライブが成功したことを誘発
# Rule 11.5.2: ‘
# Rule 11.6: センター
# Rule 11.6.1: [Icon] は、能力のプレイの制限や、能力の誘
# Rule 11.6.2: キーワード
# Rule 11.6.3: キーワード
# Rule 11.6.4: キーワード
# Rule 11.7: 左サイド
# Rule 11.7.1: [Icon] は、能力のプレイの制限や、能力の誘
# Rule 11.7.2: キーワード
# Rule 11.7.3: キーワード
# Rule 11.7.4: キーワード
# Rule 11.8: 右サイド
# Rule 11.8.1: [Icon] は、能力のプレイの制限や、能力の誘
# Rule 11.8.2: キーワード
# Rule 11.8.3: キーワード
# Rule 11.8.4: キーワード
# Rule 11.9: ポジションチェンジ
# Rule 11.9.1: ポジションチェンジするとは、そのメンバーを今い
# Rule 11.9.2: メンバーを移動させた先のエリアにすでにメンバー
# Rule 11.10: フォーメーションチェンジ
# Rule 11.10.1: フォーメーションチェンジするとは、ステージにい
# Rule 11.10.2: この効果で1 つのエリアに2 人以上のメンバー
# Rule 12: その他
# Rule 12.1: 永久循環
# Rule 12.1.1: 何らかの処理を行う際に、ある行動を永久に実行
# Rule 12.1.1.1: アクティブプレイヤー（7.2）は、その循環行
# Rule 12.1.1.2: アクティブプレイヤーが何らかの行動を行
# Rule 12.1.1.3: 何らかの理由により、どちらのプレイヤーに
# Rule 2025: 年11 月21 日 ver. 1.04
# --- END OF INDEX ---
