
import sys
import os
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from game.game_state import MemberCard, LiveCard

try:
    m = MemberCard(
        card_id=888,
        name="Easy Member",
        cost=1,
        hearts=np.array([1, 1, 1, 1, 1, 1], dtype=np.int32),
        blade_hearts=np.array([0, 0, 0, 0, 0, 0], dtype=np.int32),
        blades=1
    )
    print("MemberCard created successfully")
except Exception as e:
    print(f"Error creating MemberCard: {e}")
    
try:
    l = LiveCard(
        card_id=999,
        name="Easy Live",
        score=1,
        required_hearts=np.array([0, 0, 0, 0, 0, 0, 1], dtype=np.int32)
    )
    print("LiveCard created successfully")
except Exception as e:
    print(f"Error creating LiveCard: {e}")
