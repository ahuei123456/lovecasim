# Master Ability Verification Dashboard

## 1. System Summary

| Metric | Count | Status |
|--------|-------|--------|
| Total Cards | 1329 | - |
| Cards with Abilities | 741 | - |
| Successful Parse | 741 | ✅ |
| Behaviorally Verified | 600 | ✅ |
| Semantic Gaps found | 150 | ⚠️ |
| Heuristic Issues found | 25 | ❌ |
| Cards with FAQ | 257 | - |

## 2. Verification by Complexity Tier

| Tier | Score Range | Total Cards | Verified | % |
|------|-------------|-------------|----------|---|
| S | ≥ 35 (Final Boss) | 550 | 472 | 85.8% 💪 |
| A | ≥ 20 (Complex) | 153 | 105 | 68.6% 💪 |
| B | ≥ 10 (Advanced) | 23 | 12 | 52.2% 💪 |
| C | ≥ 5 (Standard) | 7 | 6 | 85.7% 💪 |
| D | < 5 (Minimal) | 8 | 5 | 62.5% 💪 |

## 3. Effect Coverage

| Effect Type | Count |
|-------------|-------|
| SWAP_CARDS | 380 |
| DRAW | 162 |
| MOVE_TO_DECK | 140 |
| ADD_BLADES | 133 |
| BUFF_POWER | 132 |
| LOOK_AND_CHOOSE | 106 |
| RECOVER_LIVE | 105 |
| LOOK_DECK | 103 |
| BOOST_SCORE | 102 |
| REVEAL_CARDS | 96 |
| ADD_HEARTS | 88 |
| META_RULE | 86 |
| ADD_TO_HAND | 83 |
| RECOVER_MEMBER | 77 |
| TAP_OPPONENT | 63 |

## 3. Analysis Breakdown

### Semantic Gaps (Keyword Mismatch)
- Missing 'opponent interaction': 45 cards
- Missing 'choice': 41 cards
- Missing 'hearts': 27 cards
- Missing 'blades': 23 cards
- Missing 'score interaction': 21 cards
- Missing 'live interaction': 16 cards
- Missing 'energy': 9 cards
- Missing 'discard interaction': 8 cards
- Missing 'reveal': 7 cards
- Missing 'deck interaction': 3 cards

### Heuristic Issues (Logic Gaps)
- MISSING_SCORE: 21 cards
- MISSING_BLADES: 3 cards
- MISSING_HEARTS: 1 cards

## 4. Problematic Cards (Sample)

### PL!-sd1-003-SD: 南 ことり ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室からコスト4以下の『μ's』のメンバーカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。
```
**Parsed:** [On Play] COST_CHECK → Recover 1 Member card(s) from discard | [Live Start] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) → Discard/Swap 1 card(s) | [Turn End - live] → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 87)

---

### PL!-bp3-012-PR: 南 ことり ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、選んだハートを1つ得る。
```
**Parsed:** [Live Start] | [Turn End - live] → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 55)

---

### PL!-PR-001-PR: 高坂穂乃果 
**Text:**
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、メンバー1人をアクティブにしてもよい。
```
**Parsed:** [When Leaves] → Activate/untap 1 Energy/member(s)
⚠️ **Gaps:** Missing 'discard interaction'
📈 **Tier:** C (Score: 9)

---

### PL!-PR-002-PR: 絢瀬絵里 
**Text:**
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、メンバー1人をアクティブにしてもよい。
```
**Parsed:** [When Leaves] → Activate/untap 1 Energy/member(s)
⚠️ **Gaps:** Missing 'discard interaction'
📈 **Tier:** B (Score: 18)

---

### PL!HS-bp1-019-L: Dream Believers 
**Text:**
```
(エールで出た{{icon_score.png|スコア}}1つにつき、成功したライブのスコアの合計に1を加算する。)
```
**Parsed:** 
⚠️ **Gaps:** Missing 'score interaction', Missing 'live interaction'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** D (Score: 0)

---

### PL!HS-bp1-023-L: ド！ド！ド！ 
**Text:**
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高く、かつ自分のステージに『蓮ノ空』のメンバーがいる場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```
**Parsed:** [Live Success] GROUP_FILTER(opponent)(蓮ノ空) OPPONENT_HAS(opponent) → Energy Charge 1 → Move 1 card(s) to deck → Tap 1 opponent's member(s) | [Constant - live] → [Rule modifier - Heart/Blade live rule] → [Rule modifier - Heart/Blade live rule]
⚠️ **Gaps:** Missing 'score interaction'
📈 **Tier:** S (Score: 92)
📚 **FAQ:** 1 entries

---

### PL!N-sd1-025-SD: Colorful Dreams! Colorful Smiles! 
**Text:**
```
(エールで出た{{icon_score.png|スコア}}1つにつき、成功したライブのスコアの合計に1を加算する。)
```
**Parsed:** 
⚠️ **Gaps:** Missing 'score interaction', Missing 'live interaction'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** D (Score: 0)

---

### PL!SP-sd1-001-SD: 澁谷かのん ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のエネルギー6枚につき、カードを1枚引く。
```
**Parsed:** [On Play] → Draw 6 card(s) → Buff power/Blade by 1 (live)
⚠️ **Gaps:** Missing 'energy'
📈 **Tier:** S (Score: 46)

---

### PL!SP-sd1-023-SD: WE WILL!! 
**Text:**
```
(エールで出た{{icon_score.png|スコア}}1つにつき、成功したライブのスコアの合計に1を加算する。)
```
**Parsed:** 
⚠️ **Gaps:** Missing 'score interaction', Missing 'live interaction'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** D (Score: 0)

---

### PL!SP-pb1-006-R: 桜小路きな子 ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動するたび、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
(対戦相手のカードの効果でも発動する。)
```
**Parsed:** [On Play] → Gain 1 Blade(s) (live) → Move member zone
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 36)
📚 **FAQ:** 2 entries

---

### PL!SP-pb1-006-P＋: 桜小路きな子 ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動するたび、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
(対戦相手のカードの効果でも発動する。)
```
**Parsed:** [On Play] → Gain 1 Blade(s) (live) → Move member zone
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 36)
📚 **FAQ:** 2 entries

---

### PL!SP-pb1-008-R: 若菜四季 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}カードを1枚引く。その後、登場したエリアとは別の自分のエリア1つを選ぶ。このメンバーをそのエリアに移動する。選んだエリアにメンバーがいる場合、そのメンバーは、このメンバーがいたエリアに移動させる。
```
**Parsed:** [On Play] → Draw 1 card(s) → Move member zone → Move member zone
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 56)

---

### PL!SP-pb1-008-P＋: 若菜四季 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}カードを1枚引く。その後、登場したエリアとは別の自分のエリア1つを選ぶ。このメンバーをそのエリアに移動する。選んだエリアにメンバーがいる場合、そのメンバーは、このメンバーがいたエリアに移動させる。
```
**Parsed:** [On Play] → Draw 1 card(s) → Move member zone → Move member zone
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 56)

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

### PL!S-bp2-004-R: 黒澤ダイヤ ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードがないとき、それらのカードをすべて控え室に置いてもよい。これにより1枚以上のカードが控え室に置かれた場合、そのエールで得たブレードハートを失い、もう一度エールを行う。
```
**Parsed:** [ON_REVEAL] TURN_1 COUNT_DISCARD(discard) → Reveal via cheer (live) → Discard/Swap 1 card(s) → Discard/Swap 1 card(s)
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** S (Score: 56)
📚 **FAQ:** 1 entries

---

### PL!S-bp2-004-P: 黒澤ダイヤ ✅ (Verified) 
**Text:**
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードがないとき、それらのカードをすべて控え室に置いてもよい。これにより1枚以上のカードが控え室に置かれた場合、そのエールで得たブレードハートを失い、もう一度エールを行う。
```
**Parsed:** [ON_REVEAL] TURN_1 COUNT_DISCARD(discard) → Reveal via cheer (live) → Discard/Swap 1 card(s) → Discard/Swap 1 card(s)
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** S (Score: 56)
📚 **FAQ:** 1 entries

---

### PL!S-bp2-022-L: 未熟DREAMER 
**Text:**
```
{{live_success.png|ライブ成功時}}このターン、自分のデッキがリフレッシュしていた場合、このカードのスコアを＋２する。
```
**Parsed:** [Live Success] → Boost live score by 2
⚠️ **Gaps:** Missing 'deck interaction'
📈 **Tier:** A (Score: 23)
📚 **FAQ:** 1 entries

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
**Parsed:** [Constant - live] → [Rule modifier - Heart/Blade live rule] | [Live Start] NOT COUNT_STAGE → Buff power/Blade by 1 (live)
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'reveal'
📈 **Tier:** S (Score: 52)
📚 **FAQ:** 4 entries

---

### PL!SP-bp2-010-P: ウィーン・マルガレーテ ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。
{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。
```
**Parsed:** [Constant - live] → [Rule modifier - Heart/Blade live rule] | [Live Start] NOT COUNT_STAGE → Buff power/Blade by 1 (live)
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'reveal'
📈 **Tier:** S (Score: 52)
📚 **FAQ:** 4 entries

---

### PL!SP-bp2-010-P＋: ウィーン・マルガレーテ ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。
{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。
```
**Parsed:** [Constant - live] → [Rule modifier - Heart/Blade live rule] | [Live Start] NOT COUNT_STAGE → Buff power/Blade by 1 (live)
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'reveal'
📈 **Tier:** S (Score: 52)
📚 **FAQ:** 4 entries

---

### PL!SP-bp2-010-SEC: ウィーン・マルガレーテ ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。
{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。
```
**Parsed:** [Constant - live] → [Rule modifier - Heart/Blade live rule] | [Live Start] NOT COUNT_STAGE → Buff power/Blade by 1 (live)
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'reveal'
📈 **Tier:** S (Score: 52)
📚 **FAQ:** 4 entries

---

### PL!SP-bp2-011-R: 鬼塚冬毬 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室にある、カード名の異なるライブカードを2枚選ぶ。そうした場合、相手はそれらのカードのうち1枚を選ぶ。これにより相手に選ばれたカードを自分の手札に加える。
```
**Parsed:** [On Play] → [Rule modifier - Heart/Blade live rule] → Add 1 card(s) to hand from discard
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'choice'
📈 **Tier:** S (Score: 53)
📚 **FAQ:** 1 entries

---

### PL!SP-bp2-011-P: 鬼塚冬毬 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室にある、カード名の異なるライブカードを2枚選ぶ。そうした場合、相手はそれらのカードのうち1枚を選ぶ。これにより相手に選ばれたカードを自分の手札に加える。
```
**Parsed:** [On Play] → [Rule modifier - Heart/Blade live rule] → Add 1 card(s) to hand from discard
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'choice'
📈 **Tier:** S (Score: 53)
📚 **FAQ:** 1 entries

---

### PL!SP-bp2-023-L: Go!! リスタート 
**Text:**
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場のカード枚数が相手より少ない場合、このカードのスコアを＋１する。
```
**Parsed:** [Live Start] → Buff power/Blade by 1 (live) → Boost live score by 1
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 36)

---

### PL!SP-bp2-024-L: ビタミンSUMMER！ 
**Text:**
```
{{live_success.png|ライブ成功時}}自分の手札の枚数が相手より多い場合、このカードのスコアを＋１する。
```
**Parsed:** [Live Success] → Buff power/Blade by 1 (live) → Boost live score by 1
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

### PL!HS-bp2-019-L: Bloom the smile, Bloom the dream! 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージに『蓮ノ空』のメンバーがいる場合、このカードを成功させるための必要ハートは、{{heart_01.png|heart01}}{{heart_01.png|heart01}}{{heart_00.png|heart0}}か、{{heart_04.png|heart04}}{{heart_04.png|heart04}}{{heart_00.png|heart0}}か、{{heart_05.png|heart05}}{{heart_05.png|heart05}}{{heart_00.png|heart0}}のうち、選んだ1つにしてもよい。
```
**Parsed:** [Live Start] GROUP_FILTER(蓮ノ空)
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** A (Score: 28)
📚 **FAQ:** 1 entries

---

### PL!S-pb1-002-R: 桜内梨子 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}相手は手札からライブカードを1枚控え室に置いてもよい。そうしなかった場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```
**Parsed:** [On Play] → [Rule modifier - Heart/Blade live rule] → Discard/Swap 1 card(s) | [Constant - live] → Buff power/Blade by 1 (live) → Boost live score by 1
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 67)
📚 **FAQ:** 2 entries

---

### PL!S-pb1-002-P＋: 桜内梨子 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}相手は手札からライブカードを1枚控え室に置いてもよい。そうしなかった場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```
**Parsed:** [On Play] → [Rule modifier - Heart/Blade live rule] → Discard/Swap 1 card(s) | [Constant - live] → Buff power/Blade by 1 (live) → Boost live score by 1
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 67)
📚 **FAQ:** 2 entries

---

### PL!S-pb1-003-R: 松浦果南 ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、このメンバーが元々持つハートはすべて{{heart_04.png|heart04}}になる。{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中から、ライブカードを1枚手札に加える。
```
**Parsed:** [Live Start] (Cost: ENERGY 2) → Buff power/Blade by 1 (live) | [ON_REVEAL] → Recover 1 Live card(s) from discard → Reveal via cheer (live) → Swap zone cards
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** S (Score: 57)
📚 **FAQ:** 1 entries

---

### PL!S-pb1-003-P＋: 松浦果南 ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、このメンバーが元々持つハートはすべて{{heart_04.png|heart04}}になる。{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中から、ライブカードを1枚手札に加える。
```
**Parsed:** [Live Start] (Cost: ENERGY 2) → Buff power/Blade by 1 (live) | [ON_REVEAL] → Recover 1 Live card(s) from discard → Reveal via cheer (live) → Swap zone cards
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** S (Score: 57)
📚 **FAQ:** 1 entries

---

### PL!S-pb1-005-R: 渡辺 曜 ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}相手のエネルギーが自分より多い場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [Constant - live] → Gain 1 Blade(s) (live)
⚠️ **Gaps:** Missing 'energy', Missing 'opponent interaction'
📈 **Tier:** A (Score: 33)

---

### PL!S-pb1-005-P＋: 渡辺 曜 ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}相手のエネルギーが自分より多い場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [Constant - live] → Gain 1 Blade(s) (live)
⚠️ **Gaps:** Missing 'energy', Missing 'opponent interaction'
📈 **Tier:** A (Score: 33)

---

### PL!S-pb1-006-R: 津島善子 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のライブカードを1枚公開する：相手は手札を1枚控え室に置いてもよい。そうしなかった場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [Activated] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) TURN_1 → Reveal 1 card(s) → Discard/Swap 1 card(s) | [Turn End - live] → Gain 1 Blade(s) (live)
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 80)
📚 **FAQ:** 1 entries

---

### PL!S-pb1-006-P＋: 津島善子 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のライブカードを1枚公開する：相手は手札を1枚控え室に置いてもよい。そうしなかった場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```
**Parsed:** [Activated] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) TURN_1 → Reveal 1 card(s) → Discard/Swap 1 card(s) | [Turn End - live] → Gain 1 Blade(s) (live)
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 80)
📚 **FAQ:** 1 entries

---

### PL!S-pb1-008-R: 小原鞠莉 ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーのデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```
**Parsed:** [Live Start] → Look at top 2 card(s) of deck → Choose 1 card(s) from looked deck → Buff power/Blade by 1 (live) → Move 1 card(s) to deck → Discard/Swap 1 card(s) → ORDER_DECK
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 98)
📚 **FAQ:** 1 entries

---

### PL!S-pb1-008-P＋: 小原鞠莉 ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーのデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```
**Parsed:** [Live Start] → Look at top 2 card(s) of deck → Choose 1 card(s) from looked deck → Buff power/Blade by 1 (live) → Move 1 card(s) to deck → Discard/Swap 1 card(s) → ORDER_DECK
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 98)
📚 **FAQ:** 1 entries

---

### PL!S-pb1-013-N: 黒澤ダイヤ ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中からハートに{{heart_04.png|heart04}}を2個以上持つメンバーカードか、必要ハートに{{heart_04.png|heart04}}を2以上含むライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```
**Parsed:** [On Play] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) → Look at top 4 card(s) of deck → Discard/Swap 1 card(s) → Choose 1 card(s) from looked deck → Reveal 1 card(s) → Recover 1 Live card(s) from discard → Discard/Swap 1 card(s)
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** S (Score: 86)

---

### PL!S-pb1-014-N: 渡辺 曜 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中からハートに{{heart_02.png|heart02}}を2個以上持つメンバーカードか、必要ハートに{{heart_02.png|heart02}}を2以上含むライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```
**Parsed:** [On Play] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) → Look at top 4 card(s) of deck → Discard/Swap 1 card(s) → Choose 1 card(s) from looked deck → Reveal 1 card(s) → Recover 1 Live card(s) from discard → Discard/Swap 1 card(s)
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** S (Score: 86)

---

### PL!S-pb1-015-N: 津島善子 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中からハートに{{heart_05.png|heart05}}を2個以上持つメンバーカードか、必要ハートに{{heart_05.png|heart05}}を2以上含むライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```
**Parsed:** [On Play] (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) → Look at top 4 card(s) of deck → Discard/Swap 1 card(s) → Choose 1 card(s) from looked deck → Reveal 1 card(s) → Recover 1 Live card(s) from discard → Discard/Swap 1 card(s)
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** S (Score: 86)

---

### PL!S-pb1-019-L: 元気全開DAY！DAY！DAY！ 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージにいる『Aqours』のメンバーが持つハートに、{{heart_02.png|heart02}}が合計6個以上ある場合、このカードの{{live_success.png|ライブ成功時}}能力を無効にする。{{live_success.png|ライブ成功時}}相手は、エネルギーデッキからエネルギーカードを1枚ウェイト状態で置く。
```
**Parsed:** [Live Start] GROUP_FILTER(Aqours) → NEGATE_EFFECT | [Live Success] → Energy Charge 1 → Move 1 card(s) to deck → Tap 1 opponent's member(s)
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** S (Score: 78)
📚 **FAQ:** 1 entries

---

### PL!S-pb1-020-L: トリコリコPLEASE!! 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージにいる『Aqours』のメンバーが持つハートに、{{heart_04.png|heart04}}が合計10個以上ある場合、このカードのスコアを＋２する。
```
**Parsed:** [Live Start] GROUP_FILTER(Aqours) → Boost live score by 2
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** A (Score: 24)

---

### PL!S-pb1-021-L: Strawberry Trapper 
**Text:**
```
{{live_success.png|ライブ成功時}}自分のステージにいる『Aqours』のメンバーが持つハートに、{{heart_05.png|heart05}}が合計4個以上あり、このターン、相手が余剰のハートを持たずにライブを成功させていた場合、このカードのスコアを＋２する。
```
**Parsed:** [Live Success] GROUP_FILTER(opponent)(Aqours) → Boost live score by 2
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** A (Score: 34)
📚 **FAQ:** 3 entries

---

### PL!S-pb1-022-L: 逃走迷走メビウスループ 
**Text:**
```
{{live_success.png|ライブ成功時}}このターン、ライブに勝利するプレイヤーを決定するとき、自分と相手のライブの合計スコアが同じ場合、ライブ終了時まで、自分と相手は成功ライブカード置き場にカードを置くことができない。
```
**Parsed:** [Live Success] → Buff power/Blade by 1 (live) → Apply restriction (live)
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'score interaction'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** S (Score: 51)
📚 **FAQ:** 1 entries

---

### PL!S-pb1-022-L＋: 逃走迷走メビウスループ 
**Text:**
```
{{live_success.png|ライブ成功時}}このターン、ライブに勝利するプレイヤーを決定するとき、自分と相手のライブの合計スコアが同じ場合、ライブ終了時まで、自分と相手は成功ライブカード置き場にカードを置くことができない。
```
**Parsed:** [Live Success] → Buff power/Blade by 1 (live) → Apply restriction (live)
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'score interaction'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** S (Score: 51)
📚 **FAQ:** 1 entries

---

### PL!-bp3-009-R＋: 矢澤にこ ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のステージにコスト13以上のメンバーがいる場合、カードを1枚引く。
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。
```
**Parsed:** [On Play] COST_CHECK → Draw 1 card(s) | [Activated] (Cost: TAP_SELF 0) TURN_1 | [Turn End - live] → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 80)

---

### PL!-bp3-009-P: 矢澤にこ ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分のステージにコスト13以上のメンバーがいる場合、カードを1枚引く。
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。
```
**Parsed:** [On Play] COST_CHECK → Draw 1 card(s) | [Activated] (Cost: TAP_SELF 0) TURN_1 | [Turn End - live] → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 80)

---

### PL!-bp3-009-P＋: 矢澤にこ ✅ (Verified) 
**Text:**
```
"{{toujyou.png|登場}}自分のステージにコスト13以上のメンバーがいる場合、カードを1枚引く。
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。"
```
**Parsed:** [On Play] COST_CHECK → Draw 1 card(s) | [Activated] (Cost: TAP_SELF 0) TURN_1 | [Turn End - live] → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 80)

---

### PL!-bp3-009-SEC: 矢澤にこ ✅ (Verified) 
**Text:**
```
"{{toujyou.png|登場}}自分のステージにコスト13以上のメンバーがいる場合、カードを1枚引く。
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。"
```
**Parsed:** [On Play] COST_CHECK → Draw 1 card(s) | [Activated] (Cost: TAP_SELF 0) TURN_1 | [Turn End - live] → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 80)

---

### PL!-bp3-011-N: 絢瀬絵里 ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、選んだハートを1つ得る。
```
**Parsed:** [Live Start] | [Turn End - live] → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 55)

---

### PL!-bp3-012-N: 南ことり ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、選んだハートを1つ得る。
```
**Parsed:** [Live Start] | [Turn End - live] → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 55)

---

### PL!-bp3-013-N: 園田海未 ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、選んだハートを1つ得る。
```
**Parsed:** [Live Start] | [Turn End - live] → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 55)

---

### PL!-bp3-022-L: ユメノトビラ 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のデッキの上から、自分と相手のステージにいるメンバー1人につき、1枚公開する。それらの中にあるライブカード1枚につき、このカードのスコアを＋１する。その後、これにより公開したカードを控え室に置く。
```
**Parsed:** [Live Start] → Reveal 1 card(s) → Buff power/Blade by 1 (live) → Buff power/Blade by 1 (live) → Boost live score by 1 → Reveal 1 card(s) → Discard/Swap 1 card(s)
⚠️ **Gaps:** Missing 'deck interaction', Missing 'opponent interaction'
📈 **Tier:** S (Score: 103)

---

### PL!-bp3-023-L: ミはμ'sicのミ 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーが持つ{{icon_blade.png|ブレード}}の合計が10以上の場合、このカードを成功させるための必要ハートは{{heart_00.png|heart0}}{{heart_00.png|heart0}}少なくなる。
```
**Parsed:** [Live Start] → Reduce Heart requirement (live)
⚠️ **Gaps:** Missing 'blades'
📈 **Tier:** B (Score: 18)
📚 **FAQ:** 1 entries

---

### PL!-bp3-024-L: 夏色えがおで1,2,Jump! 
**Text:**
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にカードがある場合、{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分のステージにいる『μ's』のメンバー1人は、選んだハートを1つ得る。
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にカードが2枚以上ある場合、このカードのスコアを＋１する。
```
**Parsed:** [Live Start] → [Rule modifier - Heart/Blade live rule] | [Turn End - live] → Gain 1 Heart(s) (live) | [Live Start] COUNT_SUCCESS_LIVE COUNT_STAGE → [Rule modifier - Heart/Blade live rule] → Boost live score by 1
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 86)

---

### PL!-bp3-025-L: タカラモノズ 
**Text:**
```
{{live_success.png|ライブ成功時}}このターン、自分が余剰ハートを持たない場合、このカードのスコアを＋１する。
```
**Parsed:** [Live Success] → Boost live score by 1
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** B (Score: 18)
📚 **FAQ:** 2 entries

---

### PL!-bp3-026-L: Oh,Love&Peace! 
**Text:**
```
{{live_start.png|ライブ開始時}}手札を2枚控え室に置いてもよい：ライブ終了時まで、自分のステージにいるメンバー1人は、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
{{live_success.png|ライブ成功時}}自分のステージにいるメンバーが持つハートの総数が、相手のステージにいるメンバーが持つハートの総数より多い場合、このカードのスコアを＋１する。
```
**Parsed:** [Live Start] (Cost: DISCARD_HAND 2) → Gain 1 Blade(s) (live) → Discard/Swap 2 card(s) | [Live Success] → Boost live score by 1
⚠️ **Gaps:** Missing 'hearts', Missing 'opponent interaction'
❌ **Issues:** MISSING_HEARTS
📈 **Tier:** S (Score: 64)
📚 **FAQ:** 4 entries

---

### PL!S-bp3-002-R: 桜内梨子 ✅ (Verified) 
**Text:**
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、このカードを手札に加えてもよい。この能力は、このカードが自分のエールによって公開されている場合のみ発動する。
```
**Parsed:** [Live Success] LIFE_LEAD(score/opponent) → Add 1 card(s) to hand from discard → Trigger ability from other zone
⚠️ **Gaps:** Missing 'reveal'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** S (Score: 42)

---

### PL!S-bp3-002-P: 桜内梨子 ✅ (Verified) 
**Text:**
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、このカードを手札に加えてもよい。この能力は、このカードが自分のエールによって公開されている場合のみ発動する。
```
**Parsed:** [Live Success] LIFE_LEAD(score/opponent) → Add 1 card(s) to hand from discard → Trigger ability from other zone
⚠️ **Gaps:** Missing 'reveal'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** S (Score: 42)

---

### PL!S-bp3-005-R: 渡辺 曜 ✅ (Verified) 
**Text:**
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの枚数が、相手がエールによって公開したカードの枚数より少ない場合、カードを1枚引く。
```
**Parsed:** [ON_REVEAL] → Draw 1 card(s) → Reveal via cheer (live) → Buff power/Blade by 1 (live)
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 44)
📚 **FAQ:** 1 entries

---

### PL!S-bp3-005-P: 渡辺 曜 ✅ (Verified) 
**Text:**
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの枚数が、相手がエールによって公開したカードの枚数より少ない場合、カードを1枚引く。
```
**Parsed:** [ON_REVEAL] → Draw 1 card(s) → Reveal via cheer (live) → Buff power/Blade by 1 (live)
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 44)
📚 **FAQ:** 1 entries

---

### PL!S-bp3-007-R: 国木田花丸 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分か相手を選ぶ。自分は、そのプレイヤーの控え室にあるライブカードを1枚、そのプレイヤーのデッキの一番下に置く。そうした場合、自分はカードを1枚引く。
```
**Parsed:** [Activated] (Cost: ENERGY 1) TURN_1 → Move 1 card(s) to deck → Discard/Swap 1 card(s) → Move 1 card(s) to deck → Draw 1 card(s)
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'live interaction', Missing 'choice'
📈 **Tier:** S (Score: 90)

---

### PL!S-bp3-007-P: 国木田花丸 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分か相手を選ぶ。自分は、そのプレイヤーの控え室にあるライブカードを1枚、そのプレイヤーのデッキの一番下に置く。そうした場合、自分はカードを1枚引く。
```
**Parsed:** [Activated] (Cost: ENERGY 1) TURN_1 → Move 1 card(s) to deck → Discard/Swap 1 card(s) → Move 1 card(s) to deck → Draw 1 card(s)
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'live interaction', Missing 'choice'
📈 **Tier:** S (Score: 90)

---

### PL!S-bp3-008-R: 小原鞠莉 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。それがスコア6以上の『Aqours』のライブカードの場合、エネルギーを4枚アクティブにする。
```
**Parsed:** [Activated] (Cost: SACRIFICE_SELF 0) GROUP_FILTER(Aqours) → Recover 1 Live card(s) from discard → Activate/untap 4 Energy/member(s)
⚠️ **Gaps:** Missing 'score interaction'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** S (Score: 47)
📚 **FAQ:** 1 entries

---

### PL!S-bp3-008-P: 小原鞠莉 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。それがスコア6以上の『Aqours』のライブカードの場合、エネルギーを4枚アクティブにする。
```
**Parsed:** [Activated] (Cost: SACRIFICE_SELF 0) GROUP_FILTER(Aqours) → Recover 1 Live card(s) from discard → Activate/untap 4 Energy/member(s)
⚠️ **Gaps:** Missing 'score interaction'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** S (Score: 47)
📚 **FAQ:** 1 entries

---

### PL!S-bp3-019-L: MIRACLE WAVE 
**Text:**
```
{{live_success.png|ライブ成功時}}このターン、エールにより公開された自分のカードの中にブレードハートを持たないカードが0枚の場合か、または自分が余剰ハートを2つ以上持っている場合、このカードのスコアは４になる。
```
**Parsed:** [ON_REVEAL] → Reveal via cheer (live) → Set live score to 4
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
❌ **Issues:** MISSING_SCORE
📈 **Tier:** A (Score: 26)
📚 **FAQ:** 2 entries

---

### PL!S-bp3-020-L: ダイスキだったらダイジョウブ！ 
**Text:**
```
{{jidou.png|自動}}［ターン1回］エールにより自分のカードを1枚以上公開したとき、それらのカードの中にブレードハートを持つカードが2枚以下の場合、それらのカードをすべて控え室に置いてもよい。そのエールで得たブレードハートを失い、もう一度エールを行う。
```
**Parsed:** [When Leaves] TURN_1 COUNT_DISCARD(discard) → Reveal 1 card(s) → Discard/Swap 1 card(s)
⚠️ **Gaps:** Missing 'hearts', Missing 'blades'
📈 **Tier:** S (Score: 48)
📚 **FAQ:** 1 entries

---

### PL!S-bp3-024-L: Deep Resonance 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージのセンターエリアにコスト9以上の『Aqours』のメンバーがいる場合、以下から1つを選ぶ。
・ライブ終了時まで、自分のステージにいるメンバー1人は、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
・相手のステージにいるコスト4以下のメンバー1人をウェイトにする。
```
**Parsed:** [Live Start] GROUP_FILTER(Aqours) IS_CENTER IS_CENTER COST_CHECK → Choose one effect [Option 1: Gain 1 Blade(s) (live)] [Option 2: Tap 1 opponent's member(s)]
❌ **Issues:** MISSING_BLADES
📈 **Tier:** S (Score: 79)

---

### PL!S-bp3-025-L: SUKI for you, DREAM for you! 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージにいる『Aqours』のメンバー1人を選ぶ。そのメンバーが持つ{{icon_blade.png|ブレード}}が6つ以上の場合、このカードのスコアを＋１する。
```
**Parsed:** [Live Start] → Boost live score by 1
⚠️ **Gaps:** Missing 'blades', Missing 'choice'
📈 **Tier:** A (Score: 30)

---

### PL!N-bp3-003-R: 桜坂しずく 
**Text:**
```
{{toujyou.png|登場}}自分の控え室にあるコスト4以下の『虹ヶ咲』のメンバーカードを1枚選ぶ。そのカードの{{toujyou.png|登場}}能力1つを発動させる。
（{{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。）
```
**Parsed:** [On Play] COST_CHECK → Trigger ability from other zone → Trigger ability from other zone
⚠️ **Gaps:** Missing 'discard interaction', Missing 'choice'
📈 **Tier:** S (Score: 49)
📚 **FAQ:** 1 entries

---

### PL!N-bp3-003-P: 桜坂しずく 
**Text:**
```
{{toujyou.png|登場}}自分の控え室にあるコスト4以下の『虹ヶ咲』のメンバーカードを1枚選ぶ。そのカードの{{toujyou.png|登場}}能力1つを発動させる。
（{{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。）
```
**Parsed:** [On Play] COST_CHECK → Trigger ability from other zone → Trigger ability from other zone
⚠️ **Gaps:** Missing 'discard interaction', Missing 'choice'
📈 **Tier:** S (Score: 49)
📚 **FAQ:** 1 entries

---

### PL!N-bp3-010-R: 三船栞子 ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーの控え室にあるメンバーカードを2枚まで、好きな順番でデッキの一番下に置く。
```
**Parsed:** [Live Start] → Move 1 card(s) to deck → Discard/Swap 2 card(s) → ORDER_DECK
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'choice'
📈 **Tier:** S (Score: 66)

---

### PL!N-bp3-010-P: 三船栞子 ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーの控え室にあるメンバーカードを2枚まで、好きな順番でデッキの一番下に置く。
```
**Parsed:** [Live Start] → Move 1 card(s) to deck → Discard/Swap 2 card(s) → ORDER_DECK
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'choice'
📈 **Tier:** S (Score: 66)

---

### PL!N-bp3-011-R: ミア・テイラー ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}相手のステージにいる「ミア・テイラー」以外のメンバーを1人選ぶ。そのメンバーが持つハートと、このメンバーが持つハートの中に同じ色のハートがある場合、ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。それぞれのメンバーのコストが同じ場合、元々の{{icon_blade.png|ブレード}}の数が同じ場合についても同じことを行う。
```
**Parsed:** [On Play] → Gain 1 Blade(s) (live) → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'choice'
📈 **Tier:** S (Score: 48)
📚 **FAQ:** 1 entries

---

### PL!N-bp3-011-P: ミア・テイラー ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}相手のステージにいる「ミア・テイラー」以外のメンバーを1人選ぶ。そのメンバーが持つハートと、このメンバーが持つハートの中に同じ色のハートがある場合、ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。それぞれのメンバーのコストが同じ場合、元々の{{icon_blade.png|ブレード}}の数が同じ場合についても同じことを行う。
```
**Parsed:** [On Play] → Gain 1 Blade(s) (live) → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'opponent interaction', Missing 'choice'
📈 **Tier:** S (Score: 48)
📚 **FAQ:** 1 entries

---

### PL!N-bp3-014-N: 中須かすみ 
**Text:**
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_04.png|heart04}}のうち1つを選ぶ。ライブ終了時まで、このメンバーが元々持つハートは選んだハートになる。
```
**Parsed:** [Live Start] | [Turn End - live] → Buff power/Blade by 1 (live)
⚠️ **Gaps:** Missing 'hearts', Missing 'choice'
📈 **Tier:** S (Score: 40)

---

### PL!N-bp3-015-N: 桜坂しずく 
**Text:**
```
{{live_start.png|ライブ開始時}}{{heart_02.png|heart02}}か{{heart_05.png|heart05}}か{{heart_06.png|heart06}}のうち1つを選ぶ。ライブ終了時まで、このメンバーが元々持つハートは選んだハートになる。
```
**Parsed:** [Live Start] | [Turn End - live] → Buff power/Blade by 1 (live)
⚠️ **Gaps:** Missing 'hearts', Missing 'choice'
📈 **Tier:** S (Score: 40)

---

### PL!N-bp3-025-L: Awakening Promise 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバー1人の下にあるエネルギーカードを、好きな枚数エネルギーデッキに置いてもよい。そうした場合、ライブ終了時まで、そのメンバーは、これによって置いたエネルギーカード1枚につき、［赤ハート］［赤ハート］［赤ハート］を得る。
```
**Parsed:** [Live Start] → Buff power/Blade by 1 (live) | [Turn End - live] → Gain 1 Heart(s) (live)
⚠️ **Gaps:** Missing 'energy', Missing 'deck interaction'
📈 **Tier:** S (Score: 61)

---

### PL!N-bp3-027-L: La Bella Patria 
**Text:**
```
{{live_success.png|ライブ成功時}}このターン、自分が余剰ハートに{{heart_04.png|heart04}}を1つ以上持っており、かつ自分のステージに『虹ヶ咲』のメンバーがいる場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```
**Parsed:** [Live Success] GROUP_FILTER(虹ヶ咲) → Energy Charge 1 → Move 1 card(s) to deck
⚠️ **Gaps:** Missing 'hearts'
📈 **Tier:** S (Score: 42)
📚 **FAQ:** 4 entries

---

### PL!N-bp3-030-L: Love U my friends 
**Text:**
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中に{{icon_b_all.png|ALLブレード}}を持つカードが1枚以上ある場合、このカードのスコアを＋１する。
```
**Parsed:** [ON_REVEAL] COUNT_STAGE → Reveal via cheer (live) → Boost live score by 1
⚠️ **Gaps:** Missing 'blades'
📈 **Tier:** A (Score: 32)
📚 **FAQ:** 2 entries

---

### PL!-pb1-001-R: 高坂穂乃果 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：ライブカードかコスト10以上のメンバーカードのどちらか1つを選ぶ。選んだカードが公開されるまで、自分のデッキの一番上からカードを１枚ずつ公開する。そのカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。
```
**Parsed:** [Activated] (Cost: TAP_SELF 0) (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) (Cost: SACRIFICE_SELF 0) TURN_1 COST_CHECK → [Rule modifier - Heart/Blade live rule] → Reveal 1 card(s) → Move 1 card(s) to deck → Reveal 1 card(s) → Add 1 card(s) to hand from discard → Discard/Swap 1 card(s)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 117)
📚 **FAQ:** 2 entries

---

### PL!-pb1-001-P＋: 高坂穂乃果 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：ライブカードかコスト10以上のメンバーカードのどちらか1つを選ぶ。選んだカードが公開されるまで、自分のデッキの一番上からカードを１枚ずつ公開する。そのカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。
```
**Parsed:** [Activated] (Cost: TAP_SELF 0) (Cost: DISCARD_HAND 1) (Cost: DISCARD_HAND 1) (Cost: SACRIFICE_SELF 0) TURN_1 COST_CHECK → [Rule modifier - Heart/Blade live rule] → Reveal 1 card(s) → Move 1 card(s) to deck → Reveal 1 card(s) → Add 1 card(s) to hand from discard → Discard/Swap 1 card(s)
⚠️ **Gaps:** Missing 'choice'
📈 **Tier:** S (Score: 117)
📚 **FAQ:** 2 entries

---

### PL!-pb1-002-R: 絢瀬絵里 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：自分のステージにいるメンバーが『BiBi』のみの場合、相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が3つ以下のメンバー1人をウェイトにする。
{{jyouji.png|常時}}相手のステージにいるウェイト状態のメンバー1人につき、{{heart_06.png|heart06}}を得る。
```
**Parsed:** [On Play] (Cost: TAP_SELF 0) GROUP_FILTER(opponent)(BiBi) → Tap 1 opponent's member(s) | [Live Start] (Cost: TAP_SELF 0) GROUP_FILTER(opponent)(BiBi) → Tap 1 opponent's member(s) | [Constant - live] → Gain 1 Heart(s) (live) → Tap 1 opponent's member(s)
⚠️ **Gaps:** Missing 'blades'
❌ **Issues:** MISSING_BLADES
📈 **Tier:** S (Score: 109)

---

### PL!-pb1-002-P＋: 絢瀬絵里 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：自分のステージにいるメンバーが『BiBi』のみの場合、相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が3つ以下のメンバー1人をウェイトにする。
{{jyouji.png|常時}}相手のステージにいるウェイト状態のメンバー1人につき、{{heart_06.png|heart06}}を得る。
```
**Parsed:** [On Play] (Cost: TAP_SELF 0) GROUP_FILTER(opponent)(BiBi) → Tap 1 opponent's member(s) | [Live Start] (Cost: TAP_SELF 0) GROUP_FILTER(opponent)(BiBi) → Tap 1 opponent's member(s) | [Constant - live] → Gain 1 Heart(s) (live) → Tap 1 opponent's member(s)
⚠️ **Gaps:** Missing 'blades'
❌ **Issues:** MISSING_BLADES
📈 **Tier:** S (Score: 109)

---

### PL!-pb1-005-R: 星空 凛 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にカードがある場合、カードを1枚引く。
```
**Parsed:** [On Play] → Draw 1 card(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** B (Score: 18)

---

### PL!-pb1-005-P＋: 星空 凛 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にカードがある場合、カードを1枚引く。
```
**Parsed:** [On Play] → Draw 1 card(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** B (Score: 18)

---

### PL!-pb1-006-R: 西木野真姫 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室から『μ's』のライブカードを1枚までデッキの一番上に置く。その後、相手のステージにウェイト状態のメンバーがいる場合、カードを1枚引く。
```
**Parsed:** [On Play] OPPONENT_HAS(opponent) → Move 1 card(s) to deck → Discard/Swap 1 card(s) → Move 1 card(s) to deck → Draw 1 card(s) → Tap 1 opponent's member(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 86)

---

### PL!-pb1-006-P＋: 西木野真姫 ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}自分の控え室から『μ's』のライブカードを1枚までデッキの一番上に置く。その後、相手のステージにウェイト状態のメンバーがいる場合、カードを1枚引く。
```
**Parsed:** [On Play] OPPONENT_HAS(opponent) → Move 1 card(s) to deck → Discard/Swap 1 card(s) → Move 1 card(s) to deck → Draw 1 card(s) → Tap 1 opponent's member(s)
⚠️ **Gaps:** Missing 'live interaction'
📈 **Tier:** S (Score: 86)

---

### PL!-pb1-009-R: 矢澤にこ ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が1つ以下のメンバー1人をウェイトにする。
{{toujyou.png|登場}}このターン、自分と相手のステージにいるメンバーは、効果によってはアクティブにならない。
```
**Parsed:** [On Play] → Tap 1 opponent's member(s) | [On Play] → Activate/untap 1 Energy/member(s)
⚠️ **Gaps:** Missing 'blades'
📈 **Tier:** S (Score: 61)
📚 **FAQ:** 1 entries

---

### PL!-pb1-009-P＋: 矢澤にこ ✅ (Verified) 
**Text:**
```
{{toujyou.png|登場}}相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が1つ以下のメンバー1人をウェイトにする。
{{toujyou.png|登場}}このターン、自分と相手のステージにいるメンバーは、効果によってはアクティブにならない。
```
**Parsed:** [On Play] → Tap 1 opponent's member(s) | [On Play] → Activate/untap 1 Energy/member(s)
⚠️ **Gaps:** Missing 'blades'
📈 **Tier:** S (Score: 61)
📚 **FAQ:** 1 entries

---

### PL!-pb1-013-R: 園田海未 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の手札を、相手は見ないで1枚選び公開する。これにより公開されたカードがライブカードの場合、ライブ終了時まで、このメンバーは「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```
**Parsed:** [Activated] (Cost: ENERGY 2) TURN_1 → Reveal 1 card(s) | [Constant - live] → Reveal 1 card(s) → Boost live score by 1
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 70)
📚 **FAQ:** 1 entries

---

### PL!-pb1-013-P＋: 園田海未 ✅ (Verified) 
**Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の手札を、相手は見ないで1枚選び公開する。これにより公開されたカードがライブカードの場合、ライブ終了時まで、このメンバーは「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```
**Parsed:** [Activated] (Cost: ENERGY 2) TURN_1 → Reveal 1 card(s) | [Constant - live] → Reveal 1 card(s) → Boost live score by 1
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** S (Score: 70)
📚 **FAQ:** 1 entries

---

### PL!-bp4-001-R: 高坂穂乃果 ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーのコストの合計が相手より低い場合、カードを1枚引く。
```
**Parsed:** [Live Start] → Draw 1 card(s)
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** A (Score: 28)

---

### PL!-bp4-001-P: 高坂穂乃果 ✅ (Verified) 
**Text:**
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーのコストの合計が相手より低い場合、カードを1枚引く。
```
**Parsed:** [Live Start] → Draw 1 card(s)
⚠️ **Gaps:** Missing 'opponent interaction'
📈 **Tier:** A (Score: 28)

---

### PL!-bp4-002-R＋: 絢瀬絵里 ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}自分のライブ中のライブカードに、{{live_start.png|ライブ開始時}}能力も{{live_success.png|ライブ成功時}}能力も持たないカードがあるかぎり、{{heart_06.png|heart06}}{{heart_06.png|heart06}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から『μ's』のライブカードを1枚手札に加える。この能力は、自分の成功ライブカード置き場にあるカードのスコアの合計が６以上の場合のみ起動できる。
```
**Parsed:** [Live Start] → Gain 2 Heart(s) (live) | [Activated] (Cost: DISCARD_HAND 2) TURN_1 → Recover 1 Live card(s) from discard → Discard/Swap 2 card(s) | [Activated] → [Rule modifier - Heart/Blade live rule]
⚠️ **Gaps:** Missing 'score interaction'
📈 **Tier:** S (Score: 83)

---

### PL!-bp4-002-P: 絢瀬絵里 ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}自分のライブ中のライブカードに、{{live_start.png|ライブ開始時}}能力も{{live_success.png|ライブ成功時}}能力も持たないカードがあるかぎり、{{heart_06.png|heart06}}{{heart_06.png|heart06}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から『μ's』のライブカードを1枚手札に加える。この能力は、自分の成功ライブカード置き場にあるカードのスコアの合計が６以上の場合のみ起動できる。
```
**Parsed:** [Live Start] → Gain 2 Heart(s) (live) | [Activated] (Cost: DISCARD_HAND 2) TURN_1 → Recover 1 Live card(s) from discard → Discard/Swap 2 card(s) | [Activated] → [Rule modifier - Heart/Blade live rule]
⚠️ **Gaps:** Missing 'score interaction'
📈 **Tier:** S (Score: 83)

---

### PL!-bp4-002-P＋: 絢瀬絵里 ✅ (Verified) 
**Text:**
```
{{jyouji.png|常時}}自分のライブ中のライブカードに、{{live_start.png|ライブ開始時}}能力も{{live_success.png|ライブ成功時}}能力も持たないカードがあるかぎり、{{heart_06.png|heart06}}{{heart_06.png|heart06}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から『μ's』のライブカードを1枚手札に加える。この能力は、自分の成功ライブカード置き場にあるカードのスコアの合計が６以上の場合のみ起動できる。
```
**Parsed:** [Live Start] → Gain 2 Heart(s) (live) | [Activated] (Cost: DISCARD_HAND 2) TURN_1 → Recover 1 Live card(s) from discard → Discard/Swap 2 card(s) | [Activated] → [Rule modifier - Heart/Blade live rule]
⚠️ **Gaps:** Missing 'score interaction'
📈 **Tier:** S (Score: 83)

---

