
import sys
import os
import numpy as np
import unittest

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState, Phase, MemberCard, LiveCard, PlayerState, HeartColor
from game.ability import Ability, TriggerType, Effect, EffectType, TargetType, AbilityCostType, Condition, ConditionType

class TestScore4Abilities(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.p0 = self.state.players[0]
        self.p1 = self.state.players[1]
        
    def test_honoka_blade_buff(self):
        """Test Honoka Kosaka: Gain blades per success live (CONSTANT)"""
        # Ability: {{jyouji.png|常時}}自分の成功ライブカード置き場にあるカード1枚につき、{{icon_blade.png|ブレード}}を得る。
        effect = Effect(EffectType.ADD_BLADES, 1, TargetType.MEMBER_SELF, params={"multiplier": True, "per_live": True})
        ability = Ability(raw_text="常時...", trigger=TriggerType.CONSTANT, effects=[effect])
        
        # Setup Honoka on stage
        honoka = MemberCard(card_id=1, name="Honoka", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=3, abilities=[ability], group="ラブライブ！")
        self.state.member_db[1] = honoka
        self.p0.stage[0] = 1
        
        # 1. Initially 0 success lives
        self.p0.success_lives = []
        eff_blades = self.p0.get_effective_blades(0, self.state.member_db)
        self.assertEqual(eff_blades, 3, "Should have base 3 blades with 0 success lives")
        
        # 2. Add 2 success lives
        self.p0.success_lives = [1001, 1002]
        self.state.live_db[1001] = LiveCard(1001, "S1", 1, np.zeros(7))
        self.state.live_db[1002] = LiveCard(1002, "S2", 1, np.zeros(7))
        
        eff_blades = self.p0.get_effective_blades(0, self.state.member_db)
        # 3 base + 2 from success lives = 5
        self.assertEqual(eff_blades, 5, "Should have 5 blades (3 + 2 success lives)")

    def test_nico_score_bonus(self):
        """Test Nico Yazawa: Score bonus +1 if 25 μ's cards in discard (ON_LIVE_START)"""
        # Ability: {{live_start.png|ライブ開始時}}自分の控え室に『μ's』のカードが25枚以上ある場合、ライブ終了時まで、「ライブの合計スコアを＋１する。」を得る。
        cond = Condition(ConditionType.COUNT_GROUP, params={"group": "ラブライブ！", "zone": "DISCARD", "min": 25})
        effect = Effect(EffectType.BOOST_SCORE, 1, TargetType.SELF, params={"until": "live_end"})
        ability = Ability(raw_text="ライブ開始時...", trigger=TriggerType.ON_LIVE_START, effects=[effect], conditions=[cond])
        
        # Setup Nico on stage
        nico = MemberCard(card_id=9, name="Nico", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1, abilities=[ability], group="ラブライブ！")
        self.state.member_db[9] = nico
        self.p0.stage[0] = 9
        
        # 1. Discard has 24 cards
        self.p0.discard = [i for i in range(24)]
        for i in range(24):
            self.state.member_db[i] = MemberCard(i, f"Card{i}", 1, np.zeros(6), np.zeros(6), 1, group="ラブライブ！")
            
        # Trigger live start (simplified)
        self.state._play_automatic_ability(0, ability, {"area": 0})
        self.assertEqual(self.p0.live_score_bonus, 0, "Should not gain score bonus with only 24 cards")
        
        # 2. Add 1 more for 25 cards
        self.p0.discard.append(24)
        self.state.member_db[24] = MemberCard(24, "Card24", 1, np.zeros(6), np.zeros(6), 1, group="ラブライブ！")
        
        self.state._play_automatic_ability(0, ability, {"area": 0})
        self.assertEqual(self.p0.live_score_bonus, 1, "Should gain score bonus with 25 cards")
        
        # 3. Test cleanup
        self.state._clear_expired_effects("LIVE_END")
        self.assertEqual(self.p0.live_score_bonus, 0, "Score bonus should be cleared after live")

    def test_ginko_draw(self):
        """Test Ginko Mozume: Draw (ON_PLAY)"""
        # Ability: 登場：1枚引く。
        effect = Effect(EffectType.DRAW, 1, TargetType.SELF)
        ability = Ability(raw_text="登場...", trigger=TriggerType.ON_PLAY, effects=[effect])
        
        ginko = MemberCard(card_id=20, name="Ginko", cost=1, hearts=np.zeros(6), blade_hearts=np.zeros(6), blades=1, abilities=[ability], group="蓮ノ空")
        self.state.member_db[20] = ginko
        
        self.p0.main_deck = [101, 102]
        self.p0.hand = []
        
        self.state._play_automatic_ability(0, ability, {"area": 1})
        self.assertEqual(len(self.p0.hand), 1)
        self.assertEqual(self.p0.hand[0], 101)

if __name__ == "__main__":
    unittest.main()
