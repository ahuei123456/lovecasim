"""
Test GROUP_FILTER functionality with alias-aware matching.
Verifies that group filters work correctly for franchise and subunit names.
"""

import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game_state import (
    _get_group_aliases,
    _card_matches_group,
    GROUP_ALIASES,
    MemberCard,
    LiveCard
)
import numpy as np


class TestGroupAliases:
    """Test the _get_group_aliases helper function."""
    
    def test_short_name_to_full(self):
        """Test that short names map to full series names."""
        aliases = _get_group_aliases("μ's")
        assert "μ's" in aliases
        assert "ラブライブ！" in aliases
        print("✓ μ's -> ラブライブ！")
    
    def test_liella_mapping(self):
        """Test Liella! franchise mapping."""
        aliases = _get_group_aliases("Liella!")
        assert "Liella!" in aliases
        assert "ラブライブ！スーパースター!!" in aliases
        print("✓ Liella! -> ラブライブ！スーパースター!!")
    
    def test_hasunosora_mapping(self):
        """Test Hasunosora franchise mapping."""
        aliases = _get_group_aliases("蓮ノ空")
        assert "蓮ノ空" in aliases
        assert "ラブライブ！蓮ノ空女学院スクールアイドルクラブ" in aliases
        print("✓ 蓮ノ空 -> ラブライブ！蓮ノ空女学院スクールアイドルクラブ")
    
    def test_subunit_mapping(self):
        """Test subunit name identity mapping."""
        aliases = _get_group_aliases("5yncri5e!")
        assert "5yncri5e!" in aliases
        print("✓ 5yncri5e! subunit recognized")
    
    def test_brackets_stripped(self):
        """Test that Japanese brackets are stripped correctly."""
        aliases = _get_group_aliases("『Liella!』")
        assert "Liella!" in aliases
        assert "ラブライブ！スーパースター!!" in aliases
        print("✓ Brackets stripped correctly")
    
    def test_reverse_mapping(self):
        """Test that full series names map back to short names."""
        aliases = _get_group_aliases("ラブライブ！")
        assert "ラブライブ！" in aliases
        assert "μ's" in aliases
        print("✓ Reverse mapping: ラブライブ！ -> μ's")


class TestCardMatchesGroup:
    """Test the _card_matches_group helper function."""
    
    def setup_method(self):
        """Create test cards."""
        self.member_muse = MemberCard(
            card_id=1,
            card_no="TEST-001",
            name="Test Member",
            cost=3,
            hearts=np.zeros(6, dtype=np.int32),
            blade_hearts=np.zeros(7, dtype=np.int32),
            blades=0,
            group="ラブライブ！",  # Full series name in cards.json
            unit=""
        )
        
        self.member_liella = MemberCard(
            card_id=2,
            card_no="TEST-002", 
            name="Kanon",
            cost=4,
            hearts=np.zeros(6, dtype=np.int32),
            blade_hearts=np.zeros(7, dtype=np.int32),
            blades=0,
            group="ラブライブ！スーパースター!!",
            unit="5yncri5e!"  # With subunit
        )
        
        self.live_hasunosora = LiveCard(
            card_id=3,
            card_no="TEST-003",
            name="Dream Believers",
            score=2,
            required_hearts=np.zeros(7, dtype=np.int32),
            group="ラブライブ！蓮ノ空女学院スクールアイドルクラブ"
        )
    
    def test_match_with_short_name(self):
        """Test matching using short franchise name."""
        # Card has full series name, filter uses short name
        assert _card_matches_group(self.member_muse, "μ's")
        print("✓ μ's matches card with ラブライブ！ group")
    
    def test_match_with_full_name(self):
        """Test matching using full series name."""
        assert _card_matches_group(self.member_muse, "ラブライブ！")
        print("✓ ラブライブ！ matches directly")
    
    def test_match_liella_short(self):
        """Test Liella! short name matching."""
        assert _card_matches_group(self.member_liella, "Liella!")
        print("✓ Liella! matches card with ラブライブ！スーパースター!! group")
    
    def test_match_subunit(self):
        """Test subunit matching via unit field."""
        assert _card_matches_group(self.member_liella, "5yncri5e!")
        print("✓ 5yncri5e! matches card with 5yncri5e! unit")
    
    def test_live_card_matching(self):
        """Test LiveCard matching with short name."""
        assert _card_matches_group(self.live_hasunosora, "蓮ノ空")
        print("✓ 蓮ノ空 matches LiveCard")
    
    def test_no_filter_matches_all(self):
        """Test that empty filter matches everything."""
        assert _card_matches_group(self.member_muse, "")
        assert _card_matches_group(self.member_muse, None)
        print("✓ Empty filter matches all cards")
    
    def test_wrong_group_no_match(self):
        """Test that wrong group doesn't match."""
        assert not _card_matches_group(self.member_muse, "Aqours")
        print("✓ Aqours doesn't match μ's card")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("GROUP_FILTER Alias Tests")
    print("=" * 60)
    
    print("\n--- Testing _get_group_aliases ---")
    alias_tests = TestGroupAliases()
    alias_tests.test_short_name_to_full()
    alias_tests.test_liella_mapping()
    alias_tests.test_hasunosora_mapping()
    alias_tests.test_subunit_mapping()
    alias_tests.test_brackets_stripped()
    alias_tests.test_reverse_mapping()
    
    print("\n--- Testing _card_matches_group ---")
    match_tests = TestCardMatchesGroup()
    match_tests.setup_method()
    match_tests.test_match_with_short_name()
    match_tests.test_match_with_full_name()
    match_tests.test_match_liella_short()
    match_tests.test_match_subunit()
    match_tests.test_live_card_matching()
    match_tests.test_no_filter_matches_all()
    match_tests.test_wrong_group_no_match()
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
