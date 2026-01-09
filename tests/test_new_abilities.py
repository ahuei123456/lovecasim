
import numpy as np
from game.game_state import GameState, PlayerState, MemberCard, Phase
from game.ability import Ability, TriggerType, Effect, EffectType, TargetType, AbilityParser

def test_deck_search():
    print("\n=== Testing SEARCH_DECK ===")
    gs = GameState(verbose=True)
    
    # Setup card DB
    m1 = MemberCard(1, "Rin", 2, np.zeros(6), np.zeros(6), 1, group="μ's")
    m2 = MemberCard(2, "Honoka", 3, np.zeros(6), np.zeros(6), 3, group="μ's")
    GameState.member_db = {1: m1, 2: m2}
    
    # Setup deck
    gs.players[0].main_deck = [1, 2, 1, 2]
    
    # Effect: Search "μ's" member
    effect = Effect(EffectType.SEARCH_DECK, 1, params={'group': "μ's"})
    gs.pending_effects.append(effect)
    
    # Resolve effect -> SELECT_FROM_LIST
    gs = gs.step(0) 
    
    print(f"Pending Choices: {[c[0] for c in gs.pending_choices]}")
    if gs.pending_choices:
        # Select first card (index 0 in 'cards' list)
        gs = gs.step(600)
        p0 = gs.players[0]
        print(f"Hand after search: {p0.hand}")
        print(f"Deck count after search: {len(p0.main_deck)}")
        
        if 1 in p0.hand and len(p0.main_deck) == 3:
             print("SEARCH_DECK SUCCESS!")
        else:
             print("SEARCH_DECK FAILED!")

def test_formation_change():
    print("\n=== Testing FORMATION_CHANGE ===")
    gs = GameState(verbose=True)
    gs.phase = Phase.MAIN
    
    # Setup cards
    m1 = MemberCard(1, "L", 2, np.zeros(6), np.zeros(6), 1)
    m2 = MemberCard(2, "C", 2, np.zeros(6), np.zeros(6), 1)
    m3 = MemberCard(3, "R", 2, np.zeros(6), np.zeros(6), 1)
    GameState.member_db = {1: m1, 2: m2, 3: m3}
    
    # Setup stage: L, C, R
    gs.players[0].stage = np.array([1, 2, 3], dtype=np.int32)
    
    # Trigger Formation Change
    effect = Effect(EffectType.FORMATION_CHANGE, 1)
    gs.pending_effects.append(effect)
    
    # Start resolving -> SELECT_FORMATION_SLOT (Slot 0)
    gs = gs.step(0)
    
    print(f"Pending Choices: {[c[0] for c in gs.pending_choices]}")
    
    # Choice 1: Select member for Slot 0 (Left)
    # Available: (0, 1), (1, 2), (2, 3)
    # Pick index 2 (Member 3)
    gs = gs.step(702) 
    
    # Choice 2: Select for Slot 1 (Center)
    # Available: (0, 1), (1, 2)
    # Pick index 1 (Member 2)
    gs = gs.step(701) 
    
    # Choice 3: Select for Slot 2 (Right)
    # Available: (0, 1)
    # Pick index 0 (Member 1)
    gs = gs.step(700) 
    
    p0 = gs.players[0]
    print(f"Final Stage: {p0.stage}")
    if np.array_equal(p0.stage, [3, 2, 1]):
        print("FORMATION_CHANGE SUCCESS!")
    else:
        print("FORMATION_CHANGE FAILED!")

if __name__ == "__main__":
    test_deck_search()
    test_formation_change()
