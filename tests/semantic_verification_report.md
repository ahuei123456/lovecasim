# Semantic Verification Report

Cards grouped by effect type. Review each group to verify parsed effects match card text.

## Effect Type Summary
| Effect Type | Count | Sample Card |
|-------------|-------|-------------|
| SWAP_CARDS | 380 | 高坂 穂乃果 |
| DRAW | 162 | 東條 希 |
| ADD_BLADES | 133 | 高坂 穂乃果 |
| BUFF_POWER | 132 | 矢澤 にこ |
| LOOK_AND_CHOOSE | 106 | 園田 海未 |
| ADD_TO_HAND | 104 | 園田 海未 |
| LOOK_DECK | 103 | 園田 海未 |
| BOOST_SCORE | 101 | 矢澤 にこ |
| REVEAL_CARDS | 96 | 園田 海未 |
| ADD_HEARTS | 88 | 南 ことり |
| RECOVER_LIVE | 84 | 高坂 穂乃果 |
| RECOVER_MEMBER | 77 | 絢瀬 絵里 |
| TAP_OPPONENT | 63 | 東條 希 |
| ENERGY_CHARGE | 58 | 唐 可可 |
| CHEER_REVEAL | 56 | 東條 希 |
| ACTIVATE_MEMBER | 52 | 高坂穂乃果 |
| MOVE_MEMBER | 47 | 嵐 千砂都 |
| ORDER_DECK | 36 | START:DASH!! |
| META_RULE | 31 | Reflection in the mirror |
| MOVE_TO_DECK | 29 | ミア・テイラー |
| TRIGGER_REMOTE | 22 | 桜小路きな子 |
| PLACE_UNDER | 20 | 上原歩夢 |
| SET_BLADES | 14 | 桜坂しずく |
| SWAP_ZONE | 12 | 西木野 真姫 |
| BATON_TOUCH_MOD | 11 | 眩耀夜行 |
| REDUCE_HEART_REQ | 10 | 僕らは今のなかで |
| REPLACE_EFFECT | 9 | 小原鞠莉 |
| NEGATE_EFFECT | 9 | 澁谷かのん |
| SELECT_MODE | 7 | 星空 凛 |
| REDUCE_COST | 7 | レディバグ |
| RESTRICTION | 6 | 澁谷かのん |
| TRANSFORM_COLOR | 2 | VIVID WORLD |
| FLAVOR_ACTION | 1 | 愛♡スクリ～ム！ |
| IMMUNITY | 1 | 渡辺 曜&鬼塚夏美&大沢瑠璃乃 |
| SET_SCORE | 1 | MIRACLE WAVE |

---

## SWAP_CARDS (380 cards)

### PL!-sd1-001-SD: 高坂 穂乃果
**Trigger:** ON_PLAY
**Conditions:** COUNT_SUCCESS_LIVE {'min': 2}, COUNT_STAGE {'count': 2, 'zone': 'SUCCESS_LIVE'}
**Effect Value:** 1
**Params:** `{'target': 'discard', 'from': 'hand'}`

**Original Text:**
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にカードが2枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。
{{jyouji.png|常時}}自分の成功ライブカード置き場にあるカード1枚につき、{{icon_blade.png|ブレード}}を得る。
```

### PL!-sd1-003-SD: 南 ことり
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Params:** `{'target': 'discard', 'from': 'hand'}`

**Original Text:**
```
{{toujyou.png|登場}}自分の控え室からコスト4以下の『μ's』のメンバーカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ...
```

### PL!-sd1-004-SD: 園田 海未
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'target': 'discard'}`

**Original Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを5枚見る。その中から『μ's』のライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### PL!-sd1-007-SD: 東條 希
**Trigger:** ON_PLAY
**Conditions:** HAS_LIVE_CARD {}
**Effect Value:** 5
**Params:** `{'target': 'discard', 'from': 'deck'}`

**Original Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを5枚控え室に置く。それらの中にライブカードがある場合、カードを1枚引く。
```

### PL!-sd1-008-SD: 小泉 花陽
**Trigger:** ACTIVATED
**Conditions:** TURN_1 {}
**Effect Value:** 10
**Params:** `{'target': 'discard', 'from': 'deck'}`

**Original Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分のデッキの上からカードを10枚控え室に置く。
```

*...and 375 more cards with this effect*

---

## DRAW (162 cards)

### PL!-sd1-007-SD: 東條 希
**Trigger:** ON_PLAY
**Conditions:** HAS_LIVE_CARD {}
**Effect Value:** 1
**Target:** PLAYER

**Original Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを5枚控え室に置く。それらの中にライブカードがある場合、カードを1枚引く。
```

### PL!N-bp1-019-PR: 優木せつ菜
**Trigger:** ON_PLAY
**Effect Value:** 1
**Target:** PLAYER

**Original Text:**
```
{{toujyou.png|登場}}カードを1枚引き、手札を1枚控え室に置く。
```

### PL!N-PR-005-PR: 桜坂しずく
**Trigger:** ON_PLAY
**Effect Value:** 2
**Target:** PLAYER

**Original Text:**
```
{{toujyou.png|登場}}カードを2枚引き、手札を2枚控え室に置く。
```

### PL!N-PR-007-PR: 宮下 愛
**Trigger:** ON_PLAY
**Effect Value:** 2
**Target:** PLAYER

**Original Text:**
```
{{toujyou.png|登場}}カードを2枚引き、手札を2枚控え室に置く。
```

### PL!N-PR-011-PR: 天王寺璃奈
**Trigger:** ON_PLAY
**Effect Value:** 2
**Target:** PLAYER

**Original Text:**
```
{{toujyou.png|登場}}カードを2枚引き、手札を2枚控え室に置く。
```

*...and 157 more cards with this effect*

---

## ADD_BLADES (133 cards)

### PL!-sd1-001-SD: 高坂 穂乃果
**Trigger:** CONSTANT
**Effect Value:** 1
**Target:** MEMBER_SELF
**Params:** `{'multiplier': True, 'per_live': True}`

**Original Text:**
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にカードが2枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。
{{jyouji.png|常時}}自分の成功ライブカード置き場にあるカード1枚につき、{{icon_blade.png|ブレード}}を得る。
```

### PL!S-PR-013-PR: 高海千歌
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Target:** MEMBER_SELF
**Params:** `{'until': 'live_end'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png...
```

### PL!S-PR-016-PR: 黒澤ダイヤ
**Trigger:** ON_PLAY
**Effect Value:** 1
**Target:** MEMBER_SELF
**Params:** `{'until': 'live_end'}`

**Original Text:**
```
{{toujyou.png|登場}}ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

### PL!S-PR-019-PR: 国木田花丸
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Target:** MEMBER_SELF
**Params:** `{'until': 'live_end'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png...
```

### PL!S-PR-020-PR: 小原鞠莉
**Trigger:** ON_PLAY
**Effect Value:** 1
**Target:** MEMBER_SELF
**Params:** `{'until': 'live_end'}`

**Original Text:**
```
{{toujyou.png|登場}}ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

*...and 128 more cards with this effect*

---

## BUFF_POWER (132 cards)

### PL!-sd1-009-SD: 矢澤 にこ
**Trigger:** CONSTANT
**Conditions:** COUNT_GROUP {'group': "μ's", 'min': 25, 'zone': 'DISCARD'}
**Effect Value:** 1
**Params:** `{'until': 'live_end', 'temporary': True}`

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分の控え室に『μ's』のカードが25枚以上ある場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### PL!-sd1-019-SD: START:DASH!!
**Trigger:** ON_LIVE_SUCCESS
**Effect Value:** 1
**Params:** `{'multiplier': True}`

**Original Text:**
```
{{live_success.png|ライブ成功時}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### PL!-sd1-022-SD: 僕らは今のなかで
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Params:** `{'multiplier': True, 'per_live': True}`

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にあるカード1枚につき、このカードを成功させるための必要ハートは{{heart_00.png|heart0}}{{heart_00.png|heart0}}少なくなる。
```

### PL!-PR-007-PR: 東條 希
**Trigger:** ON_PLAY
**Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1
**Params:** `{'multiplier': True, 'per_member': True}`

**Original Text:**
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### PL!-PR-009-PR: 矢澤にこ
**Trigger:** ON_PLAY
**Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1
**Params:** `{'multiplier': True, 'per_member': True}`

**Original Text:**
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

*...and 127 more cards with this effect*

---

## LOOK_AND_CHOOSE (106 cards)

### PL!-sd1-004-SD: 園田 海未
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'source': 'looked', 'group': "μ's"}`

**Original Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを5枚見る。その中から『μ's』のライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### PL!-sd1-011-SD: 絢瀬 絵里
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'source': 'looked'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### PL!-sd1-012-SD: 南 ことり
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'source': 'looked'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### PL!-sd1-015-SD: 西木野 真姫
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'source': 'looked'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中からメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### PL!-sd1-016-SD: 東條 希
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'source': 'looked'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

*...and 101 more cards with this effect*

---

## ADD_TO_HAND (104 cards)

### PL!-sd1-004-SD: 園田 海未
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'to': 'hand', 'group': "μ's"}`

**Original Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを5枚見る。その中から『μ's』のライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### PL!-sd1-006-SD: 西木野 真姫
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'to': 'hand', 'from': 'success_live'}`

**Original Text:**
```
{{toujyou.png|登場}}手札のライブカードを1枚公開してもよい：自分の成功ライブカード置き場にあるカードを1枚手札に加える。そうした場合、これにより公開したカードを自分の成功ライブカード置き場に置く。
```

### PL!-sd1-011-SD: 絢瀬 絵里
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'to': 'hand', 'from': 'discard'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### PL!-sd1-012-SD: 南 ことり
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'to': 'hand', 'from': 'discard'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### PL!-sd1-015-SD: 西木野 真姫
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'to': 'hand'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中からメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

*...and 99 more cards with this effect*

---

## LOOK_DECK (103 cards)

### PL!-sd1-004-SD: 園田 海未
**Trigger:** ON_PLAY
**Effect Value:** 5

**Original Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを5枚見る。その中から『μ's』のライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### PL!-sd1-011-SD: 絢瀬 絵里
**Trigger:** ON_PLAY
**Effect Value:** 3

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### PL!-sd1-012-SD: 南 ことり
**Trigger:** ON_PLAY
**Effect Value:** 3

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### PL!-sd1-015-SD: 西木野 真姫
**Trigger:** ON_PLAY
**Effect Value:** 5

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中からメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### PL!-sd1-016-SD: 東條 希
**Trigger:** ON_PLAY
**Effect Value:** 3

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

*...and 98 more cards with this effect*

---

## BOOST_SCORE (101 cards)

### PL!-sd1-009-SD: 矢澤 にこ
**Trigger:** CONSTANT
**Conditions:** COUNT_GROUP {'group': "μ's", 'min': 25, 'zone': 'DISCARD'}
**Effect Value:** 1

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分の控え室に『μ's』のカードが25枚以上ある場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### LL-bp1-001-R＋: 上原歩夢&澁谷かのん&日野下花帆
**Trigger:** CONSTANT
**Effect Value:** 3

**Original Text:**
```
{{toujyou.png|登場}}自分の控え室からメンバーカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札の「上原歩夢」と「澁谷かのん」と「日野下花帆」を、好きな組み合わせで合計3枚、控え室に置いてもよい：ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋３する。」を得る。
（手札のこのカードもこの効果で控え室に置ける。）
```

### PL!N-bp1-027-L: Solitude Rain
**Trigger:** ON_LIVE_START
**Effect Value:** 1

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のステージにいる『虹ヶ咲』のメンバーが持つ{{heart_01.png|heart01}}、{{heart_04.png|heart04}}、{{heart_05.png|heart05}}、{{heart_02.png|heart02}}、{{heart_03.png|heart03}}、{{heart_06.png|heart06}}のうち...
```

### PL!N-bp1-028-L: Butterfly
**Trigger:** ON_LIVE_START
**Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'STAGE'}
**Effect Value:** 1

**Original Text:**
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分のステージに『虹ヶ咲』のメンバーがいる場合、このカードのスコアを＋１する。

(エールをすべて行った後、エールで出た{{icon_draw.png|ドロー}}1つにつき、カードを1枚引く。)
```

### PL!N-bp1-029-L: Eutopia
**Trigger:** ON_LIVE_START
**Conditions:** COUNT_STAGE {'min': 3}
**Effect Value:** 2

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のライブ中のカードが3枚以上ある場合、このカードのスコアを＋２する。

(エールをすべて行った後、エールで出た{{icon_draw.png|ドロー}}1つにつき、カードを1枚引く。)
```

*...and 96 more cards with this effect*

---

## REVEAL_CARDS (96 cards)

### PL!-sd1-004-SD: 園田 海未
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを5枚見る。その中から『μ's』のライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### PL!-sd1-006-SD: 西木野 真姫
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}手札のライブカードを1枚公開してもよい：自分の成功ライブカード置き場にあるカードを1枚手札に加える。そうした場合、これにより公開したカードを自分の成功ライブカード置き場に置く。
```

### PL!-sd1-006-SD: 西木野 真姫
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}手札のライブカードを1枚公開してもよい：自分の成功ライブカード置き場にあるカードを1枚手札に加える。そうした場合、これにより公開したカードを自分の成功ライブカード置き場に置く。
```

### PL!-sd1-015-SD: 西木野 真姫
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中からメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### PL!N-PR-003-PR: 上原歩夢
**Trigger:** ACTIVATED
**Conditions:** TURN_1 {}, HAND_HAS_NO_LIVE {}
**Effect Value:** 1

**Original Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札をすべて公開する：自分のステージにほかのメンバーがおり、かつこれにより公開した手札の中にライブカードがない場合、自分のデッキの上からカードを5枚見る。その中からライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

*...and 91 more cards with this effect*

---

## ADD_HEARTS (88 cards)

### PL!-sd1-003-SD: 南 ことり
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Target:** MEMBER_SELF
**Params:** `{'until': 'live_end'}`

**Original Text:**
```
{{toujyou.png|登場}}自分の控え室からコスト4以下の『μ's』のメンバーカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ...
```

### PL!-bp3-012-PR: 南 ことり
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Target:** MEMBER_SELF
**Params:** `{'multiplier': True, 'per_live': True, 'until': 'live_end'}`

**Original Text:**
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、選んだハートを1つ得る。
```

### PL!-PR-003-PR: 南ことり
**Trigger:** ACTIVATED
**Conditions:** TURN_1 {}
**Effect Value:** 1
**Target:** MEMBER_SELF

**Original Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から必要ハートに{{heart_03.png|heart03}}を3以上含むライブカードを1枚手札に加える。
```

### PL!-PR-004-PR: 園田海未
**Trigger:** ACTIVATED
**Conditions:** TURN_1 {}
**Effect Value:** 1
**Target:** MEMBER_SELF

**Original Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から必要ハートに{{heart_01.png|heart01}}を3以上含むライブカードを1枚手札に加える。
```

### PL!HS-PR-016-PR: 日野下花帆
**Trigger:** ON_LIVE_START
**Effect Value:** 2
**Target:** MEMBER_SELF
**Params:** `{'until': 'live_end'}`

**Original Text:**
```
{{live_start.png|ライブ開始時}}手札の同じユニット名を持つカード2枚を控え室に置いてもよい：ライブ終了時まで、{{heart_04.png|heart04}}{{heart_04.png|heart04}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

*...and 83 more cards with this effect*

---

## RECOVER_LIVE (84 cards)

### PL!-sd1-001-SD: 高坂 穂乃果
**Trigger:** ON_PLAY
**Conditions:** COUNT_SUCCESS_LIVE {'min': 2}, COUNT_STAGE {'count': 2, 'zone': 'SUCCESS_LIVE'}
**Effect Value:** 1
**Target:** CARD_DISCARD
**Params:** `{'to': 'hand'}`

**Original Text:**
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にカードが2枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。
{{jyouji.png|常時}}自分の成功ライブカード置き場にあるカード1枚につき、{{icon_blade.png|ブレード}}を得る。
```

### PL!-sd1-005-SD: 星空 凛
**Trigger:** ACTIVATED
**Effect Value:** 1
**Target:** CARD_DISCARD
**Params:** `{'to': 'hand'}`

**Original Text:**
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### PL!-PR-003-PR: 南ことり
**Trigger:** ACTIVATED
**Conditions:** TURN_1 {}
**Effect Value:** 1
**Target:** CARD_DISCARD
**Params:** `{'to': 'hand', 'filter': 'heart_req'}`

**Original Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から必要ハートに{{heart_03.png|heart03}}を3以上含むライブカードを1枚手札に加える。
```

### PL!-PR-004-PR: 園田海未
**Trigger:** ACTIVATED
**Conditions:** TURN_1 {}
**Effect Value:** 1
**Target:** CARD_DISCARD
**Params:** `{'to': 'hand', 'filter': 'heart_req'}`

**Original Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から必要ハートに{{heart_01.png|heart01}}を3以上含むライブカードを1枚手札に加える。
```

### PL!S-PR-026-PR: 桜内梨子
**Trigger:** ACTIVATED
**Effect Value:** 1
**Target:** CARD_DISCARD
**Params:** `{'to': 'hand'}`

**Original Text:**
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

*...and 79 more cards with this effect*

---

## RECOVER_MEMBER (77 cards)

### PL!-sd1-002-SD: 絢瀬 絵里
**Trigger:** ACTIVATED
**Effect Value:** 1
**Target:** CARD_DISCARD
**Params:** `{'to': 'hand'}`

**Original Text:**
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### PL!-sd1-003-SD: 南 ことり
**Trigger:** ON_PLAY
**Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1
**Target:** CARD_DISCARD
**Params:** `{'to': 'hand', 'group': "μ's", 'cost_max': 4}`

**Original Text:**
```
{{toujyou.png|登場}}自分の控え室からコスト4以下の『μ's』のメンバーカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ...
```

### PL!S-PR-025-PR: 高海千歌
**Trigger:** ACTIVATED
**Effect Value:** 1
**Target:** CARD_DISCARD
**Params:** `{'to': 'hand'}`

**Original Text:**
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### PL!S-PR-027-PR: 松浦果南
**Trigger:** ACTIVATED
**Effect Value:** 1
**Target:** CARD_DISCARD
**Params:** `{'to': 'hand'}`

**Original Text:**
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### PL!HS-PR-014-PR: 日野下花帆
**Trigger:** ACTIVATED
**Effect Value:** 1
**Target:** CARD_DISCARD
**Params:** `{'to': 'hand'}`

**Original Text:**
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

*...and 72 more cards with this effect*

---

## TAP_OPPONENT (63 cards)

### PL!-PR-007-PR: 東條 希
**Trigger:** ON_PLAY
**Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1
**Target:** OPPONENT

**Original Text:**
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### PL!-PR-007-PR: 東條 希
**Trigger:** ON_LIVE_START
**Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1
**Target:** OPPONENT

**Original Text:**
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### PL!-PR-009-PR: 矢澤にこ
**Trigger:** ON_PLAY
**Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1
**Target:** OPPONENT

**Original Text:**
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### PL!-PR-009-PR: 矢澤にこ
**Trigger:** ON_LIVE_START
**Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1
**Target:** OPPONENT

**Original Text:**
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### PL!SP-bp1-023-L: START!! True dreams
**Trigger:** ON_LIVE_SUCCESS
**Conditions:** LIFE_LEAD {'type': 'score'}
**Effect Value:** 1
**Target:** OPPONENT

**Original Text:**
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。

(エールで出た{{icon_score.png|スコア}}1つにつき、成功したライブのスコアの合計に1を加算する。)
```

*...and 58 more cards with this effect*

---

## ENERGY_CHARGE (58 cards)

### PL!SP-PR-004-PR: 唐 可可
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'from': 'deck'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### PL!SP-PR-006-PR: 平安名すみれ
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'from': 'deck'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### PL!SP-PR-013-PR: 鬼塚冬毬
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'from': 'deck'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### PL!N-bp1-006-R＋: 近江彼方
**Trigger:** ON_PLAY
**Conditions:** TURN_1 {}, GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'DISCARD'}
**Effect Value:** 1

**Original Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：このターン、自分のステージに『虹ヶ咲』のメンバーが登場している場合、エネルギーを2枚アクティブにする。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：カードを1枚引く。
```

### PL!N-bp1-006-P: 近江彼方
**Trigger:** ON_PLAY
**Conditions:** TURN_1 {}, GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'DISCARD'}
**Effect Value:** 1

**Original Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：このターン、自分のステージに『虹ヶ咲』のメンバーが登場している場合、エネルギーを2枚アクティブにする。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：カードを1枚引く。
```

*...and 53 more cards with this effect*

---

## CHEER_REVEAL (56 cards)

### PL!-PR-007-PR: 東條 希
**Trigger:** ON_PLAY
**Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### PL!-PR-009-PR: 矢澤にこ
**Trigger:** ON_PLAY
**Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### PL!N-bp1-026-L: Poppin' Up!
**Trigger:** ON_LIVE_SUCCESS
**Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'OPPONENT_HAND'}, LIFE_LEAD {'type': 'score'}
**Effect Value:** 1

**Original Text:**
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、エールにより公開された自分のカードの中から、『虹ヶ咲』のカードを1枚手札に加える。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### PL!HS-bp1-021-L: Holiday∞Holiday
**Trigger:** ON_LIVE_SUCCESS
**Effect Value:** 1

**Original Text:**
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中から、『蓮ノ空』のライブカードを1枚手札に加える。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### PL!HS-bp1-022-L: AWOKE
**Trigger:** ON_LIVE_SUCCESS
**Conditions:** COUNT_GROUP {'group': '蓮ノ空', 'min': 10}
**Effect Value:** 1

**Original Text:**
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中に『蓮ノ空』のメンバーカードが10枚以上ある場合、このカードのスコアを＋１する。

(エールをすべて行った後、エールで出た{{icon_draw.png|ドロー}}1つにつき、カードを1枚引く。)
```

*...and 51 more cards with this effect*

---

## ACTIVATE_MEMBER (52 cards)

### PL!-PR-001-PR: 高坂穂乃果
**Trigger:** ON_LEAVES
**Effect Value:** 1
**Target:** MEMBER_SELF

**Original Text:**
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、メンバー1人をアクティブにしてもよい。
```

### PL!-PR-002-PR: 絢瀬絵里
**Trigger:** ON_LEAVES
**Effect Value:** 1
**Target:** MEMBER_SELF

**Original Text:**
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、メンバー1人をアクティブにしてもよい。
```

### PL!N-bp1-004-R: 朝香果林
**Trigger:** ON_PLAY
**Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'STAGE'}
**Effect Value:** 1
**Target:** MEMBER_SELECT
**Params:** `{'target': 'energy'}`

**Original Text:**
```
{{toujyou.png|登場}}自分のステージにほかの『虹ヶ咲』のメンバーがいる場合、エネルギーを1枚アクティブにする。
```

### PL!N-bp1-004-P: 朝香果林
**Trigger:** ON_PLAY
**Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'STAGE'}
**Effect Value:** 1
**Target:** MEMBER_SELECT
**Params:** `{'target': 'energy'}`

**Original Text:**
```
{{toujyou.png|登場}}自分のステージにほかの『虹ヶ咲』のメンバーがいる場合、エネルギーを1枚アクティブにする。
```

### PL!N-bp1-006-R＋: 近江彼方
**Trigger:** ON_PLAY
**Conditions:** TURN_1 {}, GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'DISCARD'}
**Effect Value:** 1
**Target:** MEMBER_SELECT
**Params:** `{'target': 'energy'}`

**Original Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：このターン、自分のステージに『虹ヶ咲』のメンバーが登場している場合、エネルギーを2枚アクティブにする。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：カードを1枚引く。
```

*...and 47 more cards with this effect*

---

## MOVE_MEMBER (47 cards)

### PL!SP-pb1-003-R: 嵐 千砂都
**Trigger:** ON_PLAY
**Conditions:** GROUP_FILTER {'group': '5yncri5e!', 'zone': 'OPPONENT_RIGHT_STAGE'}, IS_CENTER {}
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}自分のステージにいるメンバーが『5yncri5e!』のみの場合、自分と対戦相手は、センターエリアのメンバーを左サイドエリアに、左サイドエリアのメンバーを右サイドエリアに、右サイドエリアのメンバーをセンターエリアに、それぞれ移動させる。
```

### PL!SP-pb1-003-P＋: 嵐 千砂都
**Trigger:** ON_PLAY
**Conditions:** GROUP_FILTER {'group': '5yncri5e!', 'zone': 'OPPONENT_RIGHT_STAGE'}, IS_CENTER {}
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}自分のステージにいるメンバーが『5yncri5e!』のみの場合、自分と対戦相手は、センターエリアのメンバーを左サイドエリアに、左サイドエリアのメンバーを右サイドエリアに、右サイドエリアのメンバーをセンターエリアに、それぞれ移動させる。
```

### PL!SP-pb1-006-R: 桜小路きな子
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'until': 'live_end'}`

**Original Text:**
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動するたび、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
(対戦相手のカードの効果でも発動する。)
```

### PL!SP-pb1-006-P＋: 桜小路きな子
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'until': 'live_end'}`

**Original Text:**
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動するたび、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
(対戦相手のカードの効果でも発動する。)
```

### PL!SP-pb1-008-R: 若菜四季
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}カードを1枚引く。その後、登場したエリアとは別の自分のエリア1つを選ぶ。このメンバーをそのエリアに移動する。選んだエリアにメンバーがいる場合、そのメンバーは、このメンバーがいたエリアに移動させる。
```

*...and 42 more cards with this effect*

---

## ORDER_DECK (36 cards)

### PL!-sd1-019-SD: START:DASH!!
**Trigger:** ON_LIVE_SUCCESS
**Effect Value:** 1

**Original Text:**
```
{{live_success.png|ライブ成功時}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### PL!S-PR-028-PR: 黒澤ダイヤ
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### PL!S-PR-032-PR: 小原鞠莉
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### PL!S-PR-033-PR: 黒澤ルビィ
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### PL!HS-PR-020-PR: 徒町 小鈴
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Params:** `{'filter': 'live'}`

**Original Text:**
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：自分の控え室にあるメンバーカード2枚を好きな順番でデッキの一番上に置く。
```

*...and 31 more cards with this effect*

---

## META_RULE (31 cards)

### PL!HS-PR-010-PR: Reflection in the mirror
**Trigger:** CONSTANT
**Effect Value:** 0
**Target:** PLAYER
**Params:** `{'type': 'heart_rule'}`

**Original Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### PL!HS-PR-010-PR: Reflection in the mirror
**Trigger:** CONSTANT
**Effect Value:** 0
**Params:** `{'type': 'heart_rule'}`

**Original Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### PL!HS-PR-011-PR: Sparkly Spot
**Trigger:** CONSTANT
**Effect Value:** 0
**Target:** PLAYER
**Params:** `{'type': 'heart_rule'}`

**Original Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### PL!HS-PR-011-PR: Sparkly Spot
**Trigger:** CONSTANT
**Effect Value:** 0
**Params:** `{'type': 'heart_rule'}`

**Original Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### PL!HS-PR-012-PR: アイデンティティ
**Trigger:** CONSTANT
**Effect Value:** 0
**Target:** PLAYER
**Params:** `{'type': 'heart_rule'}`

**Original Text:**
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

*...and 26 more cards with this effect*

---

## MOVE_TO_DECK (29 cards)

### PL!N-bp1-011-R: ミア・テイラー
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'position': 'top'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：ライブカードが公開されるまで、自分のデッキの一番上のカードを公開し続ける。そのライブカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。
```

### PL!N-bp1-011-P: ミア・テイラー
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'position': 'top'}`

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：ライブカードが公開されるまで、自分のデッキの一番上のカードを公開し続ける。そのライブカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。
```

### PL!S-bp2-007-R＋: 国木田花丸
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Params:** `{'position': 'bottom'}`

**Original Text:**
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分の手札が7枚以下の場合、カードを1枚引く。
{{live_start.png|ライブ開始時}}手札のライブカードを1枚公開し、デッキの一番下に置いてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### PL!S-bp2-007-P: 国木田花丸
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Params:** `{'position': 'bottom'}`

**Original Text:**
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分の手札が7枚以下の場合、カードを1枚引く。
{{live_start.png|ライブ開始時}}手札のライブカードを1枚公開し、デッキの一番下に置いてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### PL!S-bp2-007-P＋: 国木田花丸
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Params:** `{'position': 'bottom'}`

**Original Text:**
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分の手札が7枚以下の場合、カードを1枚引く。
{{live_start.png|ライブ開始時}}手札のライブカードを1枚公開し、デッキの一番下に置いてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

*...and 24 more cards with this effect*

---

## TRIGGER_REMOTE (22 cards)

### PL!SP-bp2-006-R＋: 桜小路きな子
**Trigger:** ON_PLAY
**Conditions:** TURN_1 {}, COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1
**Params:** `{'from': 'discard'}`

**Original Text:**
```
{{toujyou.png|登場}}バトンタッチして登場した場合、このバトンタッチで控え室に置かれた『Liella!』のメンバーカードを1枚手札に加える。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。
...
```

### PL!SP-bp2-006-R＋: 桜小路きな子
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'from': 'stage'}`

**Original Text:**
```
{{toujyou.png|登場}}バトンタッチして登場した場合、このバトンタッチで控え室に置かれた『Liella!』のメンバーカードを1枚手札に加える。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。
...
```

### PL!SP-bp2-006-P: 桜小路きな子
**Trigger:** ON_PLAY
**Conditions:** TURN_1 {}, COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1
**Params:** `{'from': 'discard'}`

**Original Text:**
```
{{toujyou.png|登場}}バトンタッチして登場した場合、このバトンタッチで控え室に置かれた『Liella!』のメンバーカードを1枚手札に加える。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。
...
```

### PL!SP-bp2-006-P: 桜小路きな子
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'from': 'stage'}`

**Original Text:**
```
{{toujyou.png|登場}}バトンタッチして登場した場合、このバトンタッチで控え室に置かれた『Liella!』のメンバーカードを1枚手札に加える。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。
...
```

### PL!SP-bp2-006-P＋: 桜小路きな子
**Trigger:** ON_PLAY
**Conditions:** TURN_1 {}, COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 1
**Params:** `{'from': 'discard'}`

**Original Text:**
```
{{toujyou.png|登場}}バトンタッチして登場した場合、このバトンタッチで控え室に置かれた『Liella!』のメンバーカードを1枚手札に加える。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。
...
```

*...and 17 more cards with this effect*

---

## PLACE_UNDER (20 cards)

### PL!N-bp3-001-R＋: 上原歩夢
**Trigger:** ON_LIVE_START
**Effect Value:** 1

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れ...
```

### PL!N-bp3-001-R＋: 上原歩夢
**Trigger:** ON_LIVE_START
**Effect Value:** 1

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れ...
```

### PL!N-bp3-001-P: 上原歩夢
**Trigger:** ON_LIVE_START
**Effect Value:** 1

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れ...
```

### PL!N-bp3-001-P: 上原歩夢
**Trigger:** ON_LIVE_START
**Effect Value:** 1

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れ...
```

### PL!N-bp3-001-P＋: 上原歩夢
**Trigger:** ON_LIVE_START
**Effect Value:** 1

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れ...
```

*...and 15 more cards with this effect*

---

## SET_BLADES (14 cards)

### PL!N-bp1-003-R＋: 桜坂しずく
**Trigger:** ON_LIVE_START
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### PL!N-bp1-003-P: 桜坂しずく
**Trigger:** ON_LIVE_START
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### PL!N-bp1-003-P＋: 桜坂しずく
**Trigger:** ON_LIVE_START
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### PL!N-bp1-003-SEC: 桜坂しずく
**Trigger:** ON_LIVE_START
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### PL!HS-bp1-006-R＋: 藤島 慈
**Trigger:** ON_LIVE_START
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}カードを2枚引き、手札を1枚控え室に置く。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

*...and 9 more cards with this effect*

---

## SWAP_ZONE (12 cards)

### PL!-sd1-006-SD: 西木野 真姫
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}手札のライブカードを1枚公開してもよい：自分の成功ライブカード置き場にあるカードを1枚手札に加える。そうした場合、これにより公開したカードを自分の成功ライブカード置き場に置く。
```

### PL!-sd1-006-SD: 西木野 真姫
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}手札のライブカードを1枚公開してもよい：自分の成功ライブカード置き場にあるカードを1枚手札に加える。そうした場合、これにより公開したカードを自分の成功ライブカード置き場に置く。
```

### PL!N-bp1-026-L: Poppin' Up!
**Trigger:** ON_LIVE_SUCCESS
**Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'OPPONENT_HAND'}, LIFE_LEAD {'type': 'score'}
**Effect Value:** 1

**Original Text:**
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、エールにより公開された自分のカードの中から、『虹ヶ咲』のカードを1枚手札に加える。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### PL!HS-bp1-021-L: Holiday∞Holiday
**Trigger:** ON_LIVE_SUCCESS
**Effect Value:** 1

**Original Text:**
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中から、『蓮ノ空』のライブカードを1枚手札に加える。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### PL!SP-bp2-025-L: Bubble Rise
**Trigger:** ON_LIVE_SUCCESS
**Conditions:** COUNT_STAGE {'count': 2, 'zone': 'HAND'}
**Effect Value:** 1

**Original Text:**
```
{{live_success.png|ライブ成功時}}自分のステージに「澁谷かのん」、「ウィーン・マルガレーテ」、「鬼塚冬毬」のうち、名前の異なるメンバーが2人以上いる場合、エールにより公開された自分のカードの中から、カードを1枚手札に加える。
```

*...and 7 more cards with this effect*

---

## BATON_TOUCH_MOD (11 cards)

### PL!HS-bp2-021-L: 眩耀夜行
**Trigger:** ON_PLAY
**Conditions:** COUNT_GROUP {'group': '蓮ノ空', 'min': 2, 'zone': 'STAGE'}
**Effect Value:** 2

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のステージに、このターン中にバトンタッチして登場した『蓮ノ空』のメンバーが2人以上いる場合、このカードを成功させるための必要ハートを{{heart_04.png|heart04}}減らす。
```

### PL!HS-bp2-023-L: Mirage Voyage
**Trigger:** ON_PLAY
**Conditions:** COUNT_GROUP {'group': '蓮ノ空', 'min': 2, 'zone': 'STAGE'}
**Effect Value:** 2

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のステージに、このターン中にバトンタッチして登場した『蓮ノ空』のメンバーが2人以上いる場合、このカードを成功させるための必要ハートを{{heart_05.png|heart05}}減らす。
```

### PL!HS-bp2-025-L: ココン東西
**Trigger:** ON_PLAY
**Conditions:** COUNT_GROUP {'group': '蓮ノ空', 'min': 2, 'zone': 'STAGE'}
**Effect Value:** 2

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のステージに、このターン中にバトンタッチして登場した『蓮ノ空』のメンバーが2人以上いる場合、このカードを成功させるための必要ハートを{{heart_01.png|heart01}}減らす。
```

### PL!SP-bp4-004-R＋: 平安名すみれ
**Trigger:** CONSTANT
**Effect Value:** 2

**Original Text:**
```
{{jyouji.png|常時}}このカードのプレイに際し、2人のメンバーとバトンタッチしてもよい。
{{toujyou.png|登場}}{{center.png|センター}}『Liella!』のメンバー2人からバトンタッチして登場している場合、カードを2枚引き、自分の控え室にあるコスト4以下の『Liella!』のメンバーカード1枚を自分のステージのメンバーのいないエリアに登場させる。
```

### PL!SP-bp4-004-R＋: 平安名すみれ
**Trigger:** ON_PLAY
**Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}, GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}, COST_CHECK {'value': 4, 'comparison': 'LE'}
**Effect Value:** 2

**Original Text:**
```
{{jyouji.png|常時}}このカードのプレイに際し、2人のメンバーとバトンタッチしてもよい。
{{toujyou.png|登場}}{{center.png|センター}}『Liella!』のメンバー2人からバトンタッチして登場している場合、カードを2枚引き、自分の控え室にあるコスト4以下の『Liella!』のメンバーカード1枚を自分のステージのメンバーのいないエリアに登場させる。
```

*...and 6 more cards with this effect*

---

## REDUCE_HEART_REQ (10 cards)

### PL!-sd1-022-SD: 僕らは今のなかで
**Trigger:** ON_LIVE_START
**Effect Value:** 2
**Target:** PLAYER

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にあるカード1枚につき、このカードを成功させるための必要ハートは{{heart_00.png|heart0}}{{heart_00.png|heart0}}少なくなる。
```

### PL!SP-pb1-025-L: Jellyfish
**Trigger:** ON_PLAY
**Effect Value:** 1
**Target:** PLAYER

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のステージにいる、このターン中に登場、またはエリアを移動した『5yncri5e!』のメンバー1人につき、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}減らす。
```

### PL!HS-bp2-021-L: 眩耀夜行
**Trigger:** ON_PLAY
**Conditions:** COUNT_GROUP {'group': '蓮ノ空', 'min': 2, 'zone': 'STAGE'}
**Effect Value:** 1
**Target:** PLAYER

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のステージに、このターン中にバトンタッチして登場した『蓮ノ空』のメンバーが2人以上いる場合、このカードを成功させるための必要ハートを{{heart_04.png|heart04}}減らす。
```

### PL!HS-bp2-023-L: Mirage Voyage
**Trigger:** ON_PLAY
**Conditions:** COUNT_GROUP {'group': '蓮ノ空', 'min': 2, 'zone': 'STAGE'}
**Effect Value:** 1
**Target:** PLAYER

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のステージに、このターン中にバトンタッチして登場した『蓮ノ空』のメンバーが2人以上いる場合、このカードを成功させるための必要ハートを{{heart_05.png|heart05}}減らす。
```

### PL!HS-bp2-024-L: レディバグ
**Trigger:** ON_PLAY
**Conditions:** HAS_MEMBER {'name': '徒町小鈴', 'zone': 'STAGE'}, HAS_MEMBER {'name': '徒町小鈴', 'zone': 'STAGE'}, HAS_MEMBER {'name': '村野さやか', 'zone': 'STAGE'}
**Effect Value:** 3
**Target:** PLAYER

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のステージに「徒町小鈴」が登場しており、かつ「徒町小鈴」よりコストの大きい「村野さやか」が登場している場合、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}{{heart_00.png|heart0}}{{heart_00.png|heart0}}減らす。
```

*...and 5 more cards with this effect*

---

## REPLACE_EFFECT (9 cards)

### PL!S-bp2-008-R＋: 小原鞠莉
**Trigger:** ON_PLAY
**Conditions:** COUNT_GROUP {'group': 'Aqours', 'min': 1, 'zone': 'STAGE'}, COUNT_STAGE {'min': 3}
**Effect Value:** 2
**Params:** `{'replaces': 'score_boost'}`

**Original Text:**
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3...
```

### PL!S-bp2-008-P: 小原鞠莉
**Trigger:** ON_PLAY
**Conditions:** COUNT_GROUP {'group': 'Aqours', 'min': 1, 'zone': 'STAGE'}, COUNT_STAGE {'min': 3}
**Effect Value:** 2
**Params:** `{'replaces': 'score_boost'}`

**Original Text:**
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3...
```

### PL!S-bp2-008-P＋: 小原鞠莉
**Trigger:** ON_PLAY
**Conditions:** COUNT_GROUP {'group': 'Aqours', 'min': 1, 'zone': 'STAGE'}, COUNT_STAGE {'min': 3}
**Effect Value:** 2
**Params:** `{'replaces': 'score_boost'}`

**Original Text:**
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3...
```

### PL!S-bp2-008-SEC: 小原鞠莉
**Trigger:** ON_PLAY
**Conditions:** COUNT_GROUP {'group': 'Aqours', 'min': 1, 'zone': 'STAGE'}, COUNT_STAGE {'min': 3}
**Effect Value:** 2
**Params:** `{'replaces': 'score_boost'}`

**Original Text:**
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3...
```

### PL!N-bp3-026-L: サイコーハート
**Trigger:** ON_LIVE_START
**Effect Value:** 2
**Params:** `{'replaces': 'score_boost'}`

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にスコアが１か５のカードがある場合、このカードのスコアを＋１する。それらが両方ある場合、代わりにスコアを＋２する。
```

*...and 4 more cards with this effect*

---

## NEGATE_EFFECT (9 cards)

### PL!SP-bp2-001-R＋: 澁谷かのん
**Trigger:** ON_PLAY
**Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
**Effect Value:** 1
**Params:** `{'all': True}`

**Original Text:**
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```

### PL!SP-bp2-001-R＋: 澁谷かのん
**Trigger:** ON_PLAY
**Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```

### PL!SP-bp2-001-P: 澁谷かのん
**Trigger:** ON_PLAY
**Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
**Effect Value:** 1
**Params:** `{'all': True}`

**Original Text:**
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```

### PL!SP-bp2-001-P: 澁谷かのん
**Trigger:** ON_PLAY
**Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```

### PL!SP-bp2-001-P＋: 澁谷かのん
**Trigger:** ON_PLAY
**Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
**Effect Value:** 1
**Params:** `{'all': True}`

**Original Text:**
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```

*...and 4 more cards with this effect*

---

## SELECT_MODE (7 cards)

### PL!-PR-005-PR: 星空 凛
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}以下から1つを選ぶ。
・カードを1枚引き、手札を1枚控え室に置く。
・相手のステージにいるすべてのコスト2以下のメンバーをウェイトにする。
```

### PL!-PR-006-PR: 西木野真姫
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}以下から1つを選ぶ。
・カードを1枚引き、手札を1枚控え室に置く。
・相手のステージにいるすべてのコスト2以下のメンバーをウェイトにする。
```

### PL!-PR-008-PR: 小泉花陽
**Trigger:** ON_PLAY
**Effect Value:** 1

**Original Text:**
```
{{toujyou.png|登場}}以下から1つを選ぶ。
・カードを1枚引き、手札を1枚控え室に置く。
・相手のステージにいるすべてのコスト2以下のメンバーをウェイトにする。
```

### PL!S-bp3-024-L: Deep Resonance
**Trigger:** ON_LIVE_START
**Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'CENTER_STAGE'}, IS_CENTER {}, COST_CHECK {'value': 9, 'comparison': 'GE'}
**Effect Value:** 1

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のステージのセンターエリアにコスト9以上の『Aqours』のメンバーがいる場合、以下から1つを選ぶ。
・ライブ終了時まで、自分のステージにいるメンバー1人は、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
・相手のステージにいるコスト4以下のメンバー1人をウェイトにする。
```

### PL!N-bp4-030-L: Daydream Mermaid
**Trigger:** ON_LIVE_SUCCESS
**Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'SUCCESS_LIVE'}
**Effect Value:** 1

**Original Text:**
```
{{live_success.png|ライブ成功時}}以下から1つを選ぶ。自分の成功ライブカード置き場に『虹ヶ咲』のカードがある場合、代わりに1つ以上を選ぶ。
・自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
・自分の控え室からメンバーカードを1枚手札に加える。
```

*...and 2 more cards with this effect*

---

## REDUCE_COST (7 cards)

### PL!HS-bp2-024-L: レディバグ
**Trigger:** ON_PLAY
**Conditions:** HAS_MEMBER {'name': '徒町小鈴', 'zone': 'STAGE'}, HAS_MEMBER {'name': '徒町小鈴', 'zone': 'STAGE'}, HAS_MEMBER {'name': '村野さやか', 'zone': 'STAGE'}
**Effect Value:** 1

**Original Text:**
```
{{live_start.png|ライブ開始時}}自分のステージに「徒町小鈴」が登場しており、かつ「徒町小鈴」よりコストの大きい「村野さやか」が登場している場合、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}{{heart_00.png|heart0}}{{heart_00.png|heart0}}減らす。
```

### PL!-pb1-007-R: 東條 希
**Trigger:** ACTIVATED
**Effect Value:** 1

**Original Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を3枚控え室に置く：自分のステージにほかの『lilywhite』のメンバーがいる場合、自分の控え室から『μ's』のライブカードを1枚手札に加える。この能力を起動するためのコストは、自分の成功ライブカード置き場にあるカード1枚につき、控え室に置く手札の数が1枚減る。
```

### PL!-pb1-007-P＋: 東條 希
**Trigger:** ACTIVATED
**Effect Value:** 1

**Original Text:**
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を3枚控え室に置く：自分のステージにほかの『lilywhite』のメンバーがいる場合、自分の控え室から『μ's』のライブカードを1枚手札に加える。この能力を起動するためのコストは、自分の成功ライブカード置き場にあるカード1枚につき、控え室に置く手札の数が1枚減る。
```

### PL!-pb1-014-R: 星空 凛
**Trigger:** CONSTANT
**Conditions:** GROUP_FILTER {'group': 'lilywhite', 'zone': 'SUCCESS_LIVE'}
**Effect Value:** 1

**Original Text:**
```
{{jyouji.png|常時}}自分の成功ライブカード置き場に『lilywhite』のカードがある場合、手札にあるこのメンバーカードのコストは2減る。
```

### PL!-pb1-014-P＋: 星空 凛
**Trigger:** CONSTANT
**Conditions:** GROUP_FILTER {'group': 'lilywhite', 'zone': 'SUCCESS_LIVE'}
**Effect Value:** 1

**Original Text:**
```
{{jyouji.png|常時}}自分の成功ライブカード置き場に『lilywhite』のカードがある場合、手札にあるこのメンバーカードのコストは2減る。
```

*...and 2 more cards with this effect*

---

## RESTRICTION (6 cards)

### PL!SP-bp1-001-R: 澁谷かのん
**Trigger:** CONSTANT
**Effect Value:** 1
**Params:** `{'type': 'live'}`

**Original Text:**
```
{{jyouji.png|常時}}自分のステージにほかのメンバーがいない場合、自分はライブできない。
```

### PL!SP-bp1-001-P: 澁谷かのん
**Trigger:** CONSTANT
**Effect Value:** 1
**Params:** `{'type': 'live'}`

**Original Text:**
```
{{jyouji.png|常時}}自分のステージにほかのメンバーがいない場合、自分はライブできない。
```

### PL!S-bp2-024-L: 君のこころは輝いてるかい？
**Trigger:** CONSTANT
**Effect Value:** 1
**Params:** `{'type': 'placement'}`

**Original Text:**
```
{{jyouji.png|常時}}このカードは成功ライブカード置き場に置くことができない。
{{live_success.png|ライブ成功時}}カードを2枚引き、手札を1枚控え室に置く。
```

### PL!HS-bp2-014-N: 大沢瑠璃乃
**Trigger:** ON_PLAY
**Effect Value:** 1
**Params:** `{'type': 'live'}`

**Original Text:**
```
{{toujyou.png|登場}}カードを1枚引く。ライブ終了時まで、自分はライブできない。
```

### PL!S-pb1-022-L: 逃走迷走メビウスループ
**Trigger:** ON_LIVE_SUCCESS
**Effect Value:** 1
**Params:** `{'type': 'placement'}`

**Original Text:**
```
{{live_success.png|ライブ成功時}}このターン、ライブに勝利するプレイヤーを決定するとき、自分と相手のライブの合計スコアが同じ場合、ライブ終了時まで、自分と相手は成功ライブカード置き場にカードを置くことができない。
```

*...and 1 more cards with this effect*

---

## TRANSFORM_COLOR (2 cards)

### PL!N-bp4-025-L: VIVID WORLD
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Params:** `{'target_color': '青ブレード'}`

**Original Text:**
```
{{live_start.png|ライブ開始時}}ライブ終了時まで、エールによって公開される自分のカードが持つ[桃ブレード]、[赤ブレード]、[黄ブレード]、[緑ブレード]、[紫ブレード]、{{icon_b_all.png|ALLブレード}}は、すべて[青ブレード]になる。
{{live_success.png|ライブ成功時}}エールにより公開された自分の『虹ヶ咲』のメンバーカードが持つハートの中...
```

### PL!SP-bp4-023-L: Dazzling Game
**Trigger:** ON_LIVE_START
**Effect Value:** 1
**Params:** `{'target_color': '紫ブレード'}`

**Original Text:**
```
{{live_start.png|ライブ開始時}}ライブ終了時まで、自分のステージにいる、「澁谷かのん」「ウィーン・マルガレーテ」「鬼塚冬毬」のうちのメンバー1人と、これにより選んだメンバー以外の『Liella!』のメンバー1人は、{{icon_blade.png|ブレード}}を得る。
{{live_start.png|ライブ開始時}}ライブ終了時まで、エールによって公開される自分のカードが持つ[...
```


---

## FLAVOR_ACTION (1 cards)

### LL-PR-004-PR: 愛♡スクリ～ム！
**Trigger:** ON_LIVE_START
**Conditions:** MODAL_ANSWER {'answer': 'チョコミントかストロベリーフレイバーかクッキー＆クリーム'}, MODAL_ANSWER {'answer': 'あなた'}, MODAL_ANSWER {'answer': 'それ以外'}
**Effect Value:** 1

**Original Text:**
```
{{live_start.png|ライブ開始時}}相手に何が好き？と聞く。
回答がチョコミントかストロベリーフレイバーかクッキー＆クリームの場合、自分と相手は手札を1枚控え室に置く。
回答があなたの場合、自分と相手はカードを1枚引く。
回答がそれ以外の場合、ライブ終了時まで、自分と相手のステージにいるメンバーは{{icon_blade.png|ブレード}}を得る。
```


---

## IMMUNITY (1 cards)

### LL-bp2-001-R＋: 渡辺 曜&鬼塚夏美&大沢瑠璃乃
**Trigger:** CONSTANT
**Effect Value:** 1

**Original Text:**
```
{{jyouji.png|常時}}手札にあるこのメンバーカードのコストは、このカード以外の自分の手札1枚につき、1少なくなる。
{{jyouji.png|常時}}このメンバーはバトンタッチで控え室に置けない。
{{live_start.png|ライブ開始時}}手札の「渡辺曜」と「鬼塚夏美」と「大沢瑠璃乃」を、好きな枚数控え室に置いてもよい：ライブ終了時まで、これによって控え室に置いた枚数1枚につき...
```


---

## SET_SCORE (1 cards)

### PL!S-bp3-019-L: MIRACLE WAVE
**Trigger:** ON_LIVE_SUCCESS
**Effect Value:** 4

**Original Text:**
```
{{live_success.png|ライブ成功時}}このターン、エールにより公開された自分のカードの中にブレードハートを持たないカードが0枚の場合か、または自分が余剰ハートを2つ以上持っている場合、このカードのスコアは４になる。
```


---
