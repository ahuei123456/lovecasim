import os
import sys

sys.path.append(os.getcwd())

from game.ability import ConditionType, EffectType, TriggerType
from game.data_loader import CardDataLoader


def calculate_complexity(card):
    score = 0
    
    # Base complexity for having abilities
    if not card.abilities:
        return 0
        
    for ability in card.abilities:
        score += 1
        
        # Trigger Complexity
        if ability.trigger == TriggerType.CONSTANT:
            score += 2
        elif ability.trigger == TriggerType.ACTIVATED:
            score += 2
            
        # Condition Complexity
        for condition in ability.conditions:
            if condition.type in [ConditionType.COUNT_GROUP, ConditionType.GROUP_FILTER]:
                score += 2
            elif condition.type in [ConditionType.OPPONENT_HAS, ConditionType.IS_CENTER]:
                score += 3
            elif condition.type == ConditionType.SELF_IS_GROUP:
                score += 4
            elif condition.type == ConditionType.MODAL_ANSWER:
                score += 12 # Hard to map semantically
                
        # Effect Complexity (Based on "How hard it was to implement/parse")
        for effect in ability.effects:
            etype = effect.effect_type
            
            # Tier 1: The Basics (Simple Regex)
            if etype in [EffectType.DRAW, EffectType.BUFF_POWER, EffectType.ADD_HEARTS, EffectType.RECOVER_LIVE]:
                score += 1
                
            # Tier 2: Specific Logic (Targeting, Searching)
            elif etype in [EffectType.LOOK_DECK, EffectType.SEARCH_DECK, EffectType.RECOVER_MEMBER, EffectType.ENERGY_CHARGE]:
                score += 3
                
            # Tier 3: Advanced Logic (Immunity, Moving things)
            elif etype in [EffectType.IMMUNITY, EffectType.MOVE_MEMBER, EffectType.REDUCE_COST, EffectType.BOOST_SCORE]:
                score += 5
                
            # Tier 4: The Tricky Ones (Negation, Swapping)
            elif etype in [EffectType.SWAP_CARDS, EffectType.NEGATE_EFFECT, EffectType.SWAP_ZONE]:
                score += 8
                
            # Tier 5: The "Final Bosses" (Added at 95% -> 100%)
            elif etype in [EffectType.ORDER_DECK, EffectType.TAP_OPPONENT, EffectType.SELECT_MODE, 
                           EffectType.RESTRICTION, EffectType.BATON_TOUCH_MOD, EffectType.PLACE_UNDER]:
                score += 15
                
            # Special: Meta Rules (Hard to find, easy to implement)
            elif etype == EffectType.META_RULE:
                score += 5
                
            # Special: Flavor (Ambiguous text)
            elif etype == EffectType.FLAVOR_ACTION:
                score += 10

        # Multi-line/Continuation Complexity
        # If the raw text has multiple sentences/lines but one trigger
        lines = ability.raw_text.split('/') # My parser joins with ' / ' for continuation
        if len(lines) > 1:
             score += (len(lines) - 1) * 10 # 10 point penalty per continuation line

    return score

def main():
    print("Loading Cards...")
    loader = CardDataLoader("c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/data/cards.json")
    members, lives = loader.load()
    
    card_scores = []
    
    for card_id, card in members.items():
        score = calculate_complexity(card)
        card_scores.append((score, card))
        
    # Sort by score descending
    card_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Generate Report
    with open("card_complexity_tiers.md", "w", encoding="utf-8") as f:
        f.write("# Card Complexity Analysis\n")
        f.write("Tiering based on parsing/implementation difficulty.\n\n")
        
        tiers = [
            ("S Tier (The Final Bosses)", 20),
            ("A Tier (Complex Logic)", 10),
            ("B Tier (Advanced)", 5),
            ("C Tier (Standard)", 1)
        ]
        
        for tier_name, min_score in tiers:
            f.write(f"## {tier_name} (Score > {min_score})\n")
            tier_cards = [c for s, c in card_scores if s >= min_score]
            # Remove from list to avoid duplicates if I did ranges, but here I'm filtering top-down?
            # Better to capture ranges.
            
            # Let's simple filter
            if tier_name.startswith("S"):
                tier_cards = [(s, c) for s, c in card_scores if s >= 20]
            elif tier_name.startswith("A"):
                tier_cards = [(s, c) for s, c in card_scores if 10 <= s < 20]
            elif tier_name.startswith("B"):
                tier_cards = [(s, c) for s, c in card_scores if 5 <= s < 10]
            else: # C
                tier_cards = [(s, c) for s, c in card_scores if 0 < s < 5]
                
            f.write(f"Count: {len(tier_cards)}\n\n")
            
            # List top 10 unique examples
            f.write("| Card Name | Score | Key Mechanics |\n")
            f.write("|---|---|---|\n")
            for score, card in tier_cards[:20]:
                mechanics = []
                for ab in card.abilities:
                    for eff in ab.effects:
                        mechanics.append(eff.effect_type.name)
                mechanics_str = ", ".join(set(mechanics))
                f.write(f"| {card.name} | {score} | {mechanics_str} |\n")
            f.write("\n")
            
    print("Report generated: card_complexity_tiers.md")

if __name__ == "__main__":
    main()
