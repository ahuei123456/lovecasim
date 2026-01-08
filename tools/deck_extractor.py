
import re
import os
import sys
from collections import Counter

def parse_and_validate_deck(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # HTML Structure:
    # title="PL!xxx-yyy-zzz : NAME" ... <span class="num">N</span>
    # We need to extract pairs of (card_id, quantity)
    
    # Pattern to find card blocks with title and num
    # Match title="ID : Name" followed eventually by class="num">N<
    pattern = r'title="([^"]+?) :[^"]*"[^>]*>.*?class="num">(\d+)</span>'
    
    matches = re.findall(pattern, content, re.DOTALL)
    
    if not matches:
        print("No card ID + quantity pairs found. Trying alternative pattern...")
        # Fallback: just count title occurrences
        pattern_title = r'title="((?:PL!|LL-E)[^"]+?) :'
        title_matches = re.findall(pattern_title, content)
        print(f"Found {len(title_matches)} title matches (without quantities)")
        return

    # Load card DB for types
    try:
        import json
        with open('data/cards.json', 'r', encoding='utf-8') as f:
            card_db = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load cards.json for type checking: {e}")
        card_db = {}

    # Build deck and count types
    main_deck = []
    energy_deck = []
    
    type_counts = {
        "Member": 0,
        "Live": 0,
        "Energy": 0,
        "Unknown": 0
    }
    
    for card_id, qty_str in matches:
        qty = int(qty_str)
        card_id = card_id.strip()
        
        # Determine Type
        cdata = card_db.get(card_id, {})
        ctype = cdata.get('type', '')
        
        if 'メンバー' in ctype: type_counts["Member"] += qty
        elif 'ライブ' in ctype: type_counts["Live"] += qty
        elif 'エネルギー' in ctype: type_counts["Energy"] += qty
        else: type_counts["Unknown"] += qty
        
        for _ in range(qty):
            if card_id.startswith("LL-E"):
                energy_deck.append(card_id)
            else:
                main_deck.append(card_id)

    # Counts
    main_counts = Counter(main_deck)
    energy_counts = Counter(energy_deck)
    
    # Validation Rules
    errors = []
    
    # Check copy limits
    all_counts = main_counts + energy_counts
    for cid, count in all_counts.items():
        if count > 4 and not cid.startswith("LL-E"):  # Energy might have different rules
            errors.append(f"Card limit exceeded: {cid} x{count} (Max 4)")
            
    # Output Report
    with open('deck_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"=== Deck Verification Report for {os.path.basename(file_path)} ===\n")
        f.write(f"Total Cards: {len(main_deck) + len(energy_deck)}\n")
        f.write(f"Breakdown: Member: {type_counts['Member']} | Live: {type_counts['Live']} | Energy: {type_counts['Energy']}\n")
        
        f.write(f"\nMain Deck: {len(main_deck)} cards\n")
        for cid, count in sorted(main_counts.items()):
            cname = card_db.get(cid, {}).get('name', 'Unknown')
            f.write(f"  {cid}: x{count} ({cname})\n")
            
        f.write(f"\nEnergy Deck: {len(energy_deck)} cards\n")
        for cid, count in sorted(energy_counts.items()):
             cname = card_db.get(cid, {}).get('name', 'Unknown')
             f.write(f"  {cid}: x{count} ({cname})\n")
            
        f.write("\n--- Validation Results ---\n")
        if not errors:
            f.write("VALID DECK (No copy limit violations)\n")
        else:
            f.write("DECK HAS ISSUES:\n")
            for e in errors:
                f.write(f"- {e}\n")
    
    print(f"Report written to deck_report.txt")
    print(f"Total: {len(main_deck)} Main + {len(energy_deck)} Energy")
    print(f"Types: Member {type_counts['Member']}, Live {type_counts['Live']}, Energy {type_counts['Energy']}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    os.chdir(project_root) # Ensure we run from root for data/cards.json access
    parse_and_validate_deck('tests/decktest.txt')
