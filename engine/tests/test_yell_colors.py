
import pytest
import numpy as np
from engine.game.game_state import GameState, PlayerState, MemberCard, LiveCard, Phase

def test_yell_wrong_color():
    print("--- Test: Yell Hearts of Wrong Color ---")
    
    # 1. Setup minimal state
    gs = GameState()
    # Reset DBs
    GameState.member_db = {}
    GameState.live_db = {}
    
    p = gs.players[0]
    
    # Define Cards
    # Live Card: Requires 1 RED heart. ID 1001
    live = LiveCard(1001, "L-01", "Test Live", 1, np.array([1, 0, 0, 0, 0, 0, 0])) # Index 0 is Pink/Red depending on mapping, let's assume 1st element
    # Note: HeartColor mapping: PINK=0, RED=1.
    # If we want RED, we should set index 1.
    # But for this test "Wrong Color", just needs to be distinct from Yell.
    # Yell is Blue (Index 4? or 1?).
    # Let's use kwargs to be safe.
    live = LiveCard(card_id=1001, card_no="L-01", name="Test Live", score=100, required_hearts=np.zeros(7))
    live.required_hearts[1] = 1 # Red
    GameState.live_db[1001] = live
    
    # Member (Yell Source): Provides 1 BLUE blade heart. ID 101
    # Blade hearts: [Red, Blue, Green, Yellow, Purple, Pink] -> Actually [Pn, Rd, Yl, Gr, Bl, Pp]
    # Mapping: 0:PINK, 1:RED, 2:YELLOW, 3:GREEN, 4:BLUE, 5:PURPLE
    bh = np.zeros(6, dtype=np.int32)
    bh[4] = 1 # Blue (Index 4)
    member = MemberCard(101, "Blue Yeller", "Group", 1, np.zeros(6), blade_hearts=bh, blades=1) 
    GameState.member_db[101] = member
    
    # 2. Setup Scenario
    # Player has the Live Card in Live Zone
    p.live_zone = [1001]
    p.live_zone_revealed = [True]
    
    # Player has NO members on stage (so no stage hearts)
    p.stage[:] = -1
    
    # Set the Yell Card (manually inject into yell_cards)
    gs.yell_cards = [101] 
    
    # 3. Execute Heart Calculation Logic (simulate _do_performance internals)
    print(f"Live Requirement: {live.required_hearts} (1 Red)")
    print(f"Yell Card provides: {member.blade_hearts} (1 Blue)")
    
    # Replicate partial logic from _do_performance
    total_hearts = np.zeros(7, dtype=np.int32)
    blade_hearts_padded = np.zeros(7, dtype=np.int32)
    
    # Add blade hearts from yell
    for card_id in gs.yell_cards:
        if card_id in GameState.member_db:
            m = GameState.member_db[card_id]
            blade_hearts_padded[:6] = m.blade_hearts
            total_hearts += blade_hearts_padded
            
    print(f"Total Hearts Available: {total_hearts}")
    
    # Check if requirement is met
    # Indices: 0:Red, 1:Blue, 2:Green, 3:Yellow, 4:Purple, 5:Pink, 6:Any
    
    success = gs._check_hearts_meet_requirement(total_hearts.copy(), live.required_hearts)
    
    # Should FAIL because Blue != Red
    assert not success, "Failed - Wrong color heart satisfied the requirement!"

def test_yell_any_requirement():
    print("\n--- Test: Yell Hearts for ANY Requirement ---")
    
    gs = GameState()
    GameState.member_db = {}
    GameState.live_db = {}
    
    p = gs.players[0]
    
    # Live Card: Requires 1 ANY heart. ID 1002
    # Index 6 is "Any"
    # Live Card: Requires 1 ANY heart. ID 1002
    live = LiveCard(card_id=1002, card_no="L-02", name="Any Live", score=100, required_hearts=np.zeros(7))
    live.required_hearts[6] = 1 # Any
    GameState.live_db[1002] = live
    
    # Member: Provides 1 BLUE blade heart. ID 101
    bh = np.zeros(6, dtype=np.int32)
    bh[4] = 1 # Blue (Index 4)
    member = MemberCard(101, "Blue Yeller", "Group", 1, np.zeros(6), blade_hearts=bh, blades=1)
    GameState.member_db[101] = member
    
    p.live_zone = [1002]
    gs.yell_cards = [101]
    
    total_hearts = np.zeros(7, dtype=np.int32)
    blade_hearts_padded = np.zeros(7, dtype=np.int32)
    
    for card_id in gs.yell_cards:
        if card_id in GameState.member_db:
            m = GameState.member_db[card_id]
            blade_hearts_padded[:6] = m.blade_hearts
            total_hearts += blade_hearts_padded
            
    # Logic in _check_hearts_meet_requirement handles "Any" by checking sum
    success = gs._check_hearts_meet_requirement(total_hearts.copy(), live.required_hearts)
    
    # Should PASS
    assert success, "Blue heart failed to satisfy 'Any' requirement."
