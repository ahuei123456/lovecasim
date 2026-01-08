
import numpy as np
import sys
from game.game_state import GameState, PlayerState, MemberCard, Phase
from game.ability import Ability, TriggerType, Effect, EffectType, TargetType, Condition, ConditionType

# Redirect stdout to a file for clean output
with open('test_cross_output.txt', 'w', encoding='utf-8') as f:
    sys.stdout = f
    
    def test_group_alias():
        print("\n=== Testing Group Alias (μ's -> ラブライブ！) ===")
        gs = GameState(verbose=True)
        p0 = gs.players[0]
        
        # Member with 'ラブライブ！' series
        m1 = MemberCard(1, "Honoka", 2, np.zeros(6), np.zeros(6), 1, group="ラブライブ！")
        GameState.member_db = {1: m1}
        
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
        print("\n=== Testing Subunit Match (Printemps) ===")
        gs = GameState(verbose=True)
        p0 = gs.players[0]
        
        # Member with 'Printemps' unit
        m1 = MemberCard(1, "Honoka", 2, np.zeros(6), np.zeros(6), 1, group="ラブライブ！", unit="Printemps")
        GameState.member_db = {1: m1}
        
        p0.stage[1] = 1 # Honoka in center
        
        # Condition: Count 『Printemps』 members >= 1
        cond = Condition(ConditionType.COUNT_GROUP, {'group': "Printemps", 'min': 1})
        met = gs._check_condition(p0, cond)
        
        print(f"Condition 『Printemps』 met: {met}")
        if met:
            print("SUBUNIT MATCH SUCCESS!")
        else:
            print("SUBUNIT MATCH FAILED!")

    def test_named_member_targeting():
        print("\n=== Testing Named Member Targeting (「Honoka」 buff) ===")
        gs = GameState(verbose=True)
        p0 = gs.players[0]
        
        m1 = MemberCard(1, "高坂 穂乃果", 2, np.zeros(6), np.zeros(6), 1)
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
