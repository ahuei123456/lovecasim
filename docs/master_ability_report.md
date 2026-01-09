# Master Ability Verification Dashboard

## 1. System Summary

| Metric | Count | Status |
|--------|-------|--------|
| Total Cards | 1329 | - |
| Cards with Abilities | 741 | - |
| Successful Parse | 741 | ✅ |
| Behaviorally Verified | 600 | ✅ |
| Semantic Gaps found | 264 | ⚠️ |
| Heuristic Issues found | 21 | ❌ |
| Cards with FAQ | 257 | - |

## 2. Verification by Complexity Tier

| Tier | Score Range | Total Cards | Verified | % |
|------|-------------|-------------|----------|---|
| S | ≥ 35 (Final Boss) | 551 | 472 | 85.7% 💪 |
| A | ≥ 20 (Complex) | 155 | 105 | 67.7% 💪 |
| B | ≥ 10 (Advanced) | 23 | 12 | 52.2% 💪 |
| C | ≥ 5 (Standard) | 7 | 6 | 85.7% 💪 |
| D | < 5 (Minimal) | 5 | 5 | 100.0% 🏆 |

## 3. Effect Coverage

| Effect Type | Count |
|-------------|-------|
| SWAP_CARDS | 380 |
| DRAW | 162 |
| MOVE_TO_DECK | 140 |
| BUFF_POWER | 135 |
| ADD_BLADES | 134 |
| LOOK_AND_CHOOSE | 106 |
| RECOVER_LIVE | 105 |
| BOOST_SCORE | 105 |
| LOOK_DECK | 103 |
| REVEAL_CARDS | 96 |
| ADD_HEARTS | 88 |
| META_RULE | 86 |
| ADD_TO_HAND | 83 |
| RECOVER_MEMBER | 77 |
| TAP_OPPONENT | 64 |

## 3. Analysis Breakdown

### Semantic Gaps (Keyword Mismatch)
- Missing 'live interaction': 109 cards
- Missing 'opponent interaction': 59 cards
- Missing 'hearts': 46 cards
- Missing 'choice': 41 cards
- Missing 'blades': 37 cards
- Missing 'energy': 35 cards
- Missing 'score interaction': 23 cards
- Missing 'discard interaction': 20 cards
- Missing 'reveal': 7 cards
- Missing 'deck interaction': 6 cards

### Heuristic Issues (Logic Gaps)
- MISSING_SCORE: 18 cards
- MISSING_BLADES: 2 cards
- MISSING_HEARTS: 1 cards

## 4. Problematic Cards (Sample)

### PL!-sd1-003-SD: 南 ことり ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室からコスト4以下の『μ's』のメンバーカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。
```
**Parsed:** [On Play] COST_CHECK → Recover 1 Member card(s) from discard | [Live Start] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) → Discard/Swap 1 card(s) | [Turn End] → Gain 1 Heart(s)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 87)

---

### PL!-sd1-009-SD: 矢澤 にこ ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}自分の控え室に『μ's』のカードが25枚以上ある場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```
**Parsed:** [Live Start] COUNT_GROUP → Buff power/blade by 1 → Boost score by 1
⚠️ **Gaps:** Missing 'discard interaction'
📈 **Tier:** S (Score: 37)

---

### PL!-bp3-012-PR: 南 ことり ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、選んだハートを1つ得る。
```
**Parsed:** [Live Start] | [Turn End] → Gain 1 Heart(s)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 55)

---

### PL!-PR-001-PR: 高坂穂乃果 
**Text:**
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、メンバー1人をアクティブにしてもよい。
```
**Parsed:** [When Leaves] → Activate 1 member(s)
⚠️ **Gaps:** Missing 'discard interaction'
📈 **Tier:** C (Score: 9)

---

### PL!-PR-002-PR: 絢瀬絵里 
**Text:**
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、メンバー1人をアクティブにしてもよい。
```
**Parsed:** [When Leaves] → Activate 1 member(s)
⚠️ **Gaps:** Missing 'discard interaction'
📈 **Tier:** B (Score: 18)

---

### PL!-PR-005-PR: 星空 凛 
**Text:**
```
{{toujyou.png|登場}}以下から1つを選ぶ。
・カードを1枚引き、手札を1枚控え室に置く。
・相手のステージにいるすべてのコスト2以下のメンバーをウェイトにする。
```
**Parsed:** [On Play] → Choose one effect
⚠️ **Gaps:** Missing 'discard interaction', Missing 'opponent interaction'
📈 **Tier:** S (Score: 60)

---

### PL!-PR-006-PR: 西木野真姫 
**Text:**
```
{{toujyou.png|登場}}以下から1つを選ぶ。
・カードを1枚引き、手札を1枚控え室に置く。
・相手のステージにいるすべてのコスト2以下のメンバーをウェイトにする。
```
**Parsed:** [On Play] → Choose one effect
⚠️ **Gaps:** Missing 'discard interaction', Missing 'opponent interaction'
📈 **Tier:** S (Score: 55)

---

### PL!-PR-008-PR: 小泉花陽 
**Text:**
```
{{toujyou.png|登場}}以下から1つを選ぶ。
・カードを1枚引き、手札を1枚控え室に置く。
・相手のステージにいるすべてのコスト2以下のメンバーをウェイトにする。
```
**Parsed:** [On Play] → Choose one effect
⚠️ **Gaps:** Missing 'discard interaction', Missing 'opponent interaction'
📈 **Tier:** S (Score: 60)

---

### PL!S-PR-016-PR: 黒澤ダイヤ ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [On Play] → Gain 1 Blade(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** B (Score: 18)
📚 **FAQ:** 1 entries

---

### PL!S-PR-020-PR: 小原鞠莉 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [On Play] → Gain 1 Blade(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** B (Score: 18)
📚 **FAQ:** 1 entries

---

### PL!S-PR-021-PR: 黒澤ルビィ ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [On Play] → Gain 1 Blade(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** B (Score: 18)
📚 **FAQ:** 1 entries

---

### PL!HS-PR-010-PR: Reflection in the mirror 
**Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** A (Score: 26)

---

### PL!HS-PR-011-PR: Sparkly Spot 
**Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** A (Score: 26)

---

### PL!HS-PR-012-PR: アイデンティティ 
**Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** A (Score: 26)

---

### PL!HS-PR-019-PR: 百生 吟子 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚控え室に置く。それらがすべて{{heart_04.png|heart04}}を持つメンバーカードの場合、ライブ終了時まで、{{heart_04.png|heart04}}を得る。
```
**Parsed:** [On Play] → Move 1 card(s) to deck → Discard/Swap 3 card(s) | [Turn End] GROUP_FILTER → Gain 2 Heart(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 60)
📚 **FAQ:** 1 entries

---

### PL!HS-PR-021-PR: 安養寺 姫芽 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚控え室に置く。それらがすべて{{heart_01.png|heart01}}を持つメンバーカードの場合、ライブ終了時まで、{{heart_01.png|heart01}}を得る。
```
**Parsed:** [On Play] → Move 1 card(s) to deck → Discard/Swap 3 card(s) | [Turn End] GROUP_FILTER → Gain 2 Heart(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 60)
📚 **FAQ:** 1 entries

---

### LL-PR-004-PR: 愛♡スクリ～ム！ 
**Text:**
```
{{live_start.png|ライブ開始時}}相手に何が好き？と聞く。
回答がチョコミントかストロベリーフレイバーかクッキー＆クリームの場合、自分と相手は手札を1枚控え室に置く。
回答があなたの場合、自分と相手はカードを1枚引く。
回答がそれ以外の場合、ライブ終了時まで、自分と相手のステージにいるメンバーは{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [Live Start] → FLAVOR_ACTION | [Activated] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) MODAL_ANSWER → Discard/Swap 1 card(s) | [Activated] MODAL_ANSWER → Draw 1 card(s) | [Turn End] MODAL_ANSWER → Gain 1 Blade(s)
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 115)
📚 **FAQ:** 1 entries

---

### PL!N-bp1-004-R: 朝香果林 
**Text:**
```
{{toujyou.png|登場}}自分のステージにほかの『虹ヶ咲』のメンバーがいる場合、エネルギーを1枚アクティブにする。
```
**Parsed:** [On Play] GROUP_FILTER → Activate 1 member(s)
⚠️ **Gaps:** Missing 'energy'
📈 **Tier:** A (Score: 29)

---

### PL!N-bp1-004-P: 朝香果林 
**Text:**
```
{{toujyou.png|登場}}自分のステージにほかの『虹ヶ咲』のメンバーがいる場合、エネルギーを1枚アクティブにする。
```
**Parsed:** [On Play] GROUP_FILTER → Activate 1 member(s)
⚠️ **Gaps:** Missing 'energy'
📈 **Tier:** A (Score: 29)

---

### PL!N-bp1-025-L: 虹色Passions！ 
**Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** A (Score: 26)

---

### PL!N-bp1-026-L: Poppin' Up! 
**Text:**
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、エールにより公開された自分のカードの中から、『虹ヶ咲』のカードを1枚手札に加える。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Live Success] GROUP_FILTER LIFE_LEAD → Add 1 card(s) to hand → CHEER_REVEAL → SWAP_ZONE | [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades', Missing 'opponent interaction', Missing 'score interaction'
📈 **Tier:** S (Score: 82)
📚 **FAQ:** 2 entries

---

### PL!SP-bp1-001-R: 澁谷かのん 
**Text:**
```
{{jyouji.png|常時}}自分のステージにほかのメンバーがいない場合、自分はライブできない。
```
**Parsed:** [Constant] → Apply restriction
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** A (Score: 33)
📚 **FAQ:** 1 entries

---

### PL!SP-bp1-001-P: 澁谷かのん 
**Text:**
```
{{jyouji.png|常時}}自分のステージにほかのメンバーがいない場合、自分はライブできない。
```
**Parsed:** [Constant] → Apply restriction
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** A (Score: 33)
📚 **FAQ:** 1 entries

---

### PL!SP-bp1-003-R＋: 嵐 千砂都 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```
**Parsed:** [Activated] TURN_1 → Reveal 1 card(s) → Buff power/blade by 1 → Boost score by 1
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 45)
📚 **FAQ:** 3 entries

---

### PL!SP-bp1-003-P: 嵐 千砂都 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```
**Parsed:** [Activated] TURN_1 → Reveal 1 card(s) → Buff power/blade by 1 → Boost score by 1
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 45)
📚 **FAQ:** 3 entries

---

### PL!SP-bp1-003-P＋: 嵐 千砂都 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```
**Parsed:** [Activated] TURN_1 → Reveal 1 card(s) → Buff power/blade by 1 → Boost score by 1
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 45)
📚 **FAQ:** 3 entries

---

### PL!SP-bp1-003-SEC: 嵐 千砂都 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```
**Parsed:** [Activated] TURN_1 → Reveal 1 card(s) → Buff power/blade by 1 → Boost score by 1
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 45)
📚 **FAQ:** 3 entries

---

### PL!SP-bp1-025-L: Starlight Prologue 
**Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** A (Score: 26)

---

### PL!SP-bp1-026-L: 未来予報ハレルヤ！ 
**Text:**
```
{{live_start.png|ライブ開始時}}自分の、ステージと控え室に名前の異なる『Liella!』のメンバーが5人以上いる場合、このカードを使用するためのコストは{{heart_02.png|heart02}}{{heart_02.png|heart02}}{{heart_03.png|heart03}}{{heart_03.png|heart03}}{{heart_06.png|heart06}}{{heart_06.png|heart06}}になる。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Live Start] COUNT_GROUP | [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'discard interaction', Missing 'hearts', Missing 'blades'
📈 **Tier:** S (Score: 47)
📚 **FAQ:** 4 entries

---

### PL!HS-bp1-001-R: 日野下花帆 
**Text:**
```
{{toujyou.png|登場}}エネルギーを2枚アクティブにする。
```
**Parsed:** [On Play] → Activate 2 member(s)
⚠️ **Gaps:** Missing 'energy'
📈 **Tier:** A (Score: 23)

---

### PL!HS-bp1-001-P: 日野下花帆 
**Text:**
```
{{toujyou.png|登場}}エネルギーを2枚アクティブにする。
```
**Parsed:** [On Play] → Activate 2 member(s)
⚠️ **Gaps:** Missing 'energy'
📈 **Tier:** A (Score: 23)

---

### PL!HS-bp1-003-R＋: 乙宗 梢 ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}自分のステージのエリアすべてに『蓮ノ空』のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分の控え室から4コスト以下の『蓮ノ空』のメンバーカードを1枚手札に加える。
```
**Parsed:** [On Play] GROUP_FILTER → Boost score by 1 | [Activated] (Cost: ENERGY 1) TURN_1 → Recover 1 Member card(s) from discard
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 63)
📚 **FAQ:** 1 entries

---

### PL!HS-bp1-003-P: 乙宗 梢 ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}自分のステージのエリアすべてに『蓮ノ空』のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分の控え室から4コスト以下の『蓮ノ空』のメンバーカードを1枚手札に加える。
```
**Parsed:** [On Play] GROUP_FILTER → Boost score by 1 | [Activated] (Cost: ENERGY 1) TURN_1 → Recover 1 Member card(s) from discard
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 63)
📚 **FAQ:** 1 entries

---

### PL!HS-bp1-003-P＋: 乙宗 梢 ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}自分のステージのエリアすべてに『蓮ノ空』のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分の控え室から4コスト以下の『蓮ノ空』のメンバーカードを1枚手札に加える。
```
**Parsed:** [On Play] GROUP_FILTER → Boost score by 1 | [Activated] (Cost: ENERGY 1) TURN_1 → Recover 1 Member card(s) from discard
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 63)
📚 **FAQ:** 1 entries

---

### PL!HS-bp1-003-SEC: 乙宗 梢 ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}自分のステージのエリアすべてに『蓮ノ空』のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分の控え室から4コスト以下の『蓮ノ空』のメンバーカードを1枚手札に加える。
```
**Parsed:** [On Play] GROUP_FILTER → Boost score by 1 | [Activated] (Cost: ENERGY 1) TURN_1 → Recover 1 Member card(s) from discard
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 63)
📚 **FAQ:** 1 entries

---

### PL!HS-bp1-019-L: Dream Believers 
**Text:**
```
(エールで出た{{icon_score.png|スコア}}1つにつき、成功したライブのスコアの合計に1を加算する。)
```
**Parsed:** [Constant] → Buff power/blade by 1 → Boost score by 1
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** A (Score: 26)

---

### PL!HS-bp1-020-L: 365 Days 
**Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** A (Score: 26)

---

### PL!HS-bp1-021-L: Holiday∞Holiday 
**Text:**
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中から、『蓮ノ空』のライブカードを1枚手札に加える。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Live Success] → Recover 1 Live card(s) from discard → CHEER_REVEAL → SWAP_ZONE | [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** S (Score: 60)
📚 **FAQ:** 1 entries

---

### PL!HS-bp1-023-L: ド！ド！ド！ 
**Text:**
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高く、かつ自分のステージに『蓮ノ空』のメンバーがいる場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Live Success] GROUP_FILTER OPPONENT_HAS → Energy Charge 1 → Move 1 card(s) to deck → Tap 1 opponent's member(s) | [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades', Missing 'score interaction'
📈 **Tier:** S (Score: 92)
📚 **FAQ:** 1 entries

---

### PL!N-sd1-008-SD: エマ・ヴェルデ 
**Text:**
```
{{toujyou.png|登場}}エネルギーを2枚アクティブにする。
```
**Parsed:** [On Play] → Activate 2 member(s)
⚠️ **Gaps:** Missing 'energy'
📈 **Tier:** A (Score: 23)

---

### PL!N-sd1-025-SD: Colorful Dreams! Colorful Smiles! 
**Text:**
```
(エールで出た{{icon_score.png|スコア}}1つにつき、成功したライブのスコアの合計に1を加算する。)
```
**Parsed:** [Constant] → Buff power/blade by 1 → Boost score by 1
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** A (Score: 26)

---

### PL!N-sd1-026-SD: 夢が僕らの太陽さ 
**Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** A (Score: 26)

---

### PL!N-sd1-027-SD: Just Believe!!! 
**Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** A (Score: 26)

---

### PL!SP-sd1-001-SD: 澁谷かのん ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のエネルギー6枚につき、カードを1枚引く。
```
**Parsed:** [On Play] → Draw 6 card(s) → Buff power/blade by 1
⚠️ **Gaps:** Missing 'energy'
📈 **Tier:** S (Score: 46)

---

### PL!SP-sd1-004-SD: 平安名すみれ ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```
**Parsed:** [On Play] → Buff power/blade by 1 → Boost score by 1
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** A (Score: 26)
📚 **FAQ:** 1 entries

---

### PL!SP-sd1-023-SD: WE WILL!! 
**Text:**
```
(エールで出た{{icon_score.png|スコア}}1つにつき、成功したライブのスコアの合計に1を加算する。)
```
**Parsed:** [Constant] → Buff power/blade by 1 → Boost score by 1
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** A (Score: 26)

---

### PL!SP-sd1-024-SD: シェキラ☆☆☆ 
**Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** A (Score: 26)

---

### PL!SP-sd1-025-SD: 未来は風のように 
**Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Constant] → [Rule modifier] → [Rule modifier]
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** A (Score: 26)

---

### PL!SP-pb1-002-R: 唐 可可 ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}自分のエネルギーが12枚以上ある場合、ライブの合計スコアを＋１する。
```
**Parsed:** [Constant] COUNT_STAGE COUNT_ENERGY → Boost score by 1
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 35)

---

### PL!SP-pb1-002-P＋: 唐 可可 ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}自分のエネルギーが12枚以上ある場合、ライブの合計スコアを＋１する。
```
**Parsed:** [Constant] COUNT_STAGE COUNT_ENERGY → Boost score by 1
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 35)

---

### PL!SP-pb1-003-R: 嵐 千砂都 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のステージにいるメンバーが『5yncri5e!』のみの場合、自分と対戦相手は、センターエリアのメンバーを左サイドエリアに、左サイドエリアのメンバーを右サイドエリアに、右サイドエリアのメンバーをセンターエリアに、それぞれ移動させる。
```
**Parsed:** [On Play] GROUP_FILTER IS_CENTER IS_CENTER → Move member zone
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 46)

---

### PL!SP-pb1-003-P＋: 嵐 千砂都 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のステージにいるメンバーが『5yncri5e!』のみの場合、自分と対戦相手は、センターエリアのメンバーを左サイドエリアに、左サイドエリアのメンバーを右サイドエリアに、右サイドエリアのメンバーをセンターエリアに、それぞれ移動させる。
```
**Parsed:** [On Play] GROUP_FILTER IS_CENTER IS_CENTER → Move member zone
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 46)

---

### PL!SP-pb1-006-R: 桜小路きな子 ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動するたび、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
(対戦相手のカードの効果でも発動する。)
```
**Parsed:** [On Play] → Gain 1 Blade(s) → Move member zone
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'live interaction'
📈 **Tier:** S (Score: 36)
📚 **FAQ:** 2 entries

---

### PL!SP-pb1-006-P＋: 桜小路きな子 ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動するたび、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
(対戦相手のカードの効果でも発動する。)
```
**Parsed:** [On Play] → Gain 1 Blade(s) → Move member zone
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'live interaction'
📈 **Tier:** S (Score: 36)
📚 **FAQ:** 2 entries

---

### PL!SP-pb1-007-R: 米女メイ 
**Text:**
```
{{live_start.png|ライブ開始時}}エネルギーを2枚アクティブにする。
```
**Parsed:** [Live Start] → Activate 2 member(s)
⚠️ **Gaps:** Missing 'energy'
📈 **Tier:** A (Score: 23)

---

### PL!SP-pb1-007-P＋: 米女メイ 
**Text:**
```
{{live_start.png|ライブ開始時}}エネルギーを2枚アクティブにする。
```
**Parsed:** [Live Start] → Activate 2 member(s)
⚠️ **Gaps:** Missing 'energy'
📈 **Tier:** A (Score: 23)

---

### PL!SP-pb1-008-R: 若菜四季 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}カードを1枚引く。その後、登場したエリアとは別の自分のエリア1つを選ぶ。このメンバーをそのエリアに移動する。選んだエリアにメンバーがいる場合、そのメンバーは、このメンバーがいたエリアに移動させる。
```
**Parsed:** [On Play] → Draw 1 card(s) | [On Play] → Move member zone → Move member zone
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 66)

---

### PL!SP-pb1-008-P＋: 若菜四季 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}カードを1枚引く。その後、登場したエリアとは別の自分のエリア1つを選ぶ。このメンバーをそのエリアに移動する。選んだエリアにメンバーがいる場合、そのメンバーは、このメンバーがいたエリアに移動させる。
```
**Parsed:** [On Play] → Draw 1 card(s) | [On Play] → Move member zone → Move member zone
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 66)

---

### PL!SP-pb1-020-N: 鬼塚夏美 ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}このメンバーがエリアを移動するたび、カードを1枚引く。
(対戦相手のカードの効果でも発動する。)
```
**Parsed:** [When Leaves] → Draw 1 card(s) → Move member zone
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 36)

---

### PL!SP-pb1-023-L: ディストーション 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージに名前の異なる『CatChu!』のメンバーが2人以上いる場合、エネルギーを6枚までアクティブにする。その後、自分のエネルギーがすべてアクティブ状態の場合、このカードのスコアを＋１する。
```
**Parsed:** [Live Start] COUNT_GROUP → Activate 6 member(s) → Boost score by 1
⚠️ **Gaps:** Missing 'energy'
📈 **Tier:** S (Score: 47)
📚 **FAQ:** 3 entries

---

### PL!SP-pb1-025-L: Jellyfish 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージにいる、このターン中に登場、またはエリアを移動した『5yncri5e!』のメンバー1人につき、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}減らす。
```
**Parsed:** [On Play] → REDUCE_HEART_REQ → Buff power/blade by 1 → Move member zone
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 49)
📚 **FAQ:** 2 entries

---

### PL!S-bp2-003-R: 松浦果南 ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、ライブ終了時まで、［緑ハート］を得る。
```
**Parsed:** [When Leaves] TURN_1 → CHEER_REVEAL → Gain 1 Heart(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 37)

---

### PL!S-bp2-003-P: 松浦果南 ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、ライブ終了時まで、［緑ハート］を得る。
```
**Parsed:** [When Leaves] TURN_1 → CHEER_REVEAL → Gain 1 Heart(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 37)

---

### PL!S-bp2-004-R: 黒澤ダイヤ ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードがないとき、それらのカードをすべて控え室に置いてもよい。これにより1枚以上のカードが控え室に置かれた場合、そのエールで得たブレードハートを失い、もう一度エールを行う。
```
**Parsed:** [When Leaves] TURN_1 COUNT_DISCARD → CHEER_REVEAL → Discard/Swap 1 card(s) → Discard/Swap 1 card(s)
⚠️ **Gaps:** Missing 'hearts', Missing 'blades', Missing 'live interaction'
📈 **Tier:** S (Score: 56)
📚 **FAQ:** 1 entries

---

### PL!S-bp2-004-P: 黒澤ダイヤ ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードがないとき、それらのカードをすべて控え室に置いてもよい。これにより1枚以上のカードが控え室に置かれた場合、そのエールで得たブレードハートを失い、もう一度エールを行う。
```
**Parsed:** [When Leaves] TURN_1 COUNT_DISCARD → CHEER_REVEAL → Discard/Swap 1 card(s) → Discard/Swap 1 card(s)
⚠️ **Gaps:** Missing 'hearts', Missing 'blades', Missing 'live interaction'
📈 **Tier:** S (Score: 56)
📚 **FAQ:** 1 entries

---

### PL!S-bp2-008-R＋: 小原鞠莉 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3枚以上ある場合、代わりに合計スコアを＋２する。」を得る。
```
**Parsed:** [On Play] → Move 1 card(s) to deck → Discard/Swap 1 card(s) → Move 1 card(s) to deck | [On Play] COUNT_GROUP COUNT_STAGE → CHEER_REVEAL → Boost score by 1 → [Rule modifier] → Boost score by 2 → REPLACE_EFFECT
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 126)
📚 **FAQ:** 1 entries

---

### PL!S-bp2-008-P: 小原鞠莉 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3枚以上ある場合、代わりに合計スコアを＋２する。」を得る。
```
**Parsed:** [On Play] → Move 1 card(s) to deck → Discard/Swap 1 card(s) → Move 1 card(s) to deck | [On Play] COUNT_GROUP COUNT_STAGE → CHEER_REVEAL → Boost score by 1 → [Rule modifier] → Boost score by 2 → REPLACE_EFFECT
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 126)
📚 **FAQ:** 1 entries

---

### PL!S-bp2-008-P＋: 小原鞠莉 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3枚以上ある場合、代わりに合計スコアを＋２する。」を得る。
```
**Parsed:** [On Play] → Move 1 card(s) to deck → Discard/Swap 1 card(s) → Move 1 card(s) to deck | [On Play] COUNT_GROUP COUNT_STAGE → CHEER_REVEAL → Boost score by 1 → [Rule modifier] → Boost score by 2 → REPLACE_EFFECT
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 126)
📚 **FAQ:** 1 entries

---

### PL!S-bp2-008-SEC: 小原鞠莉 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3枚以上ある場合、代わりに合計スコアを＋２する。」を得る。
```
**Parsed:** [On Play] → Move 1 card(s) to deck → Discard/Swap 1 card(s) → Move 1 card(s) to deck | [On Play] COUNT_GROUP COUNT_STAGE → CHEER_REVEAL → Boost score by 1 → [Rule modifier] → Boost score by 2 → REPLACE_EFFECT
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 126)
📚 **FAQ:** 1 entries

---

### PL!S-bp2-022-L: 未熟DREAMER 
**Text:**
```
{{live_success.png|ライブ成功時}}このターン、自分のデッキがリフレッシュしていた場合、このカードのスコアを＋２する。
```
**Parsed:** [Live Success] → Boost score by 2
⚠️ **Gaps:** Missing 'deck interaction'
📈 **Tier:** A (Score: 23)
📚 **FAQ:** 1 entries

---

### PL!SP-bp2-001-R＋: 澁谷かのん ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```
**Parsed:** [On Play] GROUP_FILTER → Buff power/blade by 1 → NEGATE_EFFECT → Recover 1 Member card(s) from discard → NEGATE_EFFECT
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 53)
📚 **FAQ:** 2 entries

---

### PL!SP-bp2-001-P: 澁谷かのん ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```
**Parsed:** [On Play] GROUP_FILTER → Buff power/blade by 1 → NEGATE_EFFECT → Recover 1 Member card(s) from discard → NEGATE_EFFECT
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 53)
📚 **FAQ:** 2 entries

---

### PL!SP-bp2-001-P＋: 澁谷かのん ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```
**Parsed:** [On Play] GROUP_FILTER → Buff power/blade by 1 → NEGATE_EFFECT → Recover 1 Member card(s) from discard → NEGATE_EFFECT
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 53)
📚 **FAQ:** 2 entries

---

### PL!SP-bp2-001-SEC: 澁谷かのん ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```
**Parsed:** [On Play] GROUP_FILTER → Buff power/blade by 1 → NEGATE_EFFECT → Recover 1 Member card(s) from discard → NEGATE_EFFECT
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 53)
📚 **FAQ:** 2 entries

---

### PL!SP-bp2-008-R: 若菜四季 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：このメンバーがいるエリアとは別の自分のエリア1つを選ぶ。このメンバーをそのエリアに移動する。選んだエリアにメンバーがいる場合、そのメンバーは、このメンバーがいたエリアに移動させる。
```
**Parsed:** [Activated] (Cost: ENERGY 1) TURN_1 → Move member zone → Move member zone
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 54)

---

### PL!SP-bp2-008-P: 若菜四季 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：このメンバーがいるエリアとは別の自分のエリア1つを選ぶ。このメンバーをそのエリアに移動する。選んだエリアにメンバーがいる場合、そのメンバーは、このメンバーがいたエリアに移動させる。
```
**Parsed:** [Activated] (Cost: ENERGY 1) TURN_1 → Move member zone → Move member zone
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 54)

---

### PL!SP-bp2-010-R＋: ウィーン・マルガレーテ ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。
{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。
```
**Parsed:** [Constant] → [Rule modifier] | [Live Start] NOT COUNT_STAGE → Buff power/blade by 1
⚠️ **Gaps:** Missing 'hearts', Missing 'opponent interaction', Missing 'reveal'
📈 **Tier:** S (Score: 52)
📚 **FAQ:** 4 entries

---

### PL!SP-bp2-010-P: ウィーン・マルガレーテ ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。
{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。
```
**Parsed:** [Constant] → [Rule modifier] | [Live Start] NOT COUNT_STAGE → Buff power/blade by 1
⚠️ **Gaps:** Missing 'hearts', Missing 'opponent interaction', Missing 'reveal'
📈 **Tier:** S (Score: 52)
📚 **FAQ:** 4 entries

---

### PL!SP-bp2-010-P＋: ウィーン・マルガレーテ ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。
{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。
```
**Parsed:** [Constant] → [Rule modifier] | [Live Start] NOT COUNT_STAGE → Buff power/blade by 1
⚠️ **Gaps:** Missing 'hearts', Missing 'opponent interaction', Missing 'reveal'
📈 **Tier:** S (Score: 52)
📚 **FAQ:** 4 entries

---

### PL!SP-bp2-010-SEC: ウィーン・マルガレーテ ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。
{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。
```
**Parsed:** [Constant] → [Rule modifier] | [Live Start] NOT COUNT_STAGE → Buff power/blade by 1
⚠️ **Gaps:** Missing 'hearts', Missing 'opponent interaction', Missing 'reveal'
📈 **Tier:** S (Score: 52)
📚 **FAQ:** 4 entries

---

### PL!SP-bp2-011-R: 鬼塚冬毬 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室にある、カード名の異なるライブカードを2枚選ぶ。そうした場合、相手はそれらのカードのうち1枚を選ぶ。これにより相手に選ばれたカードを自分の手札に加える。
```
**Parsed:** [On Play] → [Rule modifier] → Add 1 card(s) to hand
⚠️ **Gaps:** Missing 'discard interaction', Missing 'opponent interaction', Missing 'live interaction', Missing 'choice'
📈 **Tier:** S (Score: 53)
📚 **FAQ:** 1 entries

---

### PL!SP-bp2-011-P: 鬼塚冬毬 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室にある、カード名の異なるライブカードを2枚選ぶ。そうした場合、相手はそれらのカードのうち1枚を選ぶ。これにより相手に選ばれたカードを自分の手札に加える。
```
**Parsed:** [On Play] → [Rule modifier] → Add 1 card(s) to hand
⚠️ **Gaps:** Missing 'discard interaction', Missing 'opponent interaction', Missing 'live interaction', Missing 'choice'
📈 **Tier:** S (Score: 53)
📚 **FAQ:** 1 entries

---

### PL!SP-bp2-015-N: 平安名すみれ ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_06.png|heart06}}を得る。
```
**Parsed:** [When Leaves] TURN_1 → CHEER_REVEAL → Gain 6 Blade(s) → Gain 1 Heart(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 45)
📚 **FAQ:** 2 entries

---

### PL!SP-bp2-020-N: 鬼塚夏美 ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_02.png|heart02}}を得る。
```
**Parsed:** [When Leaves] TURN_1 → CHEER_REVEAL → Gain 2 Blade(s) → Gain 1 Heart(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 45)
📚 **FAQ:** 2 entries

---

### PL!SP-bp2-021-N: ウィーン・マルガレーテ ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_03.png|heart03}}を得る。
```
**Parsed:** [When Leaves] TURN_1 → CHEER_REVEAL → Gain 3 Blade(s) → Gain 1 Heart(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 45)
📚 **FAQ:** 2 entries

---

### PL!SP-bp2-023-L: Go!! リスタート 
**Text:**
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場のカード枚数が相手より少ない場合、このカードのスコアを＋１する。
```
**Parsed:** [Live Start] → Buff power/blade by 1 → Boost score by 1
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 36)

---

### PL!SP-bp2-024-L: ビタミンSUMMER！ 
**Text:**
```
{{live_success.png|ライブ成功時}}自分の手札の枚数が相手より多い場合、このカードのスコアを＋１する。
```
**Parsed:** [Live Success] → Buff power/blade by 1 → Boost score by 1
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 36)
📚 **FAQ:** 3 entries

---

### PL!HS-bp2-001-R: 日野下花帆 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室からスコア3以下の『蓮ノ空』のライブカードを1枚手札に加える。
```
**Parsed:** [Activated] (Cost: ENERGY 2) TURN_1 → Recover 1 Live card(s) from discard
⚠️ **Gaps:** Missing 'score interaction'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** S (Score: 39)

---

### PL!HS-bp2-001-P: 日野下花帆 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室からスコア3以下の『蓮ノ空』のライブカードを1枚手札に加える。
```
**Parsed:** [Activated] (Cost: ENERGY 2) TURN_1 → Recover 1 Live card(s) from discard
⚠️ **Gaps:** Missing 'score interaction'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** S (Score: 39)

---

### PL!HS-bp2-005-R＋: 大沢瑠璃乃 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、自分の控え室から『みらくらぱーく！』のカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：自分のステージのエリアすべてにメンバーが登場している場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [On Play] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) GROUP_FILTER → Recover 1 Member card(s) from discard → Discard/Swap 1 card(s) | [On Play] (Cost: ENERGY 1) → Gain 1 Blade(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 70)

---

### PL!HS-bp2-005-P: 大沢瑠璃乃 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、自分の控え室から『みらくらぱーく！』のカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：自分のステージのエリアすべてにメンバーが登場している場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [On Play] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) GROUP_FILTER → Recover 1 Member card(s) from discard → Discard/Swap 1 card(s) | [On Play] (Cost: ENERGY 1) → Gain 1 Blade(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 70)

---

### PL!HS-bp2-005-P＋: 大沢瑠璃乃 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、自分の控え室から『みらくらぱーく！』のカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：自分のステージのエリアすべてにメンバーが登場している場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [On Play] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) GROUP_FILTER → Recover 1 Member card(s) from discard → Discard/Swap 1 card(s) | [On Play] (Cost: ENERGY 1) → Gain 1 Blade(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 70)

---

### PL!HS-bp2-005-SEC: 大沢瑠璃乃 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、自分の控え室から『みらくらぱーく！』のカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：自分のステージのエリアすべてにメンバーが登場している場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [On Play] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) GROUP_FILTER → Recover 1 Member card(s) from discard → Discard/Swap 1 card(s) | [On Play] (Cost: ENERGY 1) → Gain 1 Blade(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 70)

---

### PL!HS-bp2-008-R: 徒町 小鈴 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}このメンバーよりコストが低い『DOLLCHESTRA』のメンバーからバトンタッチして登場した場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [On Play] GROUP_FILTER → Gain 1 Blade(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** A (Score: 24)
📚 **FAQ:** 1 entries

---

### PL!HS-bp2-008-P: 徒町 小鈴 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}このメンバーよりコストが低い『DOLLCHESTRA』のメンバーからバトンタッチして登場した場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [On Play] GROUP_FILTER → Gain 1 Blade(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** A (Score: 24)
📚 **FAQ:** 1 entries

---

### PL!HS-bp2-009-R: 安養寺 姫芽 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}{{icon_energy.png|E}}支払ってもよい：このメンバーよりコストが低い『みらくらぱーく！』のメンバーからバトンタッチして登場した場合、ライブ終了時まで、{{heart_01.png|heart01}}{{heart_01.png|heart01}}を得る。
```
**Parsed:** [On Play] (Cost: ENERGY 1) GROUP_FILTER → Gain 2 Heart(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** A (Score: 29)
📚 **FAQ:** 1 entries

---

### PL!HS-bp2-009-P: 安養寺 姫芽 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}{{icon_energy.png|E}}支払ってもよい：このメンバーよりコストが低い『みらくらぱーく！』のメンバーからバトンタッチして登場した場合、ライブ終了時まで、{{heart_01.png|heart01}}{{heart_01.png|heart01}}を得る。
```
**Parsed:** [On Play] (Cost: ENERGY 1) GROUP_FILTER → Gain 2 Heart(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** A (Score: 29)
📚 **FAQ:** 1 entries

---

### PL!HS-bp2-014-N: 大沢瑠璃乃 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}カードを1枚引く。ライブ終了時まで、自分はライブできない。
```
**Parsed:** [On Play] → Draw 1 card(s) | [Turn End] → Buff power/blade by 1 → Apply restriction
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 59)
📚 **FAQ:** 1 entries

---

### PL!HS-bp2-018-N: 安養寺 姫芽 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のメインフェイズの場合、{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分の控え室からライブカードを1枚、表向きでライブカード置き場に置く。次のライブカードセットフェイズで自分がライブカード置き場に置けるカード枚数の上限が1枚減る。
```
**Parsed:** [On Play] (Cost: ENERGY 2) → [Rule modifier] → Discard/Swap 1 card(s) → Buff power/blade by 1
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 44)

---

### PL!HS-bp2-019-L: Bloom the smile, Bloom the dream! 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージに『蓮ノ空』のメンバーがいる場合、このカードを成功させるための必要ハートは、{{heart_01.png|heart01}}{{heart_01.png|heart01}}{{heart_00.png|heart0}}か、{{heart_04.png|heart04}}{{heart_04.png|heart04}}{{heart_00.png|heart0}}か、{{heart_05.png|heart05}}{{heart_05.png|heart05}}{{heart_00.png|heart0}}のうち、選んだ1つにしてもよい。
```
**Parsed:** [Live Start] GROUP_FILTER
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** A (Score: 28)
📚 **FAQ:** 1 entries

---

