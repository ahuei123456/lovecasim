import numpy as np
import pytest

from compiler.parser import AbilityParser
from engine.game.game_state import LiveCard, MemberCard
from engine.models.ability import Condition, ConditionType, EffectType, TriggerType

"""
Test for PL!S-pb1-001-R (高海千歌) condition:
Opponent hand >= Player hand + 2
"""


class TestChikaHandCondition:
    @pytest.fixture(autouse=True)
    def setup(self, game_state):
        self.game = game_state
        self.p0 = self.game.players[0]
        self.p1 = self.game.players[1]

        # Create a mock member cards
        for i in range(100, 110):
            self.game.member_db[i] = MemberCard(
                card_id=i,
                card_no=f"M{i}",
                name=f"Member {i}",
                cost=1,
                hearts=np.zeros(6, dtype=np.int32),
                blade_hearts=np.zeros(7, dtype=np.int32),
                blades=1,
                groups=[],
                units=[],
                img_path="",
            )

        # Create a mock live card for recovery
        self.game.live_db[200] = LiveCard(
            card_id=200,
            card_no="L200",
            name="Test Live",
            score=1,
            required_hearts=np.zeros(7, dtype=np.int32),
            img_path="",
        )

    def test_condition_met_opponent_has_more(self):
        """Opponent has 6 cards, player has 3 -> diff is 3 >= 2, should trigger"""
        self.p0.hand = [100, 101, 102]  # 3 cards
        self.p1.hand = [103, 104, 105, 106, 107, 108]  # 6 cards

        cond = Condition(ConditionType.OPPONENT_HAND_DIFF, {"diff": 2})
        result = self.game._check_condition(self.p0, cond)

        assert result, "Condition should be MET when opponent has 3 more cards (6 - 3 = 3 >= 2)"

    def test_condition_not_met_opponent_has_fewer(self):
        """Opponent has 3 cards, player has 5 -> diff is -2, NOT >= 2"""
        self.p0.hand = [100, 101, 102, 103, 104]  # 5 cards
        self.p1.hand = [105, 106, 107]  # 3 cards

        cond = Condition(ConditionType.OPPONENT_HAND_DIFF, {"diff": 2})
        result = self.game._check_condition(self.p0, cond)

        assert not result, "Condition should NOT be met when opponent has fewer cards"

    def test_condition_not_met_exactly_one_more(self):
        """Opponent has 4 cards, player has 3 -> diff is 1, NOT >= 2"""
        self.p0.hand = [100, 101, 102]  # 3 cards
        self.p1.hand = [103, 104, 105, 106]  # 4 cards

        cond = Condition(ConditionType.OPPONENT_HAND_DIFF, {"diff": 2})
        result = self.game._check_condition(self.p0, cond)

        assert not result, "Condition should NOT be met when opponent has only 1 more card"

    def test_condition_met_exactly_two_more(self):
        """Opponent has 5 cards, player has 3 -> diff is 2 == 2, should trigger"""
        self.p0.hand = [100, 101, 102]  # 3 cards
        self.p1.hand = [103, 104, 105, 106, 107]  # 5 cards

        cond = Condition(ConditionType.OPPONENT_HAND_DIFF, {"diff": 2})
        result = self.game._check_condition(self.p0, cond)

        assert result, "Condition should be MET when opponent has exactly 2 more cards"

    def test_parser_extracts_condition(self):
        """Test that the parser correctly extracts the condition from card text"""
        ability_text = "{{toujyou.png|登場}}相手の手札の枚数が自分より2枚以上多い場合、自分の控え室からライブカードを1枚手札に加える。"
        abilities = AbilityParser.parse_ability_text(ability_text)

        assert len(abilities) == 1
        ability = abilities[0]

        assert ability.trigger == TriggerType.ON_PLAY

        # Check condition
        cond_found = False
        for cond in ability.conditions:
            if cond.type == ConditionType.OPPONENT_HAND_DIFF:
                assert cond.params.get("diff") == 2
                cond_found = True
                break
        assert cond_found, "OPPONENT_HAND_DIFF condition should be parsed"

        # Check effect
        eff_found = False
        for eff in ability.effects:
            if eff.effect_type == EffectType.RECOVER_LIVE:
                eff_found = True
                break
        assert eff_found, "RECOVER_LIVE effect should be parsed"
