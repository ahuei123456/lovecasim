import sys
import os
sys.path.append(os.getcwd())

from game.game_state import GameState, Phase
from game.ability import Ability, Effect, EffectType, TriggerType

def run_execution_demo():
    print("=== Execution Logic Demo ===\n")
    
    # Initialize Game
    game = GameState()
    p0 = game.players[0]
    p1 = game.players[1]
    game.first_player = 0
    game.current_player = 0
    
    # 1. Demo: MOVE_TO_DECK (Top)
    print("--- Case 1: Move to Deck (Top) ---")
    p0.discard = [101, 102, 999] # 999 is target
    p0.main_deck = [200, 201]
    print(f"Before: Discard={p0.discard}, Deck={p0.main_deck}")
    
    # Inject Effect
    effect = Effect(EffectType.MOVE_TO_DECK, 1, params={'position': 'top'})
    game.pending_effects.append(effect)
    game._resolve_pending_effect(0)
    
    print(f"After:  Discard={p0.discard}, Deck={p0.main_deck}")
    if p0.main_deck[0] == 999:
        print("SUCCESS: Card 999 moved to Top of Deck.\n")
    else:
        print("FAILURE: Card 999 not on top.\n")

    # 2. Demo: TAP_OPPONENT
    print("--- Case 2: Tap Opponent ---")
    game.current_player = 0
    p1.stage[1] = 500 # Valid member
    p1.tapped_members[1] = False
    print(f"Before: Opponent Area 1 Tapped={p1.tapped_members[1]}")
    
    # Inject Effect
    effect = Effect(EffectType.TAP_OPPONENT, 1)
    game.pending_effects.append(effect)
    game._resolve_pending_effect(0)
    
    print(f"After:  Opponent Area 1 Tapped={p1.tapped_members[1]}")
    if p1.tapped_members[1]:
        print("SUCCESS: Opponent member tapped.\n")
    else:
        print("FAILURE: Opponent member not tapped.\n")

    # 3. Demo: PLACE_UNDER (Energy)
    print("--- Case 3: Place Energy Under Member ---")
    p0.energy_zone = [800, 801]
    p0.stage_energy[0] = []
    print(f"Before: EnergyZone={p0.energy_zone}, Member0_Energy={p0.stage_energy[0]}")
    
    # Inject Effect
    effect = Effect(EffectType.PLACE_UNDER, 1)
    game.pending_effects.append(effect)
    game._resolve_pending_effect(0)
    
    print(f"After:  EnergyZone={p0.energy_zone}, Member0_Energy={p0.stage_energy[0]}")
    if len(p0.stage_energy[0]) == 1 and p0.stage_energy[0][0] == 801:
        print("SUCCESS: Energy 801 moved under member.\n")
    else:
        print("FAILURE: Energy not moved correctly.\n")

if __name__ == "__main__":
    run_execution_demo()
