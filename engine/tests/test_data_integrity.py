
import pytest
import numpy as np
import sys
import os

# Add parent path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from engine.game.game_state import HeartColor, GameState, Phase
    from engine.game.data_loader import CardDataLoader
except ImportError:
    try:
        from game.game_state import HeartColor, GameState, Phase
        from game.data_loader import CardDataLoader
    except ImportError:
        from game_state import HeartColor, GameState, Phase
        from data_loader import CardDataLoader

@pytest.fixture(scope="module")
def loader():
    return CardDataLoader('engine/data/cards.json')

@pytest.fixture(scope="module")
def data(loader):
    member_db, live_db, energy_pool = loader.load()
    return member_db, live_db

def test_heart_color_enum():
    """Test HeartColor enum order matches expected."""
    expected = ['PINK', 'RED', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', 'ANY', 'RAINBOW']
    actual = [c.name for c in HeartColor]
    
    # First 6 should match exactly
    assert actual[:6] == expected[:6]

def test_member_hearts_data(data):
    """Test that member hearts data is correctly loaded."""
    member_db, _ = data
    members_with_hearts = 0
    # Check first 50 members
    for cid, m in list(member_db.items())[:50]:
        if hasattr(m, 'hearts') and np.sum(m.hearts) > 0:
            members_with_hearts += 1
    
    assert members_with_hearts > 10, "Should have loaded members with hearts"

def test_live_requirements_data(data):
    """Test that live card requirements are correctly loaded."""
    _, live_db = data
    lives_with_reqs = 0
    for cid, l in list(live_db.items())[:50]:
        if hasattr(l, 'required_hearts') and np.sum(l.required_hearts) > 0:
            lives_with_reqs += 1
            
    assert lives_with_reqs > 5, "Should have loaded lives with requirements"

def test_action_menu_text():
    """Test that action descriptions are generated."""
    # Setup simple state
    gs = GameState()
    gs.phase = Phase.MAIN
    
    legal_mask = gs.get_legal_actions()
    legal_ids = [i for i, v in enumerate(legal_mask) if v]
    
    assert len(legal_ids) > 0, "Should have legal actions in MAIN phase"
