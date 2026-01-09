
import pytest
import numpy as np
from engine.game.game_state import GameState, Phase, MemberCard, LiveCard, PlayerState, HeartColor
from engine.game.ability import Ability, TriggerType, Effect, EffectType, TargetType, AbilityCostType, Condition, ConditionType

@pytest.fixture
def game_state():
    state = GameState()
    # Reset class variables
    GameState.member_db = {}
    GameState.live_db = {}
    return state

def test_honoka_blade_buff(game_state):
    """Test Honoka Kosaka: Gain blades per success live (CONSTANT)"""
    state = game_state
    p0 = state.players[0]
    
    # Ability: {{jyouji.png|常時}}自分の成功ライブカード置き場にあるカード1枚につき、{{icon_blade.png|ブレード}}を得る。
    effect = Effect(EffectType.ADD_BLADES, 1, TargetType.MEMBER_SELF, params={"multiplier": True, "per_live": True})
    ability = Ability(raw_text="常時...", trigger=TriggerType.CONSTANT, effects=[effect])
    
    # Setup Honoka on stage
    honoka = MemberCard(card_id=1, card_no="HON-01", name="Honoka", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(7), blades=3, abilities=[ability], group="ラブライブ！")
    state.member_db[1] = honoka
    p0.stage[0] = 1
    
    # 1. Initially 0 success lives
    p0.success_lives = []
    eff_blades = p0.get_effective_blades(0, state.member_db)
    assert eff_blades == 3, "Should have base 3 blades with 0 success lives"
    
    # 2. Add 2 success lives
    p0.success_lives = [1001, 1002]
    state.live_db[1001] = LiveCard(1001, "L-1001", "S1", 1, np.zeros(7))
    state.live_db[1002] = LiveCard(1002, "L-1002", "S2", 1, np.zeros(7))
    
    eff_blades = p0.get_effective_blades(0, state.member_db)
    # 3 base + 2 from success lives = 5
    assert eff_blades == 5, "Should have 5 blades (3 + 2 success lives)"

def test_nico_score_bonus(game_state):
    """Test Nico Yazawa: Score bonus +1 if 25 μ's cards in discard (ON_LIVE_START)"""
    state = game_state
    p0 = state.players[0]
    
    # Ability: {{live_start.png|ライブ開始時}}自分の控え室に『μ's』のカードが25枚以上ある場合、ライブ終了時まで、「ライブの合計スコアを＋１する。」を得る。
    cond = Condition(ConditionType.COUNT_GROUP, params={"group": "ラブライブ！", "zone": "DISCARD", "min": 25})
    effect = Effect(EffectType.BOOST_SCORE, 1, TargetType.SELF, params={"until": "live_end"})
    ability = Ability(raw_text="ライブ開始時...", trigger=TriggerType.ON_LIVE_START, effects=[effect], conditions=[cond])
    
    # Setup Nico on stage
    nico = MemberCard(card_id=9, card_no="NICO-01", name="Nico", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1, abilities=[ability], group="ラブライブ！")
    state.member_db[9] = nico
    p0.stage[0] = 9
    
    # 1. Discard has 24 cards
    p0.discard = [i for i in range(24)]
    for i in range(24):
        state.member_db[i] = MemberCard(i, f"TEST-{i}", f"Card{i}", 1, np.zeros(6), np.zeros(7), 1, group="ラブライブ！")
        
    # Trigger live start (simplified)
    state._play_automatic_ability(0, ability, {"area": 0})
    assert p0.live_score_bonus == 0, "Should not gain score bonus with only 24 cards"
    
    # 2. Add 1 more for 25 cards
    p0.discard.append(24)
    state.member_db[24] = MemberCard(24, "TEST-24", "Card24", 1, np.zeros(6), np.zeros(7), 1, group="ラブライブ！")
    
    state._play_automatic_ability(0, ability, {"area": 0})
    assert p0.live_score_bonus == 1, "Should gain score bonus with 25 cards"
    
    # 3. Test cleanup
    state._clear_expired_effects("LIVE_END")
    assert p0.live_score_bonus == 0, "Score bonus should be cleared after live"

def test_ginko_draw(game_state):
    """Test Ginko Mozume: Draw (ON_PLAY)"""
    state = game_state
    p0 = state.players[0]
    
    # Ability: 登場：1枚引く。
    effect = Effect(EffectType.DRAW, 1, TargetType.SELF)
    ability = Ability(raw_text="登場...", trigger=TriggerType.ON_PLAY, effects=[effect])
    
    ginko = MemberCard(card_id=20, card_no="GIN-01", name="Ginko", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1, abilities=[ability], group="蓮ノ空")
    state.member_db[20] = ginko
    
    p0.main_deck = [101, 102]
    p0.hand = []
    
    state._play_automatic_ability(0, ability, {"area": 1})
    assert len(p0.hand) == 1
    assert p0.hand[0] == 101
