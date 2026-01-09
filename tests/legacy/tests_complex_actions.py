
import sys
import os
import numpy as np

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import GameState, Phase, MemberCard, PlayerState
from game.ability import Ability, TriggerType, Effect, EffectType, AbilityCostType, Cost, TargetType

def test_activated_ability():
    print("Testing Activated Ability and Targeting...")
    
    state = GameState()
    
    # Setup card with activated ability: "Discard 1 card from hand"
    ability = Ability(
        raw_text="起動: 手札を1枚捨てる",
        trigger=TriggerType.ACTIVATED,
        effects=[Effect(EffectType.SWAP_CARDS, 1, TargetType.CARD_HAND, params={"effect": "discard"})],
        costs=[]
    )
    
    member = MemberCard(
        card_id=999,
        name="Test Member",
        cost=1,
        hearts=np.zeros(6),
        blade_hearts=np.zeros(6),
        blades=1,
        abilities=[ability]
    )
    
    GameState.member_db[999] = member
    
    # Set stage
    p0 = state.players[0]
    p0.stage[1] = 999 # Center
    p0.hand = [1, 2, 3] # Some dummy cards
    
    state.phase = Phase.MAIN
    state.current_player = 0
    state.first_player = 0
    
    print(f"Initial Hand: {p0.hand}")
    
    # 1. Check legal actions
    legal = state.get_legal_actions()
    assert legal[201], "Action 201 (Activate Center) should be legal"
    print("Action 201 is legal.")
    
    # 2. Step: Activate
    state = state.step(201)
    
    # 3. Check pending choices
    assert len(state.pending_choices) > 0, "Should have a pending choice"
    assert state.pending_choices[0][0] == "TARGET_HAND", "Choice should be TARGET_HAND"
    print("Pending choice TARGET_HAND created successfully.")
    
    # 4. Check legal actions for targeting
    legal = state.get_legal_actions()
    assert not legal[0], "Pass should NOT be legal while choosing"
    assert legal[203], "Targeting card 0 should be legal"
    assert legal[204], "Targeting card 1 should be legal"
    assert legal[205], "Targeting card 2 should be legal"
    assert not legal[206], "Targeting card 3 (non-existent) should NOT be legal"
    print("Targeting actions are correctly masked.")
    
    # 5. Step: Select Target (Card index 1 -> Action 203 + 1 = 204)
    state = state.step(204)
    p0 = state.players[0] # Re-fetch p0 from the new state
    
    # 6. Verify result
    print(f"Final Hand: {p0.hand}")
    assert len(p0.hand) == 2, f"Hand should have 2 cards, got {len(p0.hand)}"
    assert 2 not in p0.hand, "Card '2' (index 1) should have been removed"
    assert p0.discard[-1] == 2, "Card '2' should be in discard"
    print("Card successfully discarded via activated ability and targeting!")
    
    print("\nTest PASSED!")

if __name__ == "__main__":
    test_activated_ability()
