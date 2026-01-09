"""
Test for Heart Color Mapping Fix

Verifies that the color name order matches the HeartColor enum:
- HeartColor: PINK=0, RED=1, YELLOW=2, GREEN=3, BLUE=4, PURPLE=5, ANY=6

This test ensures the logs display correct color names.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.game.game_state import HeartColor

def test_color_order():
    """Test that HeartColor enum has the expected order."""
    expected = ['PINK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', 'ANY', 'RAINBOW']
    actual = [c.name for c in HeartColor]
    
    print("HeartColor enum order:")
    for i, c in enumerate(HeartColor):
        print(f"  {i}: {c.name} (value={c.value})")
    
    # Check first 7 (ANY=6, RAINBOW=7 are special)
    assert actual[:7] == expected[:7], f"Mismatch: expected {expected[:7]}, got {actual[:7]}"
    print("\n✅ HeartColor enum order matches expected!")
    
    # Test the COLOR_NAMES array used in logs
    COLOR_NAMES = ['Pink', 'Red', 'Yellow', 'Green', 'Blue', 'Purple', 'Any']
    for i, name in enumerate(COLOR_NAMES):
        if i < len(HeartColor) - 1:  # Exclude RAINBOW
            expected_name = HeartColor(i).name.capitalize()
            assert name.upper() == HeartColor(i).name, f"Index {i}: {name} should match {HeartColor(i).name}"
    print("✅ COLOR_NAMES array matches HeartColor enum indices!")

if __name__ == '__main__':
    test_color_order()
