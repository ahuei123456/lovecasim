
import sys
import os
import numpy as np

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState, Phase, MemberCard, LiveCard, PlayerState
from game.ability import Ability, TriggerType, Effect, EffectType, TargetType, AbilityCostType

def test_flavor_modal():
    print("Testing Flavor and Modal Action (LL-PR-004-PR)...")
    
    state = GameState()
    
    # Setup Live card with trigger: "When live starts, ask what they like..."
    ability = Ability(
        raw_text="ライブ開始時相手に何が好き？と聞く。",
        trigger=TriggerType.ON_LIVE_START,
        effects=[Effect(EffectType.FLAVOR_ACTION, 1, TargetType.SELF, params={"text": "何が好き？"})],
        costs=[]
    )
    
    live = LiveCard(
        card_id=4004,
        name="AiScReam",
        score=3,
        required_hearts=np.zeros(7),
        abilities=[ability]
    )
    
    GameState.live_db[4004] = live
    
    # Set player 0 live zone
    p0 = state.players[0]
    p0.live_zone = [4004]
    p0.hand = [1, 2, 3] # Dummy hand
    p0.main_deck = [10, 11, 12, 13, 14] # Add a deck for drawing
    
    # Also for p1
    p1 = state.players[1]
    p1.main_deck = [20, 21, 22]
    
    print(f"Initial Hand P0: {p0.hand}")
    
    # Trigger performance for P1 (Phase.PERFORMANCE_P1)
    state.phase = Phase.PERFORMANCE_P1
    state.current_player = 0
    
    # 1. Step: Performance starts (action 0 to confirm)
    # The _do_performance(0) should be called via _execute_action(0)
    state = state.step(0)
    
    # 2. Check pending choices (Modal Choice should be there)
    assert len(state.pending_choices) > 0, "Should have a pending choice (MODAL)"
    assert state.pending_choices[0][0] == "MODAL", "Choice should be MODAL"
    print("MODAL choice triggered successfully at Live Start.")
    
    # 3. Check legal actions
    legal = state.get_legal_actions()
    assert legal[270], "Option 0 (チョコミント) should be legal"
    assert legal[271], "Option 1 (あなた) should be legal"
    assert legal[272], "Option 2 (その他) should be legal"
    print("Modal options are correctly masked.")
    
    # 4. Step: Select Option 1 (あなた -> Actions 270 + 1 = 271)
    # This choice should make both players draw 1 card.
    state = state.step(271)
    p0 = state.players[0] # Re-fetch p0 from the new state
    
    # 5. Verify result
    assert len(p0.hand) == 4, f"Hand should have 4 cards after drawing 1, got {len(p0.hand)}"
    print("Modal effect (DRAW 1) resolved successfully!")
    
    print("\nTest PASSED!")

if __name__ == "__main__":
    test_flavor_modal()
