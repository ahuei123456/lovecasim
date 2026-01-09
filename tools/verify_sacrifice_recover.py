
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from game.data_loader import CardDataLoader
from game.game_state import GameState, Phase


def verify():
    print("Loading Data...")
    loader = CardDataLoader("data/cards.json")
    member_db, live_db, energy_db = loader.load()
    GameState.member_db = member_db
    GameState.live_db = live_db
    GameState.energy_db = energy_db
    
    # Target Card: PL!-pb1-024-N (Nishikino Maki)
    # Finding integer ID
    target_id = -1
    for k, v in member_db.items():
        if v.name == '西木野真姫' and 'このメンバーをステージから控え室に置く' in v.ability_text:
            target_id = k
            break
            
    if target_id == -1:
        print("Error: Target card not found in DB.")
        return

    print(f"Testing with Card ID {target_id} ({member_db[target_id].name})")

    # Setup State
    gs = GameState()
    gs.phase = Phase.MAIN
    p = gs.players[0]
    
    # 1. Place Member on Center Stage
    p.stage[1] = target_id
    p.tapped_members[:] = False # Active
    
    # 2. Place a Live Card in Discard
    live_id = list(live_db.keys())[0]
    p.discard = [live_id]
    
    # 3. Energy just in case (though cost is sacrifice)
    p.energy_zone = [2000] * 3
    p.tapped_energy = np.zeros(100, dtype=bool)

    # 4. Check Legal Actions
    mask = gs.get_legal_actions()
    action_id = 201 # Ability of Center (200=Left, 201=Center, 202=Right)
    
    if not mask[action_id]:
        print(f"FAILURE: Action {action_id} is NOT legal.")
        # Debug why
        # Check cost?
        print(f"Stage: {p.stage}")
        print(f"Tapped: {p.tapped_members}")
        return

    print(f"SUCCESS: Action {action_id} is legal.")
    
    # 5. Execute Action
    new_gs = gs.step(action_id)
    new_p = new_gs.players[0]
    
    # 6. Verify Cost Paid (Sacrifice)
    # Member should be GONE from stage (replaced by -1)
    if new_p.stage[1] == -1:
        print("SUCCESS: Member left stage (Sacrifice cost paid).")
    else:
        print(f"FAILURE: Member still on stage: {new_p.stage[1]}")
        
    # Member should be in Discard (or Pending Zone? or Logic handles it)
    # The cost "SACRIFICE_SELF" moves it to discard immediately usually.
    # Note: If it moved to discard, it should be in new_p.discard.
    # But wait! We also had the Live card in discard.
    # So discard count should be 2 (Live + Maki) OR 1 (if Live picked up immediately? Unlikely)
    print(f"Discard len: {len(new_p.discard)} (Expected increasing)")
    if target_id in new_p.discard:
         print("SUCCESS: Member found in discard.")
    else:
         print("FAILURE: Member NOT in discard (Where is it?)")
         
    # 7. Verify Effect (Recover Live)
    # Should have a pending choice "SELECT_FROM_DISCARD"
    if new_gs.pending_choices:
        choice = new_gs.pending_choices[0]
        print(f"Pending Choice: {choice[0]}")
        if choice[0] == "SELECT_FROM_DISCARD":
            print("SUCCESS: Choice 'SELECT_FROM_DISCARD' triggered.")
            # Check params
            params = choice[1]
            print(f"  Params: {params}")
            if live_id in params.get('cards', []):
                print("SUCCESS: Live card is available in choice.")
            else:
                print("FAILURE: Target Live card NOT in choice options.")
                
            # Simulate selection
            # Action for selection?
            # get_legal_actions for new_gs should show selection actions (660+)
            sel_mask = new_gs.get_legal_actions()
            # We need to find which action corresponds to selecting our live_id
            # The choice logic maps 'cards' list index to action ID offset.
            # 660 + index
            try:
                live_idx = params['cards'].index(live_id)
                sel_action = 660 + live_idx
                if sel_mask[sel_action]:
                    print(f"SUCCESS: Selection action {sel_action} is legal.")
                    final_gs = new_gs.step(sel_action)
                    if final_gs.players[0].hand and final_gs.players[0].hand[-1] == live_id:
                        print("SUCCESS: Live card added to hand!")
                    else:
                        print(f"FAILURE: Live card not in hand? Hand: {final_gs.players[0].hand}")
                else:
                    print(f"FAILURE: Selection action {sel_action} NOT legal.")
            except ValueError:
                print("FAILURE: Live ID not in params list?")
        else:
            print(f"FAILURE: Unexpected choice type: {choice[0]}")
    else:
        print("FAILURE: No pending choice (Did it auto-resolve? Check hand)")
        if new_p.hand and live_id in new_p.hand:
             print("SUCCESS: Live card added to hand (Auto-resolved).")
        else:
             print("FAILURE: Nothing happened? Hand empty.")

if __name__ == '__main__':
    verify()
