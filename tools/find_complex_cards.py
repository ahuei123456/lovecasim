
import json


def find_complex_logic_cards():
    input_file = "c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/data/cards.json"
    keywords = ["聞く", "回答", "質問", "選ぶ", "答え"]
    
    with open(input_file, 'r', encoding='utf-8') as f:
        cards = json.load(f)
    
    found = []
    for card_id, data in cards.items():
        text = data.get('ability', '')
        if any(kw in text for kw in keywords):
            found.append({
                'id': card_id,
                'name': data.get('name'),
                'text': text
            })
            
    print(f"Found {len(found)} cards with complex selection/interaction logic.")
    for card in found[:20]: # Show first 20 as sample
        print(f"[{card['id']}] {card['name']}: {card['text'][:100]}...")

if __name__ == "__main__":
    find_complex_logic_cards()
