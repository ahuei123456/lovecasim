| Successful Parse | 741 | ✅ 100% (for true abilities) |
| Behavioral Verified | 372 | ✅ 100% (for standard effects) |
| Semantic Gaps | 262 | ⚠️ Improved (Live/Deck/Opponent) |
| Cards with FAQ | 257 | - |

---

## Effect Types - Verification Status

| Effect Type | Est. Cards | Status | Notes |
|-------------|------------|--------|-------|
| DRAW | 162 | ✅ Verified | 100% Behavioral Pass |
| SWAP_CARDS | 380 | ⚠️ Partial | Parser Gaps closing |
| ADD_BLADES | 133 | ✅ Verified | 100% Behavioral Pass |
| ENERGY_CHARGE | 58 | ✅ Verified | 100% Behavioral Pass |
| BOOST_SCORE | 101 | ✅ Verified | 100% Behavioral Pass |
| RECOVER_MEMBER | 77 | ✅ Verified | 100% Behavioral Pass |
| RECOVER_LIVE | 84 | ⚠️ Partial | Parser improved |
| LOOK_AND_CHOOSE | ~50 | ⚠️ Partial | UI panel added |
| ADD_BLADES | ~60 | ❓ Unknown | Needs testing |
| ADD_HEARTS | ~30 | ❓ Unknown | Needs testing |
| ENERGY_CHARGE | ~25 | ❓ Unknown | Needs testing |
| SACRIFICE_SELF (cost) | ~20 | ✅ Verified | Tested with PL!-sd1-002-SD |
| META_RULE | ~10 | ✅ Verified | ALL Blade implemented |
| SWAP_CARDS | ~30 | ❓ Unknown | Needs testing |
| BUFF_POWER | ~20 | ❓ Unknown | Needs testing |
| SET_HEARTS | ~10 | ❓ Unknown | Needs testing |
| SET_BLADES | ~10 | ❓ Unknown | Needs testing |

---

## Trigger Types - Verification Status

| Trigger | Est. Count | Status | Notes |
|---------|------------|--------|-------|
| ON_PLAY | ~250 | ⚠️ Partial | Core trigger works |
| ACTIVATED | ~100 | ✅ Verified | Tested sacrifice flow |
| CONSTANT | ~80 | ⚠️ Partial | Meta rules work |
| ON_LIVE_START | ~40 | ❓ Unknown | Needs testing |
| ON_LIVE_SUCCESS | ~30 | ❓ Unknown | Needs testing |
| ON_ENTER_YELL | ~20 | ❓ Unknown | Needs testing |
| END_OF_TURN | ~15 | ❓ Unknown | Needs testing |

---

## Condition Types - Verification Status

| Condition | Count | Status | Notes |
|-----------|-------|--------|-------|
| COUNT_GROUP | ~40 | ❓ Unknown | Needs testing |
| COUNT_SUCCESS_LIVE | ~30 | ❓ Unknown | Needs testing |
| OPPONENT_HAND_DIFF | 2 | ✅ Verified | PL!S-pb1-001-R |
| HAS_MEMBER | ~15 | ❓ Unknown | Needs testing |

---

## Individually Tested Cards

| Card No | Name | Ability | Status |
|---------|------|---------|--------|
| PL!-sd1-002-SD | 絢瀬 絵里 | Sacrifice → Recover Member | ✅ Pass |
| PL!-sd1-001-SD | 高坂 穂乃果 | Constant +Blade per success | ⚠️ Partial |
| PL!S-pb1-001-R | 高海千歌 | On Play: Hand diff condition | ✅ Pass |
| PL!SP-bp1-010-R | ウィーン・マルガレーテ | Look 5, Pick 1 | ⚠️ UI done |

---

## Known Issues

1. **Empty deck triggers Refresh (Rule 10.2)**: Can cause unexpected discard clearing during tests
2. **Look & Choose UI**: Panel added but needs full verification
3. **Optional costs**: `てもよい` pattern needs skip action verification

---

## Next Steps

1. Create `tools/ability_verifier.py` - automated bulk tester
2. Test each effect type systematically
3. Run stress tests with random ability sequences
4. Document all failures in `tests/failing_cards.txt`
