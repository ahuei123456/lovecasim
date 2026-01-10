import numpy as np
import pytest

from engine.game.game_state import Condition, ConditionType, GameState, Group, MemberCard


class TestGroupFilter:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.game = GameState()
        self.p0 = self.game.players[0]

        # Mock Member DB
        # ID 1: Liella! Member
        self.game.member_db[1] = MemberCard(
            card_id=1,
            card_no="L-001",
            name="Kanon",
            cost=1,
            hearts=np.zeros(6, dtype=np.int32),
            blade_hearts=np.zeros(7, dtype=np.int32),
            blades=1,
            groups=[Group.from_japanese_name("ラブライブ！スーパースター!!")],
        )
        # ID 2: Aqours Member
        self.game.member_db[2] = MemberCard(
            card_id=2,
            card_no="A-001",
            name="Chika",
            cost=1,
            hearts=np.zeros(6, dtype=np.int32),
            blade_hearts=np.zeros(7, dtype=np.int32),
            blades=1,
            groups=[Group.from_japanese_name("ラブライブ！サンシャイン!!")],
        )

    def test_zone_check_stage(self):
        """Test checking for group member existence on stage."""
        self.p0.stage[0] = 1  # Liella! on Left

        cond = Condition(ConditionType.GROUP_FILTER, {"group": "Liella!", "zone": "STAGE"})

        # Should be True (Liella member is on stage)
        assert self.game._check_condition(self.p0, cond)

        # Clear stage
        self.p0.stage[0] = -1
        assert not self.game._check_condition(self.p0, cond)

    def test_zone_check_discard(self):
        """Test checking for group member existence in discard."""
        self.p0.discard.append(1)  # Liella! in discard

        cond = Condition(ConditionType.GROUP_FILTER, {"group": "Liella!", "zone": "DISCARD"})
        assert self.game._check_condition(self.p0, cond)

        self.p0.discard = []
        assert not self.game._check_condition(self.p0, cond)

    def test_context_check_self(self):
        """Test checking if 'this' card belongs to group."""
        cond = Condition(ConditionType.SELF_IS_GROUP, {"group": "Aqours"})

        # Context is card ID 2 (Aqours)
        context = {"card_id": 2}
        assert self.game._check_condition(self.p0, cond, context)

        # Context is card ID 1 (Liella) -> Should fail for checking Aqours
        context = {"card_id": 1}
        assert not self.game._check_condition(self.p0, cond, context)

    def test_context_check_revealed(self):
        """Test checking if observed/revealed cards belong to group."""
        self.game.looked_cards = [1, 1]  # Two Liella cards

        cond = Condition(ConditionType.GROUP_FILTER, {"group": "Liella!", "context": "revealed"})

        # Should pass because all looked cards are Liella
        assert self.game._check_condition(self.p0, cond)

        # Mixed group (Both Aqours)
        self.game.looked_cards = [2, 2]
        # Should fail because logic requires ALL to match (match_count == len)
        assert not self.game._check_condition(self.p0, cond)
