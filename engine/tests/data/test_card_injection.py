import numpy as np
import pytest

from engine.game.game_state import GameState, LiveCard, MemberCard


class TestCardInjection:
    @pytest.fixture(autouse=True)
    def setup(self, game_state):
        # Create a fresh game state for each test
        self.state = game_state
        # Ensure we have dummy DBs
        GameState.member_db = {
            101: MemberCard(
                card_id=101,
                card_no="m1",
                name="M1",
                cost=1,
                hearts=np.zeros(6, dtype=np.int32),
                blade_hearts=np.zeros(7, dtype=np.int32),
                blades=1,
            ),
            102: MemberCard(
                card_id=102,
                card_no="m2",
                name="M2",
                cost=2,
                hearts=np.zeros(6, dtype=np.int32),
                blade_hearts=np.zeros(7, dtype=np.int32),
                blades=1,
            ),
        }
        GameState.live_db = {
            201: LiveCard(card_id=201, card_no="l1", name="L1", score=100, required_hearts=np.zeros(7, dtype=np.int32))
        }

    def test_inject_hand(self):
        # Inject into empty hand
        self.state.players[0].hand = []
        self.state.inject_card(0, 101, "hand")
        assert len(self.state.players[0].hand) == 1
        assert self.state.players[0].hand[0] == 101

        # Inject at position 0
        self.state.inject_card(0, 102, "hand", 0)
        assert self.state.players[0].hand[0] == 102
        assert self.state.players[0].hand[1] == 101

    def test_inject_stage(self):
        self.state.inject_card(0, 101, "stage", 0)  # Left
        self.state.inject_card(0, 102, "stage", 2)  # Right

        assert self.state.players[0].stage[0] == 101
        assert self.state.players[0].stage[1] == -1  # Center empty
        assert self.state.players[0].stage[2] == 102

    def test_inject_energy(self):
        self.state.players[0].energy_zone = []
        self.state.inject_card(0, 200, "energy")
        assert len(self.state.players[0].energy_zone) == 1
        assert self.state.players[0].energy_zone[0] == 200

    def test_inject_live(self):
        self.state.players[0].live_zone = []
        self.state.inject_card(0, 201, "live")
        assert len(self.state.players[0].live_zone) == 1
        assert self.state.players[0].live_zone[0] == 201
        # Check revealed array grew
        assert len(self.state.players[0].live_zone_revealed) == 1
        assert self.state.players[0].live_zone_revealed[0] == 0

    def test_inject_opponent(self):
        # Verify we can mess with player 1
        self.state.players[1].hand = []
        self.state.inject_card(1, 101, "hand")
        assert len(self.state.players[1].hand) == 1
        assert self.state.players[1].hand[0] == 101

    def test_invalid_input(self):
        with pytest.raises(ValueError):
            self.state.inject_card(2, 101, "hand")  # Bad player
        with pytest.raises(ValueError):
            self.state.inject_card(0, 101, "invalid_zone")  # Bad zone
        with pytest.raises(ValueError):
            self.state.inject_card(0, 101, "stage", 3)  # Bad stage pos
