import sys
import os
import json
sys.path.append(os.getcwd())

from game.ability import AbilityParser

from game.data_loader import CardDataLoader

def find_and_parse(card_id):
    loader = CardDataLoader("c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/data/cards.json")
    members, lives = loader.load()
    
    target_card = None
    # Check members
    for cid, card in members.items():
        # card_no might strict match but loader uses Int ID as key.
        # We check card.card_id or try to match string ID if stored?
        # Loader parsed IDs as ints. The user gave 'LL-PR-004-PR'.
        # This string ID implies it's in the JSON under 'card_no'.
        # But loader might not expose original string ID easily?
        # Wait, verify_parser_verbose used text.
        # Let's search raw JSON correctly or search helper.
        pass

    # Revert to raw json but inspect structure first?
    # No, let's fix the raw json iteration.
    with open("c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/data/cards.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Data is likely a dict with keys? Or list?
    if isinstance(data, dict):
        if 'cards' in data:
            data = data['cards']
        else:
             # creating a list of values if it is a dict
             data = list(data.values())

    print(f"Total cards scanned: {len(data)}")
    
    # DEBUG: Print first 5
    print("--- First 5 Cards ---")
    for i, card in enumerate(data[:5]):
        if isinstance(card, dict):
            # Print ALL keys for the first one to debug
            if i == 0:
                print(f"Keys: {list(card.keys())}")
            print(f"ID: {card.get('card_no')} | Name: {card.get('name')}")
    print("-------------------")
    
    # 1. Try Exact match
    for card in data:
        if isinstance(card, dict):
            cnum = card.get('card_no', '')
            if cnum == card_id:
                target_card = card
                break
                
    # fuzzy search.
    candidates = []
    for card in data:
        cnum = card.get('card_no', '')
        if 'PR' in cnum:
            candidates.append(cnum)
            
    print(f"PR Candidates found ({len(candidates)}): {candidates[:20]}")
    
    # Also just search for '004' in name or number
    name_candidates = []
    for card in data:
        if '004' in card.get('card_no', ''):
            name_candidates.append(card.get('card_no', ''))
            
    print(f"004 Candidates found ({len(name_candidates)}): {name_candidates[:20]}")
        
    # If one candidate, use it.
    if len(candidates) == 1:
            print(f"Auto-selecting: {candidates[0]}")
            for card in data:
                if card.get('card_no') == candidates[0]:
                    target_card = card
                    break
    
    if not target_card:
        print("Could not locate card.")
        return

    print(f"--- Card: {target_card.get('name')} ({target_card.get('card_no')}) ---")
    raw_text = target_card.get('ability', '')
    print(f"Raw Text:\n{raw_text}\n")
    
    abilities = AbilityParser.parse_ability_text(raw_text)
    
    print("--- Parsed Logic ---")
    for i, ab in enumerate(abilities):
        print(f"Ability {i+1}:")
        print(f"  Trigger: {ab.trigger.name}")
        if ab.conditions:
            print(f"  Conditions: {[f'{c.type.name} {c.params}' for c in ab.conditions]}")
        for e in ab.effects:
            print(f"  Effect: {e.effect_type.name} (Val={e.value}) Params={e.params}")
        print("")

if __name__ == "__main__":
    find_and_parse("LL-PR-004-PR")
