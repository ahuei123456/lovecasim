
import sys
import os
import unittest
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from engine.game.game_state import GameState, PlayerState, MemberCard, Phase
from engine.game.ability import Ability, TriggerType, Effect, EffectType, TargetType, Condition, ConditionType

# Redirect stdout to a file for clean output
with open('test_cross_output.txt', 'w', encoding='utf-8') as f:
    sys.stdout = f
    
    def test_group_alias():
        print("\n=== Testing Group Alias (μ's -> ラブライブ！) ===")
        gs = GameState(verbose=True)
        p0 = gs.players[0]
        
        # Member with 'ラブライブ！' series
        GameState.member_db[1] = MemberCard(1, "MS-01", "MemberMuse", 4, np.zeros(6), np.zeros(7), 1, group="μ's")  # Alias target
        GameState.member_db[2] = MemberCard(2, "LL-01", "MemberLoveLive", 3, np.zeros(6), np.zeros(7), 1, group="ラブライブ！")
        
        p0.stage[1] = 1 # Honoka in center
        
        # Condition: Count『μ's』members >= 1
        cond = Condition(ConditionType.COUNT_GROUP, {'group': "μ's", 'min': 1})
        met = gs._check_condition(p0, cond)
        
        print(f"Condition 『μ's』 met: {met}")
        if met:
            print("μ's ALIAS SUCCESS!")
        else:
            print("μ's ALIAS FAILED!")

    def test_subunit_match():
        """Verify μ's matches Printemps"""
        
        # Test generic group matching
        GameState.member_db[5] = MemberCard(5, "PT-01", "PrintempsMember", 3, np.zeros(6), np.zeros(7), 1, group="μ's", unit="Printemps")
        
        gs = GameState(verbose=True)
        p0 = gs.players[0]
        
        p0.stage[1] = 5 # PrintempsMember in center
        
        # Condition: Count 『Printemps』 members >= 1
        cond = Condition(ConditionType.COUNT_GROUP, {'group': "Printemps", 'min': 1})
        assert gs._check_condition(p0, cond, {}), "Should match Printemps group/unit"

    def test_named_member_targeting():
        print("\n=== Testing Named Member Targeting (「Honoka」 buff) ===")
        gs = GameState(verbose=True)
        p0 = gs.players[0]
        
        # Member named "Honoka"
        m1 = MemberCard(1, "HK-01", "高坂 穂乃果", 2, np.zeros(6), np.zeros(7), 1, group="μ's")
        GameState.member_db = {1: m1}
        
        p0.stage[0] = 1 # Honoka in slot 0 (Left)
        
        # Effect: Buff 「穂乃果」 with 1 power
        effect = Effect(EffectType.BUFF_POWER, 1, TargetType.MEMBER_NAMED, params={'target_name': "穂乃果"})
        gs.pending_effects.append(effect)
        
        # Resolve
        gs._resolve_pending_effect(0)
        
        # Verify continuous effect added for slot 0
        found = False
        for ce in p0.continuous_effects:
            if ce.get('target_slot') == 0:
                found = True
                break
                
        print(f"Buff applied to Slot 0: {found}")
        if found:
            print("NAMED TARGETING SUCCESS!")
        else:
            print("NAMED TARGETING FAILED!")

    if __name__ == "__main__":
        test_group_alias()
        test_subunit_match()
        test_named_member_targeting()
