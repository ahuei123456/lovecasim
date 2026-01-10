import numpy as np

from engine.game.game_state import Condition, ConditionType, GameState, Group, MemberCard
from engine.models.enums import ensure_group_list

print("DEBUG Start")

# 1. Test Validator
try:
    groups = ensure_group_list("ラブライブ！スーパースター!!")
    print(f"Validator Output: {groups} (Type: {type(groups)})")
    if groups and isinstance(groups[0], Group):
        print(f"Group Value: {groups[0].value}")
except Exception as e:
    print(f"Validator Error: {e}")

# 2. Test MemberCard Instantiation
try:
    m = MemberCard(
        card_id=1,
        card_no="L-001",
        name="Kanon",
        cost=1,
        hearts=np.zeros(6, dtype=np.int32),
        blade_hearts=np.zeros(7, dtype=np.int32),
        blades=1,
        groups=[Group.from_japanese_name("ラブライブ！スーパースター!!")],
    )
    print(f"MemberCard.groups: {m.groups} (Type: {type(m.groups)})")
except Exception as e:
    print(f"MemberCard Error: {e}")

# 3. Test GameState Check
game = GameState()
p0 = game.players[0]
p0.stage[0] = 1
game.member_db[1] = m

cond = Condition(ConditionType.GROUP_FILTER, {"group": "Liella!", "zone": "STAGE"})
try:
    res = game._check_condition(p0, cond)
    print(f"Condition Check Result: {res}")
except Exception as e:
    print(f"Condition Check Error: {e}")

# Debug internal check logic
target_group = Group.from_japanese_name("Liella!")
print(f"Target Group from 'Liella!': {target_group}")
print(f"Is Target ({target_group}) in Member Groups ({m.groups})? {target_group in m.groups}")
