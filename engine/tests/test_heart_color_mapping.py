
from engine.game.game_state import HeartColor


def test_color_order():
    """Test that HeartColor enum has the expected order."""
    expected = ['PINK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', 'ANY', 'RAINBOW']
    # Filter only expected keys from enum incase of extra
    actual = [c.name for c in HeartColor]
    
    # Check first 8 match
    assert actual[:8] == expected[:8]
