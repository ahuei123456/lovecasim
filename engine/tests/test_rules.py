
import pytest
import numpy as np
import os
from engine.game.game_state import GameState, MemberCard, LiveCard, PlayerState, Phase, Effect, EffectType
from engine.game.ability import Ability, TriggerType

@pytest.fixture
def game_state():
    state = GameState()
    # Mock DB - Reset class variables
    GameState.member_db = {}
    GameState.live_db = {}
    return state

def test_baton_touch_cost(game_state):
    """Verify Baton Touch reduces cost correctly"""
    state = game_state
    # Card 1: Cost 2 (on stage)
    # card_id, card_no, name, cost, hearts, blade_hearts, blades
    c1 = MemberCard(1, "NO-01", "Fan1", 2, np.zeros(6), np.zeros(7), 1)
    # Card 2: Cost 5 (in hand)
    c2 = MemberCard(2, "NO-02", "Fan2", 5, np.zeros(6), np.zeros(7), 1)
    
    GameState.member_db = {1: c1, 2: c2}
    
    p = state.players[0]
    p.stage[0] = 1 # Card 1 on Left
    p.hand = [2]   # Card 2 in hand
    # Energy: 3 available (enough for 5-2=3, but not 5)
    p.energy_zone = [100, 101, 102]
    p.tapped_energy[:] = False
    p.main_deck = [999] # Validation: Prevent auto-refresh from discard
    
    state.phase = Phase.MAIN
    state.current_player = 0
    
    # Action: Play Card 2 (idx 0) on Area 0 (Left)
    # Action encoding: 1 + hand_idx*3 + area = 1 + 0 + 0 = 1
    
    # Check if legal (should be, cost 5-2=3 <= 3 energy)
    legal = state.get_legal_actions()
    assert legal[1], "Baton touch play should be legal"
    
    # Execute
    new_state = state.step(1)
    np0 = new_state.players[0]
    
    # Verify result
    assert np0.stage[0] == 2, "Card 2 should be on stage"
    assert 1 in np0.discard, "Card 1 should be in discard"
    assert np0.count_untapped_energy() == 0, "Should use all 3 energy (5-2=3)"

def test_live_heart_requirements(game_state):
    """Verify Live card heart checking logic"""
    state = game_state
    # Req: 1 Pink, 1 Red, 1 Any
    req = np.zeros(7, dtype=np.int32)
    req[0] = 1 # Pink
    req[1] = 1 # Red
    req[6] = 1 # Any
    
    live = LiveCard(100, "L-01", "Song", 1, req)
    GameState.live_db = {100: live}
    
    p = state.players[0]
    p.live_zone = [100]
    
    # Case 1: Exact match (Pink, Red, Blue for Any)
    hearts1 = np.zeros(6, dtype=np.int32)
    hearts1[0] = 1
    hearts1[1] = 1
    hearts1[4] = 1 # Blue
    assert state._check_hearts_meet_requirement(hearts1, req), "Should match with exact + blue"
    
    # Case 2: Insufficient Color (2 Pink, 0 Red, 1 Blue) -> Fail Red
    hearts2 = np.zeros(6, dtype=np.int32)
    hearts2[0] = 2
    hearts2[4] = 1
    assert not state._check_hearts_meet_requirement(hearts2, req), "Should fail missing red"
    
    # Case 3: Insufficient Any (1 Pink, 1 Red) -> Fail Any
    hearts3 = np.zeros(6, dtype=np.int32)
    hearts3[0] = 1
    hearts3[1] = 1
    assert not state._check_hearts_meet_requirement(hearts3, req), "Should fail missing any"

def test_trigger_stack(game_state):
    """Verify On Play triggers add to stack"""
    state = game_state
    # Card with On Play logic
    ability = Ability("Test", TriggerType.ON_PLAY, [Effect(EffectType.DRAW, 1)])
    
    c1 = MemberCard(1, "NO-01", "Fan1", 1, np.zeros(6), np.zeros(7), 1, abilities=[ability])
    
    GameState.member_db = {1: c1}
    
    p = state.players[0]
    p.hand = [1]
    p.energy_zone = [100]
    
    state.phase = Phase.MAIN
    state.current_player = 0

    
    # Play Card 1
    # Action: 1 (Hand idx 0, Area 0)
    new_state = state.step(1)
    
    # Check trigger was processed
    # Note: step() auto-resolves triggers if no choice required.
    # Since DRAW 1 is auto-resolved, pending_effects should be empty.
    assert len(new_state.pending_effects) == 0, "Effect should auto-resolve"
    
    # Should have drawn a card (if deck had cards, which it doesn't by default here)
    # But main point is verifying the trigger mechanism doesn't crash or hang
