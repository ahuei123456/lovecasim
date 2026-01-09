# Card-by-Card Ability Analysis

## Methodology
1. Read each card ability individually
2. Document EXACTLY what it does
3. Note required effects, conditions, triggers
4. Group cards with IDENTICAL mechanics
5. Implement handlers for verified groups

---

## Batch 1: Cards 1-20

### Card #1: PL!-sd1-001-SD (高坂 穂乃果)
**Ability Text**:
- {{登場}}自分の成功ライブカード置き場にカードが2枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。
- {{常時}}自分の成功ライブカード置き場にあるカード1枚につき、{{ブレード}}を得る。

**Analysis**:
- Trigger: ON_PLAY
- Condition: COUNT_SUCCESS_PILE >= 2
- Effect: RECOVER_LIVE (from discard to hand, quantity=1)
- Trigger: CONSTANT
- Effect: ADD_BLADES (value = success_pile count)

**Required Handlers**:
- ✅ TriggerType.ON_PLAY (exists)
- 🆕 ConditionType.COUNT_SUCCESS_PILE (NEW)
- 🆕 EffectType.RECOVER_LIVE (NEW - needs SELECT_FROM_DISCARD)
- ✅ TriggerType.CONSTANT (exists)
- ✅ EffectType.ADD_BLADES (exists, but needs multiplier from condition)

**Similar Cards**: TBD (will check as I read more)

---

### Card #2: PL!-sd1-002-SD (絢瀬 絵里)
**Ability Text**:
- {{起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。

**Analysis**:
- Trigger: ACTIVATED
- Cost: SACRIFICE_SELF
- Effect: RECOVER_MEMBER (from discard to hand, quantity=1)

**Required Handlers**:
- ✅ TriggerType.ACTIVATED (exists)
- ✅ AbilityCostType.SACRIFICE_SELF (exists)
- 🆕 EffectType.RECOVER_MEMBER (NEW - needs SELECT_FROM_DISCARD)

**Pattern**: Sacrifice-for-recovery
**Similar Cards**: TBD

---

### Card #3: PL!-sd1-019-SD (START:DASH!!)
**Ability Text**:
- {{ライブ成功時}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。

**Analysis**:
- Trigger: ON_LIVE_SUCCESS
- Effect 1: LOOK_DECK (count=3)
- Effect 2: ORDER_DECK (player chooses order for top, rest to discard)

**Required Handlers**:
- ✅ TriggerType.ON_LIVE_SUCCESS (exists)
- ✅ EffectType.LOOK_DECK (Phase 1 - implemented)
- 🆕 EffectType.ORDER_DECK (NEW - interactive deck ordering)

**Pattern**: Deck manipulation
**Similar Cards**: Card #50 (similar "see and choose" mechanic)

---

### Card #4: PL!-sd1-022-SD (僕らは今のなかで)
**Ability Text**:
- {{ライブ開始時}}自分の成功ライブカード置き場にあるカード1枚につき、このカードを成功させるための必要ハートは{{heart0}}{{heart0}}少なくなる。

**Analysis**:
- Trigger: ON_LIVE_START
- Condition: (implicit - count success pile)
- Effect: REDUCE_HEARTS_REQUIRED (amount = success_pile_count * 2)

**Required Handlers**:
- ✅ TriggerType.ON_LIVE_START (exists)
- 🆕 EffectType.REDUCE_HEARTS_REQUIRED (NEW - modifies live card requirements)
- 🆕 Multiplier from success pile count

**Pattern**: Dynamic cost reduction
**Similar Cards**: TBD

---

### Card #5: PL!N-bp4-025-L (VIVID WORLD)
**Ability Text**:
- {{ライブ開始時}}ライブ終了時まで、エールによって公開される自分のカードが持つ[桃ブレード]、[赤ブレード]、[黄ブレード]、[緑ブレード]、[紫ブレード]、{{ALLブレード}}は、すべて[青ブレード]になる。
- {{ライブ成功時}}エールにより公開された自分の『虹ヶ咲』のメンバーカードが持つハートの中に{{heart01-06}}がある場合、このカードのスコアを＋１する。

**Analysis**:
- Trigger: ON_LIVE_START
- Effect: TRANSFORM_COLOR (all blade types → blue, duration: LIVE_END)
- Trigger: ON_LIVE_SUCCESS
- Condition: YELL_HAS_RAINBOW_HEARTS (check if all 6 colors present in yell)
- Effect: BOOST_SCORE (+1)

**Required Handlers**:
- ✅ TriggerType.ON_LIVE_START (exists)
- 🆕 EffectType.TRANSFORM_COLOR (NEW - color transformation)
- ✅ TriggerType.ON_LIVE_SUCCESS (exists)
- 🆕 ConditionType.YELL_HAS_RAINBOW (NEW)
- ✅ EffectType.BOOST_SCORE (exists)

**Pattern**: Yell manipulation
**Unique**: This is complex color transformation

---

## Pattern Summary (After 5 cards)

**New Handlers Needed**:
1. COUNT_SUCCESS_PILE condition
2. RECOVER_LIVE effect
3. RECOVER_MEMBER effect
4. ORDER_DECK effect
5. REDUCE_HEARTS_REQUIRED effect
6. TRANSFORM_COLOR effect
7. YELL_HAS_RAINBOW condition

**Grouping**:
- Cards #1, #2: Recovery mechanics (different sources)
- Card #3: Deck manipulation
- Card #4: Dynamic cost modification
- Card #5: Unique yell transformation

---

*Continuing analysis...*
