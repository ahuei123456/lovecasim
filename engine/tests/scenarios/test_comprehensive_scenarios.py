import numpy as np
import pytest

from compiler.parser import AbilityParser
from engine.game.game_state import Condition, ConditionType, GameState, Group, MemberCard


class TestComprehensiveGroupLogic:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.game = GameState()
        self.p0 = self.game.players[0]

        # Setup DB with diverse groups
        groups = {
            100: "ラブライブ！",  # u's
            200: "ラブライブ！サンシャイン!!",  # Aqours
            300: "ラブライブ！虹ヶ咲学園スクールアイドル同好会",  # Nijigasaki
            400: "ラブライブ！スーパースター!!",  # Liella!
            500: "ラブライブ！蓮ノ空女学院スクールアイドルクラブ",  # Hasunosora
        }

        for cid, gname in groups.items():
            self.game.member_db[cid] = MemberCard(
                card_id=cid,
                card_no=f"M-{cid}",
                name=f"Member {cid}",
                cost=1,
                hearts=np.zeros(6),
                blade_hearts=np.zeros(7),
                blades=1,
                groups=[Group.from_japanese_name(gname)],
                units=[],
            )

    def test_alias_matching(self):
        """Test that short aliases map correctly to full group names."""
        aliases = [("μ's", 100), ("Aqours", 200), ("虹ヶ咲", 300), ("Liella!", 400), ("蓮ノ空", 500)]

        for alias, cid in aliases:
            # Clear stage
            self.p0.stage[:] = [-1, -1, -1]
            # Add member
            self.p0.stage[0] = cid

            cond = Condition(ConditionType.GROUP_FILTER, {"group": alias, "zone": "STAGE"})
            assert self.game._check_condition(self.p0, cond), f"Alias {alias} should match member {cid}"

            # Negative check
            self.p0.stage[0] = -1
            assert not self.game._check_condition(self.p0, cond), f"Alias {alias} should fail on empty stage"

    def test_zone_handling(self):
        """Verify checking different zones works correctly."""
        # Target Liella
        cond = Condition(ConditionType.GROUP_FILTER, {"group": "Liella!", "zone": "DISCARD"})

        self.p0.discard = [400]  # Liella member
        assert self.game._check_condition(self.p0, cond), "Should detect in Discard"

        self.p0.discard = [100]  # u's member
        assert not self.game._check_condition(self.p0, cond), "Should NOT detect wrong group in Discard"

        # Hand
        cond_hand = Condition(ConditionType.GROUP_FILTER, {"group": "Liella!", "zone": "HAND"})
        self.p0.hand = [400]
        assert self.game._check_condition(self.p0, cond_hand), "Should detect in Hand"

    def test_parser_negative_condition(self):
        """Verify parser DOES NOT create GROUP_FILTER for basic search/recovery effects."""
        # Text: "Search deck for u's member" (Implied: No "If" condition)
        text_search = "自分のデッキから『μ's』のメンバーを1枚探して手札に加える。"
        abilities = AbilityParser.parse_ability_text(text_search)

        has_group_filter = any(c.type == ConditionType.GROUP_FILTER for c in abilities[0].conditions)
        assert not has_group_filter, "Search text without 'If/Case' should NOT have GROUP_FILTER"

    def test_parser_positive_condition(self):
        """Verify parser DOES create GROUP_FILTER for explicit 'If' text."""
        # Text: "If you have a Liella! member..."
        text_cond = "自分のステージに『Liella!』のメンバーがいる場合、カードを1枚引く。"
        abilities = AbilityParser.parse_ability_text(text_cond)

        has_group_filter = any(c.type == ConditionType.GROUP_FILTER for c in abilities[0].conditions)
        assert has_group_filter, "Text with '場合' SHOULD have GROUP_FILTER"

        cond = [c for c in abilities[0].conditions if c.type == ConditionType.GROUP_FILTER][0]
        assert cond.params.get("group") == "Liella!"
