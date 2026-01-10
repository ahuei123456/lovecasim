"""
Test Real Card: PL!-sd1-002-SD (絢瀬 絵里)

Card Text:
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。

Expected Behavior:
- Trigger: ACTIVATED (can be used during Main Phase)
- Cost: Sacrifice this member (move from stage to discard)
- Effect: Add 1 Member card from discard to hand

FAQ (Q79):
- The ability can be used the same turn the member was played
- After sacrificing, the area becomes empty and another member can be played there
"""

import os
from typing import Any

import pytest

from engine.game.data_loader import CardDataLoader
from engine.game.game_state import GameState, LiveCard, MemberCard, Phase
from engine.models.ability import AbilityCostType, EffectType, TriggerType


class TestEriSacrificeAbility:
    """Test 絢瀬 絵里 (PL!-sd1-002-SD) sacrifice-recover ability."""

    member_db: dict[int, MemberCard]
    live_db: dict[int, LiveCard]
    energy_db: dict[int, Any]
    eli_card_id: int

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self):
        """Load real card data once for all tests."""
        loader = CardDataLoader(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/cards_compiled.json"))
        )
        self.__class__.member_db, self.__class__.live_db, self.__class__.energy_db = loader.load()

        # Find Eli's card ID
        eli_id = next((cid for cid, m in self.__class__.member_db.items() if m.card_no == "PL!-sd1-002-SD"), None)
        assert eli_id is not None
        self.__class__.eli_card_id = eli_id

    @pytest.fixture(autouse=True)
    def setup(self):
        # Assign databases to class level (as done in server.py)
        GameState.member_db = self.__class__.member_db
        GameState.live_db = self.__class__.live_db

        self.game = GameState(verbose=False)
        self.p0 = self.game.players[0]
        self.p1 = self.game.players[1]

        self.game.phase = Phase.MAIN
        self.game.current_player = 0

    def test_eli_ability_is_parsed_correctly(self):
        """Verify Eli's ability is parsed with correct trigger/cost/effect."""
        eli = self.__class__.member_db[self.__class__.eli_card_id]

        assert len(eli.abilities) >= 1, f"Eli should have at least 1 ability, found {len(eli.abilities)}"

        ability = eli.abilities[0]

        # Check trigger
        assert ability.trigger == TriggerType.ACTIVATED, f"Trigger should be ACTIVATED, got {ability.trigger}"

        # Check cost (sacrifice self)
        sacrifice_cost = next((c for c in ability.costs if c.type == AbilityCostType.SACRIFICE_SELF), None)
        assert sacrifice_cost is not None, "Should have SACRIFICE_SELF cost"

        # Check effect (recover member)
        recover_effect = next((e for e in ability.effects if e.effect_type == EffectType.RECOVER_MEMBER), None)
        assert recover_effect is not None, "Should have RECOVER_MEMBER effect"

    def test_eli_sacrifice_produces_correct_state_change(self):
        """Verify sacrificing Eli moves her to discard and allows recovery."""
        # Setup: Eli on stage, another member in discard
        self.p0.stage[0] = self.eli_card_id  # Eli in left area

        # Put a different member in discard for recovery
        other_member_id = next((cid for cid in self.__class__.member_db if cid != self.eli_card_id), None)
        assert other_member_id is not None
        self.p0.discard = [other_member_id]
        self.p0.hand = []

        initial_stage = self.p0.stage[0]

        # Verify Eli is on stage
        assert initial_stage == self.eli_card_id

        # Find the ability action (should be action 200 for left area ability)
        legal_mask = self.game.get_legal_actions()
        ability_action = 200  # ABILITY_LEFT = 200

        if legal_mask[ability_action]:
            # Execute ability
            new_state = self.game.step(ability_action)
            p0_new = new_state.players[0]

            # Eli should be moved to discard (sacrifice cost paid)
            assert self.eli_card_id in p0_new.discard, "Eli should be in discard after sacrifice"
            assert p0_new.stage[0] == -1, "Left stage area should be empty after sacrifice"

            # Check if a choice was created for which member to recover
            if new_state.pending_choices:
                choice_type, params = new_state.pending_choices[0]
                assert choice_type == "SELECT_FROM_DISCARD", "Should create SELECT_FROM_DISCARD choice"

                # The other member should be in the choices (but NOT Eli since she's just added)
                # Actually, Eli is now in discard too - the filter should be 'member'
                assert len(params["cards"]) > 0, "Should have at least 1 card to choose from"
        else:
            pytest.fail("Eli's ability action should be legal")

    def test_eli_cannot_recover_if_discard_empty(self):
        """If no members in discard, ability can still be used but no recovery."""
        # Setup: Eli on stage, NO members in discard
        self.p0.stage[0] = self.__class__.eli_card_id
        self.p0.discard = []  # Empty discard
        self.p0.hand = []
        # Ensure deck has cards so Rule 10.2 (Refresh) doesn't trigger
        self.p0.main_deck = [1, 2, 3]

        legal_mask = self.game.get_legal_actions()
        ability_action = 200

        # According to FAQ, ability CAN be used even with empty discard
        # (Similar cards have this ruling)
        # The sacrifice still happens, just no card to recover

        if legal_mask[ability_action]:
            new_state = self.game.step(ability_action)
            p0_new = new_state.players[0]

            # Eli should still be sacrificed
            assert self.__class__.eli_card_id in p0_new.discard, "Eli should be in discard even with no recovery target"


class TestHonokaConstantAbility:
    """Test 高坂 穂乃果 (PL!-sd1-001-SD) blade buff ability."""

    member_db: dict[int, MemberCard]
    live_db: dict[int, LiveCard]
    energy_db: dict[int, Any]
    honoka_card_id: int

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self):
        loader = CardDataLoader(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/cards_compiled.json"))
        )
        self.__class__.member_db, self.__class__.live_db, self.__class__.energy_db = loader.load()

        honoka_id = next((cid for cid, m in self.__class__.member_db.items() if m.card_no == "PL!-sd1-001-SD"), None)
        assert honoka_id is not None
        self.__class__.honoka_card_id = honoka_id

    @pytest.fixture(autouse=True)
    def setup(self):
        GameState.member_db = self.__class__.member_db
        GameState.live_db = self.__class__.live_db

        self.game = GameState(verbose=False)
        self.p0 = self.game.players[0]

    def test_honoka_constant_blade_buff(self):
        """Verify Honoka gains +1 blade per success live."""
        honoka = self.__class__.member_db[self.__class__.honoka_card_id]
        base_blades = honoka.blades

        # Setup: Honoka on stage
        self.p0.stage[1] = self.honoka_card_id  # Center stage

        # 0 success lives -> base blades
        effective_blades_0 = self.p0.get_effective_blades(1, self.__class__.member_db)

        # Add 2 success lives
        # Find any 2 live card IDs
        live_ids = list(self.live_db.keys())[:2]
        self.p0.success_lives = live_ids

        # Should now have base + 2 blades
        effective_blades_2 = self.p0.get_effective_blades(1, self.__class__.member_db)

        # The CONSTANT ability should add +1 blade per success live
        expected_increase = len(self.p0.success_lives)
        actual_increase = effective_blades_2 - effective_blades_0

        assert actual_increase == expected_increase, (
            f"Blades should increase by {expected_increase} with {len(self.p0.success_lives)} success lives, "
            f"but got increase of {actual_increase} (base:{base_blades}, before:{effective_blades_0}, after:{effective_blades_2})"
        )
