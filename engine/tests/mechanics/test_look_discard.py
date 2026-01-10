import numpy as np
import pytest

from engine.game.game_state import Effect, EffectType, GameState, Group, MemberCard


class TestLookDiscard:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.game = GameState(verbose=True)
        self.p0 = self.game.players[0]

    def test_look_and_discard_mechanic(self):
        """
        Verify effectively: Look 5, Choose 1, Discard 4.
        """
        # 1. Setup Deck with known cards
        # We need 5 cards in deck.
        # Let's mock cards.
        for i in range(1, 11):
            self.game.member_db[i] = MemberCard(
                card_id=i,
                card_no=f"M{i}",
                name=f"Member {i}",
                cost=1,
                hearts=np.zeros(6),
                blade_hearts=np.zeros(6),
                blades=1,
                groups=[Group.from_japanese_name("ラブライブ！スーパースター!!")],
                units=[],
                img_path="",
            )

        self.p0.main_deck = list(range(1, 11))
        self.p0.hand = []
        self.p0.discard = []

        # 2. Trigger LOOK_AND_CHOOSE Effect manually
        # This simulates an ability like "Look 5, add 1 to hand"
        effect = Effect(EffectType.LOOK_AND_CHOOSE, 1, params={"group": "ラブライブ！スーパースター!!"})

        # Step A: LOOK_DECK
        # Manually resolving for test isolation
        # Logic from _resolve_pending_effect roughly:
        self.game.looked_cards = []
        for _ in range(5):
            self.game.looked_cards.append(self.p0.main_deck.pop(0))

        assert len(self.game.looked_cards) == 5, "Should have looked at 5 cards"
        assert self.game.looked_cards == [1, 2, 3, 4, 5]

        # Step B: LOOK_AND_CHOOSE
        self.game.pending_effects.append(effect)
        self.game._resolve_pending_effect(0)

        # Verify choice is created
        assert self.game.pending_choices, "Should have a pending choice"
        choice_type, params = self.game.pending_choices[0]
        assert choice_type == "SELECT_FROM_LIST"
        assert len(params["cards"]) == 5

        # 3. Execute Selection
        # Choose index 2 (Card 3)
        # Action ID mapping: 600 + index
        action_id = 602

        # Step returns new state
        self.game = self.game.step(action_id)
        self.p0 = self.game.players[0]

        # 4. Verify Results
        # Card 3 in hand
        assert 3 in self.p0.hand
        assert len(self.p0.hand) == 1

        # Others (1, 2, 4, 5) in discard
        assert len(self.p0.discard) == 4
        expected_discard = {1, 2, 4, 5}
        assert set(self.p0.discard) == expected_discard

        # Looked cards cleared
        assert len(self.game.looked_cards) == 0
