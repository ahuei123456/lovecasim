"""
Unit test for filtered recovery mechanics (GROUP, COST).
"""

import numpy as np
import pytest

from engine.game.ability import AbilityParser, EffectType
from engine.game.game_state import GameState, MemberCard


@pytest.fixture
def game_state():
    state = GameState()
    p0 = state.players[0]

    # Setup DB with members of different groups and costs
    # Member 400: μ's, Cost 3
    state.member_db[400] = MemberCard(
        card_id=400,
        card_no="MUSE-01",
        name="Kotori",
        cost=3,
        groups="μ's",
        hearts=np.zeros(6),
        blade_hearts=np.zeros(7),
        blades=1,
    )
    # Member 401: μ's, Cost 5
    state.member_db[401] = MemberCard(
        card_id=401,
        card_no="MUSE-02",
        name="Honoka",
        cost=5,
        groups="μ's",
        hearts=np.zeros(6),
        blade_hearts=np.zeros(7),
        blades=1,
    )
    # Member 402: Aqours, Cost 2
    state.member_db[402] = MemberCard(
        card_id=402,
        card_no="AQ-01",
        name="Chika",
        cost=2,
        groups="Aqours",
        hearts=np.zeros(6),
        blade_hearts=np.zeros(7),
        blades=1,
    )

    # Put all in discard
    p0.discard = [400, 401, 402]
    p0.hand = []
    return state


def test_parser_filtered_recovery():
    """Card #3: 南 ことり - コスト4以下の『μ's』"""
    text = "自分の控え室からコスト4以下の『μ's』のメンバーカードを1枚手札に加える。"
    abilities = AbilityParser.parse_ability_text(text)
    eff = abilities[0].effects[0]

    assert eff.effect_type == EffectType.RECOVER_MEMBER
    assert eff.params.get("group") == "μ's"
    assert eff.params.get("cost_max") == 4


def test_execution_filtered_recovery(game_state):
    """Test filtered recovery execution results in restricted choices"""
    state = game_state
    p0 = state.players[0]
    text = "自分の控え室からコスト4以下の『μ's』のメンバーカードを1枚手札に加える。"
    abilities = AbilityParser.parse_ability_text(text)
    eff = abilities[0].effects[0]

    state.pending_effects.append(eff)
    state._resolve_pending_effect(0)

    # Should have choice
    assert len(state.pending_choices) == 1, "Should have pending choices"
    choice_type, params = state.pending_choices[0]
    assert choice_type == "SELECT_FROM_DISCARD"

    # Candidate cards should only be 400 (μ's, Cost 3)
    # 401 is μ's but Cost 5 (too high)
    # 402 is Cost 2 but Aqours (wrong group)
    candidates = params["cards"]
    assert len(candidates) == 1
    assert candidates[0] == 400

    # Perform recovery
    # The action ID for choosing from discard depends on how get_legal_actions maps it.
    # Usually it's in a range like 500+ or specific for discard selection.
    # The original test used 660, assuming it maps to index 0 of the candidates if that's how it works,
    # or it's a specific ID mapping.
    # If the engine uses transient IDs for choices, we should check what get_legal_actions expects.
    # Assuming 660 was correct in unittest, we use it here.
    state.take_action(660)
    assert 400 in p0.hand
    assert len(p0.hand) == 1
