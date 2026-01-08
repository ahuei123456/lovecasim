# Baseline Coverage Report (Pre-Phase 2)

## Overall Metrics
- **Total Cards**: 886
- **Fully Supported**: 209 (23.6%)
- **Partially Supported**: 677 (76.4%)

## Top Missing Effects (Need Engine Handlers)
1. **SWAP_CARDS**: 449 cards (50.7%) ⚠️ HIGH PRIORITY
2. **LOOK_AND_CHOOSE**: 106 cards (12.0%)
3. **TAP_OPPONENT**: 106 cards (12.0%)
4. **ADD_TO_HAND**: 104 cards (11.7%)
5. **LOOK_DECK**: 102 cards (11.5%)
6. **REVEAL_CARDS**: 96 cards (10.8%)
7. **RECOVER_LIVE**: 84 cards (9.5%)
8. **RECOVER_MEMBER**: 77 cards (8.7%)
9. **ENERGY_CHARGE**: 58 cards (6.5%)
10. **CHEER_REVEAL**: 56 cards (6.3%)

## Top Missing Conditions
1. **GROUP_FILTER**: 254 cards (28.7%) ⚠️ HIGH PRIORITY
2. **TURN_1**: 119 cards (13.4%)
3. **COUNT_STAGE**: 57 cards (6.4%)
4. **IS_CENTER**: 26 cards (2.9%)
5. **OPPONENT_HAS**: 13 cards (1.5%)

## Phase 1 Status
✅ **SWAP_CARDS** - Handler implemented (Phase 1)
✅ **LOOK_DECK** - Handler implemented (Phase 1)
✅ **LOOK_AND_CHOOSE** - Handler implemented (Phase 1)

**Expected Impact**: Phase 1 should move ~450 cards to "Fully Supported"
**Need to re-run analysis** to confirm Phase 1 impact

## Next Priorities (Phase 2)
Based on frequency:
1. **GROUP_FILTER** condition (254 cards)
2. **RECOVER_LIVE** / **RECOVER_MEMBER** (161 cards combined)
3. **TAP_OPPONENT** (106 cards)
4. **TURN_1** condition (119 cards)
