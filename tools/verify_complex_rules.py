
import os
import sys

import numpy as np

# Add game directory to path
sys.path.append(os.path.join(os.getcwd(), 'game'))

# Attempting strict imports
try:
    from ability import Ability, AbilityCostType, Condition, TriggerType
    from game_state import GameState, MemberCard, Phase
except ImportError:
    # Fallback if running from within game dir
    sys.path.append(os.getcwd())
    from ability import Ability, TriggerType
    from game_state import GameState, MemberCard, Phase

# Mock Color class to avoid import headaches if it's not behaving
class Color:
    RED = 1

def test_structural_rules():
    """Verify 'Index Only' rules that are implemented via Data Structures"""
    print("\n=== Testing Structural Rules (Yellow Status in Report) ===")
    game = GameState()
    
    # Rule 1.1: Game has 2 players
    if len(game.players) == 2:
        print("✅ Rule 1.1 (2 Players): Verified game initialized with 2 PlayerState objects.")
    else:
        print(f"❌ Rule 1.1 Failed: Found {len(game.players)} players.")

    # Rule 4.11: Hand Zone
    if isinstance(game.players[0].hand, list):
         print("✅ Rule 4.11 (Hand): Verified Player 0 has a Hand data structure.")
    
    # Rule 4.8: Main Deck Zone
    if hasattr(game.players[0], 'main_deck'):
         print("✅ Rule 4.8 (Main Deck): Verified Player 0 has a Main Deck zone.")
         
    # Rule 4.5: Member Area (3 slots)
    if len(game.players[0].stage) == 3:
        print("✅ Rule 4.5.2 (3 Member Areas): Verified Stage has 3 slots (Left, Center, Right).")

def test_rule_11_2_once_per_turn():
    print("\n=== Testing Rule 11.2: Once Per Turn Restriction ===")
    game = GameState()
    p0 = game.players[0]
    game.active_player_id = 0
    game.phase = Phase.MAIN # Main phase to allow playing abilities
    
    # Create test member with ACTIVATED ability + Once Per Turn
    # FIX: MemberCard uses hearts array, not color/original_hearts
    hearts = np.zeros(6, dtype=int)
    hearts[Color.RED] = 1
    
    blade_hearts = np.zeros(6, dtype=int)
    
    m1 = MemberCard(
        card_id=999, 
        name="Test Idol", 
        cost=1, 
        hearts=hearts, 
        blade_hearts=blade_hearts,
        blades=1
    )
    
    # Manually attach ability
    # (Checking game_state logic: if ab.trigger == TriggerType.ACTIVATED and ab.is_once_per_turn)
    opt_ability = Ability(
        raw_text="Test Ability",
        trigger=TriggerType.ACTIVATED,
        effects=[], # No effects needed for legality check
        costs=[],
        is_once_per_turn=True
    )
    m1.abilities = [opt_ability]
    
    game.member_db[999] = m1
    p0.stage[0] = 999 # Left Stage
    p0.tapped_members[0] = False # Untapped
    
    # INDEX: 200 + area (0) = 200
    action_idx = 200 # Activate ability for member at Left Stage
    
    # 1. Fresh -> Should be legal
    mask = game.get_legal_actions()
    if mask[action_idx]:
        print("Step 1: Ability available (Fresh) -> OK")
    else:
        print("Step 1 Failed: Ability NOT available.")
        return

    # 2. Mark as Used (Simulate usage)
    # Key format: "{card_id}-{abi_idx}"
    abi_key = "999-0"
    p0.used_abilities.add(abi_key)
    
    # 3. Check again -> Should be illegal (masked out)
    mask = game.get_legal_actions()
    if not mask[action_idx]:
        print("Step 2: Ability BLOCKED (Used) -> ✅ Rule 11.2 Enforced!")
    else:
        print("Step 2 Failed: Ability still available despite OPT usage!")
        return

    # 4. Cleanup (Simulate Turn End)
    p0.used_abilities.clear()
    mask = game.get_legal_actions()
    if mask[action_idx]:
        print("Step 3: Ability reset (Turn End) -> OK")
    else:
        print("Step 3 Failed: Ability not reset.")

def test_rule_10_2_refresh():
    print("\n=== Testing Rule 10.2: Refresh (Deck Shuffle) ===")
    game = GameState()
    p0 = game.players[0]
    
    # Setup: Empty deck, Cards in waiting room
    p0.main_deck = []
    p0.discard = [1, 2, 3, 4, 5]
    
    print(f"Initial: Deck={len(p0.main_deck)}, WaitingRoom={len(p0.discard)}")
    
    # Trigger Rule Check
    game._process_rule_checks()
    
    print(f"Final: Deck={len(p0.main_deck)}, WaitingRoom={len(p0.discard)}")
    
    if len(p0.main_deck) == 5 and len(p0.discard) == 0:
        print("✅ Rule 10.2 (Refresh): Deck automatically refilled from Waiting Room.")
    else:
        print("❌ Rule 10.2 Failed.")

if __name__ == "__main__":
    test_structural_rules()
    test_rule_11_2_once_per_turn()
    test_rule_10_2_refresh()
