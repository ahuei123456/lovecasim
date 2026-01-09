
import numpy as np
import pytest

from engine.game.ability import (
    Ability,
    AbilityCostType,
    AbilityParser,
    Condition,
    ConditionType,
    Cost,
    Effect,
    EffectType,
    TriggerType,
)
from engine.game.game_state import GameState, LiveCard, MemberCard


@pytest.fixture
def game_state():
    state = GameState()
    # Reset variables
    GameState.member_db = {}
    GameState.live_db = {}
    return state

# --- Ability Parser Tests ---

def test_nico_dual_trigger():
    """Test PL!-PR-009-PR: Dual trigger ON_PLAY / ON_LIVE_START"""
    text = "{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。"
    abilities = AbilityParser.parse_ability_text(text)
    
    assert len(abilities) == 2, "Should parse into 2 abilities"
    assert abilities[0].trigger == TriggerType.ON_PLAY
    assert abilities[1].trigger == TriggerType.ON_LIVE_START
    
    for abi in abilities:
        assert len(abi.costs) == 1
        assert abi.costs[0].type == AbilityCostType.TAP_SELF
        assert len(abi.effects) == 1
        assert abi.effects[0].effect_type == EffectType.TAP_OPPONENT

def test_kanata_reveal_hand():
    """Test PL!N-PR-008-PR: Reveal hand cost + condition"""
    text = "{{kidou.png|起動}}{{turn1.png|ターン1回}}手札をすべて公開する：自分のステージにほかのメンバーがおり、かつこれにより公開した手札の中にライブカードがない場合、自分のデッキの上からカードを5枚見る。その中からライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。"
    abilities = AbilityParser.parse_ability_text(text)
    
    assert len(abilities) == 1
    abi = abilities[0]
    
    # Check Cost
    assert any(c.type == AbilityCostType.REVEAL_HAND_ALL for c in abi.costs), "Should have REVEAL_HAND_ALL cost"
    
    # Check Condition
    assert any(c.type == ConditionType.HAND_HAS_NO_LIVE for c in abi.conditions), "Should have HAND_HAS_NO_LIVE condition"
    
    # Check Effect
    assert abi.effects[0].effect_type == EffectType.LOOK_DECK
    assert abi.effects[0].value == 5

def test_ginko_parsing():
    """Test PL!N-PR-012-PR: Look 5, Choose 1 Member"""
    text = "【登場時】手札を1枚捨ててもよい：そうしたら、デッキの上から5枚見る。その中からメンバーを1枚まで公開し、手札に加える。残りを山札の一番下に望む順番で置く。"
    abilities = AbilityParser.parse_ability_text(text)
    assert len(abilities) == 1
    abi = abilities[0]
    
    # Check Effects chain
    # 1. Look Deck 5
    assert abi.effects[0].effect_type == EffectType.LOOK_DECK
    assert abi.effects[0].value == 5
    # 2. Look and Choose (Member)
    assert abi.effects[1].effect_type == EffectType.LOOK_AND_CHOOSE
    assert abi.effects[1].params.get('filter') == 'member', "Should capture member filter"
    # 3. Order Deck (Remainder to bottom)
    assert any(e.effect_type in (EffectType.ORDER_DECK, EffectType.MOVE_TO_DECK) for e in abi.effects), "Should handle remainder"

def test_honoka_parsing():
    """Test PL!-sd1-001-SD: Count Success Live Condition & Recover Live Effect"""
    text = "【登場時】自分の成功ライブカード置き場にカードが2枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。"
    abilities = AbilityParser.parse_ability_text(text)
    assert len(abilities) == 1
    abi = abilities[0]

    # Verify Trigger
    assert abi.trigger == TriggerType.ON_PLAY

    # Verify Condition
    assert len(abi.conditions) == 1
    assert abi.conditions[0].type == ConditionType.COUNT_SUCCESS_LIVE
    assert abi.conditions[0].params.get('min') == 2

    # Verify Effect
    assert len(abi.effects) == 1
    assert abi.effects[0].effect_type == EffectType.RECOVER_LIVE

# --- Execution Tests ---

def test_kanata_execution(game_state):
    """Test PL!N-PR-008-PR execution logic for Condition and Cost"""
    state = game_state
    p0 = state.players[0]
    
    # Create a mock ability
    abi = Ability(
        raw_text="Test Kanata",
        trigger=TriggerType.ACTIVATED,
        costs=[Cost(AbilityCostType.REVEAL_HAND_ALL)],
        conditions=[Condition(ConditionType.HAND_HAS_NO_LIVE)],
        effects=[Effect(EffectType.DRAW, 1)] # Simple effect to verify success
    )
    
    # Test Case 1: Hand has NO live cards -> Should Succeed
    p0.hand = [10, 11] # Assume member IDs
    GameState.member_db[10] = MemberCard(10, "M-01", "M1", 1, np.zeros(6), np.zeros(7), 1)
    GameState.member_db[11] = MemberCard(11, "M-02", "M2", 1, np.zeros(6), np.zeros(7), 1)
    
    # Verify condition
    assert state._check_condition(p0, abi.conditions[0]), "Condition HAND_HAS_NO_LIVE should be True (no lives)"
    
    # Test Case 2: Hand HAS live card -> Should Fail
    p0.hand.append(100)
    GameState.live_db[100] = LiveCard(100, "L-01", "L1", 1, np.zeros(7))
    
    assert not state._check_condition(p0, abi.conditions[0]), "Condition HAND_HAS_NO_LIVE should be False (has live)"
