
import sys
import os
import numpy as np

# Add game directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.game_state import GameState, PlayerState, MemberCard, LiveCard, Phase

def test_yell_wrong_color():
    print("--- Test: Yell Hearts of Wrong Color ---")
    
    # 1. Setup minimal state
    gs = GameState()
    p = gs.players[0]
    
    # Define Cards
    # Live Card: Requires 1 RED heart. ID 1001
    live = LiveCard(1001, "Test Live", 100, np.array([1, 0, 0, 0, 0, 0, 0]), [], "Group") # Index 0 is Red
    gs.live_db[1001] = live
    
    # Member (Yell Source): Provides 1 BLUE blade heart. ID 101
    # Blade hearts: [Red, Blue, Green, Yellow, Purple, Pink]
    member = MemberCard(101, "Blue Yeller", "Group", 1, np.zeros(6), 1, np.array([0, 1, 0, 0, 0, 0])) 
    gs.member_db[101] = member
    
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
        if card_id in gs.member_db:
            m = gs.member_db[card_id]
            blade_hearts_padded[:6] = m.blade_hearts
            total_hearts += blade_hearts_padded
            
    print(f"Total Hearts Available: {total_hearts}")
    
    # Check if requirement is met
    # Indices: 0:Red, 1:Blue, 2:Green, 3:Yellow, 4:Purple, 5:Pink, 6:Any
    
    success = gs._check_hearts_meet_requirement(total_hearts.copy(), live.required_hearts)
    
    if success:
        print("RESULT: FAILED - Wrong color heart satisfied the requirement!")
    else:
        print("RESULT: PASSED - Wrong color heart did NOT satisfy the requirement.")

def test_yell_any_requirement():
    print("\n--- Test: Yell Hearts for ANY Requirement ---")
    
    gs = GameState()
    p = gs.players[0]
    
    # Live Card: Requires 1 ANY heart. ID 1002
    # Index 6 is "Any"
    live = LiveCard(1002, "Any Live", 100, np.array([0, 0, 0, 0, 0, 0, 1]), [], "Group")
    gs.live_db[1002] = live
    
    # Member: Provides 1 BLUE blade heart. ID 101
    member = MemberCard(101, "Blue Yeller", "Group", 1, np.zeros(6), 1, np.array([0, 1, 0, 0, 0, 0]))
    gs.member_db[101] = member
    
    p.live_zone = [1002]
    gs.yell_cards = [101]
    
    total_hearts = np.zeros(7, dtype=np.int32)
    blade_hearts_padded = np.zeros(7, dtype=np.int32)
    
    for card_id in gs.yell_cards:
        if card_id in gs.member_db:
            m = gs.member_db[card_id]
            blade_hearts_padded[:6] = m.blade_hearts
            total_hearts += blade_hearts_padded
            
    # Logic in _check_hearts_meet_requirement handles "Any" by checking sum
    success = gs._check_hearts_meet_requirement(total_hearts.copy(), live.required_hearts)
    
    if success:
        print("RESULT: PASSED - Blue heart correctly satisfied 'Any' requirement.")
    else:
        print("RESULT: FAILED - Blue heart failed to satisfy 'Any' requirement.")

if __name__ == "__main__":
    test_yell_wrong_color()
    test_yell_any_requirement()
