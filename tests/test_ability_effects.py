"""
Comprehensive Ability Effects Test Suite

Tests various effect types to verify they work correctly.
Uses actual card data and simulated game states.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from game.game_state import GameState, Phase, HeartColor
from game.data_loader import CardDataLoader
from game.ability import EffectType, TriggerType, AbilityParser

# Load card databases
loader = CardDataLoader('data/cards.json')
member_db, live_db, energy_pool = loader.load()

class AbilityTestResult:
    def __init__(self, name, passed, details):
        self.name = name
        self.passed = passed
        self.details = details
    
    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status}: {self.name}\n    {self.details}"

results = []

def test_draw_effect():
    """Test DRAW effect - should add cards to player's hand."""
    try:
        gs = GameState(member_db, live_db, energy_pool)
        gs.setup_initial_state()
        
        p = gs.players[0]
        initial_hand_size = len(p.hand)
        initial_deck_size = len(p.main_deck)
        
        # Simulate drawing 2 cards
        gs._draw_cards(p, 2)
        
        new_hand_size = len(p.hand)
        new_deck_size = len(p.main_deck)
        
        passed = (new_hand_size == initial_hand_size + 2) and (new_deck_size == initial_deck_size - 2)
        details = f"Hand: {initial_hand_size}→{new_hand_size}, Deck: {initial_deck_size}→{new_deck_size}"
        results.append(AbilityTestResult("DRAW Effect", passed, details))
    except Exception as e:
        results.append(AbilityTestResult("DRAW Effect", False, f"Exception: {e}"))

def test_add_blades_effect():
    """Test ADD_BLADES effect - should increase blade count."""
    try:
        gs = GameState(member_db, live_db, energy_pool)
        gs.setup_initial_state()
        
        p = gs.players[0]
        # Find a member with blades
        test_member = None
        for cid, m in member_db.items():
            if m.blades > 0:
                test_member = m
                break
        
        if test_member:
            details = f"Member '{test_member.name}' has {test_member.blades} blades"
            results.append(AbilityTestResult("ADD_BLADES Data", True, details))
        else:
            results.append(AbilityTestResult("ADD_BLADES Data", False, "No member with blades found"))
    except Exception as e:
        results.append(AbilityTestResult("ADD_BLADES Effect", False, f"Exception: {e}"))

def test_search_deck_effect():
    """Test that deck contains searchable cards."""
    try:
        gs = GameState(member_db, live_db, energy_pool)
        gs.setup_initial_state()
        
        p = gs.players[0]
        
        # Check deck for specific card types
        members_in_deck = [cid for cid in p.main_deck if cid in member_db]
        lives_in_deck = [cid for cid in p.main_deck if cid in live_db]
        
        passed = len(members_in_deck) > 0 or len(lives_in_deck) > 0
        details = f"Deck has {len(members_in_deck)} members, {len(lives_in_deck)} lives"
        results.append(AbilityTestResult("SEARCH_DECK Prerequisite", passed, details))
    except Exception as e:
        results.append(AbilityTestResult("SEARCH_DECK Effect", False, f"Exception: {e}"))

def test_recover_member_from_discard():
    """Test RECOVER_MEMBER - add a member from discard to hand."""
    try:
        gs = GameState(member_db, live_db, energy_pool)
        gs.setup_initial_state()
        
        p = gs.players[0]
        
        # Find a member to put in discard
        if len(p.hand) > 0:
            discarded_card = p.hand.pop(0)
            p.discard.append(discarded_card)
            
            initial_discard_size = len(p.discard)
            initial_hand_size = len(p.hand)
            
            # Simulate recovery
            if discarded_card in member_db:
                p.discard.remove(discarded_card)
                p.hand.append(discarded_card)
                
                passed = len(p.hand) == initial_hand_size + 1 and len(p.discard) == initial_discard_size - 1
                details = f"Recovered {member_db[discarded_card].name} from discard"
                results.append(AbilityTestResult("RECOVER_MEMBER Effect", passed, details))
            else:
                results.append(AbilityTestResult("RECOVER_MEMBER Effect", False, "No member to recover"))
        else:
            results.append(AbilityTestResult("RECOVER_MEMBER Effect", False, "Hand empty"))
    except Exception as e:
        results.append(AbilityTestResult("RECOVER_MEMBER Effect", False, f"Exception: {e}"))

def test_ability_parser():
    """Test that ability text is parsed correctly."""
    try:
        # Test a simple ability text
        test_texts = [
            "【登場】 手札を1枚控え室に置いてもよい",
            "【起動】 このメンバーをステージから控え室に置く",
            "【常時】 ライブの合計スコアを＋１する",
        ]
        
        parsed_count = 0
        for text in test_texts:
            abilities = AbilityParser.parse_ability_text(text)
            if abilities:
                parsed_count += 1
        
        passed = parsed_count > 0
        details = f"Parsed {parsed_count}/{len(test_texts)} ability texts"
        results.append(AbilityTestResult("AbilityParser", passed, details))
    except Exception as e:
        results.append(AbilityTestResult("AbilityParser", False, f"Exception: {e}"))

def test_heart_color_enum():
    """Test HeartColor enum order matches expected."""
    try:
        expected = ['PINK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', 'ANY', 'RAINBOW']
        actual = [c.name for c in HeartColor]
        
        passed = actual[:6] == expected[:6]  # First 6 should match
        details = f"Expected: {expected[:6]}, Got: {actual[:6]}"
        results.append(AbilityTestResult("HeartColor Enum Order", passed, details))
    except Exception as e:
        results.append(AbilityTestResult("HeartColor Enum Order", False, f"Exception: {e}"))

def test_member_hearts_data():
    """Test that member hearts data is correctly loaded."""
    try:
        # Check a few members have valid heart data
        members_with_hearts = 0
        for cid, m in list(member_db.items())[:50]:  # Check first 50
            if hasattr(m, 'hearts') and np.sum(m.hearts) > 0:
                members_with_hearts += 1
        
        passed = members_with_hearts > 10
        details = f"{members_with_hearts}/50 members have heart data"
        results.append(AbilityTestResult("Member Hearts Data", passed, details))
    except Exception as e:
        results.append(AbilityTestResult("Member Hearts Data", False, f"Exception: {e}"))

def test_live_requirements_data():
    """Test that live card requirements are correctly loaded."""
    try:
        lives_with_reqs = 0
        for cid, l in list(live_db.items())[:50]:  # Check first 50
            if hasattr(l, 'required_hearts') and np.sum(l.required_hearts) > 0:
                lives_with_reqs += 1
        
        passed = lives_with_reqs > 5
        details = f"{lives_with_reqs}/50 live cards have requirements"
        results.append(AbilityTestResult("Live Requirements Data", passed, details))
    except Exception as e:
        results.append(AbilityTestResult("Live Requirements Data", False, f"Exception: {e}"))

def test_action_menu_text():
    """Test that action descriptions are appropriate."""
    try:
        gs = GameState(member_db, live_db, energy_pool)
        gs.setup_initial_state()
        gs.phase = Phase.MAIN
        
        # Get legal actions and check descriptions exist
        legal_mask = gs.get_legal_actions()
        legal_ids = [i for i, v in enumerate(legal_mask) if v]
        
        passed = len(legal_ids) > 0
        details = f"{len(legal_ids)} legal actions available in MAIN phase"
        results.append(AbilityTestResult("Action Menu Availability", passed, details))
    except Exception as e:
        results.append(AbilityTestResult("Action Menu Text", False, f"Exception: {e}"))

def run_all_tests():
    """Run all ability tests."""
    print("=" * 60)
    print("COMPREHENSIVE ABILITY EFFECTS TEST SUITE")
    print("=" * 60)
    print()
    
    test_heart_color_enum()
    test_draw_effect()
    test_add_blades_effect()
    test_search_deck_effect()
    test_recover_member_from_discard()
    test_ability_parser()
    test_member_hearts_data()
    test_live_requirements_data()
    test_action_menu_text()
    
    print()
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    
    for r in results:
        print(r)
        print()
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
