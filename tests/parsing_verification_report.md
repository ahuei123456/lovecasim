# Summary

| Metric | Count |
|--------|-------|
| Total cards | 1329 |
| Cards with abilities | 741 |
| Successfully parsed | 738 |
| Parse failed | 3 |
| Cards with FAQ | 257 |
| Parse rate | 99.6% |

---

# Ability Parsing Verification Report

This report shows each card's ability text and how it is parsed by the game engine.
Use this to verify that all abilities are correctly interpreted.

---

## PL!-sd1-001-SD: 高坂 穂乃果
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にカードが2枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。
{{jyouji.png|常時}}自分の成功ライブカード置き場にあるカード1枚につき、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_SUCCESS_LIVE {'min': 2}, COUNT_STAGE {'count': 2, 'zone': 'SUCCESS_LIVE'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'per_live': True}

---

## PL!-sd1-002-SD: 絢瀬 絵里
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!-sd1-003-SD: 南 ことり
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からコスト4以下の『μ's』のメンバーカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's", 'cost_max': 4}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!-sd1-004-SD: 園田 海未
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを5枚見る。その中から『μ's』のライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=5)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': "μ's"}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': "μ's"}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!-sd1-005-SD: 星空 凛
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!-sd1-006-SD: 西木野 真姫
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札のライブカードを1枚公開してもよい：自分の成功ライブカード置き場にあるカードを1枚手札に加える。そうした場合、これにより公開したカードを自分の成功ライブカード置き場に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'success_live'}
  **Effect:** SWAP_ZONE (value=1)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** SWAP_ZONE (value=1)

### FAQ
**Q:** 『{{jyouji.png|常時}}このカードは成功ライブカード置き場に置くことができない。』について。
この能力をもつライブカードを成功ライブカード置き場と入れ替える効果などで成功ライブカード置き場に置くことができますか？...
**A:** いいえ、できません。...

---

## PL!-sd1-007-SD: 東條 希
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを5枚控え室に置く。それらの中にライブカードがある場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** HAS_LIVE_CARD {}
  **Effect:** SWAP_CARDS (value=5) {'target': 'discard', 'from': 'deck'}
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!-sd1-008-SD: 小泉 花陽
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分のデッキの上からカードを10枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** SWAP_CARDS (value=10) {'target': 'discard', 'from': 'deck'}

---

## PL!-sd1-009-SD: 矢澤 にこ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の控え室に『μ's』のカードが25枚以上ある場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_GROUP {'group': "μ's", 'min': 25, 'zone': 'DISCARD'}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!-sd1-011-SD: 絢瀬 絵里
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!-sd1-012-SD: 南 ことり
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!-sd1-015-SD: 西木野 真姫
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中からメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!-sd1-016-SD: 東條 希
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!-sd1-019-SD: START:DASH!!
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!-sd1-022-SD: 僕らは今のなかで
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にあるカード1枚につき、このカードを成功させるための必要ハートは{{heart_00.png|heart0}}{{heart_00.png|heart0}}少なくなる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** REDUCE_HEART_REQ (value=2) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_live': True}

---

## PL!-bp3-012-PR: 南 ことり
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、選んだハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'multiplier': True, 'per_live': True, 'until': 'live_end'}

---

## PL!-PR-001-PR: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、メンバー1人をアクティブにしてもよい。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELF

---

## PL!-PR-002-PR: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、メンバー1人をアクティブにしてもよい。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELF

---

## PL!-PR-003-PR: 南ことり
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から必要ハートに{{heart_03.png|heart03}}を3以上含むライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=2
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'filter': 'heart_req'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!-PR-004-PR: 園田海未
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から必要ハートに{{heart_01.png|heart01}}を3以上含むライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=2
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'filter': 'heart_req'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!-PR-005-PR: 星空 凛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}以下から1つを選ぶ。
・カードを1枚引き、手札を1枚控え室に置く。
・相手のステージにいるすべてのコスト2以下のメンバーをウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SELECT_MODE (value=1)

---

## PL!-PR-006-PR: 西木野真姫
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}以下から1つを選ぶ。
・カードを1枚引き、手札を1枚控え室に置く。
・相手のステージにいるすべてのコスト2以下のメンバーをウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SELECT_MODE (value=1)

---

## PL!-PR-007-PR: 東條 希
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!-PR-008-PR: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}以下から1つを選ぶ。
・カードを1枚引き、手札を1枚控え室に置く。
・相手のステージにいるすべてのコスト2以下のメンバーをウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SELECT_MODE (value=1)

---

## PL!-PR-009-PR: 矢澤にこ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!S-PR-013-PR: 高海千歌
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!S-PR-016-PR: 黒澤ダイヤ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!S-PR-019-PR: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!S-PR-020-PR: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!S-PR-021-PR: 黒澤ルビィ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!S-PR-025-PR: 高海千歌
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!S-PR-026-PR: 桜内梨子
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!S-PR-027-PR: 松浦果南
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!S-PR-028-PR: 黒澤ダイヤ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

---

## PL!S-PR-029-PR: 渡辺 曜
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分か相手のステージにコスト13以上のメンバーがいる場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** OPPONENT_HAS {}, COST_CHECK {'value': 13, 'comparison': 'GE'}
  **Effect:** ADD_BLADES (value=1) → OPPONENT

---

## PL!S-PR-030-PR: 津島善子
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分か相手のステージにコスト13以上のメンバーがいる場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** OPPONENT_HAS {}, COST_CHECK {'value': 13, 'comparison': 'GE'}
  **Effect:** ADD_BLADES (value=1) → OPPONENT

---

## PL!S-PR-031-PR: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分か相手のステージにコスト13以上のメンバーがいる場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** OPPONENT_HAS {}, COST_CHECK {'value': 13, 'comparison': 'GE'}
  **Effect:** ADD_BLADES (value=1) → OPPONENT

---

## PL!S-PR-032-PR: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

---

## PL!S-PR-033-PR: 黒澤ルビィ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

---

## PL!N-bp1-019-PR: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-PR-003-PR: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札をすべて公開する：自分のステージにほかのメンバーがおり、かつこれにより公開した手札の中にライブカードがない場合、自分のデッキの上からカードを5枚見る。その中からライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** REVEAL_HAND_ALL=0
  **Conditions:** TURN_1 {}, HAND_HAS_NO_LIVE {}
  **Effect:** LOOK_DECK (value=5)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-PR-004-PR: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-PR-005-PR: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを2枚引き、手札を2枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-PR-006-PR: 朝香果林
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-PR-007-PR: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを2枚引き、手札を2枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-PR-008-PR: 近江彼方
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札をすべて公開する：自分のステージにほかのメンバーがおり、かつこれにより公開した手札の中にライブカードがない場合、自分のデッキの上からカードを5枚見る。その中からライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** REVEAL_HAND_ALL=0
  **Conditions:** TURN_1 {}, HAND_HAS_NO_LIVE {}
  **Effect:** LOOK_DECK (value=5)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-PR-009-PR: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!N-PR-010-PR: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札をすべて公開する：自分のステージにほかのメンバーがおり、かつこれにより公開した手札の中にライブカードがない場合、自分のデッキの上からカードを5枚見る。その中からライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** REVEAL_HAND_ALL=0
  **Conditions:** TURN_1 {}, HAND_HAS_NO_LIVE {}
  **Effect:** LOOK_DECK (value=5)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-PR-011-PR: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを2枚引き、手札を2枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-PR-012-PR: 三船栞子
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!N-PR-013-PR: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-PR-014-PR: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!SP-PR-003-PR: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギーが7枚以上ある場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_STAGE {'min': 7}, COUNT_ENERGY {'min': 7}
  **Effect:** DRAW (value=7) → PLAYER

---

## PL!SP-PR-004-PR: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}

---

## PL!SP-PR-006-PR: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}

---

## PL!SP-PR-007-PR: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギーが7枚以上ある場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_STAGE {'min': 7}, COUNT_ENERGY {'min': 7}
  **Effect:** DRAW (value=7) → PLAYER

---

## PL!SP-PR-009-PR: 米女メイ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。これによりライブカードを控え室に置いた場合、さらにカードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-PR-010-PR: 若菜四季
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギーが7枚以上ある場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_STAGE {'min': 7}, COUNT_ENERGY {'min': 7}
  **Effect:** DRAW (value=7) → PLAYER

---

## PL!SP-PR-011-PR: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。これによりライブカードを控え室に置いた場合、さらにカードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-PR-012-PR: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。これによりライブカードを控え室に置いた場合、さらにカードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-PR-013-PR: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}

---

## PL!HS-bp2-011-PR: 村野さやか
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}デッキの上からカードを5枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=5) {'target': 'discard', 'from': 'deck'}

---

## PL!HS-PR-001-PR: 日野下花帆
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-PR-002-PR: 村野さやか
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-PR-005-PR: 大沢瑠璃乃
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-PR-010-PR: Reflection in the mirror
Type: ライブ

### Original Ability Text
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

---

## PL!HS-PR-011-PR: Sparkly Spot
Type: ライブ

### Original Ability Text
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

---

## PL!HS-PR-012-PR: アイデンティティ
Type: ライブ

### Original Ability Text
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

---

## PL!HS-PR-014-PR: 日野下花帆
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!HS-PR-016-PR: 日野下花帆
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札の同じユニット名を持つカード2枚を控え室に置いてもよい：ライブ終了時まで、{{heart_04.png|heart04}}{{heart_04.png|heart04}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}手札の同じユニット名を持つカード2枚を控え室に置いてもよい：ライブ終了時まで、{{heart_04.png|heart04}}{{heart_04.png|heart04}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。』などについて、この能力を使用しているメンバーカードと同じユニットの必要は...
**A:** いいえ、同じユニットである必要はありません。
手札から控え室に置くカードのユニットが同じである必要があります。ただし、「μ's」や「Aqours」など、グループ名は参照できません。...

---

## PL!HS-PR-017-PR: 村野さやか
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札の同じユニット名を持つカード2枚を控え室に置いてもよい：ライブ終了時まで、{{heart_05.png|heart05}}{{heart_05.png|heart05}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}手札の同じユニット名を持つカード2枚を控え室に置いてもよい：ライブ終了時まで、{{heart_04.png|heart04}}{{heart_04.png|heart04}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。』などについて、この能力を使用しているメンバーカードと同じユニットの必要は...
**A:** いいえ、同じユニットである必要はありません。
手札から控え室に置くカードのユニットが同じである必要があります。ただし、「μ's」や「Aqours」など、グループ名は参照できません。...

---

## PL!HS-PR-018-PR: 大沢瑠璃乃
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-PR-019-PR: 百生 吟子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚控え室に置く。それらがすべて{{heart_04.png|heart04}}を持つメンバーカードの場合、ライブ終了時まで、{{heart_04.png|heart04}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '{{heart_04.png|heart04}}を持つメンバーカード', 'context': 'revealed'}
  **Effect:** SWAP_CARDS (value=3) {'target': 'discard', 'from': 'deck'}
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!HS-PR-020-PR: 徒町 小鈴
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：自分の控え室にあるメンバーカード2枚を好きな順番でデッキの一番上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1) {'filter': 'live'}

---

## PL!HS-PR-021-PR: 安養寺 姫芽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚控え室に置く。それらがすべて{{heart_01.png|heart01}}を持つメンバーカードの場合、ライブ終了時まで、{{heart_01.png|heart01}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '{{heart_01.png|heart01}}を持つメンバーカード', 'context': 'revealed'}
  **Effect:** SWAP_CARDS (value=3) {'target': 'discard', 'from': 'deck'}
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!HS-PR-022-PR: 桂城 泉
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：自分の控え室にあるメンバーカード2枚を好きな順番でデッキの一番上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1) {'filter': 'live'}

---

## PL!HS-PR-023-PR: セラス 柳田 リリエンフェルト
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## LL-PR-004-PR: 愛♡スクリ～ム！
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}相手に何が好き？と聞く。
回答がチョコミントかストロベリーフレイバーかクッキー＆クリームの場合、自分と相手は手札を1枚控え室に置く。
回答があなたの場合、自分と相手はカードを1枚引く。
回答がそれ以外の場合、ライブ終了時まで、自分と相手のステージにいるメンバーは{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Conditions:** MODAL_ANSWER {'answer': 'チョコミントかストロベリーフレイバーかクッキー＆クリーム'}, MODAL_ANSWER {'answer': 'あなた'}, MODAL_ANSWER {'answer': 'それ以外'}
  **Effect:** FLAVOR_ACTION (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** ADD_BLADES (value=1) → OPPONENT {'until': 'live_end'}

### FAQ
**Q:** {{live_start.png|ライブ開始時}}能力による質問への回答が「クッキー＆クリームよりもあなた」でした。
この場合、どの回答として扱いますか？...
**A:** 質問者と回答者のお互いが正しく認識できる場合、回答が一字一句同じものである必要はありません。
対戦相手がどの回答として答えたのか確認をしてください。...

---

## LL-bp1-001-R＋: 上原歩夢&澁谷かのん&日野下花帆
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からメンバーカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札の「上原歩夢」と「澁谷かのん」と「日野下花帆」を、好きな組み合わせで合計3枚、控え室に置いてもよい：ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋３する。」を得る。
（手札のこのカードもこの効果で控え室に置ける。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** SWAP_CARDS (value=3) {'target': 'discard', 'from': 'hand'}
  **Effect:** BOOST_SCORE (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}手札の「上原歩夢」と「澁谷かのん」と「日野下花帆」を、好きな組み合わせで合計3枚、控え室に置いてもよい：ライブ終了時まで、「常時ライブの合計スコアを＋３する。」を得る。』について。
控え室に置くカードとして「私のSymphony〜澁谷かのんVer.〜」を選択できますか？...
**A:** はい、カード名に「澁谷かのん」を含むため、選択できます。...

**Q:** このカードはグループ名やユニット名を持っていますか？...
**A:** カードに記載されているグループ名は持っていますが、カードに記載されていないユニット名は持っていません。...

**Q:** 『{{live_start.png|ライブ開始時}}手札の「上原歩夢」と「澁谷かのん」と「日野下花帆」を、好きな組み合わせで合計3枚、控え室に置いてもよい：ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋３する。」を得る。』について。
『「上原歩夢」を3枚』や『「澁谷かのん」を2枚と「日野下花帆」を1枚』という組み合わせでコストを支払うことはできますか？...
**A:** はい、できます。「上原歩夢」「澁谷かのん」「日野下花帆」のいずれかの名前を持つカードを合わせて3枚の組み合わせでコストを支払うことができます。...

**Q:** 『{{live_start.png|ライブ開始時}}手札の「上原歩夢」と「澁谷かのん」と「日野下花帆」を、好きな組み合わせで合計3枚、控え室に置いてもよい：ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋３する。」を得る。』について。
「上原歩夢&澁谷かのん&日野下花帆」を1枚と（3人のいずれの名前も持たない）任意のカードを2枚の組み合わせでコストを支払うことはできます...
**A:** いいえ、できません。...

**Q:** 「◯◯＆△△」のように名前が「＆」で並んでいるカード名のカードは、「◯◯」「△△」それぞれの名前を持ちますか？（例：「上原歩夢＆澁谷かのん＆日野下花帆」は「上原歩夢」「澁谷かのん」「日野下花帆」それぞれの名前を持ちますか？）...
**A:** はい、それぞれの名前を持ちます。...

---

## PL!N-bp1-001-R: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp1-001-P: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp1-002-R＋: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, ENERGY=2
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ACTIVATED

### FAQ
**Q:** 『{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。』について。
自分のメインデッキが3枚の時にこの能力を使用してデッキの上から3枚見ているとき、リフレッシュは行いますか？...
**A:** いいえ、リフレッシュは行いません。
デッキのカードのすべて見ていますが、それらはデッキから移動していないため、リフレッシュは行いません。
見たカード全てを控え室に置いた場合、リフレッシュを行います。...

**Q:** 『{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。』について。
メンバーカードがあるエリアに登場させることはできますか？...
**A:** はい、できます。
その場合、指定したエリアに置かれているメンバーカードは控え室に置かれます。
ただし、このターンに登場しているメンバーのいるエリアを指定することはできません。...

**Q:** 『{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。』について。
この能力で登場したメンバーを対象にこのターン手札のメンバーとバトンタッチはできますか？...
**A:** いいえ、できません。登場したターン中はバトンタッチはできません。登場した次のターン以降はバトンタッチができます。...

**Q:** 能力の効果でメンバーカードをステージに登場させる場合、能力のコストとは別に、手札から登場させる場合と同様にメンバーカードのコストを支払いますか？...
**A:** いいえ、支払いません。効果で登場する場合、メンバーカードのコストは支払いません。...

---

## PL!N-bp1-002-P: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, ENERGY=2
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ACTIVATED

### FAQ
**Q:** 『{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。』について。
メンバーカードがあるエリアに登場させることはできますか？...
**A:** はい、できます。
その場合、指定したエリアに置かれているメンバーカードは控え室に置かれます。
ただし、このターンに登場しているメンバーのいるエリアを指定することはできません。...

**Q:** 『{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。』について。
この能力で登場したメンバーを対象にこのターン手札のメンバーとバトンタッチはできますか？...
**A:** いいえ、できません。登場したターン中はバトンタッチはできません。登場した次のターン以降はバトンタッチができます。...

**Q:** 能力の効果でメンバーカードをステージに登場させる場合、能力のコストとは別に、手札から登場させる場合と同様にメンバーカードのコストを支払いますか？...
**A:** いいえ、支払いません。効果で登場する場合、メンバーカードのコストは支払いません。...

---

## PL!N-bp1-002-P＋: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, ENERGY=2
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ACTIVATED

### FAQ
**Q:** 『{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。』について。
メンバーカードがあるエリアに登場させることはできますか？...
**A:** はい、できます。
その場合、指定したエリアに置かれているメンバーカードは控え室に置かれます。
ただし、このターンに登場しているメンバーのいるエリアを指定することはできません。...

**Q:** 『{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。』について。
この能力で登場したメンバーを対象にこのターン手札のメンバーとバトンタッチはできますか？...
**A:** いいえ、できません。登場したターン中はバトンタッチはできません。登場した次のターン以降はバトンタッチができます。...

**Q:** 能力の効果でメンバーカードをステージに登場させる場合、能力のコストとは別に、手札から登場させる場合と同様にメンバーカードのコストを支払いますか？...
**A:** いいえ、支払いません。効果で登場する場合、メンバーカードのコストは支払いません。...

---

## PL!N-bp1-002-SEC: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, ENERGY=2
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ACTIVATED

### FAQ
**Q:** 『{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。』について。
メンバーカードがあるエリアに登場させることはできますか？...
**A:** はい、できます。
その場合、指定したエリアに置かれているメンバーカードは控え室に置かれます。
ただし、このターンに登場しているメンバーのいるエリアを指定することはできません。...

**Q:** 『{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：このカードを控え室からステージに登場させる。この能力は、このカードが控え室にある場合のみ起動できる。』について。
この能力で登場したメンバーを対象にこのターン手札のメンバーとバトンタッチはできますか？...
**A:** いいえ、できません。登場したターン中はバトンタッチはできません。登場した次のターン以降はバトンタッチができます。...

**Q:** 能力の効果でメンバーカードをステージに登場させる場合、能力のコストとは別に、手札から登場させる場合と同様にメンバーカードのコストを支払いますか？...
**A:** いいえ、支払いません。効果で登場する場合、メンバーカードのコストは支払いません。...

---

## PL!N-bp1-003-R＋: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp1-003-P: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp1-003-P＋: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp1-003-SEC: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp1-004-R: 朝香果林
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにほかの『虹ヶ咲』のメンバーがいる場合、エネルギーを1枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'STAGE'}
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT {'target': 'energy'}

---

## PL!N-bp1-004-P: 朝香果林
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにほかの『虹ヶ咲』のメンバーがいる場合、エネルギーを1枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'STAGE'}
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT {'target': 'energy'}

---

## PL!N-bp1-005-R: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp1-005-P: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp1-006-R＋: 近江彼方
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：このターン、自分のステージに『虹ヶ咲』のメンバーが登場している場合、エネルギーを2枚アクティブにする。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, DISCARD_ENERGY=1
  **Conditions:** TURN_1 {}, GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'DISCARD'}
  **Effect:** ENERGY_CHARGE (value=1)
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT {'target': 'energy'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：このターン、自分のステージに「虹ヶ咲」のメンバーが登場している場合、エネルギーを2枚アクティブにする。』について。
このターン中に登場したメンバーがこのカードだけの状況です。「自分のステージに「虹ヶ咲」のメンバーが登場している場合」の条件は満たしていますか？...
**A:** はい、条件を満たしています。...

---

## PL!N-bp1-006-P: 近江彼方
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：このターン、自分のステージに『虹ヶ咲』のメンバーが登場している場合、エネルギーを2枚アクティブにする。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, DISCARD_ENERGY=1
  **Conditions:** TURN_1 {}, GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'DISCARD'}
  **Effect:** ENERGY_CHARGE (value=1)
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT {'target': 'energy'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：このターン、自分のステージに「虹ヶ咲」のメンバーが登場している場合、エネルギーを2枚アクティブにする。』について。
このターン中に登場したメンバーがこのカードだけの状況です。「自分のステージに「虹ヶ咲」のメンバーが登場している場合」の条件は満たしていますか？...
**A:** はい、条件を満たしています。...

---

## PL!N-bp1-006-P＋: 近江彼方
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：このターン、自分のステージに『虹ヶ咲』のメンバーが登場している場合、エネルギーを2枚アクティブにする。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, DISCARD_ENERGY=1
  **Conditions:** TURN_1 {}, GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'DISCARD'}
  **Effect:** ENERGY_CHARGE (value=1)
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT {'target': 'energy'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：このターン、自分のステージに「虹ヶ咲」のメンバーが登場している場合、エネルギーを2枚アクティブにする。』について。
このターン中に登場したメンバーがこのカードだけの状況です。「自分のステージに「虹ヶ咲」のメンバーが登場している場合」の条件は満たしていますか？...
**A:** はい、条件を満たしています。...

---

## PL!N-bp1-006-SEC: 近江彼方
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：このターン、自分のステージに『虹ヶ咲』のメンバーが登場している場合、エネルギーを2枚アクティブにする。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, DISCARD_ENERGY=1
  **Conditions:** TURN_1 {}, GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'DISCARD'}
  **Effect:** ENERGY_CHARGE (value=1)
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT {'target': 'energy'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：このターン、自分のステージに「虹ヶ咲」のメンバーが登場している場合、エネルギーを2枚アクティブにする。』について。
このターン中に登場したメンバーがこのカードだけの状況です。「自分のステージに「虹ヶ咲」のメンバーが登場している場合」の条件は満たしていますか？...
**A:** はい、条件を満たしています。...

---

## PL!N-bp1-007-R: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp1-007-P: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp1-008-R: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のメンバーカードを1枚控え室に置く：自分の控え室から、これにより控え室に置いたメンバーカードより、コストの低いメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp1-008-P: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のメンバーカードを1枚控え室に置く：自分の控え室から、これにより控え室に置いたメンバーカードより、コストの低いメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp1-009-R: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを2枚控え室に置く。その後、自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

---

## PL!N-bp1-009-P: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを2枚控え室に置く。その後、自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

---

## PL!N-bp1-010-R: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp1-010-P: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp1-011-R: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：ライブカードが公開されるまで、自分のデッキの一番上のカードを公開し続ける。そのライブカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** REVEAL_CARDS (value=1) {'all': True}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard', 'all': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand', 'all': True}

### FAQ
**Q:** 『{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：ライブカードが公開されるまで、自分のデッキの一番上のカードを公開し続ける。そのライブカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。』について。
メインデッキにも控え室にもライブカードがない状態で、この能力を使った場合、どうなりますか？...
**A:** 効果や処理は実行可能な限り解決し、一部でも実行可能な場合はその一部を解決します。まったく解決できない場合は何も行いません。

この場合、メインデッキのカードをすべて公開してリフレッシュを行い、さらに新しいメインデッキのカードをすべて公開した時点で『ライブカードが公開されるまで、自分のデッキの一番上のカードを公開し続ける。』の解決を終了します。

続いて『そのライブカードを手札に加え、これにより公開...

**Q:** 『{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：ライブカードが公開されるまで、自分のデッキの一番上のカードを公開し続ける。そのライブカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。』について。
この能力の効果の解決中に、メインデッキのカードが無くなりました。「リフレッシュ」の処理はどうなりますか？...
**A:** 能力に効果によって公開しているカードを含めずに「リフレッシュ」をして控え室のカードを新たなメインデッキにします。その後、効果の解決を再開します。...

---

## PL!N-bp1-011-P: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：ライブカードが公開されるまで、自分のデッキの一番上のカードを公開し続ける。そのライブカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** REVEAL_CARDS (value=1) {'all': True}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard', 'all': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand', 'all': True}

### FAQ
**Q:** 『{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：ライブカードが公開されるまで、自分のデッキの一番上のカードを公開し続ける。そのライブカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。』について。
メインデッキにも控え室にもライブカードがない状態で、この能力を使った場合、どうなりますか？...
**A:** 効果や処理は実行可能な限り解決し、一部でも実行可能な場合はその一部を解決します。まったく解決できない場合は何も行いません。

この場合、メインデッキのカードをすべて公開してリフレッシュを行い、さらに新しいメインデッキのカードをすべて公開した時点で『ライブカードが公開されるまで、自分のデッキの一番上のカードを公開し続ける。』の解決を終了します。

続いて『そのライブカードを手札に加え、これにより公開...

**Q:** 『{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：ライブカードが公開されるまで、自分のデッキの一番上のカードを公開し続ける。そのライブカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。』について。
この能力の効果の解決中に、メインデッキのカードが無くなりました。「リフレッシュ」の処理はどうなりますか？...
**A:** 能力に効果によって公開しているカードを含めずに「リフレッシュ」をして控え室のカードを新たなメインデッキにします。その後、効果の解決を再開します。...

---

## PL!N-bp1-012-R＋: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のライブ中のカードが3枚以上あり、その中に『虹ヶ咲』のライブカードを1枚以上含む場合、{{icon_all.png|ハート}}{{icon_all.png|ハート}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_GROUP {'group': '虹ヶ咲', 'min': 1}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': '虹ヶ咲'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=3
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 「ライブ中のカード」とはどのようなカードですか？...
**A:** ライブカード置き場に表向きに置かれているライブカードです。...

---

## PL!N-bp1-012-P: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のライブ中のカードが3枚以上あり、その中に『虹ヶ咲』のライブカードを1枚以上含む場合、{{icon_all.png|ハート}}{{icon_all.png|ハート}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_GROUP {'group': '虹ヶ咲', 'min': 1}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': '虹ヶ咲'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=3
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 「ライブ中のカード」とはどのようなカードですか？...
**A:** ライブカード置き場に表向きに置かれているライブカードです。...

---

## PL!N-bp1-012-P＋: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のライブ中のカードが3枚以上あり、その中に『虹ヶ咲』のライブカードを1枚以上含む場合、{{icon_all.png|ハート}}{{icon_all.png|ハート}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_GROUP {'group': '虹ヶ咲', 'min': 1}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': '虹ヶ咲'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=3
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 「ライブ中のカード」とはどのようなカードですか？...
**A:** ライブカード置き場に表向きに置かれているライブカードです。...

---

## PL!N-bp1-012-SEC: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のライブ中のカードが3枚以上あり、その中に『虹ヶ咲』のライブカードを1枚以上含む場合、{{icon_all.png|ハート}}{{icon_all.png|ハート}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_GROUP {'group': '虹ヶ咲', 'min': 1}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': '虹ヶ咲'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=3
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 「ライブ中のカード」とはどのようなカードですか？...
**A:** ライブカード置き場に表向きに置かれているライブカードです。...

---

## PL!N-bp1-014-N: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp1-015-N: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp1-019-N: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp1-025-L: 虹色Passions！
Type: ライブ

### Original Ability Text
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

---

## PL!N-bp1-026-L: Poppin' Up!
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、エールにより公開された自分のカードの中から、『虹ヶ咲』のカードを1枚手札に加える。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'OPPONENT_HAND'}, LIFE_LEAD {'type': 'score'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_ZONE (value=1)

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

### FAQ
**Q:** 『ライブの合計スコアが相手より高い場合』について。
自分のライブカード置き場にライブカードがあり、相手のライブカード置き場にライブカードがない場合、この条件は満たしますか？...
**A:** はい、満たします。自分のライブカード置き場にライブカードがあり、相手のライブカード置き場にライブカードがない場合、自分のライブの合計スコアがいくつであっても、相手より合計スコアが高いものとして扱います。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!N-bp1-027-L: Solitude Rain
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいる『虹ヶ咲』のメンバーが持つ{{heart_01.png|heart01}}、{{heart_04.png|heart04}}、{{heart_05.png|heart05}}、{{heart_02.png|heart02}}、{{heart_03.png|heart03}}、{{heart_06.png|heart06}}のうち1色につき、このカードのスコアを＋１する。

(エールをすべて行った後、エールで出た{{icon_draw.png|ドロー}}1つにつき、カードを1枚引く。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにいる『虹ヶ咲』のメンバーが持つ{{heart_01.png|heart01}}、{{heart_04.png|heart04}}、{{heart_05.png|heart05}}、{{heart_02.png|heart02}}、{{heart_03.png|heart03}}、{{heart_06.png|heart06}}のう...
**A:** いいえ、扱えません。{{icon_all.png|ハート}}はライブの必要ハートの確認を行う時に任意の色として扱いますが、ライブ開始時には任意の色として扱いません。...

---

## PL!N-bp1-028-L: Butterfly
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分のステージに『虹ヶ咲』のメンバーがいる場合、このカードのスコアを＋１する。

(エールをすべて行った後、エールで出た{{icon_draw.png|ドロー}}1つにつき、カードを1枚引く。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'STAGE'}
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}

---

## PL!N-bp1-029-L: Eutopia
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のライブ中のカードが3枚以上ある場合、このカードのスコアを＋２する。

(エールをすべて行った後、エールで出た{{icon_draw.png|ドロー}}1つにつき、カードを1枚引く。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_STAGE {'min': 3}
  **Effect:** BOOST_SCORE (value=2)
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}

### FAQ
**Q:** 「ライブ中のカード」とはどのようなカードですか？...
**A:** ライブカード置き場に表向きに置かれているライブカードです。...

---

## PL!SP-bp1-001-R: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージにほかのメンバーがいない場合、自分はライブできない。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** RESTRICTION (value=1) {'type': 'live'}

### FAQ
**Q:** 『自分はライブできない』とはどのような状態ですか？...
**A:** 『ライブできない』状態のプレイヤーは、ライブカードセットフェイズでライブカード置き場に手札のカードを裏向きで置くことはできますが、パフォーマンスフェイズで表向きにしたカードの中にライブカードがあったとしても、そのライブカードを含めて控え室に置きます。
その結果、ライブカード置き場にライブカードが置かれていないため、ライブは行われません。（{{live_start.png|ライブ開始時}}の能力は使...

---

## PL!SP-bp1-001-P: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージにほかのメンバーがいない場合、自分はライブできない。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** RESTRICTION (value=1) {'type': 'live'}

### FAQ
**Q:** 『自分はライブできない』とはどのような状態ですか？...
**A:** 『ライブできない』状態のプレイヤーは、ライブカードセットフェイズでライブカード置き場に手札のカードを裏向きで置くことはできますが、パフォーマンスフェイズで表向きにしたカードの中にライブカードがあったとしても、そのライブカードを含めて控え室に置きます。
その結果、ライブカード置き場にライブカードが置かれていないため、ライブは行われません。（{{live_start.png|ライブ開始時}}の能力は使...

---

## PL!SP-bp1-002-R＋: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ステージの左サイドエリアに登場しているなら、カードを2枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Effect:** DRAW (value=2) → PLAYER

---

## PL!SP-bp1-002-P: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ステージの左サイドエリアに登場しているなら、カードを2枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Effect:** DRAW (value=2) → PLAYER

---

## PL!SP-bp1-002-P＋: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ステージの左サイドエリアに登場しているなら、カードを2枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Effect:** DRAW (value=2) → PLAYER

---

## PL!SP-bp1-002-SEC: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ステージの左サイドエリアに登場しているなら、カードを2枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Effect:** DRAW (value=2) → PLAYER

---

## PL!SP-bp1-003-R＋: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** TURN_1 {}
  **Effect:** REVEAL_CARDS (value=1) {'until': 'live_end'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True, 'until': 'live_end'}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
手札が「[LL-bp2-001-R＋]渡辺曜&鬼塚夏美&大沢瑠璃乃」を含めて5枚の時、「[LL-...
**A:** いいえ、得ません。
「[LL-bp2-001-R＋]渡辺曜&鬼塚夏美&大沢瑠璃乃」の『{{jyouji.png|常時}}手札にあるこのメンバーカードのコストは、このカード以外の自分の手札1枚につき、1少なくなる。』の能力によってコストが下がっているため、条件を満たさず「公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合」は満たしません。...

**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
この能力を使用したあと、このメンバーカードがステージから離れました。『{{jyouji.png|...
**A:** いいえ、できません。
{{kidou.png|起動}}能力の効果で{{jyouji.png|常時}}能力を得たこのメンバーカードがステージから離れることで、この{{jyouji.png|常時}}能力が無くなるため、合計スコアは＋１されません。...

---

## PL!SP-bp1-003-P: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** TURN_1 {}
  **Effect:** REVEAL_CARDS (value=1) {'until': 'live_end'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True, 'until': 'live_end'}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
手札が「[LL-bp2-001-R＋]渡辺曜&鬼塚夏美&大沢瑠璃乃」を含めて5枚の時、「[LL-...
**A:** いいえ、得ません。
「[LL-bp2-001-R＋]渡辺曜&鬼塚夏美&大沢瑠璃乃」の『{{jyouji.png|常時}}手札にあるこのメンバーカードのコストは、このカード以外の自分の手札1枚につき、1少なくなる。』の能力によってコストが下がっているため、条件を満たさず「公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合」は満たしません。...

**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
この能力を使用したあと、このメンバーカードがステージから離れました。『{{jyouji.png|...
**A:** いいえ、できません。
{{kidou.png|起動}}能力の効果で{{jyouji.png|常時}}能力を得たこのメンバーカードがステージから離れることで、この{{jyouji.png|常時}}能力が無くなるため、合計スコアは＋１されません。...

---

## PL!SP-bp1-003-P＋: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** TURN_1 {}
  **Effect:** REVEAL_CARDS (value=1) {'until': 'live_end'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True, 'until': 'live_end'}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
手札が「[LL-bp2-001-R＋]渡辺曜&鬼塚夏美&大沢瑠璃乃」を含めて5枚の時、「[LL-...
**A:** いいえ、得ません。
「[LL-bp2-001-R＋]渡辺曜&鬼塚夏美&大沢瑠璃乃」の『{{jyouji.png|常時}}手札にあるこのメンバーカードのコストは、このカード以外の自分の手札1枚につき、1少なくなる。』の能力によってコストが下がっているため、条件を満たさず「公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合」は満たしません。...

**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
この能力を使用したあと、このメンバーカードがステージから離れました。『{{jyouji.png|...
**A:** いいえ、できません。
{{kidou.png|起動}}能力の効果で{{jyouji.png|常時}}能力を得たこのメンバーカードがステージから離れることで、この{{jyouji.png|常時}}能力が無くなるため、合計スコアは＋１されません。...

---

## PL!SP-bp1-003-SEC: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** TURN_1 {}
  **Effect:** REVEAL_CARDS (value=1) {'until': 'live_end'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True, 'until': 'live_end'}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
手札が「[LL-bp2-001-R＋]渡辺曜&鬼塚夏美&大沢瑠璃乃」を含めて5枚の時、「[LL-...
**A:** いいえ、得ません。
「[LL-bp2-001-R＋]渡辺曜&鬼塚夏美&大沢瑠璃乃」の『{{jyouji.png|常時}}手札にあるこのメンバーカードのコストは、このカード以外の自分の手札1枚につき、1少なくなる。』の能力によってコストが下がっているため、条件を満たさず「公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合」は満たしません。...

**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
この能力を使用したあと、このメンバーカードがステージから離れました。『{{jyouji.png|...
**A:** いいえ、できません。
{{kidou.png|起動}}能力の効果で{{jyouji.png|常時}}能力を得たこのメンバーカードがステージから離れることで、この{{jyouji.png|常時}}能力が無くなるため、合計スコアは＋１されません。...

---

## PL!SP-bp1-004-R: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}ステージのセンターエリアにいる場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** IS_CENTER {}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!SP-bp1-004-P: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}ステージのセンターエリアにいる場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** IS_CENTER {}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!SP-bp1-005-R: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中から『Liella!』のカードを1枚まで公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Liella!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp1-005-P: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中から『Liella!』のカードを1枚まで公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Liella!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp1-006-R: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!SP-bp1-006-P: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!SP-bp1-007-R＋: 米女メイ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギーが11枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_DISCARD {'count': 11, 'zone': 'DISCARD'}, COUNT_ENERGY {'min': 11}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}
  **Effect:** ENERGY_CHARGE (value=1)

---

## PL!SP-bp1-007-P: 米女メイ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギーが11枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_DISCARD {'count': 11, 'zone': 'DISCARD'}, COUNT_ENERGY {'min': 11}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}
  **Effect:** ENERGY_CHARGE (value=1)

---

## PL!SP-bp1-007-P＋: 米女メイ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギーが11枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_DISCARD {'count': 11, 'zone': 'DISCARD'}, COUNT_ENERGY {'min': 11}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}
  **Effect:** ENERGY_CHARGE (value=1)

---

## PL!SP-bp1-007-SEC: 米女メイ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギーが11枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_DISCARD {'count': 11, 'zone': 'DISCARD'}, COUNT_ENERGY {'min': 11}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}
  **Effect:** ENERGY_CHARGE (value=1)

---

## PL!SP-bp1-008-R: 若菜四季
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引く。自分のステージに「米女メイ」がいる場合、さらにカードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** HAS_MEMBER {'name': '米女メイ', 'zone': 'STAGE'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!SP-bp1-008-P: 若菜四季
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引く。自分のステージに「米女メイ」がいる場合、さらにカードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** HAS_MEMBER {'name': '米女メイ', 'zone': 'STAGE'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!SP-bp1-009-R: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!SP-bp1-009-P: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!SP-bp1-010-R: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：自分のデッキの上からカードを5枚見る。その中から『Liella!』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Liella!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp1-010-P: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：自分のデッキの上からカードを5枚見る。その中から『Liella!』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Liella!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp1-011-R: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!SP-bp1-011-P: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!SP-bp1-012-N: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}支払ってもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!SP-bp1-021-N: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}

---

## PL!SP-bp1-023-L: START!! True dreams
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。

(エールで出た{{icon_score.png|スコア}}1つにつき、成功したライブのスコアの合計に1を加算する。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** LIFE_LEAD {'type': 'score'}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** META_RULE (value=0) {'type': 'score_rule'}

### FAQ
**Q:** 『ライブの合計スコアが相手より高い場合』について。
自分のライブカード置き場にライブカードがあり、相手のライブカード置き場にライブカードがない場合、この条件は満たしますか？...
**A:** はい、満たします。自分のライブカード置き場にライブカードがあり、相手のライブカード置き場にライブカードがない場合、自分のライブの合計スコアがいくつであっても、相手より合計スコアが高いものとして扱います。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!SP-bp1-024-L: Tiny Stars
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}ライブ終了時まで、自分のステージにいる「澁谷かのん」1人は{{heart_05.png|heart05}}{{icon_blade.png|ブレード}}を、「唐可可」1人は{{heart_01.png|heart01}}{{icon_blade.png|ブレード}}を得る。
{{live_success.png|ライブ成功時}}自分のステージに「澁谷かのん」と「唐可可」がいる場合、カードを1枚引く。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_NAMED {'target_name': '澁谷かのん', 'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=2) → MEMBER_NAMED {'target_name': '澁谷かのん', 'until': 'live_end'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** HAS_MEMBER {'name': '澁谷かのん', 'zone': 'STAGE'}, HAS_MEMBER {'name': '唐可可', 'zone': 'STAGE'}
  **Effect:** DRAW (value=1) → PLAYER

**Ability 3:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!SP-bp1-025-L: Starlight Prologue
Type: ライブ

### Original Ability Text
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

---

## PL!SP-bp1-026-L: 未来予報ハレルヤ！
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の、ステージと控え室に名前の異なる『Liella!』のメンバーが5人以上いる場合、このカードを使用するためのコストは{{heart_02.png|heart02}}{{heart_02.png|heart02}}{{heart_03.png|heart03}}{{heart_03.png|heart03}}{{heart_06.png|heart06}}{{heart_06.png|heart06}}になる。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_GROUP {'group': 'Liella!', 'min': 5, 'zone': 'DISCARD'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

### FAQ
**Q:** 『{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}1つ分多くなる。』について。
条件を満たすと必要ハートを変更するライブカードでライブを行った場合どうなりますか？...
**A:** 変更したハートに{{heart_00.png|heart0}}１つを加えたものが必要になります。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにいる名前の異なる『蓮ノ空』のメンバー1人につき、このカードのスコアを＋２する。』について。
ステージに「[LL-bp2-001]渡辺曜&鬼塚夏美&大沢瑠璃乃」など複数の名前を持つカードがある場合、どのように参照されますか？...
**A:** 例えば、『蓮ノ空』のメンバーのうち「大沢瑠璃乃」の名前を持つカードのように参照されます。...

**Q:** 『{{live_start.png|ライブ開始時}}自分の、ステージと控え室に名前の異なる『Liella!』のメンバーが5人以上いる場合、このカードを使用するための必要ハートは{{heart_02.png|heart02}}{{heart_02.png|heart02}}{{heart_03.png|heart03}}{{heart_03.png|heart03}}{{heart_06.png|h...
**A:** 例えば、『Liella!』のメンバーのうち「澁谷かのん」の名前を持つカードとして参照されます。...

**Q:** 『{{live_start.png|ライブ開始時}}自分の、ステージと控え室に名前の異なる『Liella!』のメンバーが5人以上いる場合、このカードを使用するための必要ハートは{{heart_02.png|heart02}}{{heart_02.png|heart02}}{{heart_03.png|heart03}}{{heart_03.png|heart03}}{{heart_06.png|h...
**A:** はい、条件を満たしています。...

---

## PL!SP-bp1-027-L: Sing！Shine！Smile！
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のエネルギーが12枚以上ある場合、このカードのスコアを＋１する。

(エールをすべて行った後、エールで出た{{icon_draw.png|ドロー}}1つにつき、カードを1枚引く。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_STAGE {'min': 12}, COUNT_ENERGY {'min': 12}
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}

---

## PL!HS-bp1-001-R: 日野下花帆
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}エネルギーを2枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

---

## PL!HS-bp1-001-P: 日野下花帆
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}エネルギーを2枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

---

## PL!HS-bp1-002-R: 村野さやか
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}、このメンバーをステージから控え室に置く：自分の控え室からコスト15以下の『蓮ノ空』のメンバーカードを1枚、このメンバーがいたエリアに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** SACRIFICE_SELF=0, ENERGY=2
  **Conditions:** COST_CHECK {'value': 15, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}

### FAQ
**Q:** 『{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}、このメンバーをステージから控え室に置く：自分の控え室からコスト15以下の「蓮ノ空」のメンバーカードを1枚、このメンバーがいたエリアに登場させる。』について。
このメンバーカードが登場したターンにこの能力を使用しても、このターンに登場したメンバーカードがエリアに置かれているため、効...
**A:** いいえ、効果でメンバーカードが登場します。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

**Q:** 能力の効果でメンバーカードをステージに登場させる場合、能力のコストとは別に、手札から登場させる場合と同様にメンバーカードのコストを支払いますか？...
**A:** いいえ、支払いません。効果で登場する場合、メンバーカードのコストは支払いません。...

---

## PL!HS-bp1-002-P: 村野さやか
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}、このメンバーをステージから控え室に置く：自分の控え室からコスト15以下の『蓮ノ空』のメンバーカードを1枚、このメンバーがいたエリアに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** SACRIFICE_SELF=0, ENERGY=2
  **Conditions:** COST_CHECK {'value': 15, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}

### FAQ
**Q:** 『{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}、このメンバーをステージから控え室に置く：自分の控え室からコスト15以下の「蓮ノ空」のメンバーカードを1枚、このメンバーがいたエリアに登場させる。』について。
このメンバーカードが登場したターンにこの能力を使用しても、このターンに登場したメンバーカードがエリアに置かれているため、効...
**A:** いいえ、効果でメンバーカードが登場します。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!HS-bp1-003-R＋: 乙宗 梢
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージのエリアすべてに『蓮ノ空』のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分の控え室から4コスト以下の『蓮ノ空』のメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '蓮ノ空', 'zone': 'STAGE'}
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': '蓮ノ空'}

### FAQ
**Q:** 『{{jyouji.png|常時}}自分のステージのエリアすべてに「蓮ノ空」のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
ステージに「[LL-bp1-001]上原歩夢&澁谷かのん&日野下花帆」がある場合、どのように参照されますか？...
**A:** 『蓮ノ空』のメンバーのうち「日野下花帆」の名前を持つカードとして参照されます。...

---

## PL!HS-bp1-003-P: 乙宗 梢
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージのエリアすべてに『蓮ノ空』のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分の控え室から4コスト以下の『蓮ノ空』のメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '蓮ノ空', 'zone': 'STAGE'}
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': '蓮ノ空'}

### FAQ
**Q:** 『{{jyouji.png|常時}}自分のステージのエリアすべてに「蓮ノ空」のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
ステージに「[LL-bp1-001]上原歩夢&澁谷かのん&日野下花帆」がある場合、どのように参照されますか？...
**A:** 『蓮ノ空』のメンバーのうち「日野下花帆」の名前を持つカードとして参照されます。...

---

## PL!HS-bp1-003-P＋: 乙宗 梢
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージのエリアすべてに『蓮ノ空』のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分の控え室から4コスト以下の『蓮ノ空』のメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '蓮ノ空', 'zone': 'STAGE'}
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': '蓮ノ空'}

### FAQ
**Q:** 『{{jyouji.png|常時}}自分のステージのエリアすべてに「蓮ノ空」のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
ステージに「[LL-bp1-001]上原歩夢&澁谷かのん&日野下花帆」がある場合、どのように参照されますか？...
**A:** 『蓮ノ空』のメンバーのうち「日野下花帆」の名前を持つカードとして参照されます。...

---

## PL!HS-bp1-003-SEC: 乙宗 梢
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージのエリアすべてに『蓮ノ空』のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分の控え室から4コスト以下の『蓮ノ空』のメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '蓮ノ空', 'zone': 'STAGE'}
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': '蓮ノ空'}

### FAQ
**Q:** 『{{jyouji.png|常時}}自分のステージのエリアすべてに「蓮ノ空」のメンバーが登場しており、かつ名前が異なる場合、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
ステージに「[LL-bp1-001]上原歩夢&澁谷かのん&日野下花帆」がある場合、どのように参照されますか？...
**A:** 『蓮ノ空』のメンバーのうち「日野下花帆」の名前を持つカードとして参照されます。...

---

## PL!HS-bp1-004-R＋: 夕霧綴理
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室から『蓮ノ空』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、自分のライブ中のカード1枚につき、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=3
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '蓮ノ空'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}

### FAQ
**Q:** 「ライブ中のカード」とはどのようなカードですか？...
**A:** ライブカード置き場に表向きに置かれているライブカードです。...

---

## PL!HS-bp1-004-P: 夕霧綴理
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室から『蓮ノ空』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、自分のライブ中のカード1枚につき、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=3
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '蓮ノ空'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}

### FAQ
**Q:** 「ライブ中のカード」とはどのようなカードですか？...
**A:** ライブカード置き場に表向きに置かれているライブカードです。...

---

## PL!HS-bp1-004-P＋: 夕霧綴理
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室から『蓮ノ空』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、自分のライブ中のカード1枚につき、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=3
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '蓮ノ空'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}

### FAQ
**Q:** 「ライブ中のカード」とはどのようなカードですか？...
**A:** ライブカード置き場に表向きに置かれているライブカードです。...

---

## PL!HS-bp1-004-SEC: 夕霧綴理
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室から『蓮ノ空』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、自分のライブ中のカード1枚につき、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=3
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '蓮ノ空'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}

### FAQ
**Q:** 「ライブ中のカード」とはどのようなカードですか？...
**A:** ライブカード置き場に表向きに置かれているライブカードです。...

---

## PL!HS-bp1-005-R: 大沢瑠璃乃
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を3枚まで控え室に置いてもよい：これにより置いた枚数分カードを引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=3) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=3) {'target': 'discard', 'from': 'hand'}

---

## PL!HS-bp1-005-P: 大沢瑠璃乃
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を3枚まで控え室に置いてもよい：これにより置いた枚数分カードを引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=3) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=3) {'target': 'discard', 'from': 'hand'}

---

## PL!HS-bp1-006-R＋: 藤島 慈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを2枚引き、手札を1枚控え室に置く。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-bp1-006-P: 藤島 慈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを2枚引き、手札を1枚控え室に置く。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-bp1-006-P＋: 藤島 慈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを2枚引き、手札を1枚控え室に置く。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-bp1-006-SEC: 藤島 慈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを2枚引き、手札を1枚控え室に置く。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-bp1-007-R: 百生 吟子
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!HS-bp1-007-P: 百生 吟子
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!HS-bp1-008-R: 徒町 小鈴
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚控え室に置く。それらがすべてメンバーカードの場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'メンバーカード', 'context': 'revealed'}
  **Effect:** SWAP_CARDS (value=3) {'target': 'discard', 'from': 'deck'}
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!HS-bp1-008-P: 徒町 小鈴
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚控え室に置く。それらがすべてメンバーカードの場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'メンバーカード', 'context': 'revealed'}
  **Effect:** SWAP_CARDS (value=3) {'target': 'discard', 'from': 'deck'}
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!HS-bp1-009-R: 安養寺 姫芽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中から『みらくらぱーく！』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'みらくらぱーく！'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'みらくらぱーく！'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

### FAQ
**Q:** 『{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中から『みらくらぱーく！』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。』について。
この能力の効果でライブカードの「[PL!HS-bp1-023]ド！ド！ド！」や「[PL!HS-PR-012]アイデンティティ」を手札に加えることはできますか？...
**A:** はい、できます。
「[PL!HS-bp1-023]ド！ド！ド！」や「[PL!HS-PR-012]アイデンティティ」は『みらくらぱーく！』のカードのため、この能力の効果で手札に加えることができます。...

---

## PL!HS-bp1-009-P: 安養寺 姫芽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中から『みらくらぱーく！』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'みらくらぱーく！'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'みらくらぱーく！'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

### FAQ
**Q:** 『{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中から『みらくらぱーく！』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。』について。
この能力の効果でライブカードの「[PL!HS-bp1-023]ド！ド！ド！」や「[PL!HS-PR-012]アイデンティティ」を手札に加えることはできますか？...
**A:** はい、できます。
「[PL!HS-bp1-023]ド！ド！ド！」や「[PL!HS-PR-012]アイデンティティ」は『みらくらぱーく！』のカードのため、この能力の効果で手札に加えることができます。...

---

## PL!HS-bp1-010-N: 日野下花帆
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!HS-bp1-011-N: 村野さやか
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中からライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!HS-bp1-014-N: 大沢瑠璃乃
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!HS-bp1-019-L: Dream Believers
Type: ライブ

### Original Ability Text
```
(エールで出た{{icon_score.png|スコア}}1つにつき、成功したライブのスコアの合計に1を加算する。)
```

### Parsed Abilities
⚠️ **PARSE FAILED** - No abilities extracted

---

## PL!HS-bp1-020-L: 365 Days
Type: ライブ

### Original Ability Text
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

---

## PL!HS-bp1-021-L: Holiday∞Holiday
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中から、『蓮ノ空』のライブカードを1枚手札に加える。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': '蓮ノ空'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_ZONE (value=1)

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!HS-bp1-022-L: AWOKE
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中に『蓮ノ空』のメンバーカードが10枚以上ある場合、このカードのスコアを＋１する。

(エールをすべて行った後、エールで出た{{icon_draw.png|ドロー}}1つにつき、カードを1枚引く。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_GROUP {'group': '蓮ノ空', 'min': 10}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にライブカードがないとき、それらのカードをすべて控え室に置いてもよい。これにより1枚以上のカードが控え室に置かれた場合、そのエールで得たブレードハートを失い、もう一度エールを行う。』
『{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中に『蓮ノ空』...
**A:** いいえ、2つ目の能力を使用する時点で公開されている、2回目のエールにより公開された自分のカードのみ参照します。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!HS-bp1-023-L: ド！ド！ド！
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高く、かつ自分のステージに『蓮ノ空』のメンバーがいる場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。

(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** GROUP_FILTER {'group': '蓮ノ空', 'zone': 'OPPONENT_STAGE'}, OPPONENT_HAS {}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!N-sd1-001-SD: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを5枚見る。その中から『虹ヶ咲』のライブカードを1枚まで公開して手札に加えてもよい。残りを控え室に置く。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、自分のステージにいるほかの『虹ヶ咲』のメンバーは{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=5)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': '虹ヶ咲'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-sd1-002-SD: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-sd1-003-SD: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-sd1-004-SD: 朝香果林
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-sd1-005-SD: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から『虹ヶ咲』のメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=2
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-sd1-006-SD: 近江彼方
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!N-sd1-007-SD: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=2
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-sd1-008-SD: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}エネルギーを2枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

---

## PL!N-sd1-009-SD: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}手札を1枚控え室に置く：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1, ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-sd1-010-SD: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを2枚引き、手札を1枚控え室に置く。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{heart_04.png|heart04}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-sd1-011-SD: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!N-sd1-013-SD: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-sd1-021-SD: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-sd1-022-SD: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-sd1-025-SD: Colorful Dreams! Colorful Smiles!
Type: ライブ

### Original Ability Text
```
(エールで出た{{icon_score.png|スコア}}1つにつき、成功したライブのスコアの合計に1を加算する。)
```

### Parsed Abilities
⚠️ **PARSE FAILED** - No abilities extracted

---

## PL!N-sd1-026-SD: 夢が僕らの太陽さ
Type: ライブ

### Original Ability Text
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

---

## PL!N-sd1-027-SD: Just Believe!!!
Type: ライブ

### Original Ability Text
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

---

## PL!N-sd1-028-SD: Dream with You
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーが持つ{{icon_blade.png|ブレード}}の合計が10以上の場合、このカードのスコアを＋１する。

(エールをすべて行った後、エールで出た{{icon_draw.png|ドロー}}1つにつき、カードを1枚引く。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにいるメンバーが持つブレードの合計が10以上の場合、このカードのスコアを＋１する。』について。
ブレードの合計が10以上で、エールによって公開される自分のカードの枚数が減る効果が有効なため、公開される枚数が9枚以下になる場合であっても、このカードのスコアを＋１することはできますか？...
**A:** はい、このカードのスコアを＋１します。...

---

## PL!SP-sd1-001-SD: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギー6枚につき、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=6) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_energy': True}

---

## PL!SP-sd1-002-SD: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札からコスト4以下の『Liella!』のメンバーカードを1枚ステージに登場させてもよい。
（この効果で既にメンバーがいるエリアにも登場できる。ただし、このターンにステージに登場したメンバーがいるエリアには登場できない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}

**Ability 2:**
  **Trigger:** ON_PLAY

**Ability 3:**
  **Trigger:** ON_PLAY

### FAQ
**Q:** 能力の効果でメンバーカードをステージに登場させる場合、能力のコストとは別に、手札から登場させる場合と同様にメンバーカードのコストを支払いますか？...
**A:** いいえ、支払いません。効果で登場する場合、メンバーカードのコストは支払いません。...

---

## PL!SP-sd1-003-SD: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を2枚控え室に置いてもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=2 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!SP-sd1-004-SD: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!SP-sd1-005-SD: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=3
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

---

## PL!SP-sd1-006-SD: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!SP-sd1-007-SD: 米女メイ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分の控え室から『Liella!』のメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'Liella!'}

---

## PL!SP-sd1-008-SD: 若菜四季
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}支払ってもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!SP-sd1-009-SD: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}支払ってもよい：自分のエネルギーが9枚以上ある場合、自分のデッキの上からカードを5枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=1 (optional)
  **Conditions:** COUNT_STAGE {'count': 9, 'zone': 'DECK'}, COUNT_ENERGY {'min': 9}
  **Effect:** LOOK_DECK (value=5)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!SP-sd1-011-SD: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

---

## PL!SP-sd1-014-SD: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}

---

## PL!SP-sd1-016-SD: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}

---

## PL!SP-sd1-017-SD: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}支払ってもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!SP-sd1-023-SD: WE WILL!!
Type: ライブ

### Original Ability Text
```
(エールで出た{{icon_score.png|スコア}}1つにつき、成功したライブのスコアの合計に1を加算する。)
```

### Parsed Abilities
⚠️ **PARSE FAILED** - No abilities extracted

---

## PL!SP-sd1-024-SD: シェキラ☆☆☆
Type: ライブ

### Original Ability Text
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

---

## PL!SP-sd1-025-SD: 未来は風のように
Type: ライブ

### Original Ability Text
```
(必要ハートを確認する時、エールで出た{{icon_b_all.png|ALLブレード}}は任意の色のハートとして扱う。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** META_RULE (value=0) → PLAYER {'type': 'heart_rule'}
  **Effect:** META_RULE (value=0) {'type': 'heart_rule'}

---

## PL!SP-sd1-026-SD: 私のSymphony 〜澁谷かのんVer.〜
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のエネルギーが9枚以上ある場合、このカードのスコアを＋１する。

(エールをすべて行った後、エールで出た{{icon_draw.png|ドロー}}1つにつき、カードを1枚引く。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_STAGE {'min': 9}, COUNT_ENERGY {'min': 9}
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}手札の「上原歩夢」と「澁谷かのん」と「日野下花帆」を、好きな組み合わせで合計3枚、控え室に置いてもよい：ライブ終了時まで、「常時ライブの合計スコアを＋３する。」を得る。』について。
控え室に置くカードとして「私のSymphony〜澁谷かのんVer.〜」を選択できますか？...
**A:** はい、カード名に「澁谷かのん」を含むため、選択できます。...

---

## PL!SP-pb1-001-R: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払わないかぎり、自分の手札を2枚控え室に置く。
{{live_success.png|ライブ成功時}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブの合計スコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=2, ENERGY=2
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** ENERGY=6 (optional)
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払わないかぎり、自分の手札を2枚控え室に置く。』について。
{{icon_energy.png|E}}{{icon_energy.png|E}}を支払わず、自分の手札が1枚以下の場合、どうなりますか？...
**A:** 効果や処理は実行可能な限り解決し、一部でも実行可能な場合はその一部を解決します。まったく解決できない場合は何も行いません。
手札が1枚の場合、その1枚を控え室に置きます。手札が0枚の場合、特に何も行いません。...

**Q:** 『{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払わないかぎり、自分の手札を2枚控え室に置く。』について。
アクティブ状態のエネルギーが1枚以下の場合、{{icon_energy.png|E}}{{icon_energy.png|E}}を支払うことはできますか？また、アクティブ状態のエネルギーが2枚以上の場合...
**A:** コストはすべて支払う必要があります。アクティブ状態のエネルギーが1枚以下の場合、{{icon_energy.png|E}}{{icon_energy.png|E}}を支払うことはできません。1枚だけ支払うということもできません。
コストを支払うかどうかは選択できます。{{icon_energy.png|E}}{{icon_energy.png|E}}を支払える状況であったとしても、支払わないことを...

**Q:** 『{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払わないかぎり、自分の手札を2枚控え室に置く。』について。
ライブを行わない場合、この自動能力は発動しないですか？...
**A:** はい、発動しません。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!SP-pb1-001-P＋: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払わないかぎり、自分の手札を2枚控え室に置く。
{{live_success.png|ライブ成功時}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブの合計スコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=2, ENERGY=2
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** ENERGY=6 (optional)
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払わないかぎり、自分の手札を2枚控え室に置く。』について。
{{icon_energy.png|E}}{{icon_energy.png|E}}を支払わず、自分の手札が1枚以下の場合、どうなりますか？...
**A:** 効果や処理は実行可能な限り解決し、一部でも実行可能な場合はその一部を解決します。まったく解決できない場合は何も行いません。
手札が1枚の場合、その1枚を控え室に置きます。手札が0枚の場合、特に何も行いません。...

**Q:** 『{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払わないかぎり、自分の手札を2枚控え室に置く。』について。
アクティブ状態のエネルギーが1枚以下の場合、{{icon_energy.png|E}}{{icon_energy.png|E}}を支払うことはできますか？また、アクティブ状態のエネルギーが2枚以上の場合...
**A:** コストはすべて支払う必要があります。アクティブ状態のエネルギーが1枚以下の場合、{{icon_energy.png|E}}{{icon_energy.png|E}}を支払うことはできません。1枚だけ支払うということもできません。
コストを支払うかどうかは選択できます。{{icon_energy.png|E}}{{icon_energy.png|E}}を支払える状況であったとしても、支払わないことを...

**Q:** 『{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払わないかぎり、自分の手札を2枚控え室に置く。』について。
ライブを行わない場合、この自動能力は発動しないですか？...
**A:** はい、発動しません。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!SP-pb1-002-R: 唐 可可
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のエネルギーが12枚以上ある場合、ライブの合計スコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_STAGE {'min': 12}, COUNT_ENERGY {'min': 12}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!SP-pb1-002-P＋: 唐 可可
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のエネルギーが12枚以上ある場合、ライブの合計スコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_STAGE {'min': 12}, COUNT_ENERGY {'min': 12}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!SP-pb1-003-R: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバーが『5yncri5e!』のみの場合、自分と対戦相手は、センターエリアのメンバーを左サイドエリアに、左サイドエリアのメンバーを右サイドエリアに、右サイドエリアのメンバーをセンターエリアに、それぞれ移動させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '5yncri5e!', 'zone': 'OPPONENT_RIGHT_STAGE'}, IS_CENTER {}
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-pb1-003-P＋: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバーが『5yncri5e!』のみの場合、自分と対戦相手は、センターエリアのメンバーを左サイドエリアに、左サイドエリアのメンバーを右サイドエリアに、右サイドエリアのメンバーをセンターエリアに、それぞれ移動させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '5yncri5e!', 'zone': 'OPPONENT_RIGHT_STAGE'}, IS_CENTER {}
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-pb1-004-R: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
{{live_success.png|ライブ成功時}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** ENERGY=3 (optional)
  **Effect:** DRAW (value=1) → PLAYER

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!SP-pb1-004-P＋: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
{{live_success.png|ライブ成功時}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** ENERGY=3 (optional)
  **Effect:** DRAW (value=1) → PLAYER

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!SP-pb1-005-R: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

---

## PL!SP-pb1-005-P＋: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

---

## PL!SP-pb1-006-R: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動するたび、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
(対戦相手のカードの効果でも発動する。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** MOVE_MEMBER (value=1) {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{jidou.png|自動}}このメンバーが登場か、エリアを移動するたび、ライブ終了時まで、ブレードブレードを得る。』について。
例えば、このメンバーカードが登場して、その後、このメンバーカードが別のエリアに移動した場合、この自動能力は合わせて2回発動しますか？...
**A:** はい、登場した時と移動した時の合わせて2回発動します。...

---

## PL!SP-pb1-006-P＋: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動するたび、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
(対戦相手のカードの効果でも発動する。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** MOVE_MEMBER (value=1) {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{jidou.png|自動}}このメンバーが登場か、エリアを移動するたび、ライブ終了時まで、ブレードブレードを得る。』について。
例えば、このメンバーカードが登場して、その後、このメンバーカードが別のエリアに移動した場合、この自動能力は合わせて2回発動しますか？...
**A:** はい、登場した時と移動した時の合わせて2回発動します。...

---

## PL!SP-pb1-007-R: 米女メイ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}エネルギーを2枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

---

## PL!SP-pb1-007-P＋: 米女メイ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}エネルギーを2枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

---

## PL!SP-pb1-008-R: 若菜四季
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引く。その後、登場したエリアとは別の自分のエリア1つを選ぶ。このメンバーをそのエリアに移動する。選んだエリアにメンバーがいる場合、そのメンバーは、このメンバーがいたエリアに移動させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-pb1-008-P＋: 若菜四季
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引く。その後、登場したエリアとは別の自分のエリア1つを選ぶ。このメンバーをそのエリアに移動する。選んだエリアにメンバーがいる場合、そのメンバーは、このメンバーがいたエリアに移動させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-pb1-009-R: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにほかの『5yncri5e!』のメンバーがいる場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '5yncri5e!', 'zone': 'STAGE'}
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!SP-pb1-009-P＋: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにほかの『5yncri5e!』のメンバーがいる場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '5yncri5e!', 'zone': 'STAGE'}
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!SP-pb1-010-R: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のエネルギーが10枚以上ある場合、ステージにいるこのメンバーのコストを＋４する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_STAGE {'count': 10, 'zone': 'STAGE'}, COUNT_ENERGY {'min': 10}
  **Effect:** BUFF_POWER (value=4)

---

## PL!SP-pb1-010-P＋: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のエネルギーが10枚以上ある場合、ステージにいるこのメンバーのコストを＋４する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_STAGE {'count': 10, 'zone': 'STAGE'}, COUNT_ENERGY {'min': 10}
  **Effect:** BUFF_POWER (value=4)

---

## PL!SP-pb1-011-R: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}「鬼塚冬毬」以外の『Liella!』のメンバー1人をステージから控え室に置いてもよい：自分の控え室から、これにより控え室に置いたメンバーカードを1枚、そのメンバーがいたエリアに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

### FAQ
**Q:** 『{{toujyou.png|登場}}「鬼塚冬毬」以外の『Liella!』のメンバー1人をステージから控え室に置いてもよい：自分の控え室から、これにより控え室に置いたメンバーカードを1枚、そのメンバーがいたエリアに登場させる。』について。
この能力のコストで控え室に置いたメンバーカードと同じカード名を持つ、控え室に置いたメンバーカード以外のメンバーカードを登場させることはできますか？...
**A:** いいえ、できません。
この能力の効果で登場させることができるのは、この能力のコストで控え室に置いたメンバーカードのみです。
なお、登場させるメンバーカードは新しいカードとして扱うため、ステージにいた時に適用されていた効果などは適用されていない状態で登場します。...

**Q:** 能力の効果でメンバーカードをステージに登場させる場合、能力のコストとは別に、手札から登場させる場合と同様にメンバーカードのコストを支払いますか？...
**A:** いいえ、支払いません。効果で登場する場合、メンバーカードのコストは支払いません。...

---

## PL!SP-pb1-011-P＋: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}「鬼塚冬毬」以外の『Liella!』のメンバー1人をステージから控え室に置いてもよい：自分の控え室から、これにより控え室に置いたメンバーカードを1枚、そのメンバーがいたエリアに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

### FAQ
**Q:** 『{{toujyou.png|登場}}「鬼塚冬毬」以外の『Liella!』のメンバー1人をステージから控え室に置いてもよい：自分の控え室から、これにより控え室に置いたメンバーカードを1枚、そのメンバーがいたエリアに登場させる。』について。
この能力のコストで控え室に置いたメンバーカードと同じカード名を持つ、控え室に置いたメンバーカード以外のメンバーカードを登場させることはできますか？...
**A:** いいえ、できません。
この能力の効果で登場させることができるのは、この能力のコストで控え室に置いたメンバーカードのみです。
なお、登場させるメンバーカードは新しいカードとして扱うため、ステージにいた時に適用されていた効果などは適用されていない状態で登場します。...

**Q:** 能力の効果でメンバーカードをステージに登場させる場合、能力のコストとは別に、手札から登場させる場合と同様にメンバーカードのコストを支払いますか？...
**A:** いいえ、支払いません。効果で登場する場合、メンバーカードのコストは支払いません。...

---

## PL!SP-pb1-015-N: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中から『CatChu!』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'CatChu!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'CatChu!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-pb1-016-N: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中から『KALEIDOSCORE』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'KALEIDOSCORE'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'KALEIDOSCORE'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-pb1-017-N: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中から『5yncri5e!』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': '5yncri5e!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': '5yncri5e!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-pb1-018-N: 米女メイ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!SP-pb1-020-N: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーがエリアを移動するたび、カードを1枚引く。
(対戦相手のカードの効果でも発動する。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-pb1-021-N: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!SP-pb1-023-L: ディストーション
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージに名前の異なる『CatChu!』のメンバーが2人以上いる場合、エネルギーを6枚までアクティブにする。その後、自分のエネルギーがすべてアクティブ状態の場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_GROUP {'group': 'CatChu!', 'min': 2, 'zone': 'STAGE'}
  **Effect:** ACTIVATE_MEMBER (value=6) → MEMBER_SELECT {'target': 'energy'}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}自分のステージに名前の異なる『CatChu!』のメンバーが2人以上いる場合、エネルギーを6枚までアクティブにする。その後、自分のエネルギーがすべてアクティブ状態の場合、このカードのスコアを＋１する。』について。
自分のウェイト状態のエネルギーが7枚ある状態で、この能力が2つ発動しました。1つ目の能力の効果を解決してもまだウェイト状態のエネルギーが...
**A:** いいえ、できません。
「自分のエネルギーがすべてアクティブ状態の場合」を満たしているのは2つ目の能力の効果を解決する時のみのため、スコアは＋２ではなく、＋１されます。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージに名前の異なる『CatChu!』のメンバーが2人以上いる場合、エネルギーを6枚までアクティブにする。その後、自分のエネルギーがすべてアクティブ状態の場合、このカードのスコアを＋１する。』について。
自分のエネルギーがすべてアクティブ状態で、自分のステージに名前の異なる『CatChu!』のメンバーが2人以上いません。この場合、このカー...
**A:** はい、できます。
自分のステージに名前の異なる『CatChu!』のメンバーが2人以上いない場合、「自分のエネルギーを6枚までアクティブにする。」の効果は解決しません。その後、「自分のエネルギーがすべてアクティブ状態の場合」の条件を満たしていることを確認して、「このカードのスコアを＋１する。」の効果を解決します。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージに名前の異なる『CatChu!』のメンバーが2人以上いる場合、エネルギーを6枚までアクティブにする。その後、自分のエネルギーがすべてアクティブ状態の場合、このカードのスコアを＋１する。』について。
この能力の効果を解決して、このカードのスコアを＋１しました。その後、エネルギーカードを何枚かウェイト状態にした場合、「自分のエネルギーが...
**A:** いいえ、無効にはなりません。
「自分のエネルギーがすべてアクティブ状態の場合」という条件は、この能力の効果を解決する時に確認し、それ以降は確認しません。...

---

## PL!SP-pb1-024-L: ニュートラル
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージに名前の異なる『KALEIDOSCORE』のメンバーが2人以上いる場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_GROUP {'group': 'KALEIDOSCORE', 'min': 2, 'zone': 'STAGE'}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!SP-pb1-025-L: Jellyfish
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいる、このターン中に登場、またはエリアを移動した『5yncri5e!』のメンバー1人につき、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}減らす。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** REDUCE_HEART_REQ (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}
  **Effect:** MOVE_MEMBER (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにいる、このターン中に登場、またはエリアを移動した『5yncri5e!』のメンバー1人につき、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}減らす。』について。
この自動能力の効果を解決する時点で、ステージにいる「このターンに登場、かつエリアを移動した『5yncri5e!』のメンバー」は2人分...
**A:** いいえ、2人分としては数えず、1人分として数えます。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにいる、このターン中に登場、またはエリアを移動した『5yncri5e!』のメンバー1人につき、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}減らす。』について。
この自動能力の効果を解決する時点で、ステージにいない「このターンに登場、またはエリアを移動した『5yncri5e!』のメンバー」は1...
**A:** いいえ、数えません。...

---

## PL!S-bp2-001-R: 高海千歌
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分の成功ライブカード置き場のカードが0枚で、かつ相手の成功ライブカード置き場にカードが1枚以上ある場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_SUCCESS_LIVE {'min': 1}, COUNT_STAGE {'count': 1, 'zone': 'OPPONENT_SUCCESS_LIVE'}, OPPONENT_HAS {}
  **Effect:** ADD_BLADES (value=1) → OPPONENT

---

## PL!S-bp2-001-P: 高海千歌
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分の成功ライブカード置き場のカードが0枚で、かつ相手の成功ライブカード置き場にカードが1枚以上ある場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_SUCCESS_LIVE {'min': 1}, COUNT_STAGE {'count': 1, 'zone': 'OPPONENT_SUCCESS_LIVE'}, OPPONENT_HAS {}
  **Effect:** ADD_BLADES (value=1) → OPPONENT

---

## PL!S-bp2-002-R: 桜内梨子
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、手札を1枚控え室に置いてもよい。そうした場合、自分の控え室から『Aqours』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'Aqours'}

---

## PL!S-bp2-002-P: 桜内梨子
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、手札を1枚控え室に置いてもよい。そうした場合、自分の控え室から『Aqours』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'Aqours'}

---

## PL!S-bp2-003-R: 松浦果南
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、ライブ終了時まで、［緑ハート］を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}
  **Effect:** CHEER_REVEAL (value=1) {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!S-bp2-003-P: 松浦果南
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、ライブ終了時まで、［緑ハート］を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}
  **Effect:** CHEER_REVEAL (value=1) {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!S-bp2-004-R: 黒澤ダイヤ
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードがないとき、それらのカードをすべて控え室に置いてもよい。これにより1枚以上のカードが控え室に置かれた場合、そのエールで得たブレードハートを失い、もう一度エールを行う。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}, COUNT_DISCARD {'count': 1, 'zone': 'DISCARD'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にライブカードがないとき、それらのカードをすべて控え室に置いてもよい。これにより1枚以上のカードが控え室に置かれた場合、そのエールで得たブレードハートを失い、もう一度エールを行う。』
『{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中に『蓮ノ空』...
**A:** いいえ、2つ目の能力を使用する時点で公開されている、2回目のエールにより公開された自分のカードのみ参照します。...

---

## PL!S-bp2-004-P: 黒澤ダイヤ
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードがないとき、それらのカードをすべて控え室に置いてもよい。これにより1枚以上のカードが控え室に置かれた場合、そのエールで得たブレードハートを失い、もう一度エールを行う。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}, COUNT_DISCARD {'count': 1, 'zone': 'DISCARD'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にライブカードがないとき、それらのカードをすべて控え室に置いてもよい。これにより1枚以上のカードが控え室に置かれた場合、そのエールで得たブレードハートを失い、もう一度エールを行う。』
『{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中に『蓮ノ空』...
**A:** いいえ、2つ目の能力を使用する時点で公開されている、2回目のエールにより公開された自分のカードのみ参照します。...

---

## PL!S-bp2-005-R＋: 渡辺 曜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを7枚見る。その中から{{heart_02.png|heart02}}か{{heart_04.png|heart04}}か{{heart_05.png|heart05}}を持つメンバーカードを3枚まで公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=7)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=3)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

### FAQ
**Q:** 『{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを7枚見る。その中から{{heart_02.png|heart02}}か{{heart_04.png|heart04}}か{{heart_05.png|heart05}}を持つメンバーカードを3枚まで公開して手札に加えてもよい。残りを控え室に置く。』について。
この能力で{{blade_heart02....
**A:** いいえ、加えられません。
基本ハートに{{heart_02.png|heart02}}か{{heart_04.png|heart04}}か{{heart_05.png|heart05}}をもつメンバーカードを手札に加えられます。{{blade_heart02.png|ハート}}と[]緑ブレードハートと{{blade_heart05.png|ハート}}は参照しません。...

---

## PL!S-bp2-005-P: 渡辺 曜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを7枚見る。その中から{{heart_02.png|heart02}}か{{heart_04.png|heart04}}か{{heart_05.png|heart05}}を持つメンバーカードを3枚まで公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=7)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=3)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

### FAQ
**Q:** 『{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを7枚見る。その中から{{heart_02.png|heart02}}か{{heart_04.png|heart04}}か{{heart_05.png|heart05}}を持つメンバーカードを3枚まで公開して手札に加えてもよい。残りを控え室に置く。』について。
この能力で{{blade_heart02....
**A:** いいえ、加えられません。
基本ハートに{{heart_02.png|heart02}}か{{heart_04.png|heart04}}か{{heart_05.png|heart05}}をもつメンバーカードを手札に加えられます。{{blade_heart02.png|ハート}}と[]緑ブレードハートと{{blade_heart05.png|ハート}}は参照しません。...

---

## PL!S-bp2-005-P＋: 渡辺 曜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを7枚見る。その中から{{heart_02.png|heart02}}か{{heart_04.png|heart04}}か{{heart_05.png|heart05}}を持つメンバーカードを3枚まで公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=7)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=3)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!S-bp2-005-SEC: 渡辺 曜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを7枚見る。その中から{{heart_02.png|heart02}}か{{heart_04.png|heart04}}か{{heart_05.png|heart05}}を持つメンバーカードを3枚まで公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=7)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=3)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

### FAQ
**Q:** 『{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを7枚見る。その中から{{heart_02.png|heart02}}か{{heart_04.png|heart04}}か{{heart_05.png|heart05}}を持つメンバーカードを3枚まで公開して手札に加えてもよい。残りを控え室に置く。』について。
この能力で{{blade_heart02....
**A:** いいえ、加えられません。
基本ハートに{{heart_02.png|heart02}}か{{heart_04.png|heart04}}か{{heart_05.png|heart05}}をもつメンバーカードを手札に加えられます。{{blade_heart02.png|ハート}}と[]緑ブレードハートと{{blade_heart05.png|ハート}}は参照しません。...

---

## PL!S-bp2-006-R: 津島善子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分の控え室から、コストの合計が4以下になるようにメンバーカードを2枚までステージに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=4 (optional)
  **Effect:** RECOVER_MEMBER (value=2) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}

---

## PL!S-bp2-006-P: 津島善子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分の控え室から、コストの合計が4以下になるようにメンバーカードを2枚までステージに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=4 (optional)
  **Effect:** RECOVER_MEMBER (value=2) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}

---

## PL!S-bp2-007-R＋: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分の手札が7枚以下の場合、カードを1枚引く。
{{live_start.png|ライブ開始時}}手札のライブカードを1枚公開し、デッキの一番下に置いてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}, COUNT_STAGE {'count': 1, 'zone': 'HAND'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** CHEER_REVEAL (value=1)

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** LOOK_DECK (value=2)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'bottom'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分の手札が7枚以下の場合、カードを1枚引く。』について。
自分の手札が7枚の状態でエールを行い、{{icon_draw.png|ドロー}}のブレードハートを持つライブカードが1枚公開されました。この能力の効果でカードを1枚引くことはできますか？...
**A:** いいえ、この能力の効果でカードを1枚引くことはできません。
発動した自動能力を使うのは、エールで公開された{{icon_draw.png|ドロー}}のブレードハートの効果を解決したあとです。
例の場合、まず{{icon_draw.png|ドロー}}のブレードハートの効果でカードを1枚引き、手札が8枚になります。その後、発動した自動能力を使い、効果を解決する時点で「自分の手札が7枚以下の場合」を満た...

---

## PL!S-bp2-007-P: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分の手札が7枚以下の場合、カードを1枚引く。
{{live_start.png|ライブ開始時}}手札のライブカードを1枚公開し、デッキの一番下に置いてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}, COUNT_STAGE {'count': 1, 'zone': 'HAND'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** CHEER_REVEAL (value=1)

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** LOOK_DECK (value=2)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'bottom'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分の手札が7枚以下の場合、カードを1枚引く。』について。
自分の手札が7枚の状態でエールを行い、{{icon_draw.png|ドロー}}のブレードハートを持つライブカードが1枚公開されました。この能力の効果でカードを1枚引くことはできますか？...
**A:** いいえ、この能力の効果でカードを1枚引くことはできません。
発動した自動能力を使うのは、エールで公開された{{icon_draw.png|ドロー}}のブレードハートの効果を解決したあとです。
例の場合、まず{{icon_draw.png|ドロー}}のブレードハートの効果でカードを1枚引き、手札が8枚になります。その後、発動した自動能力を使い、効果を解決する時点で「自分の手札が7枚以下の場合」を満た...

---

## PL!S-bp2-007-P＋: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分の手札が7枚以下の場合、カードを1枚引く。
{{live_start.png|ライブ開始時}}手札のライブカードを1枚公開し、デッキの一番下に置いてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}, COUNT_STAGE {'count': 1, 'zone': 'HAND'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** CHEER_REVEAL (value=1)

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** LOOK_DECK (value=2)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'bottom'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分の手札が7枚以下の場合、カードを1枚引く。』について。
自分の手札が7枚の状態でエールを行い、{{icon_draw.png|ドロー}}のブレードハートを持つライブカードが1枚公開されました。この能力の効果でカードを1枚引くことはできますか？...
**A:** いいえ、この能力の効果でカードを1枚引くことはできません。
発動した自動能力を使うのは、エールで公開された{{icon_draw.png|ドロー}}のブレードハートの効果を解決したあとです。
例の場合、まず{{icon_draw.png|ドロー}}のブレードハートの効果でカードを1枚引き、手札が8枚になります。その後、発動した自動能力を使い、効果を解決する時点で「自分の手札が7枚以下の場合」を満た...

---

## PL!S-bp2-007-SEC: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}［ターン1回］エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分の手札が7枚以下の場合、カードを1枚引く。
{{live_start.png|ライブ開始時}}手札のライブカードを1枚公開し、デッキの一番下に置いてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}, COUNT_STAGE {'count': 1, 'zone': 'HAND'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** CHEER_REVEAL (value=1)

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** LOOK_DECK (value=2)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'bottom'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分の手札が7枚以下の場合、カードを1枚引く。』について。
自分の手札が7枚の状態でエールを行い、{{icon_draw.png|ドロー}}のブレードハートを持つライブカードが1枚公開されました。この能力の効果でカードを1枚引くことはできますか？...
**A:** いいえ、この能力の効果でカードを1枚引くことはできません。
発動した自動能力を使うのは、エールで公開された{{icon_draw.png|ドロー}}のブレードハートの効果を解決したあとです。
例の場合、まず{{icon_draw.png|ドロー}}のブレードハートの効果でカードを1枚引き、手札が8枚になります。その後、発動した自動能力を使い、効果を解決する時点で「自分の手札が7枚以下の場合」を満た...

---

## PL!S-bp2-008-R＋: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3枚以上ある場合、代わりに合計スコアを＋２する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'bottom'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'Aqours', 'min': 1, 'zone': 'STAGE'}, COUNT_STAGE {'min': 3}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** BOOST_SCORE (value=2)
  **Effect:** REPLACE_EFFECT (value=2) {'replaces': 'score_boost'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-bp2-008-P: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3枚以上ある場合、代わりに合計スコアを＋２する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'bottom'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'Aqours', 'min': 1, 'zone': 'STAGE'}, COUNT_STAGE {'min': 3}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** BOOST_SCORE (value=2)
  **Effect:** REPLACE_EFFECT (value=2) {'replaces': 'score_boost'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-bp2-008-P＋: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3枚以上ある場合、代わりに合計スコアを＋２する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'bottom'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'Aqours', 'min': 1, 'zone': 'STAGE'}, COUNT_STAGE {'min': 3}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** BOOST_SCORE (value=2)
  **Effect:** REPLACE_EFFECT (value=2) {'replaces': 'score_boost'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-bp2-008-SEC: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からライブカードを1枚までデッキの一番下に置く。
{{jyouji.png|常時}}自分のステージのエリアすべてに『Aqours』のメンバーが登場しており、かつ名前が異なる場合、「{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上ある場合、ライブの合計スコアを＋１する。ライブカードが3枚以上ある場合、代わりに合計スコアを＋２する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'bottom'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'Aqours', 'min': 1, 'zone': 'STAGE'}, COUNT_STAGE {'min': 3}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** BOOST_SCORE (value=2)
  **Effect:** REPLACE_EFFECT (value=2) {'replaces': 'score_boost'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-bp2-009-R: 黒澤ルビィ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!S-bp2-009-P: 黒澤ルビィ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!S-bp2-010-N: 高海千歌
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを2枚引き、手札を2枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!S-bp2-016-N: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!S-bp2-021-L: 未体験HORIZON
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中から、ライブカードを1枚までデッキの一番下に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'bottom'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-bp2-022-L: 未熟DREAMER
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}このターン、自分のデッキがリフレッシュしていた場合、このカードのスコアを＋２する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** BOOST_SCORE (value=2)

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-bp2-023-L: MY舞☆TONIGHT
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のライブカード置き場に「MY舞☆TONIGHT」以外の『Aqours』のライブカードがある場合、ライブ終了時まで、自分のステージのメンバーは{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'LIVE_ZONE'}, NOT HAS_MEMBER {'name': 'MY舞☆TONIGHT', 'zone': 'LIVE_ZONE'}, HAS_LIVE_CARD {}
  **Effect:** ADD_BLADES (value=1) → MEMBER_NAMED {'target_name': 'MY舞☆TONIGHT', 'until': 'live_end'}

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}自分のライブカード置き場に「MY舞☆TONIGHT」以外の『Aqours』のライブカードがある場合、ライブ終了時まで、自分のステージのメンバーは{{icon_blade.png|ブレード}}を得る。』について。
{{icon_blade.png|ブレード}}を得るのは自分のステージのメンバーいずれか1人だけですか？...
**A:** いいえ、自分のステージのメンバー全員が{{icon_blade.png|ブレード}}を得ます。...

---

## PL!S-bp2-024-L: 君のこころは輝いてるかい？
Type: ライブ

### Original Ability Text
```
{{jyouji.png|常時}}このカードは成功ライブカード置き場に置くことができない。
{{live_success.png|ライブ成功時}}カードを2枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** RESTRICTION (value=1) {'type': 'placement'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

### FAQ
**Q:** 『{{jyouji.png|常時}}このカードは成功ライブカード置き場に置くことができない。』について。
この能力をもつライブカードを成功ライブカード置き場と入れ替える効果などで成功ライブカード置き場に置くことができますか？...
**A:** いいえ、できません。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-bp2-025-L: 青空Jumping Heart
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にカードが2枚以上ある場合、ライブ終了時まで、自分のステージにいるメンバー1人は、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_SUCCESS_LIVE {'min': 2}, COUNT_STAGE {'count': 2, 'zone': 'SUCCESS_LIVE'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!SP-bp2-001-R＋: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True, 'all': True}
  **Effect:** NEGATE_EFFECT (value=1) {'all': True}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'Liella!'}
  **Effect:** NEGATE_EFFECT (value=1)

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。』について。
すべての{{live_start.png|ライブ開始時}}能力が無効になっているメンバーを選んで、もう一...
**A:** いいえ、できません。
無効である能力がさらに無効にはならないため、「無効にした場合」の条件を満たしていません。...

---

## PL!SP-bp2-001-P: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True, 'all': True}
  **Effect:** NEGATE_EFFECT (value=1) {'all': True}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'Liella!'}
  **Effect:** NEGATE_EFFECT (value=1)

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。』について。
すべての{{live_start.png|ライブ開始時}}能力が無効になっているメンバーを選んで、もう一...
**A:** いいえ、できません。
無効である能力がさらに無効にはならないため、「無効にした場合」の条件を満たしていません。...

---

## PL!SP-bp2-001-P＋: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True, 'all': True}
  **Effect:** NEGATE_EFFECT (value=1) {'all': True}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'Liella!'}
  **Effect:** NEGATE_EFFECT (value=1)

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。』について。
すべての{{live_start.png|ライブ開始時}}能力が無効になっているメンバーを選んで、もう一...
**A:** いいえ、できません。
無効である能力がさらに無効にはならないため、「無効にした場合」の条件を満たしていません。...

---

## PL!SP-bp2-001-SEC: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True, 'all': True}
  **Effect:** NEGATE_EFFECT (value=1) {'all': True}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'Liella!'}
  **Effect:** NEGATE_EFFECT (value=1)

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{toujyou.png|登場}}自分のステージにいる『Liella!』のメンバー1人のすべての{{live_start.png|ライブ開始時}}能力を、ライブ終了時まで、無効にしてもよい。これにより無効にした場合、自分の控え室から『Liella!』のカードを1枚手札に加える。』について。
すべての{{live_start.png|ライブ開始時}}能力が無効になっているメンバーを選んで、もう一...
**A:** いいえ、できません。
無効である能力がさらに無効にはならないため、「無効にした場合」の条件を満たしていません。...

---

## PL!SP-bp2-002-R: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中からコスト11以上のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 11, 'comparison': 'GE'}
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp2-002-P: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを3枚見る。その中からコスト11以上のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 11, 'comparison': 'GE'}
  **Effect:** LOOK_DECK (value=3)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp2-003-R: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}このメンバーがエリアを移動したとき、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** MOVE_MEMBER (value=1)

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}このメンバーがエリアを移動したとき、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。』について。
この能力をもつカードがステージから控え室に移動したときも発動しますか？...
**A:** いいえ、発動しません。
ステージに登場しているこの能力をもつメンバーが左サイドエリア、センターエリア、右サイドエリアのいずれかのエリアに移動した時に発動する自動能力です。...

---

## PL!SP-bp2-003-P: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}このメンバーがエリアを移動したとき、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** MOVE_MEMBER (value=1)

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}このメンバーがエリアを移動したとき、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。』について。
この能力をもつカードがステージから控え室に移動したときも発動しますか？...
**A:** いいえ、発動しません。
ステージに登場しているこの能力をもつメンバーが左サイドエリア、センターエリア、右サイドエリアのいずれかのエリアに移動した時に発動する自動能力です。...

---

## PL!SP-bp2-004-R: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージにいるメンバーのうち、センターエリアにいるメンバーが最も大きいコストを持つ場合、{{heart_03.png|heart03}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** IS_CENTER {}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF

---

## PL!SP-bp2-004-P: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージにいるメンバーのうち、センターエリアにいるメンバーが最も大きいコストを持つ場合、{{heart_03.png|heart03}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** IS_CENTER {}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF

---

## PL!SP-bp2-005-R: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分のデッキの上からカードを7枚見る。その中から『Liella!』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Effect:** LOOK_DECK (value=7)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Liella!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp2-005-P: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分のデッキの上からカードを7枚見る。その中から『Liella!』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Effect:** LOOK_DECK (value=7)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Liella!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp2-006-R＋: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}バトンタッチして登場した場合、このバトンタッチで控え室に置かれた『Liella!』のメンバーカードを1枚手札に加える。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。
({{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** TURN_1 {}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。({{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。)』について。
この{{kidou.png|起動}}能力の効果で発動する{...
**A:** いいえ、控え室に置いたメンバーカードが持つ{{toujyou.png|登場}}能力として扱います。
（例）「[PL!SP-pb1-009]鬼塚夏美」の『{{toujyou.png|登場}}自分のステージにほかの『5yncri5e!』のメンバーがいる場合、カードを1枚引く。』を発動した場合、この能力を持つ「鬼塚夏美」のほかに自分のステージに『5yncri5e!』のメンバーがいる場合、カードを引きます...

---

## PL!SP-bp2-006-P: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}バトンタッチして登場した場合、このバトンタッチで控え室に置かれた『Liella!』のメンバーカードを1枚手札に加える。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。
({{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** TURN_1 {}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。({{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。)』について。
この{{kidou.png|起動}}能力の効果で発動する{...
**A:** いいえ、控え室に置いたメンバーカードが持つ{{toujyou.png|登場}}能力として扱います。
（例）「[PL!SP-pb1-009]鬼塚夏美」の『{{toujyou.png|登場}}自分のステージにほかの『5yncri5e!』のメンバーがいる場合、カードを1枚引く。』を発動した場合、この能力を持つ「鬼塚夏美」のほかに自分のステージに『5yncri5e!』のメンバーがいる場合、カードを引きます...

---

## PL!SP-bp2-006-P＋: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}バトンタッチして登場した場合、このバトンタッチで控え室に置かれた『Liella!』のメンバーカードを1枚手札に加える。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。
({{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** TURN_1 {}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。({{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。)』について。
この{{kidou.png|起動}}能力の効果で発動する{...
**A:** いいえ、控え室に置いたメンバーカードが持つ{{toujyou.png|登場}}能力として扱います。
（例）「[PL!SP-pb1-009]鬼塚夏美」の『{{toujyou.png|登場}}自分のステージにほかの『5yncri5e!』のメンバーがいる場合、カードを1枚引く。』を発動した場合、この能力を持つ「鬼塚夏美」のほかに自分のステージに『5yncri5e!』のメンバーがいる場合、カードを引きます...

---

## PL!SP-bp2-006-SEC: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}バトンタッチして登場した場合、このバトンタッチで控え室に置かれた『Liella!』のメンバーカードを1枚手札に加える。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。
({{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** TURN_1 {}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のコスト4以下の『Liella!』のメンバーカードを1枚控え室に置く：これにより控え室に置いたメンバーカードの{{toujyou.png|登場}}能力1つを発動させる。({{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。)』について。
この{{kidou.png|起動}}能力の効果で発動する{...
**A:** いいえ、控え室に置いたメンバーカードが持つ{{toujyou.png|登場}}能力として扱います。
（例）「[PL!SP-pb1-009]鬼塚夏美」の『{{toujyou.png|登場}}自分のステージにほかの『5yncri5e!』のメンバーがいる場合、カードを1枚引く。』を発動した場合、この能力を持つ「鬼塚夏美」のほかに自分のステージに『5yncri5e!』のメンバーがいる場合、カードを引きます...

---

## PL!SP-bp2-007-R: 米女メイ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中から『Liella!』のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Liella!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp2-007-P: 米女メイ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中から『Liella!』のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Liella!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp2-008-R: 若菜四季
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：このメンバーがいるエリアとは別の自分のエリア1つを選ぶ。このメンバーをそのエリアに移動する。選んだエリアにメンバーがいる場合、そのメンバーは、このメンバーがいたエリアに移動させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-bp2-008-P: 若菜四季
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：このメンバーがいるエリアとは別の自分のエリア1つを選ぶ。このメンバーをそのエリアに移動する。選んだエリアにメンバーがいる場合、そのメンバーは、このメンバーがいたエリアに移動させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-bp2-009-R＋: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}ライブ終了時まで、自分の手札2枚につき、{{icon_blade.png|ブレード}}を得る。
{{live_success.png|ライブ成功時}}カードを2枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}ライブ終了時まで、自分の手札2枚につき、{{icon_blade.png|ブレード}}を得る。』について。
この能力を使用して効果を解決したあと、手札の枚数が増減しました。この効果で得た{{icon_blade.png|ブレード}}の数も増減しますか？...
**A:** いいえ、増減しません。
この能力を使用して効果を解決する時点の手札の枚数を参照して、得られる{{icon_blade.png|ブレード}}の数は決まります。
この効果を解決したあとに手札の枚数が増減したとしても、この効果で得た{{icon_blade.png|ブレード}}の数は増減しません。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!SP-bp2-009-P: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}ライブ終了時まで、自分の手札2枚につき、{{icon_blade.png|ブレード}}を得る。
{{live_success.png|ライブ成功時}}カードを2枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}ライブ終了時まで、自分の手札2枚につき、{{icon_blade.png|ブレード}}を得る。』について。
この能力を使用して効果を解決したあと、手札の枚数が増減しました。この効果で得た{{icon_blade.png|ブレード}}の数も増減しますか？...
**A:** いいえ、増減しません。
この能力を使用して効果を解決する時点の手札の枚数を参照して、得られる{{icon_blade.png|ブレード}}の数は決まります。
この効果を解決したあとに手札の枚数が増減したとしても、この効果で得た{{icon_blade.png|ブレード}}の数は増減しません。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!SP-bp2-009-P＋: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}ライブ終了時まで、自分の手札2枚につき、{{icon_blade.png|ブレード}}を得る。
{{live_success.png|ライブ成功時}}カードを2枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}ライブ終了時まで、自分の手札2枚につき、{{icon_blade.png|ブレード}}を得る。』について。
この能力を使用して効果を解決したあと、手札の枚数が増減しました。この効果で得た{{icon_blade.png|ブレード}}の数も増減しますか？...
**A:** いいえ、増減しません。
この能力を使用して効果を解決する時点の手札の枚数を参照して、得られる{{icon_blade.png|ブレード}}の数は決まります。
この効果を解決したあとに手札の枚数が増減したとしても、この効果で得た{{icon_blade.png|ブレード}}の数は増減しません。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!SP-bp2-009-SEC: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}ライブ終了時まで、自分の手札2枚につき、{{icon_blade.png|ブレード}}を得る。
{{live_success.png|ライブ成功時}}カードを2枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}ライブ終了時まで、自分の手札2枚につき、{{icon_blade.png|ブレード}}を得る。』について。
この能力を使用して効果を解決したあと、手札の枚数が増減しました。この効果で得た{{icon_blade.png|ブレード}}の数も増減しますか？...
**A:** いいえ、増減しません。
この能力を使用して効果を解決する時点の手札の枚数を参照して、得られる{{icon_blade.png|ブレード}}の数は決まります。
この効果を解決したあとに手札の枚数が増減したとしても、この効果で得た{{icon_blade.png|ブレード}}の数は増減しません。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!SP-bp2-010-R＋: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。
{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Conditions:** NOT COUNT_STAGE {'count': 1, 'zone': 'STAGE'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True, 'until': 'live_end'}

### FAQ
**Q:** 『{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}1つ分多くなる。』について。
条件を満たすと必要ハートを変更するライブカードでライブを行った場合どうなりますか？...
**A:** 変更したハートに{{heart_00.png|heart0}}１つを加えたものが必要になります。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。』について。
この能力を持つ「[PL!SP-bp2-010]ウィーン・マルガレーテ」以外のメンバーもすべて「ウィーン・マルガレーテ」の場合、エールによって公開される自分のカードの枚数は減らないですか？...
**A:** いいえ、減ります。
「このメンバー以外のメンバー」には特に指定がないため、同じカードかどうかや同じカード名のカードかどうかに関わらず、この能力を持つメンバー以外のメンバーが1人以上いる場合、「自分のステージにこのメンバー以外のメンバーが1人以上いる場合」を満たすため、「ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る」が有効になります。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。』について。
自分のステージにいるメンバーの{{icon_blade.png|ブレード}}の総数が7つのときにこの能力の効果を解決しました。その後、何らかの理由で{{icon_blade.png|ブレード}}{{i...
**A:** いいえ、{{icon_blade.png|ブレード}}の総数は9つで、エールによって公開される自分のカードの枚数が1枚になります。
例の場合、「もともとの{{icon_blade.png|ブレード}}が7つ」の状態に「エールによって公開される自分のカードの枚数が8枚減る」「{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る」を適用し、{{icon_b...

**Q:** 『{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。』について。
自分のステージにこの能力を持つメンバーが2人いる場合、成功させるための必要ハートが{{heart_00.png|heart0}}{{heart_00.png|heart0}}多くなりますか？...
**A:** はい、そうなります。...

---

## PL!SP-bp2-010-P: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。
{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Conditions:** NOT COUNT_STAGE {'count': 1, 'zone': 'STAGE'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True, 'until': 'live_end'}

### FAQ
**Q:** 『{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}1つ分多くなる。』について。
条件を満たすと必要ハートを変更するライブカードでライブを行った場合どうなりますか？...
**A:** 変更したハートに{{heart_00.png|heart0}}１つを加えたものが必要になります。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。』について。
この能力を持つ「[PL!SP-bp2-010]ウィーン・マルガレーテ」以外のメンバーもすべて「ウィーン・マルガレーテ」の場合、エールによって公開される自分のカードの枚数は減らないですか？...
**A:** いいえ、減ります。
「このメンバー以外のメンバー」には特に指定がないため、同じカードかどうかや同じカード名のカードかどうかに関わらず、この能力を持つメンバー以外のメンバーが1人以上いる場合、「自分のステージにこのメンバー以外のメンバーが1人以上いる場合」を満たすため、「ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る」が有効になります。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。』について。
自分のステージにいるメンバーの{{icon_blade.png|ブレード}}の総数が7つのときにこの能力の効果を解決しました。その後、何らかの理由で{{icon_blade.png|ブレード}}{{i...
**A:** いいえ、{{icon_blade.png|ブレード}}の総数は9つで、エールによって公開される自分のカードの枚数が1枚になります。
例の場合、「もともとの{{icon_blade.png|ブレード}}が7つ」の状態に「エールによって公開される自分のカードの枚数が8枚減る」「{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る」を適用し、{{icon_b...

**Q:** 『{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。』について。
自分のステージにこの能力を持つメンバーが2人いる場合、成功させるための必要ハートが{{heart_00.png|heart0}}{{heart_00.png|heart0}}多くなりますか？...
**A:** はい、そうなります。...

---

## PL!SP-bp2-010-P＋: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。
{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Conditions:** NOT COUNT_STAGE {'count': 1, 'zone': 'STAGE'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True, 'until': 'live_end'}

### FAQ
**Q:** 『{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}1つ分多くなる。』について。
条件を満たすと必要ハートを変更するライブカードでライブを行った場合どうなりますか？...
**A:** 変更したハートに{{heart_00.png|heart0}}１つを加えたものが必要になります。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。』について。
この能力を持つ「[PL!SP-bp2-010]ウィーン・マルガレーテ」以外のメンバーもすべて「ウィーン・マルガレーテ」の場合、エールによって公開される自分のカードの枚数は減らないですか？...
**A:** いいえ、減ります。
「このメンバー以外のメンバー」には特に指定がないため、同じカードかどうかや同じカード名のカードかどうかに関わらず、この能力を持つメンバー以外のメンバーが1人以上いる場合、「自分のステージにこのメンバー以外のメンバーが1人以上いる場合」を満たすため、「ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る」が有効になります。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。』について。
自分のステージにいるメンバーの{{icon_blade.png|ブレード}}の総数が7つのときにこの能力の効果を解決しました。その後、何らかの理由で{{icon_blade.png|ブレード}}{{i...
**A:** いいえ、{{icon_blade.png|ブレード}}の総数は9つで、エールによって公開される自分のカードの枚数が1枚になります。
例の場合、「もともとの{{icon_blade.png|ブレード}}が7つ」の状態に「エールによって公開される自分のカードの枚数が8枚減る」「{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る」を適用し、{{icon_b...

**Q:** 『{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。』について。
自分のステージにこの能力を持つメンバーが2人いる場合、成功させるための必要ハートが{{heart_00.png|heart0}}{{heart_00.png|heart0}}多くなりますか？...
**A:** はい、そうなります。...

---

## PL!SP-bp2-010-SEC: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。
{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Conditions:** NOT COUNT_STAGE {'count': 1, 'zone': 'STAGE'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True, 'until': 'live_end'}

### FAQ
**Q:** 『{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}1つ分多くなる。』について。
条件を満たすと必要ハートを変更するライブカードでライブを行った場合どうなりますか？...
**A:** 変更したハートに{{heart_00.png|heart0}}１つを加えたものが必要になります。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。』について。
この能力を持つ「[PL!SP-bp2-010]ウィーン・マルガレーテ」以外のメンバーもすべて「ウィーン・マルガレーテ」の場合、エールによって公開される自分のカードの枚数は減らないですか？...
**A:** いいえ、減ります。
「このメンバー以外のメンバー」には特に指定がないため、同じカードかどうかや同じカード名のカードかどうかに関わらず、この能力を持つメンバー以外のメンバーが1人以上いる場合、「自分のステージにこのメンバー以外のメンバーが1人以上いる場合」を満たすため、「ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る」が有効になります。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにこのメンバー以外のメンバーが1人以上いる場合、ライブ終了時まで、エールによって公開される自分のカードの枚数が8枚減る。』について。
自分のステージにいるメンバーの{{icon_blade.png|ブレード}}の総数が7つのときにこの能力の効果を解決しました。その後、何らかの理由で{{icon_blade.png|ブレード}}{{i...
**A:** いいえ、{{icon_blade.png|ブレード}}の総数は9つで、エールによって公開される自分のカードの枚数が1枚になります。
例の場合、「もともとの{{icon_blade.png|ブレード}}が7つ」の状態に「エールによって公開される自分のカードの枚数が8枚減る」「{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る」を適用し、{{icon_b...

**Q:** 『{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}多くなる。』について。
自分のステージにこの能力を持つメンバーが2人いる場合、成功させるための必要ハートが{{heart_00.png|heart0}}{{heart_00.png|heart0}}多くなりますか？...
**A:** はい、そうなります。...

---

## PL!SP-bp2-011-R: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室にある、カード名の異なるライブカードを2枚選ぶ。そうした場合、相手はそれらのカードのうち1枚を選ぶ。これにより相手に選ばれたカードを自分の手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}

### FAQ
**Q:** 『{{toujyou.png|登場}}自分の控え室にある、カード名の異なるライブカードを2枚選ぶ。そうした場合、相手はそれらのカードのうち1枚を選ぶ。これにより相手に選ばれたカードを自分の手札に加える。』について。
ライブカードを1枚しか選べなかった場合、相手はその1枚を選んで、そのカードを自分の手札に加えることはできますか？...
**A:** いいえ、できません。
カード名の異なるライブカードを2枚選ばなかった場合、「そうした場合」を満たさないため、「相手はそれらのカードのうち1枚を選ぶ。これにより相手に選ばれたカードを自分の手札に加える。」の効果は解決しません。...

---

## PL!SP-bp2-011-P: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室にある、カード名の異なるライブカードを2枚選ぶ。そうした場合、相手はそれらのカードのうち1枚を選ぶ。これにより相手に選ばれたカードを自分の手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}

### FAQ
**Q:** 『{{toujyou.png|登場}}自分の控え室にある、カード名の異なるライブカードを2枚選ぶ。そうした場合、相手はそれらのカードのうち1枚を選ぶ。これにより相手に選ばれたカードを自分の手札に加える。』について。
ライブカードを1枚しか選べなかった場合、相手はその1枚を選んで、そのカードを自分の手札に加えることはできますか？...
**A:** いいえ、できません。
カード名の異なるライブカードを2枚選ばなかった場合、「そうした場合」を満たさないため、「相手はそれらのカードのうち1枚を選ぶ。これにより相手に選ばれたカードを自分の手札に加える。」の効果は解決しません。...

---

## PL!SP-bp2-013-N: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からカードを1枚までデッキの一番上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}

---

## PL!SP-bp2-014-N: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からカードを1枚までデッキの一番上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}

---

## PL!SP-bp2-015-N: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_06.png|heart06}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}
  **Effect:** CHEER_REVEAL (value=1) {'until': 'live_end'}
  **Effect:** ADD_BLADES (value=6) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_06.png|heart06}}を得る。』などについて。
ブレードがないなど何らかの理由でエールを行わなかった場合、この能力は発動しますか？...
**A:** いいえ、発動しません。...

**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_06.png|heart06}}を得る。』などについて。
{{icon_b_all.png|ALLブレード}}、{{icon_score.png|スコア}}、{{icon_draw.png|ドロー}}はブレードハート...
**A:** はい、含まれます。...

---

## PL!SP-bp2-018-N: 米女メイ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からカードを1枚までデッキの一番上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}

---

## PL!SP-bp2-019-N: 若菜四季
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!SP-bp2-020-N: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_02.png|heart02}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}
  **Effect:** CHEER_REVEAL (value=1) {'until': 'live_end'}
  **Effect:** ADD_BLADES (value=2) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_06.png|heart06}}を得る。』などについて。
ブレードがないなど何らかの理由でエールを行わなかった場合、この能力は発動しますか？...
**A:** いいえ、発動しません。...

**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_06.png|heart06}}を得る。』などについて。
{{icon_b_all.png|ALLブレード}}、{{icon_score.png|スコア}}、{{icon_draw.png|ドロー}}はブレードハート...
**A:** はい、含まれます。...

---

## PL!SP-bp2-021-N: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_03.png|heart03}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}
  **Effect:** CHEER_REVEAL (value=1) {'until': 'live_end'}
  **Effect:** ADD_BLADES (value=3) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_06.png|heart06}}を得る。』などについて。
ブレードがないなど何らかの理由でエールを行わなかった場合、この能力は発動しますか？...
**A:** いいえ、発動しません。...

**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより公開された自分のカードの中にブレードハートを持つカードがないとき、ライブ終了時まで、{{heart_06.png|heart06}}を得る。』などについて。
{{icon_b_all.png|ALLブレード}}、{{icon_score.png|スコア}}、{{icon_draw.png|ドロー}}はブレードハート...
**A:** はい、含まれます。...

---

## PL!SP-bp2-022-N: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!SP-bp2-023-L: Go!! リスタート
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場のカード枚数が相手より少ない場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_live': True}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!SP-bp2-024-L: ビタミンSUMMER！
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}自分の手札の枚数が相手より多い場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{live_success.png|ライブ成功時}}自分の手札の枚数が相手より多い場合、このカードのスコアを＋１する。』について。
{{icon_draw.png|ドロー}}によって手札の枚数が相手より多くなった場合、どうなりますか？...
**A:** {{live_success.png|ライブ成功時}}能力の効果はライブ勝敗判定フェイズで発動します。
そのため、ドローアイコンを解決したことで条件を満たし、{{live_success.png|ライブ成功時}}能力の効果を発動することができます。...

**Q:** 『{{live_success.png|ライブ成功時}}自分の手札の枚数が相手より多い場合、このカードのスコアを＋１する。』について。
この能力を使用して効果を解決したあと、手札の枚数が増減しました。この能力を持つカードのスコアも増減しますか？...
**A:** いいえ、増減しません。
この能力を使用して効果を解決する時点の手札の枚数を参照して、「このカードのスコアを＋１する」の効果が有効になるかどうかが決まります。この能力の効果を解決したあとに手札の枚数が増減したとしても、「このカードのスコアを＋１する」の効果が、有効から無効、または、無効から有効にはなりません。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!SP-bp2-025-L: Bubble Rise
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}自分のステージに「澁谷かのん」、「ウィーン・マルガレーテ」、「鬼塚冬毬」のうち、名前の異なるメンバーが2人以上いる場合、エールにより公開された自分のカードの中から、カードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_STAGE {'count': 2, 'zone': 'HAND'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_ZONE (value=1)

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!HS-bp2-001-R: 日野下花帆
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室からスコア3以下の『蓮ノ空』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '蓮ノ空'}

---

## PL!HS-bp2-001-P: 日野下花帆
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の控え室からスコア3以下の『蓮ノ空』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '蓮ノ空'}

---

## PL!HS-bp2-002-R＋: 村野さやか
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からコスト2以下のメンバーカードを2枚まで手札に加える。
{{jyouji.png|常時}}自分のステージに、このメンバーよりコストの大きいメンバーがいる場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 2, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'cost_max': 2}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!HS-bp2-002-P: 村野さやか
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からコスト2以下のメンバーカードを2枚まで手札に加える。
{{jyouji.png|常時}}自分のステージに、このメンバーよりコストの大きいメンバーがいる場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 2, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'cost_max': 2}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!HS-bp2-002-P＋: 村野さやか
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からコスト2以下のメンバーカードを2枚まで手札に加える。
{{jyouji.png|常時}}自分のステージに、このメンバーよりコストの大きいメンバーがいる場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 2, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'cost_max': 2}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!HS-bp2-002-SEC: 村野さやか
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からコスト2以下のメンバーカードを2枚まで手札に加える。
{{jyouji.png|常時}}自分のステージに、このメンバーよりコストの大きいメンバーがいる場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 2, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'cost_max': 2}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!HS-bp2-003-R: 乙宗 梢
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

---

## PL!HS-bp2-003-P: 乙宗 梢
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

---

## PL!HS-bp2-004-R: 夕霧綴理
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

---

## PL!HS-bp2-004-P: 夕霧綴理
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

---

## PL!HS-bp2-005-R＋: 大沢瑠璃乃
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、自分の控え室から『みらくらぱーく！』のカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：自分のステージのエリアすべてにメンバーが登場している場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** GROUP_FILTER {'group': 'みらくらぱーく！', 'zone': 'DISCARD'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'みらくらぱーく！'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-bp2-005-P: 大沢瑠璃乃
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、自分の控え室から『みらくらぱーく！』のカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：自分のステージのエリアすべてにメンバーが登場している場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** GROUP_FILTER {'group': 'みらくらぱーく！', 'zone': 'DISCARD'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'みらくらぱーく！'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-bp2-005-P＋: 大沢瑠璃乃
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、自分の控え室から『みらくらぱーく！』のカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：自分のステージのエリアすべてにメンバーが登場している場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** GROUP_FILTER {'group': 'みらくらぱーく！', 'zone': 'DISCARD'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'みらくらぱーく！'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-bp2-005-SEC: 大沢瑠璃乃
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のステージにほかのメンバーがいる場合、自分の控え室から『みらくらぱーく！』のカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：自分のステージのエリアすべてにメンバーが登場している場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** GROUP_FILTER {'group': 'みらくらぱーく！', 'zone': 'DISCARD'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'みらくらぱーく！'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!HS-bp2-006-R: 藤島 慈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバーを、それぞれ好きなエリアに移動させてもよい。
{{jyouji.png|常時}}自分のステージにいるほかの『みらくらぱーく！』のメンバー1人につき、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** MOVE_MEMBER (value=1)

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'per_member': True}

---

## PL!HS-bp2-006-P: 藤島 慈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバーを、それぞれ好きなエリアに移動させてもよい。
{{jyouji.png|常時}}自分のステージにいるほかの『みらくらぱーく！』のメンバー1人につき、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** MOVE_MEMBER (value=1)

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'per_member': True}

---

## PL!HS-bp2-007-R＋: 百生 吟子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーよりコストが低い『スリーズブーケ』のメンバーからバトンタッチして登場した場合、自分の控え室から『蓮ノ空』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：これにより控え室に置いたカードがメンバーカードの場合、控え室に置いたカードと同じ名前を持つメンバー1人は、ライブ終了時まで、{{heart_04.png|heart04}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'スリーズブーケ', 'zone': 'DISCARD'}, GROUP_FILTER {'group': '蓮ノ空', 'zone': 'DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'スリーズブーケ'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!HS-bp2-007-P: 百生 吟子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーよりコストが低い『スリーズブーケ』のメンバーからバトンタッチして登場した場合、自分の控え室から『蓮ノ空』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：これにより控え室に置いたカードがメンバーカードの場合、控え室に置いたカードと同じ名前を持つメンバー1人は、ライブ終了時まで、{{heart_04.png|heart04}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'スリーズブーケ', 'zone': 'DISCARD'}, GROUP_FILTER {'group': '蓮ノ空', 'zone': 'DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'スリーズブーケ'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!HS-bp2-007-P＋: 百生 吟子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーよりコストが低い『スリーズブーケ』のメンバーからバトンタッチして登場した場合、自分の控え室から『蓮ノ空』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：これにより控え室に置いたカードがメンバーカードの場合、控え室に置いたカードと同じ名前を持つメンバー1人は、ライブ終了時まで、{{heart_04.png|heart04}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'スリーズブーケ', 'zone': 'DISCARD'}, GROUP_FILTER {'group': '蓮ノ空', 'zone': 'DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'スリーズブーケ'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!HS-bp2-007-SEC: 百生 吟子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーよりコストが低い『スリーズブーケ』のメンバーからバトンタッチして登場した場合、自分の控え室から『蓮ノ空』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：これにより控え室に置いたカードがメンバーカードの場合、控え室に置いたカードと同じ名前を持つメンバー1人は、ライブ終了時まで、{{heart_04.png|heart04}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'スリーズブーケ', 'zone': 'DISCARD'}, GROUP_FILTER {'group': '蓮ノ空', 'zone': 'DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'スリーズブーケ'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!HS-bp2-008-R: 徒町 小鈴
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーよりコストが低い『DOLLCHESTRA』のメンバーからバトンタッチして登場した場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'DOLLCHESTRA'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!HS-bp2-008-P: 徒町 小鈴
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーよりコストが低い『DOLLCHESTRA』のメンバーからバトンタッチして登場した場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'DOLLCHESTRA'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!HS-bp2-009-R: 安養寺 姫芽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}支払ってもよい：このメンバーよりコストが低い『みらくらぱーく！』のメンバーからバトンタッチして登場した場合、ライブ終了時まで、{{heart_01.png|heart01}}{{heart_01.png|heart01}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=1 (optional)
  **Conditions:** GROUP_FILTER {'group': 'みらくらぱーく！'}
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!HS-bp2-009-P: 安養寺 姫芽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}支払ってもよい：このメンバーよりコストが低い『みらくらぱーく！』のメンバーからバトンタッチして登場した場合、ライブ終了時まで、{{heart_01.png|heart01}}{{heart_01.png|heart01}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=1 (optional)
  **Conditions:** GROUP_FILTER {'group': 'みらくらぱーく！'}
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!HS-bp2-010-N: 日野下花帆
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中からメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!HS-bp2-011-N: 村野さやか
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}デッキの上からカードを5枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=5) {'target': 'discard', 'from': 'deck'}

---

## PL!HS-bp2-012-N: 乙宗 梢
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、自分のデッキの上からカードを5枚見る。その中からメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Effect:** LOOK_DECK (value=5)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!HS-bp2-013-N: 夕霧綴理
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、自分のデッキの上からカードを5枚見る。その中からライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Effect:** LOOK_DECK (value=5)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!HS-bp2-014-N: 大沢瑠璃乃
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを1枚引く。ライブ終了時まで、自分はライブできない。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** RESTRICTION (value=1) {'type': 'live'}

### FAQ
**Q:** 『自分はライブできない』とはどのような状態ですか？...
**A:** 『ライブできない』状態のプレイヤーは、ライブカードセットフェイズでライブカード置き場に手札のカードを裏向きで置くことはできますが、パフォーマンスフェイズで表向きにしたカードの中にライブカードがあったとしても、そのライブカードを含めて控え室に置きます。
その結果、ライブカード置き場にライブカードが置かれていないため、ライブは行われません。（{{live_start.png|ライブ開始時}}の能力は使...

---

## PL!HS-bp2-015-N: 藤島 慈
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーがステージから控え室に置かれたとき、カードを2枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER

---

## PL!HS-bp2-016-N: 百生 吟子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

---

## PL!HS-bp2-017-N: 徒町 小鈴
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室にカードが10枚以上ある場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_DISCARD {'count': 10, 'zone': 'DISCARD'}
  **Effect:** DRAW (value=10) → PLAYER

---

## PL!HS-bp2-018-N: 安養寺 姫芽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のメインフェイズの場合、{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分の控え室からライブカードを1枚、表向きでライブカード置き場に置く。次のライブカードセットフェイズで自分がライブカード置き場に置けるカード枚数の上限が1枚減る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_live': True}

---

## PL!HS-bp2-019-L: Bloom the smile, Bloom the dream!
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージに『蓮ノ空』のメンバーがいる場合、このカードを成功させるための必要ハートは、{{heart_01.png|heart01}}{{heart_01.png|heart01}}{{heart_00.png|heart0}}か、{{heart_04.png|heart04}}{{heart_04.png|heart04}}{{heart_00.png|heart0}}か、{{heart_05.png|heart05}}{{heart_05.png|heart05}}{{heart_00.png|heart0}}のうち、選んだ1つにしてもよい。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': '蓮ノ空', 'zone': 'STAGE'}

### FAQ
**Q:** 『{{jyouji.png|常時}}相手のライブカード置き場にあるすべてのライブカードは、成功させるための必要ハートが{{heart_00.png|heart0}}1つ分多くなる。』について。
条件を満たすと必要ハートを変更するライブカードでライブを行った場合どうなりますか？...
**A:** 変更したハートに{{heart_00.png|heart0}}１つを加えたものが必要になります。...

---

## PL!HS-bp2-020-L: Link to the FUTURE
Type: ライブ

### Original Ability Text
```
{{jyouji.png|常時}}すべての領域にあるこのカードは『スリーズブーケ』、『DOLLCHESTRA』、『みらくらぱーく！』として扱う。
{{live_start.png|ライブ開始時}}自分のステージにいる名前の異なる『蓮ノ空』のメンバー1人につき、このカードのスコアを＋２する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}
  **Effect:** BOOST_SCORE (value=2)

---

## PL!HS-bp2-021-L: 眩耀夜行
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージに、このターン中にバトンタッチして登場した『蓮ノ空』のメンバーが2人以上いる場合、このカードを成功させるための必要ハートを{{heart_04.png|heart04}}減らす。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': '蓮ノ空', 'min': 2, 'zone': 'STAGE'}
  **Effect:** REDUCE_HEART_REQ (value=1) → PLAYER
  **Effect:** BATON_TOUCH_MOD (value=2)

---

## PL!HS-bp2-022-L: アオクハルカ
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の控え室に『スリーズブーケ』のライブカードが3枚以上ある場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_GROUP {'group': 'スリーズブーケ', 'min': 3, 'zone': 'DISCARD'}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!HS-bp2-023-L: Mirage Voyage
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージに、このターン中にバトンタッチして登場した『蓮ノ空』のメンバーが2人以上いる場合、このカードを成功させるための必要ハートを{{heart_05.png|heart05}}減らす。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': '蓮ノ空', 'min': 2, 'zone': 'STAGE'}
  **Effect:** REDUCE_HEART_REQ (value=1) → PLAYER
  **Effect:** BATON_TOUCH_MOD (value=2)

---

## PL!HS-bp2-024-L: レディバグ
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージに「徒町小鈴」が登場しており、かつ「徒町小鈴」よりコストの大きい「村野さやか」が登場している場合、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}{{heart_00.png|heart0}}{{heart_00.png|heart0}}減らす。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** HAS_MEMBER {'name': '徒町小鈴', 'zone': 'STAGE'}, HAS_MEMBER {'name': '徒町小鈴', 'zone': 'STAGE'}, HAS_MEMBER {'name': '村野さやか', 'zone': 'STAGE'}
  **Effect:** REDUCE_HEART_REQ (value=3) → PLAYER
  **Effect:** REDUCE_COST (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}自分のステージに「徒町小鈴」が登場しており、かつ「徒町小鈴」よりコストの大きい「村野さやか」が登場している場合、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}{{heart_00.png|heart0}}{{heart_00.png|heart0}}減らす。』について。
「徒町小鈴」と「村野さやか」はこの能...
**A:** いいえ、この能力を使うときに自分のステージにいる必要はありますが、この能力を使うターンに登場している必要はありません。...

---

## PL!HS-bp2-025-L: ココン東西
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージに、このターン中にバトンタッチして登場した『蓮ノ空』のメンバーが2人以上いる場合、このカードを成功させるための必要ハートを{{heart_01.png|heart01}}減らす。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': '蓮ノ空', 'min': 2, 'zone': 'STAGE'}
  **Effect:** REDUCE_HEART_REQ (value=1) → PLAYER
  **Effect:** BATON_TOUCH_MOD (value=2)

---

## PL!HS-bp2-026-L: みらくりえーしょん
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージの右サイドエリアに「大沢瑠璃乃」が、左サイドエリアに「安養寺姫芽」が、センターエリアに「藤島慈」がそれぞれ登場している場合、このカードのスコアを＋２する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** HAS_MEMBER {'name': '大沢瑠璃乃', 'area': 'RIGHT_STAGE', 'zone': 'STAGE'}, HAS_MEMBER {'name': '安養寺姫芽', 'area': 'LEFT_STAGE', 'zone': 'STAGE'}, HAS_MEMBER {'name': '藤島慈', 'area': 'CENTER_STAGE', 'zone': 'STAGE'}
  **Effect:** BOOST_SCORE (value=2)

---

## LL-bp2-001-R＋: 渡辺 曜&鬼塚夏美&大沢瑠璃乃
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}手札にあるこのメンバーカードのコストは、このカード以外の自分の手札1枚につき、1少なくなる。
{{jyouji.png|常時}}このメンバーはバトンタッチで控え室に置けない。
{{live_start.png|ライブ開始時}}手札の「渡辺曜」と「鬼塚夏美」と「大沢瑠璃乃」を、好きな枚数控え室に置いてもよい：ライブ終了時まで、これによって控え室に置いた枚数1枚につき、{{icon_blade.png|ブレード}}を得る。
（手札のこのカードもこの効果で控え室に置ける。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** IMMUNITY (value=1)

**Ability 3:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

### FAQ
**Q:** 『{{jyouji.png|常時}}手札にあるこのメンバーカードのコストは、このカード以外の自分の手札1枚につき、1少なくなる。』について、
手札の枚数によって、LL-bp2-001-R+のコストは0になりますか？...
**A:** はい、なります。...

**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}手札にあるメンバーカードを好きな枚数公開する：公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
手札が「[LL-bp2-001-R＋]渡辺曜&鬼塚夏美&大沢瑠璃乃」を含めて5枚の時、「[LL-...
**A:** いいえ、得ません。
「[LL-bp2-001-R＋]渡辺曜&鬼塚夏美&大沢瑠璃乃」の『{{jyouji.png|常時}}手札にあるこのメンバーカードのコストは、このカード以外の自分の手札1枚につき、1少なくなる。』の能力によってコストが下がっているため、条件を満たさず「公開したカードのコストの合計が、10、20、30、40、50のいずれかの場合」は満たしません。...

**Q:** このカードはグループ名やユニット名を持っていますか？...
**A:** カードに記載されているグループ名は持っていますが、カードに記載されていないユニット名は持っていません。...

**Q:** 「◯◯＆△△」のように名前が「＆」で並んでいるカード名のカードは、「◯◯」「△△」それぞれの名前を持ちますか？（例：「上原歩夢＆澁谷かのん＆日野下花帆」は「上原歩夢」「澁谷かのん」「日野下花帆」それぞれの名前を持ちますか？）...
**A:** はい、それぞれの名前を持ちます。...

---

## PL!S-pb1-001-R: 高海千歌
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}相手の手札の枚数が自分より2枚以上多い場合、自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** OPPONENT_HAND_DIFF {'diff': 2}, COUNT_STAGE {'count': 2, 'zone': 'OPPONENT_DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → OPPONENT_HAND {'to': 'hand'}
  **Effect:** BUFF_POWER (value=1) → OPPONENT_HAND {'multiplier': True, 'per_live': True}

---

## PL!S-pb1-001-P＋: 高海千歌
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}相手の手札の枚数が自分より2枚以上多い場合、自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** OPPONENT_HAND_DIFF {'diff': 2}, COUNT_STAGE {'count': 2, 'zone': 'OPPONENT_DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → OPPONENT_HAND {'to': 'hand'}
  **Effect:** BUFF_POWER (value=1) → OPPONENT_HAND {'multiplier': True, 'per_live': True}

---

## PL!S-pb1-002-R: 桜内梨子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}相手は手札からライブカードを1枚控え室に置いてもよい。そうしなかった場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{toujyou.png|登場}}相手は手札からライブカードを1枚控え室に置いてもよい。そうしなかった場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
この能力を使用したターンにライブを行いませんでした。、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」は次のターンも得ている状態ですか？...
**A:** いいえ、ライブを行わない場合でもライブ勝敗判定フェイズの終了時に能力は消滅します。...

---

## PL!S-pb1-002-P＋: 桜内梨子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}相手は手札からライブカードを1枚控え室に置いてもよい。そうしなかった場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{toujyou.png|登場}}相手は手札からライブカードを1枚控え室に置いてもよい。そうしなかった場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
この能力を使用したターンにライブを行いませんでした。、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」は次のターンも得ている状態ですか？...
**A:** いいえ、ライブを行わない場合でもライブ勝敗判定フェイズの終了時に能力は消滅します。...

---

## PL!S-pb1-003-R: 松浦果南
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、このメンバーが元々持つハートはすべて{{heart_04.png|heart04}}になる。{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中から、ライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_ZONE (value=1)

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-pb1-003-P＋: 松浦果南
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、このメンバーが元々持つハートはすべて{{heart_04.png|heart04}}になる。{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中から、ライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_ZONE (value=1)

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-pb1-004-R: 黒澤ダイヤ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!S-pb1-004-P＋: 黒澤ダイヤ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』について。
控え室にライブカードがない状態で、この能力は使用できますか？...
**A:** はい、使用できます。
ライブカードが控え室に1枚以上ある場合は必ず手札に加える必要があります。...

**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!S-pb1-005-R: 渡辺 曜
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}相手のエネルギーが自分より多い場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → OPPONENT

---

## PL!S-pb1-005-P＋: 渡辺 曜
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}相手のエネルギーが自分より多い場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → OPPONENT

---

## PL!S-pb1-006-R: 津島善子
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のライブカードを1枚公開する：相手は手札を1枚控え室に置いてもよい。そうしなかった場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** TURN_1 {}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!S-pb1-006-P＋: 津島善子
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札のライブカードを1枚公開する：相手は手札を1枚控え室に置いてもよい。そうしなかった場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** TURN_1 {}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!S-pb1-007-R: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_STAGE {'count': 1, 'zone': 'DECK'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-pb1-007-P＋: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中にライブカードが1枚以上あるとき、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_STAGE {'count': 1, 'zone': 'DECK'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-pb1-008-R: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーのデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーのデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。』について。
相手が先行の場合、相手のライブ開始時に能力を使用できますか？...
**A:** いいえ、発動できません。
{{live_start.png|ライブ開始時}}能力の効果は自分のライブ開始時に発動します。...

---

## PL!S-pb1-008-P＋: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーのデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーのデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。』について。
相手が先行の場合、相手のライブ開始時に能力を使用できますか？...
**A:** いいえ、発動できません。
{{live_start.png|ライブ開始時}}能力の効果は自分のライブ開始時に発動します。...

---

## PL!S-pb1-009-R: 黒澤ルビィ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分と相手の成功ライブカード置き場にカードが合計3枚以上ある場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_SUCCESS_LIVE {'min': 3}, COUNT_STAGE {'count': 3, 'zone': 'OPPONENT_SUCCESS_LIVE'}, OPPONENT_HAS {}
  **Effect:** ADD_BLADES (value=1) → OPPONENT

---

## PL!S-pb1-009-P＋: 黒澤ルビィ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分と相手の成功ライブカード置き場にカードが合計3枚以上ある場合、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_SUCCESS_LIVE {'min': 3}, COUNT_STAGE {'count': 3, 'zone': 'OPPONENT_SUCCESS_LIVE'}, OPPONENT_HAS {}
  **Effect:** ADD_BLADES (value=1) → OPPONENT

---

## PL!S-pb1-013-N: 黒澤ダイヤ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中からハートに{{heart_04.png|heart04}}を2個以上持つメンバーカードか、必要ハートに{{heart_04.png|heart04}}を2以上含むライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=4)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!S-pb1-014-N: 渡辺 曜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中からハートに{{heart_02.png|heart02}}を2個以上持つメンバーカードか、必要ハートに{{heart_02.png|heart02}}を2以上含むライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=4)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!S-pb1-015-N: 津島善子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中からハートに{{heart_05.png|heart05}}を2個以上持つメンバーカードか、必要ハートに{{heart_05.png|heart05}}を2以上含むライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=4)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!S-pb1-016-N: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!S-pb1-017-N: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!S-pb1-018-N: 黒澤ルビィ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!S-pb1-019-L: 元気全開DAY！DAY！DAY！
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいる『Aqours』のメンバーが持つハートに、{{heart_02.png|heart02}}が合計6個以上ある場合、このカードの{{live_success.png|ライブ成功時}}能力を無効にする。{{live_success.png|ライブ成功時}}相手は、エネルギーデッキからエネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'STAGE'}
  **Effect:** NEGATE_EFFECT (value=1)

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-pb1-020-L: トリコリコPLEASE!!
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいる『Aqours』のメンバーが持つハートに、{{heart_04.png|heart04}}が合計10個以上ある場合、このカードのスコアを＋２する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'STAGE'}
  **Effect:** BOOST_SCORE (value=2)

---

## PL!S-pb1-021-L: Strawberry Trapper
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}自分のステージにいる『Aqours』のメンバーが持つハートに、{{heart_05.png|heart05}}が合計4個以上あり、このターン、相手が余剰のハートを持たずにライブを成功させていた場合、このカードのスコアを＋２する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'OPPONENT_STAGE'}
  **Effect:** BOOST_SCORE (value=2)

### FAQ
**Q:** 余剰ハートを持つとは、どのような状態ですか？...
**A:** ライブカードの必要ハートよりもステージのメンバーが持つ基本ハートとエールで獲得したブレードハートが多い状態です。
例えば、必要ハートが{{heart_02.png|heart02}}{{heart_02.png|heart02}}{{heart_01.png|heart01}}の時、基本ハートとエールで獲得したハートが{{heart_02.png|heart02}}{{heart_02.png|h...

**Q:** 『{{live_success.png|ライブ成功時}}自分のステージにいる『Aqours』のメンバーが持つハートに、{{heart_05.png|heart05}}が合計4個以上あり、このターン、相手が余剰のハートを持たずにライブを成功させていた場合、このカードのスコアを＋２する。』について。
自分が先行の場合、この能力が発動しますか？...
**A:** はい、発動します。
{{live_success.png|ライブ成功時}}能力の効果はライブ勝敗判定フェイズで発動するため、条件を満たせばする加算することができます。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-pb1-022-L: 逃走迷走メビウスループ
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}このターン、ライブに勝利するプレイヤーを決定するとき、自分と相手のライブの合計スコアが同じ場合、ライブ終了時まで、自分と相手は成功ライブカード置き場にカードを置くことができない。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** RESTRICTION (value=1) {'type': 'placement'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-pb1-022-L＋: 逃走迷走メビウスループ
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}このターン、ライブに勝利するプレイヤーを決定するとき、自分と相手のライブの合計スコアが同じ場合、ライブ終了時まで、自分と相手は成功ライブカード置き場にカードを置くことができない。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** RESTRICTION (value=1) {'type': 'placement'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-pb1-024-L: 僕らの走ってきた道は・・・
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}カードを2枚引き、手札を2枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!-bp3-001-R: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：カードを1枚引き、手札を1枚控え室に置く。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーを1人までアクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, DISCARD_HAND=1, DISCARD_HAND=1, SACRIFICE_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT

---

## PL!-bp3-001-P: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：カードを1枚引き、手札を1枚控え室に置く。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーを1人までアクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, DISCARD_HAND=1, DISCARD_HAND=1, SACRIFICE_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT

---

## PL!-bp3-002-R: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：相手のステージにいるコスト4以下のメンバーを2人までウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
{{jyouji.png|常時}}相手のステージにいるウェイト状態のメンバー1人につき、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** TAP_OPPONENT (value=2) → OPPONENT
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → OPPONENT {'multiplier': True, 'per_member': True}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

### FAQ
**Q:** 『{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：相手のステージにいるコスト4以下のメンバーを2人までウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）』について。
相手のステージにいるコスト4のメンバーが1人の時にこの能力を使用しました。相手のメンバーはウェイトにできますか？...
**A:** はい、可能です。
「～まで」の能力は指定された数字以内の数字を選択することができます。...

---

## PL!-bp3-002-P: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：相手のステージにいるコスト4以下のメンバーを2人までウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
{{jyouji.png|常時}}相手のステージにいるウェイト状態のメンバー1人につき、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** TAP_OPPONENT (value=2) → OPPONENT
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → OPPONENT {'multiplier': True, 'per_member': True}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

### FAQ
**Q:** 『{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：相手のステージにいるコスト4以下のメンバーを2人までウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）』について。
相手のステージにいるコスト4のメンバーが1人の時にこの能力を使用しました。相手のメンバーはウェイトにできますか？...
**A:** はい、可能です。
「～まで」の能力は指定された数字以内の数字を選択することができます。...

---

## PL!-bp3-003-R: 南ことり
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分の控え室から『μ's』のメンバーカードを1枚手札に加える。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

### FAQ
**Q:** 『{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分の控え室から『μ's』のメンバーカードを1枚手札に加える。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）』などについて。
自分の控え室にメンバーカードがない時にこの能力を使用できますか？...
**A:** はい、可能です。
ただし、手札に加えられるカードが控え室にある場合は必ず手札に加えます。...

---

## PL!-bp3-003-P: 南ことり
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分の控え室から『μ's』のメンバーカードを1枚手札に加える。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

### FAQ
**Q:** 『{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分の控え室から『μ's』のメンバーカードを1枚手札に加える。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）』などについて。
自分の控え室にメンバーカードがない時にこの能力を使用できますか？...
**A:** はい、可能です。
ただし、手札に加えられるカードが控え室にある場合は必ず手札に加えます。...

---

## PL!-bp3-004-R＋: 園田海未
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバー1人につき、カードを1枚引く。その後、手札を1枚控え室に置く。
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にカードがある場合、手札を1枚控え室に置いてもよい。そうした場合、自分の控え室から『μ's』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** GROUP_FILTER {'group': "μ's", 'zone': 'DISCARD'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}

### FAQ
**Q:** 『{{toujyou.png|登場}}自分のステージにいるメンバー1人につき、カードを1枚引く。その後、手札を1枚控え室に置く。』について。
この能力を使用する時、能力を発動しているステージに「[PL!-bp3-004-R＋]園田海未」のみの場合、カードを1枚引けますか？...
**A:** はい、可能です。
能力を発動メンバーも含めてステージにいるメンバーを数えます。...

---

## PL!-bp3-004-P: 園田海未
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバー1人につき、カードを1枚引く。その後、手札を1枚控え室に置く。
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にカードがある場合、手札を1枚控え室に置いてもよい。そうした場合、自分の控え室から『μ's』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** GROUP_FILTER {'group': "μ's", 'zone': 'DISCARD'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}

### FAQ
**Q:** 『{{toujyou.png|登場}}自分のステージにいるメンバー1人につき、カードを1枚引く。その後、手札を1枚控え室に置く。』について。
この能力を使用する時、能力を発動しているステージに「[PL!-bp3-004-R＋]園田海未」のみの場合、カードを1枚引けますか？...
**A:** はい、可能です。
能力を発動メンバーも含めてステージにいるメンバーを数えます。...

---

## PL!-bp3-004-P＋: 園田海未
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバー1人につき、カードを1枚引く。その後、手札を1枚控え室に置く。
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にカードがある場合、手札を1枚控え室に置いてもよい。そうした場合、自分の控え室から『μ's』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** GROUP_FILTER {'group': "μ's", 'zone': 'DISCARD'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}

### FAQ
**Q:** 『{{toujyou.png|登場}}自分のステージにいるメンバー1人につき、カードを1枚引く。その後、手札を1枚控え室に置く。』について。
この能力を使用する時、能力を発動しているステージに「[PL!-bp3-004-R＋]園田海未」のみの場合、カードを1枚引けますか？...
**A:** はい、可能です。
能力を発動メンバーも含めてステージにいるメンバーを数えます。...

---

## PL!-bp3-004-SEC: 園田海未
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバー1人につき、カードを1枚引く。その後、手札を1枚控え室に置く。
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にカードがある場合、手札を1枚控え室に置いてもよい。そうした場合、自分の控え室から『μ's』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** GROUP_FILTER {'group': "μ's", 'zone': 'DISCARD'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}

### FAQ
**Q:** 『{{toujyou.png|登場}}自分のステージにいるメンバー1人につき、カードを1枚引く。その後、手札を1枚控え室に置く。』について。
この能力を使用する時、能力を発動しているステージに「[PL!-bp3-004-R＋]園田海未」のみの場合、カードを1枚引けますか？...
**A:** はい、可能です。
能力を発動メンバーも含めてステージにいるメンバーを数えます。...

---

## PL!-bp3-005-R: 星空 凛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるすべてのメンバーをアクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT {'all': True}

---

## PL!-bp3-005-P: 星空 凛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるすべてのメンバーをアクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT {'all': True}

---

## PL!-bp3-006-R: 西木野真姫
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'per_live': True, 'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!-bp3-006-P: 西木野真姫
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'per_live': True, 'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!-bp3-007-R: 東條 希
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を2枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、1枚をデッキの上に置き、1枚を控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=2 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'deck'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}

---

## PL!-bp3-007-P: 東條 希
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を2枚控え室に置いてもよい：自分のデッキの上からカードを3枚見る。その中から1枚を手札に加え、1枚をデッキの上に置き、1枚を控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=2 (optional)
  **Effect:** LOOK_DECK (value=3)
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'deck'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}

---

## PL!-bp3-008-R＋: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：自分の控え室から『μ's』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}『μ's』のメンバー1人をウェイトにしてもよい：ライブ終了時まで、{{heart_03.png|heart03}}{{heart_03.png|heart03}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分の控え室から『μ's』のメンバーカードを1枚手札に加える。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）』などについて。
自分の控え室にメンバーカードがない時にこの能力を使用できますか？...
**A:** はい、可能です。
ただし、手札に加えられるカードが控え室にある場合は必ず手札に加えます。...

---

## PL!-bp3-008-P: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：自分の控え室から『μ's』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}『μ's』のメンバー1人をウェイトにしてもよい：ライブ終了時まで、{{heart_03.png|heart03}}{{heart_03.png|heart03}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分の控え室から『μ's』のメンバーカードを1枚手札に加える。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）』などについて。
自分の控え室にメンバーカードがない時にこの能力を使用できますか？...
**A:** はい、可能です。
ただし、手札に加えられるカードが控え室にある場合は必ず手札に加えます。...

---

## PL!-bp3-008-P＋: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：自分の控え室から『μ's』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}『μ's』のメンバー1人をウェイトにしてもよい：ライブ終了時まで、{{heart_03.png|heart03}}{{heart_03.png|heart03}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分の控え室から『μ's』のメンバーカードを1枚手札に加える。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）』などについて。
自分の控え室にメンバーカードがない時にこの能力を使用できますか？...
**A:** はい、可能です。
ただし、手札に加えられるカードが控え室にある場合は必ず手札に加えます。...

---

## PL!-bp3-008-SEC: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：自分の控え室から『μ's』のライブカードを1枚手札に加える。
{{live_start.png|ライブ開始時}}『μ's』のメンバー1人をウェイトにしてもよい：ライブ終了時まで、{{heart_03.png|heart03}}{{heart_03.png|heart03}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分の控え室から『μ's』のメンバーカードを1枚手札に加える。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）』などについて。
自分の控え室にメンバーカードがない時にこの能力を使用できますか？...
**A:** はい、可能です。
ただし、手札に加えられるカードが控え室にある場合は必ず手札に加えます。...

---

## PL!-bp3-009-R＋: 矢澤にこ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにコスト13以上のメンバーがいる場合、カードを1枚引く。
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 13, 'comparison': 'GE'}
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!-bp3-009-P: 矢澤にこ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにコスト13以上のメンバーがいる場合、カードを1枚引く。
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 13, 'comparison': 'GE'}
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!-bp3-009-P＋: 矢澤にこ
Type: メンバー

### Original Ability Text
```
"{{toujyou.png|登場}}自分のステージにコスト13以上のメンバーがいる場合、カードを1枚引く。
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。"
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 13, 'comparison': 'GE'}
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!-bp3-009-SEC: 矢澤にこ
Type: メンバー

### Original Ability Text
```
"{{toujyou.png|登場}}自分のステージにコスト13以上のメンバーがいる場合、カードを1枚引く。
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにする：{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、選んだハートを1つ得る。"
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 13, 'comparison': 'GE'}
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!-bp3-010-N: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを5枚見る。その中からライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=5)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!-bp3-011-N: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、選んだハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'multiplier': True, 'per_live': True, 'until': 'live_end'}

---

## PL!-bp3-012-N: 南ことり
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、選んだハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'multiplier': True, 'per_live': True, 'until': 'live_end'}

---

## PL!-bp3-013-N: 園田海未
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分の成功ライブカード置き場にあるカード1枚につき、選んだハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'multiplier': True, 'per_live': True, 'until': 'live_end'}

---

## PL!-bp3-014-N: 星空 凛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

---

## PL!-bp3-017-N: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

---

## PL!-bp3-018-N: 矢澤にこ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

---

## PL!-bp3-019-L: 僕らのLIVE 君とのLIFE
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のライブ中の『μ's』のカードが2枚以上ある場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_GROUP {'group': "μ's", 'min': 2}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}自分のライブ中の『μ's』のカードが2枚以上ある場合、このカードのスコアを＋１する。』について。
この能力の「自分のライブ中の『μ's』のカードが2枚以上ある場合」を満たさず、このカードがスコア0の時、成功ライブカード置き場に置けますか？...
**A:** はい、可能です。
スコア０の場合でもライブに勝利すれば成功ライブカード置き場に置くことができます。...

---

## PL!-bp3-022-L: ユメノトビラ
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のデッキの上から、自分と相手のステージにいるメンバー1人につき、1枚公開する。それらの中にあるライブカード1枚につき、このカードのスコアを＋１する。その後、これにより公開したカードを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_live': True}
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!-bp3-023-L: ミはμ'sicのミ
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーが持つ{{icon_blade.png|ブレード}}の合計が10以上の場合、このカードを成功させるための必要ハートは{{heart_00.png|heart0}}{{heart_00.png|heart0}}少なくなる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** REDUCE_HEART_REQ (value=2) → PLAYER

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにいるメンバーが持つ{{icon_blade.png|ブレード}}の合計が10以上の場合、このカードを成功させるための必要ハートは{{heart_00.png|heart0}}{{heart_00.png|heart0}}少なくなる。』について。
この能力で自分のステージにいるウェイト状態のメンバーの{{icon_blade.png...
**A:** はい、含みます。...

---

## PL!-bp3-024-L: 夏色えがおで1,2,Jump!
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にカードがある場合、{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_06.png|heart06}}のうち、1つを選ぶ。ライブ終了時まで、自分のステージにいる『μ's』のメンバー1人は、選んだハートを1つ得る。
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にカードが2枚以上ある場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_SUCCESS_LIVE {'min': 2}, COUNT_STAGE {'count': 2, 'zone': 'SUCCESS_LIVE'}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!-bp3-025-L: タカラモノズ
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}このターン、自分が余剰ハートを持たない場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 余剰ハートを持つとは、どのような状態ですか？...
**A:** ライブカードの必要ハートよりもステージのメンバーが持つ基本ハートとエールで獲得したブレードハートが多い状態です。
例えば、必要ハートが{{heart_02.png|heart02}}{{heart_02.png|heart02}}{{heart_01.png|heart01}}の時、基本ハートとエールで獲得したハートが{{heart_02.png|heart02}}{{heart_02.png|h...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!-bp3-026-L: Oh,Love&Peace!
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を2枚控え室に置いてもよい：ライブ終了時まで、自分のステージにいるメンバー1人は、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
{{live_success.png|ライブ成功時}}自分のステージにいるメンバーが持つハートの総数が、相手のステージにいるメンバーが持つハートの総数より多い場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=2 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{live_success.png|ライブ成功時}}自分のステージにいるメンバーが持つハートの総数が、相手のステージにいるメンバーが持つハートの総数より多い場合、このカードのスコアを＋１する。』について、ハートの総数を数えるとき、能力によって得たハートも含みますか？...
**A:** はい、含みます。ただし、エールによって得たブレードハートは含みません。...

**Q:** 『{{live_success.png|ライブ成功時}}自分のステージにいるメンバーが持つハートの総数が、相手のステージにいるメンバーが持つハートの総数より多い場合、このカードのスコアを＋１する。』について。
自分のステージに、ハートの数が2,3,5のメンバーがいます。相手のステージには、ハートの数が3,6のメンバーがいます。このとき、ライブ成功時の効果は発動しますか？...
**A:** はい、発動します。
自分のステージのいるメンバーのハートの総数は10、相手のステージにいるメンバーのハートの総数は9となり、自分のほうが多いため発動します。...

**Q:** 『{{live_success.png|ライブ成功時}}自分のステージにいるメンバーが持つハートの総数が、相手のステージにいるメンバーが持つハートの総数より多い場合、このカードのスコアを＋１する。』について。
ハートの総数とはどのハートのことですか？...
**A:** メンバーが持つ基本ハートの数を、色を無視して数えた値のことです。
例えば、{{heart_03.png|heart03}}{{heart_03.png|heart03}}{{heart_03.png|heart03}}{{heart_01.png|heart01}}{{heart_06.png|heart06}}を持つメンバーの場合、そのメンバーのハートの数は5つとなります。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-bp3-001-R＋: 高海千歌
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** TURN_1 {}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）』について。
この能力で相手のメンバーをウェイトにして能力を...
**A:** いいえ、できません。...

**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）』について。
この能力でウェイトにしたメンバーがステージから...
**A:** いいえ、できません。
{{kidou.png|起動}}能力の効果で{{jyouji.png|常時}}能力を得たこのメンバーカードがステージから離れることで、この{{jyouji.png|常時}}能力が無くなるため、合計スコアは＋１されません。...

---

## PL!S-bp3-001-P: 高海千歌
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** TURN_1 {}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）』について。
この能力で相手のメンバーをウェイトにして能力を...
**A:** いいえ、できません。...

**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）』について。
この能力でウェイトにしたメンバーがステージから...
**A:** いいえ、できません。
{{kidou.png|起動}}能力の効果で{{jyouji.png|常時}}能力を得たこのメンバーカードがステージから離れることで、この{{jyouji.png|常時}}能力が無くなるため、合計スコアは＋１されません。...

---

## PL!S-bp3-001-P＋: 高海千歌
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** TURN_1 {}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）』について。
この能力で相手のメンバーをウェイトにして能力を...
**A:** いいえ、できません。...

**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）』について。
この能力でウェイトにしたメンバーがステージから...
**A:** いいえ、できません。
{{kidou.png|起動}}能力の効果で{{jyouji.png|常時}}能力を得たこのメンバーカードがステージから離れることで、この{{jyouji.png|常時}}能力が無くなるため、合計スコアは＋１されません。...

---

## PL!S-bp3-001-SEC: 高海千歌
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** TURN_1 {}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）』について。
この能力で相手のメンバーをウェイトにして能力を...
**A:** いいえ、できません。...

**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}メンバー1人をウェイトにする：ライブ終了時まで、これによってウェイト状態になったメンバーは、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。（この能力はセンターエリアに登場している場合のみ起動できる。）』について。
この能力でウェイトにしたメンバーがステージから...
**A:** いいえ、できません。
{{kidou.png|起動}}能力の効果で{{jyouji.png|常時}}能力を得たこのメンバーカードがステージから離れることで、この{{jyouji.png|常時}}能力が無くなるため、合計スコアは＋１されません。...

---

## PL!S-bp3-002-R: 桜内梨子
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、このカードを手札に加えてもよい。この能力は、このカードが自分のエールによって公開されている場合のみ発動する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** LIFE_LEAD {'type': 'score'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

---

## PL!S-bp3-002-P: 桜内梨子
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、このカードを手札に加えてもよい。この能力は、このカードが自分のエールによって公開されている場合のみ発動する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** LIFE_LEAD {'type': 'score'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

---

## PL!S-bp3-003-R＋: 松浦果南
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札のライブカードを1枚控え室に置いてもよい：カードを3枚引く。
{{live_start.png|ライブ開始時}}手札を2枚まで控え室に置いてもよい：ライブ終了時まで、これによって控え室に置いたカード1枚につき、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!S-bp3-003-P: 松浦果南
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札のライブカードを1枚控え室に置いてもよい：カードを3枚引く。
{{live_start.png|ライブ開始時}}手札を2枚まで控え室に置いてもよい：ライブ終了時まで、これによって控え室に置いたカード1枚につき、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!S-bp3-003-P＋: 松浦果南
Type: メンバー

### Original Ability Text
```
"{{toujyou.png|登場}}手札のライブカードを1枚控え室に置いてもよい：カードを3枚引く。
{{live_start.png|ライブ開始時}}手札を2枚まで控え室に置いてもよい：ライブ終了時まで、これによって控え室に置いたカード1枚につき、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。"
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!S-bp3-003-SEC: 松浦果南
Type: メンバー

### Original Ability Text
```
"{{toujyou.png|登場}}手札のライブカードを1枚控え室に置いてもよい：カードを3枚引く。
{{live_start.png|ライブ開始時}}手札を2枚まで控え室に置いてもよい：ライブ終了時まで、これによって控え室に置いたカード1枚につき、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。"
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!S-bp3-004-R: 黒澤ダイヤ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中からメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=4)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!S-bp3-004-P: 黒澤ダイヤ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中からメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=4)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!S-bp3-005-R: 渡辺 曜
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの枚数が、相手がエールによって公開したカードの枚数より少ない場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}

### FAQ
**Q:** 『{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの枚数が、相手がエールによって公開したカードの枚数より少ない場合、カードを1枚引く。』について。

相手がライブをしていないときどうなりますか？...
**A:** 相手がライブをしていない場合、エールにより公開されたカードが0枚のときと同じ扱いとなります。...

---

## PL!S-bp3-005-P: 渡辺 曜
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの枚数が、相手がエールによって公開したカードの枚数より少ない場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}

### FAQ
**Q:** 『{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの枚数が、相手がエールによって公開したカードの枚数より少ない場合、カードを1枚引く。』について。

相手がライブをしていないときどうなりますか？...
**A:** 相手がライブをしていない場合、エールにより公開されたカードが0枚のときと同じ扱いとなります。...

---

## PL!S-bp3-006-R＋: 津島善子
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：このメンバー以外の『Aqours』のメンバー1人を自分のステージから控え室に置く。そうした場合、自分の控え室から、そのメンバーのコストに2を足した数に等しいコストの『Aqours』のメンバーカードを1枚、そのメンバーがいたエリアに登場させる。（この能力はセンターエリアに登場している場合のみ起動できる。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, DISCARD_HAND=1, DISCARD_HAND=1, SACRIFICE_SELF=0
  **Conditions:** NOT TURN_1 {}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'DISCARD'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}

### FAQ
**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：このメンバー以外の『Aqours』のメンバー1人を自分のステージから控え室に置く。そうした場合、自分の控え室から、そのメンバーのコストに2を足した数に等しいコストの『Aqours』のメンバーカードを1枚、そのメンバーがいたエリアに登場させ...
**A:** 自分の控え室からメンバーカードを登場させず、そのままこの能力の処理を終わります。...

---

## PL!S-bp3-006-P: 津島善子
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：このメンバー以外の『Aqours』のメンバー1人を自分のステージから控え室に置く。そうした場合、自分の控え室から、そのメンバーのコストに2を足した数に等しいコストの『Aqours』のメンバーカードを1枚、そのメンバーがいたエリアに登場させる。（この能力はセンターエリアに登場している場合のみ起動できる。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, DISCARD_HAND=1, DISCARD_HAND=1, SACRIFICE_SELF=0
  **Conditions:** NOT TURN_1 {}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'DISCARD'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}

### FAQ
**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：このメンバー以外の『Aqours』のメンバー1人を自分のステージから控え室に置く。そうした場合、自分の控え室から、そのメンバーのコストに2を足した数に等しいコストの『Aqours』のメンバーカードを1枚、そのメンバーがいたエリアに登場させ...
**A:** 自分の控え室からメンバーカードを登場させず、そのままこの能力の処理を終わります。...

---

## PL!S-bp3-006-P＋: 津島善子
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：このメンバー以外の『Aqours』のメンバー1人を自分のステージから控え室に置く。そうした場合、自分の控え室から、そのメンバーのコストに2を足した数に等しいコストの『Aqours』のメンバーカードを1枚、そのメンバーがいたエリアに登場させる。（この能力はセンターエリアに登場している場合のみ起動できる。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, DISCARD_HAND=1, DISCARD_HAND=1, SACRIFICE_SELF=0
  **Conditions:** NOT TURN_1 {}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'DISCARD'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}

### FAQ
**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：このメンバー以外の『Aqours』のメンバー1人を自分のステージから控え室に置く。そうした場合、自分の控え室から、そのメンバーのコストに2を足した数に等しいコストの『Aqours』のメンバーカードを1枚、そのメンバーがいたエリアに登場させ...
**A:** 自分の控え室からメンバーカードを登場させず、そのままこの能力の処理を終わります。...

---

## PL!S-bp3-006-SEC: 津島善子
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：このメンバー以外の『Aqours』のメンバー1人を自分のステージから控え室に置く。そうした場合、自分の控え室から、そのメンバーのコストに2を足した数に等しいコストの『Aqours』のメンバーカードを1枚、そのメンバーがいたエリアに登場させる。（この能力はセンターエリアに登場している場合のみ起動できる。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, DISCARD_HAND=1, DISCARD_HAND=1, SACRIFICE_SELF=0
  **Conditions:** NOT TURN_1 {}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'DISCARD'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}

### FAQ
**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：このメンバー以外の『Aqours』のメンバー1人を自分のステージから控え室に置く。そうした場合、自分の控え室から、そのメンバーのコストに2を足した数に等しいコストの『Aqours』のメンバーカードを1枚、そのメンバーがいたエリアに登場させ...
**A:** 自分の控え室からメンバーカードを登場させず、そのままこの能力の処理を終わります。...

---

## PL!S-bp3-007-R: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分か相手を選ぶ。自分は、そのプレイヤーの控え室にあるライブカードを1枚、そのプレイヤーのデッキの一番下に置く。そうした場合、自分はカードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'bottom'}
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!S-bp3-007-P: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}：自分か相手を選ぶ。自分は、そのプレイヤーの控え室にあるライブカードを1枚、そのプレイヤーのデッキの一番下に置く。そうした場合、自分はカードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'bottom'}
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!S-bp3-008-R: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。それがスコア6以上の『Aqours』のライブカードの場合、エネルギーを4枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Conditions:** GROUP_FILTER {'group': 'Aqours'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}
  **Effect:** ACTIVATE_MEMBER (value=4) → MEMBER_SELECT {'target': 'energy'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!S-bp3-008-P: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。それがスコア6以上の『Aqours』のライブカードの場合、エネルギーを4枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Conditions:** GROUP_FILTER {'group': 'Aqours'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}
  **Effect:** ACTIVATE_MEMBER (value=4) → MEMBER_SELECT {'target': 'energy'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!S-bp3-009-R: 黒澤ルビィ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを6枚見る。その中から『Aqours』のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=6)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Aqours'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Aqours'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!S-bp3-009-P: 黒澤ルビィ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを6枚見る。その中から『Aqours』のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=6)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Aqours'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Aqours'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!S-bp3-010-N: 高海千歌
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバーを1人までアクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT

---

## PL!S-bp3-011-N: 桜内梨子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバーを1人までアクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT

---

## PL!S-bp3-012-N: 松浦果南
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!S-bp3-016-N: 国木田花丸
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分の成功ライブカード置き場にあるカード1枚につき、ステージにいるこのメンバーのコストを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_live': True}
  **Effect:** BUFF_POWER (value=1)

### FAQ
**Q:** 『{{jyouji.png|常時}}自分の成功ライブカード置き場にあるカード1枚につき、ステージにいるこのメンバーのコストを＋１する。』について。
自分の成功ライブカード置き場に1枚ある場合、このカードを登場させるコストは＋１されますか？...
**A:** いいえ、されません。
この能力はステージにいる場合、コストが＋１されます。...

---

## PL!S-bp3-017-N: 小原鞠莉
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!S-bp3-019-L: MIRACLE WAVE
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}このターン、エールにより公開された自分のカードの中にブレードハートを持たないカードが0枚の場合か、または自分が余剰ハートを2つ以上持っている場合、このカードのスコアは４になる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SET_SCORE (value=4)

### FAQ
**Q:** 『{{live_success.png|ライブ成功時}}このターン、エールにより公開された自分のカードの中にブレードハートを持たないカードが0枚の場合か、または自分が余剰ハートを2つ以上持っている場合、このカードのスコアは４になる。』について、
ウェイト状態などによってエールで公開したカードが０枚の場合、このライブカードのスコアはいくつになりますか？...
**A:** 「エールにより公開された自分のカードの中にブレードハートを持たないカードが0枚の場合」という条件を満たすため、ライブに成功した際のスコアは4となります。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!S-bp3-020-L: ダイスキだったらダイジョウブ！
Type: ライブ

### Original Ability Text
```
{{jidou.png|自動}}［ターン1回］エールにより自分のカードを1枚以上公開したとき、それらのカードの中にブレードハートを持つカードが2枚以下の場合、それらのカードをすべて控え室に置いてもよい。そのエールで得たブレードハートを失い、もう一度エールを行う。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}, COUNT_DISCARD {'count': 1, 'zone': 'DISCARD'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}エールにより自分のカードを1枚以上公開したとき、それらのカードの中にブレードハートを持つカードが2枚以下の場合、それらのカードをすべて控え室に置いてもよい。そのエールで得たブレードハートを失い、もう一度エールを行う。』について。
「[PL!S-bp3-020-L]ダイスキだったらダイジョウブ！」2枚でライブをしている時、この能...
**A:** はい、可能です。...

---

## PL!S-bp3-021-L: 想いよひとつになれ
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の控え室にあるメンバーカード1枚をデッキの一番上に置いてもよい。そうした場合、ライブ終了時まで、自分のステージにいるメンバー1人は、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!S-bp3-024-L: Deep Resonance
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージのセンターエリアにコスト9以上の『Aqours』のメンバーがいる場合、以下から1つを選ぶ。
・ライブ終了時まで、自分のステージにいるメンバー1人は、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
・相手のステージにいるコスト4以下のメンバー1人をウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': 'Aqours', 'zone': 'CENTER_STAGE'}, IS_CENTER {}, COST_CHECK {'value': 9, 'comparison': 'GE'}
  **Effect:** SELECT_MODE (value=1)

---

## PL!S-bp3-025-L: SUKI for you, DREAM for you!
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいる『Aqours』のメンバー1人を選ぶ。そのメンバーが持つ{{icon_blade.png|ブレード}}が6つ以上の場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BOOST_SCORE (value=1)

---

## PL!N-bp3-001-R＋: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れたとき、下に置かれているエネルギーカードはエネルギーデッキに置く。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** DRAW (value=1) → PLAYER {'until': 'live_end'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

### FAQ
**Q:** エネルギーカードをメンバーカードの下に置いているとき、メンバーカードの下に置かれたエネルギーカードはエネルギーの数として数えますか？...
**A:** いいえ。数えません。
エネルギーの枚数を参照する際、メンバーカードの下に置かれたエネルギーカードは参照しません。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離...
**A:** はい、得ます。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離...
**A:** はい、可能です。
エネルギーの状態に限らずメンバーの下に置くことができます。...

---

## PL!N-bp3-001-P: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れたとき、下に置かれているエネルギーカードはエネルギーデッキに置く。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** DRAW (value=1) → PLAYER {'until': 'live_end'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

### FAQ
**Q:** エネルギーカードをメンバーカードの下に置いているとき、メンバーカードの下に置かれたエネルギーカードはエネルギーの数として数えますか？...
**A:** いいえ。数えません。
エネルギーの枚数を参照する際、メンバーカードの下に置かれたエネルギーカードは参照しません。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離...
**A:** はい、得ます。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離...
**A:** はい、可能です。
エネルギーの状態に限らずメンバーの下に置くことができます。...

---

## PL!N-bp3-001-P＋: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れたとき、下に置かれているエネルギーカードはエネルギーデッキに置く。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** DRAW (value=1) → PLAYER {'until': 'live_end'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

### FAQ
**Q:** エネルギーカードをメンバーカードの下に置いているとき、メンバーカードの下に置かれたエネルギーカードはエネルギーの数として数えますか？...
**A:** いいえ。数えません。
エネルギーの枚数を参照する際、メンバーカードの下に置かれたエネルギーカードは参照しません。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離...
**A:** はい、得ます。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離...
**A:** はい、可能です。
エネルギーの状態に限らずメンバーの下に置くことができます。...

---

## PL!N-bp3-001-SEC: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れたとき、下に置かれているエネルギーカードはエネルギーデッキに置く。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** DRAW (value=1) → PLAYER {'until': 'live_end'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

### FAQ
**Q:** エネルギーカードをメンバーカードの下に置いているとき、メンバーカードの下に置かれたエネルギーカードはエネルギーの数として数えますか？...
**A:** いいえ。数えません。
エネルギーの枚数を参照する際、メンバーカードの下に置かれたエネルギーカードは参照しません。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離...
**A:** はい、得ます。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離...
**A:** はい、可能です。
エネルギーの状態に限らずメンバーの下に置くことができます。...

---

## PL!N-bp3-002-R: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：好きなハートの色を1つ指定する。ライブ終了時まで、自分のステージにいるこのメンバー以外の『虹ヶ咲』のメンバー1人は、そのハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp3-002-P: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：好きなハートの色を1つ指定する。ライブ終了時まで、自分のステージにいるこのメンバー以外の『虹ヶ咲』のメンバー1人は、そのハートを1つ得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp3-003-R: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室にあるコスト4以下の『虹ヶ咲』のメンバーカードを1枚選ぶ。そのカードの{{toujyou.png|登場}}能力1つを発動させる。
（{{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

### FAQ
**Q:** 『{{toujyou.png|登場}}自分の控え室にあるコスト4以下の『虹ヶ咲』のメンバーカードを1枚選ぶ。そのカードの{{toujyou.png|登場}}能力1つを発動させる。
（{{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。）』
この能力で「このメンバーをウェイトにしてもよい」をコストに持つ{{toujyou.png|登場}}能力を発動できますか？...
**A:** いいえ、できません。...

---

## PL!N-bp3-003-P: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室にあるコスト4以下の『虹ヶ咲』のメンバーカードを1枚選ぶ。そのカードの{{toujyou.png|登場}}能力1つを発動させる。
（{{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

### FAQ
**Q:** 『{{toujyou.png|登場}}自分の控え室にあるコスト4以下の『虹ヶ咲』のメンバーカードを1枚選ぶ。そのカードの{{toujyou.png|登場}}能力1つを発動させる。
（{{toujyou.png|登場}}能力がコストを持つ場合、支払って発動させる。）』
この能力で「このメンバーをウェイトにしてもよい」をコストに持つ{{toujyou.png|登場}}能力を発動できますか？...
**A:** いいえ、できません。...

---

## PL!N-bp3-004-R: 朝香果林
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, DISCARD_HAND=1, DISCARD_HAND=1, SACRIFICE_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}

---

## PL!N-bp3-004-P: 朝香果林
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, DISCARD_HAND=1, DISCARD_HAND=1, SACRIFICE_SELF=0
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}

---

## PL!N-bp3-005-R＋: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。
{{live_start.png|ライブ開始時}}このターン、自分のステージにメンバーが2回以上登場している場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=5) → PLAYER

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このターンに既に2枚メンバーを登場させており、その後このメンバーカードを登場させたとき、自動能力は発動しますか？...
**A:** はい、発動します。...

**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このメンバーカードを登場させたときも、登場した回数に数えますか？...
**A:** はい、数えます。...

**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このターン登場してステージを離れたメンバーは登場したメンバーの回数に含みますか？...
**A:** はい、含みます。
そのターン中に登場したメンバーの数を参照します。
いずれかの効果によってキャラがステージから別の領域に移動していても登場した回数に数えます。...

---

## PL!N-bp3-005-P: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。
{{live_start.png|ライブ開始時}}このターン、自分のステージにメンバーが2回以上登場している場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=5) → PLAYER

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このターンに既に2枚メンバーを登場させており、その後このメンバーカードを登場させたとき、自動能力は発動しますか？...
**A:** はい、発動します。...

**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このメンバーカードを登場させたときも、登場した回数に数えますか？...
**A:** はい、数えます。...

**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このターン登場してステージを離れたメンバーは登場したメンバーの回数に含みますか？...
**A:** はい、含みます。
そのターン中に登場したメンバーの数を参照します。
いずれかの効果によってキャラがステージから別の領域に移動していても登場した回数に数えます。...

---

## PL!N-bp3-005-P＋: 宮下 愛
Type: メンバー

### Original Ability Text
```
"{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。
{{live_start.png|ライブ開始時}}このターン、自分のステージにメンバーが2回以上登場している場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。"
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=5) → PLAYER

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このターンに既に2枚メンバーを登場させており、その後このメンバーカードを登場させたとき、自動能力は発動しますか？...
**A:** はい、発動します。...

**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このメンバーカードを登場させたときも、登場した回数に数えますか？...
**A:** はい、数えます。...

**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このターン登場してステージを離れたメンバーは登場したメンバーの回数に含みますか？...
**A:** はい、含みます。
そのターン中に登場したメンバーの数を参照します。
いずれかの効果によってキャラがステージから別の領域に移動していても登場した回数に数えます。...

---

## PL!N-bp3-005-SEC: 宮下 愛
Type: メンバー

### Original Ability Text
```
"{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。
{{live_start.png|ライブ開始時}}このターン、自分のステージにメンバーが2回以上登場している場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。"
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=5) → PLAYER

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このターンに既に2枚メンバーを登場させており、その後このメンバーカードを登場させたとき、自動能力は発動しますか？...
**A:** はい、発動します。...

**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このメンバーカードを登場させたときも、登場した回数に数えますか？...
**A:** はい、数えます。...

**Q:** 『{{jidou.png|自動}}このターン、自分のステージにメンバーが3回登場したとき、手札が5枚になるまでカードを引く。』について。
このターン登場してステージを離れたメンバーは登場したメンバーの回数に含みますか？...
**A:** はい、含みます。
そのターン中に登場したメンバーの数を参照します。
いずれかの効果によってキャラがステージから別の領域に移動していても登場した回数に数えます。...

---

## PL!N-bp3-006-R: 近江彼方
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

---

## PL!N-bp3-006-P: 近江彼方
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

---

## PL!N-bp3-007-R: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}このメンバーをステージから控え室に置く：自分の手札からコスト13以下の「優木せつ菜」のメンバーカードを1枚、このメンバーがいたエリアに登場させる。その後、自分のエネルギー置き場にあるエネルギー1枚をそのメンバーの下に置く。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れたとき、下に置かれているエネルギーカードはエネルギーデッキに置く。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** SACRIFICE_SELF=0, ENERGY=2
  **Conditions:** COST_CHECK {'value': 13, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}
  **Effect:** ENERGY_CHARGE (value=1)
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

### FAQ
**Q:** エネルギーカードをメンバーカードの下に置いているとき、メンバーカードの下に置かれたエネルギーカードはエネルギーの数として数えますか？...
**A:** いいえ。数えません。
エネルギーの枚数を参照する際、メンバーカードの下に置かれたエネルギーカードは参照しません。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離...
**A:** はい、可能です。
エネルギーの状態に限らずメンバーの下に置くことができます。...

---

## PL!N-bp3-007-P: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}このメンバーをステージから控え室に置く：自分の手札からコスト13以下の「優木せつ菜」のメンバーカードを1枚、このメンバーがいたエリアに登場させる。その後、自分のエネルギー置き場にあるエネルギー1枚をそのメンバーの下に置く。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れたとき、下に置かれているエネルギーカードはエネルギーデッキに置く。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** SACRIFICE_SELF=0, ENERGY=2
  **Conditions:** COST_CHECK {'value': 13, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}
  **Effect:** ENERGY_CHARGE (value=1)
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

### FAQ
**Q:** エネルギーカードをメンバーカードの下に置いているとき、メンバーカードの下に置かれたエネルギーカードはエネルギーの数として数えますか？...
**A:** いいえ。数えません。
エネルギーの枚数を参照する際、メンバーカードの下に置かれたエネルギーカードは参照しません。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離...
**A:** はい、可能です。
エネルギーの状態に限らずメンバーの下に置くことができます。...

---

## PL!N-bp3-008-R＋: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバー以外の『虹ヶ咲』のメンバー1人をウェイトにする：カードを1枚引く。
{{live_start.png|ライブ開始時}}手札を2枚控え室に置いてもよい：自分のステージにいるこのメンバー以外のウェイト状態のメンバー1人をアクティブにする。そうした場合、ライブ終了時まで、これによりアクティブにしたメンバーと、このメンバーは、それぞれ{{heart_04.png|heart04}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Conditions:** NOT TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=2 (optional)
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELF
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバー以外の『虹ヶ咲』のメンバー1人をウェイトにする：カードを1枚引く。』について。
相手の『虹ヶ咲』のメンバーカードをウェイトにできますか？...
**A:** いいえ、できません。
自分の『虹ヶ咲』のメンバーのみウェイトにすることができます。...

---

## PL!N-bp3-008-P: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバー以外の『虹ヶ咲』のメンバー1人をウェイトにする：カードを1枚引く。
{{live_start.png|ライブ開始時}}手札を2枚控え室に置いてもよい：自分のステージにいるこのメンバー以外のウェイト状態のメンバー1人をアクティブにする。そうした場合、ライブ終了時まで、これによりアクティブにしたメンバーと、このメンバーは、それぞれ{{heart_04.png|heart04}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Conditions:** NOT TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=2 (optional)
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELF
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバー以外の『虹ヶ咲』のメンバー1人をウェイトにする：カードを1枚引く。』について。
相手の『虹ヶ咲』のメンバーカードをウェイトにできますか？...
**A:** いいえ、できません。
自分の『虹ヶ咲』のメンバーのみウェイトにすることができます。...

---

## PL!N-bp3-008-P＋: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
"{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバー以外の『虹ヶ咲』のメンバー1人をウェイトにする：カードを1枚引く。
{{live_start.png|ライブ開始時}}手札を2枚控え室に置いてもよい：自分のステージにいるこのメンバー以外のウェイト状態のメンバー1人をアクティブにする。そうした場合、ライブ終了時まで、これによりアクティブにしたメンバーと、このメンバーは、それぞれ{{heart_04.png|heart04}}を得る。"
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Conditions:** NOT TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=2 (optional)
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELF
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバー以外の『虹ヶ咲』のメンバー1人をウェイトにする：カードを1枚引く。』について。
相手の『虹ヶ咲』のメンバーカードをウェイトにできますか？...
**A:** いいえ、できません。
自分の『虹ヶ咲』のメンバーのみウェイトにすることができます。...

---

## PL!N-bp3-008-SEC: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
"{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバー以外の『虹ヶ咲』のメンバー1人をウェイトにする：カードを1枚引く。
{{live_start.png|ライブ開始時}}手札を2枚控え室に置いてもよい：自分のステージにいるこのメンバー以外のウェイト状態のメンバー1人をアクティブにする。そうした場合、ライブ終了時まで、これによりアクティブにしたメンバーと、このメンバーは、それぞれ{{heart_04.png|heart04}}を得る。"
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Conditions:** NOT TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=2 (optional)
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELF
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}このメンバー以外の『虹ヶ咲』のメンバー1人をウェイトにする：カードを1枚引く。』について。
相手の『虹ヶ咲』のメンバーカードをウェイトにできますか？...
**A:** いいえ、できません。
自分の『虹ヶ咲』のメンバーのみウェイトにすることができます。...

---

## PL!N-bp3-009-R＋: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}控え室にあるメンバーカード2枚を好きな順番でデッキの一番下に置いてもよい：それらのカードのコストの合計が、6の場合、カードを1枚引く。合計が8の場合、ライブ終了時まで、{{icon_all.png|ハート}}を得る。合計が25の場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1) {'filter': 'live'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}控え室にあるメンバーカード2枚を好きな順番でデッキの一番下に置いてもよい：それらのカードのコストの合計が、6の場合、カードを1枚引く。合計が8の場合、ライブ終了時まで、{{icon_all.png|ハート}}を得る。合計が25の場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
この能...
**A:** いいえ、できません。
自分の控え室にあるカードをデッキの下に置く必要があります。...

---

## PL!N-bp3-009-P: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}控え室にあるメンバーカード2枚を好きな順番でデッキの一番下に置いてもよい：それらのカードのコストの合計が、6の場合、カードを1枚引く。合計が8の場合、ライブ終了時まで、{{icon_all.png|ハート}}を得る。合計が25の場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1) {'filter': 'live'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}控え室にあるメンバーカード2枚を好きな順番でデッキの一番下に置いてもよい：それらのカードのコストの合計が、6の場合、カードを1枚引く。合計が8の場合、ライブ終了時まで、{{icon_all.png|ハート}}を得る。合計が25の場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
この能...
**A:** いいえ、できません。
自分の控え室にあるカードをデッキの下に置く必要があります。...

---

## PL!N-bp3-009-P＋: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}控え室にあるメンバーカード2枚を好きな順番でデッキの一番下に置いてもよい：それらのカードのコストの合計が、6の場合、カードを1枚引く。合計が8の場合、ライブ終了時まで、{{icon_all.png|ハート}}を得る。合計が25の場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1) {'filter': 'live'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}控え室にあるメンバーカード2枚を好きな順番でデッキの一番下に置いてもよい：それらのカードのコストの合計が、6の場合、カードを1枚引く。合計が8の場合、ライブ終了時まで、{{icon_all.png|ハート}}を得る。合計が25の場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
この能...
**A:** いいえ、できません。
自分の控え室にあるカードをデッキの下に置く必要があります。...

---

## PL!N-bp3-009-SEC: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}控え室にあるメンバーカード2枚を好きな順番でデッキの一番下に置いてもよい：それらのカードのコストの合計が、6の場合、カードを1枚引く。合計が8の場合、ライブ終了時まで、{{icon_all.png|ハート}}を得る。合計が25の場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1) {'filter': 'live'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}控え室にあるメンバーカード2枚を好きな順番でデッキの一番下に置いてもよい：それらのカードのコストの合計が、6の場合、カードを1枚引く。合計が8の場合、ライブ終了時まで、{{icon_all.png|ハート}}を得る。合計が25の場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について。
この能...
**A:** いいえ、できません。
自分の控え室にあるカードをデッキの下に置く必要があります。...

---

## PL!N-bp3-010-R: 三船栞子
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーの控え室にあるメンバーカードを2枚まで、好きな順番でデッキの一番下に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1) {'filter': 'member'}

---

## PL!N-bp3-010-P: 三船栞子
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーの控え室にあるメンバーカードを2枚まで、好きな順番でデッキの一番下に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1) {'filter': 'member'}

---

## PL!N-bp3-011-R: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}相手のステージにいる「ミア・テイラー」以外のメンバーを1人選ぶ。そのメンバーが持つハートと、このメンバーが持つハートの中に同じ色のハートがある場合、ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。それぞれのメンバーのコストが同じ場合、元々の{{icon_blade.png|ブレード}}の数が同じ場合についても同じことを行う。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!N-bp3-011-P: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}相手のステージにいる「ミア・テイラー」以外のメンバーを1人選ぶ。そのメンバーが持つハートと、このメンバーが持つハートの中に同じ色のハートがある場合、ライブ終了時まで、{{icon_blade.png|ブレード}}を得る。それぞれのメンバーのコストが同じ場合、元々の{{icon_blade.png|ブレード}}の数が同じ場合についても同じことを行う。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『ライブ終了時まで』と指定のある能力を使用したターンのパフォーマンスフェイズにライブを行わなかった場合、どうなりますか。...
**A:** ライブを行ったかどうかにかかわらず、ライブ終了時を期限とする能力はライブ勝敗判定フェイズの終了時に無くなります。...

---

## PL!N-bp3-012-R: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中から『虹ヶ咲』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=4)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': '虹ヶ咲'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-bp3-012-P: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中から『虹ヶ咲』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=4)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': '虹ヶ咲'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-bp3-013-N: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを2枚引く。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離れたとき、下に置かれているエネルギーカードはエネルギーデッキに置く。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** PLACE_UNDER (value=1)
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

### FAQ
**Q:** エネルギーカードをメンバーカードの下に置いているとき、メンバーカードの下に置かれたエネルギーカードはエネルギーの数として数えますか？...
**A:** いいえ。数えません。
エネルギーの枚数を参照する際、メンバーカードの下に置かれたエネルギーカードは参照しません。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置いてもよい。そうした場合、カードを1枚引き、ライブ終了時まで、自分のステージにいるメンバーは{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（メンバーの下に置かれているエネルギーカードではコストを支払えない。メンバーがステージから離...
**A:** はい、可能です。
エネルギーの状態に限らずメンバーの下に置くことができます。...

---

## PL!N-bp3-014-N: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_03.png|heart03}}か{{heart_04.png|heart04}}のうち1つを選ぶ。ライブ終了時まで、このメンバーが元々持つハートは選んだハートになる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}

---

## PL!N-bp3-015-N: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{heart_02.png|heart02}}か{{heart_05.png|heart05}}か{{heart_06.png|heart06}}のうち1つを選ぶ。ライブ終了時まで、このメンバーが元々持つハートは選んだハートになる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}

---

## PL!N-bp3-017-N: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!N-bp3-022-N: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

---

## PL!N-bp3-023-N: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!N-bp3-024-N: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}カードを2枚引き、手札を2枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp3-025-L: Awakening Promise
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバー1人の下にあるエネルギーカードを、好きな枚数エネルギーデッキに置いてもよい。そうした場合、ライブ終了時まで、そのメンバーは、これによって置いたエネルギーカード1枚につき、［赤ハート］［赤ハート］［赤ハート］を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_energy': True}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'multiplier': True, 'per_energy': True, 'until': 'live_end'}

---

## PL!N-bp3-026-L: サイコーハート
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にスコアが１か５のカードがある場合、このカードのスコアを＋１する。それらが両方ある場合、代わりにスコアを＋２する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** BOOST_SCORE (value=2)
  **Effect:** REPLACE_EFFECT (value=2) {'replaces': 'score_boost'}

---

## PL!N-bp3-027-L: La Bella Patria
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}このターン、自分が余剰ハートに{{heart_04.png|heart04}}を1つ以上持っており、かつ自分のステージに『虹ヶ咲』のメンバーがいる場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'STAGE'}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

### FAQ
**Q:** 『{{live_success.png|ライブ成功時}}このターン、自分が余剰ハートに{{heart_04.png|heart04}}を1つ以上持っており、かつ自分のステージに『虹ヶ咲』のメンバーがいる場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。』について、ステージに緑ハートがなくエールによってALLハートを3枚獲得してライブ成功した時、ライブ成功時能力は使えますか...
**A:** いいえ。使えません。...

**Q:** 『{{live_success.png|ライブ成功時}}このターン、自分が余剰ハートに{{heart_04.png|heart04}}を1つ以上持っており、かつ自分のステージに『虹ヶ咲』のメンバーがいる場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。』について、この能力を持つカードを2枚同時にライブをしました。この時、余剰ハートが{{heart_04.png|heart...
**A:** はい、可能です。...

**Q:** 余剰ハートを持つとは、どのような状態ですか？...
**A:** ライブカードの必要ハートよりもステージのメンバーが持つ基本ハートとエールで獲得したブレードハートが多い状態です。
例えば、必要ハートが{{heart_02.png|heart02}}{{heart_02.png|heart02}}{{heart_01.png|heart01}}の時、基本ハートとエールで獲得したハートが{{heart_02.png|heart02}}{{heart_02.png|h...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!N-bp3-028-L: ツナガルコネクト
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいる『虹ヶ咲』のメンバー1人につき、自分のデッキの上からカードを1枚見る。その中から1枚までをデッキの上に置き、残りを控え室に置く。その後、自分のデッキの一番上のカードを1枚公開する。これによりライブカードを公開した場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** LOOK_DECK (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** BOOST_SCORE (value=1)

---

## PL!N-bp3-030-L: Love U my friends
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中に{{icon_b_all.png|ALLブレード}}を持つカードが1枚以上ある場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_STAGE {'min': 1}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** ライブ成功時効果によって公開されたブレードハートの色が変更されており、かつALLハートをエールによって得た場合、PL!N-bp03-030-Lのライブ成功時効果の条件を満たしますか？...
**A:** いいえ。満たしません。...

**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!N-bp3-031-L: MONSTER GIRLS
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}自分のステージにいるウェイト状態のメンバー1人につき、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## LL-bp3-001-R＋: 園田海未&津島善子&天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}自分の控え室にある「園田海未」と「津島善子」と「天王寺璃奈」を、合計6枚をシャッフルしてデッキの一番下に置く：エネルギーを6枚までアクティブにする。
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Conditions:** TURN_1 {}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** ACTIVATE_MEMBER (value=6) → MEMBER_SELECT {'target': 'energy'}
  **Effect:** SWAP_CARDS (value=6) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=6) {'shuffle': True, 'position': 'bottom', 'target_zone': 'discard', 'target_names': ['園田海未', '津島善子', '天王寺璃奈']}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=6 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}自分の控え室にある「園田海未」と「津島善子」と「天王寺璃奈」を、合計6枚をシャッフルしてデッキの一番下に置く：エネルギーを6枚までアクティブにする。』について。
「園田海未」と「津島善子」と「天王寺璃奈」をそれぞれ1枚以上含める必要はありますか？...
**A:** いいえ、ありません。
「園田海未」と「津島善子」と「天王寺璃奈」のいずれか合計6枚をシャッフルしてデッキの下に置くことで能力を使用することができます。...

**Q:** このカードはグループ名やユニット名を持っていますか？...
**A:** カードに記載されているグループ名は持っていますが、カードに記載されていないユニット名は持っていません。...

**Q:** 「◯◯＆△△」のように名前が「＆」で並んでいるカード名のカードは、「◯◯」「△△」それぞれの名前を持ちますか？（例：「上原歩夢＆澁谷かのん＆日野下花帆」は「上原歩夢」「澁谷かのん」「日野下花帆」それぞれの名前を持ちますか？）...
**A:** はい、それぞれの名前を持ちます。...

---

## PL!-pb1-001-R: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：ライブカードかコスト10以上のメンバーカードのどちらか1つを選ぶ。選んだカードが公開されるまで、自分のデッキの一番上からカードを１枚ずつ公開する。そのカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, DISCARD_HAND=1, DISCARD_HAND=1, SACRIFICE_SELF=0
  **Conditions:** TURN_1 {}, COST_CHECK {'value': 10, 'comparison': 'GE'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** REVEAL_CARDS (value=1) {'all': True}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard', 'all': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand', 'all': True}

### FAQ
**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：ライブカードかコスト10以上のメンバーカードのどちらか1つを選ぶ。選んだカードが公開されるまで、自分のデッキの一番上からカードを１枚ずつ公開する。そのカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。』について。...
**A:** 効果や処理は実行可能な限り解決し、一部でも実行可能な場合はその一部を解決します。まったく解決できない場合は何も行いません。

この場合、メインデッキのカードをすべて公開してリフレッシュを行い、さらに新しいメインデッキのカードをすべて公開した時点で『選んだカードが公開されるまで、自分のデッキの一番上からカードを1枚ずつ公開する。そのカードを手札に加え、これにより公開されたほかのすべてのカードを控え室...

**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：ライブカードかコスト10以上のメンバーカードのどちらか1つを選ぶ。選んだカードが公開されるまで、自分のデッキの一番上からカードを１枚ずつ公開する。そのカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。』について。...
**A:** 能力に効果によって公開しているカードを含めずに「リフレッシュ」をして控え室のカードを新たなメインデッキにします。その後、効果の解決を再開します。...

---

## PL!-pb1-001-P＋: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：ライブカードかコスト10以上のメンバーカードのどちらか1つを選ぶ。選んだカードが公開されるまで、自分のデッキの一番上からカードを１枚ずつ公開する。そのカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, DISCARD_HAND=1, DISCARD_HAND=1, SACRIFICE_SELF=0
  **Conditions:** TURN_1 {}, COST_CHECK {'value': 10, 'comparison': 'GE'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** REVEAL_CARDS (value=1) {'all': True}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard', 'all': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand', 'all': True}

### FAQ
**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：ライブカードかコスト10以上のメンバーカードのどちらか1つを選ぶ。選んだカードが公開されるまで、自分のデッキの一番上からカードを１枚ずつ公開する。そのカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。』について。...
**A:** 効果や処理は実行可能な限り解決し、一部でも実行可能な場合はその一部を解決します。まったく解決できない場合は何も行いません。

この場合、メインデッキのカードをすべて公開してリフレッシュを行い、さらに新しいメインデッキのカードをすべて公開した時点で『選んだカードが公開されるまで、自分のデッキの一番上からカードを1枚ずつ公開する。そのカードを手札に加え、これにより公開されたほかのすべてのカードを控え室...

**Q:** 『{{kidou.png|起動}}{{center.png|センター}}{{turn1.png|ターン1回}}このメンバーをウェイトにし、手札を1枚控え室に置く：ライブカードかコスト10以上のメンバーカードのどちらか1つを選ぶ。選んだカードが公開されるまで、自分のデッキの一番上からカードを１枚ずつ公開する。そのカードを手札に加え、これにより公開されたほかのすべてのカードを控え室に置く。』について。...
**A:** 能力に効果によって公開しているカードを含めずに「リフレッシュ」をして控え室のカードを新たなメインデッキにします。その後、効果の解決を再開します。...

---

## PL!-pb1-002-R: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：自分のステージにいるメンバーが『BiBi』のみの場合、相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が3つ以下のメンバー1人をウェイトにする。
{{jyouji.png|常時}}相手のステージにいるウェイト状態のメンバー1人につき、{{heart_06.png|heart06}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** GROUP_FILTER {'group': 'BiBi', 'zone': 'OPPONENT_STAGE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** GROUP_FILTER {'group': 'BiBi', 'zone': 'OPPONENT_STAGE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 3:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=1) → OPPONENT {'multiplier': True, 'per_member': True}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!-pb1-002-P＋: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：自分のステージにいるメンバーが『BiBi』のみの場合、相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が3つ以下のメンバー1人をウェイトにする。
{{jyouji.png|常時}}相手のステージにいるウェイト状態のメンバー1人につき、{{heart_06.png|heart06}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** GROUP_FILTER {'group': 'BiBi', 'zone': 'OPPONENT_STAGE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Costs:** TAP_SELF=0 (optional)
  **Conditions:** GROUP_FILTER {'group': 'BiBi', 'zone': 'OPPONENT_STAGE'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 3:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=1) → OPPONENT {'multiplier': True, 'per_member': True}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!-pb1-003-R: 南ことり
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分のステージにいる『Printemps』のメンバー1人につき、エネルギーを1枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_energy': True}
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELF {'target': 'energy'}

---

## PL!-pb1-003-P＋: 南ことり
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分のステージにいる『Printemps』のメンバー1人につき、エネルギーを1枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_energy': True}
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELF {'target': 'energy'}

---

## PL!-pb1-004-R: 園田海未
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{center.png|センター}}自分の成功ライブカード置き場に{{icon_score.png|スコア}}を持つ『μ's』のカードが1枚ある場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。2枚以上ある場合、代わりに「{{jyouji.png|常時}}ライブの合計スコアを＋２する。」を得る。（この能力はセンターエリアに登場した場合のみ発動する。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': "μ's", 'zone': 'SUCCESS_LIVE'}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_STAGE {'min': 2}
  **Effect:** BOOST_SCORE (value=2)
  **Effect:** REPLACE_EFFECT (value=2) {'replaces': 'score_boost'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

---

## PL!-pb1-004-P＋: 園田海未
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{center.png|センター}}自分の成功ライブカード置き場に{{icon_score.png|スコア}}を持つ『μ's』のカードが1枚ある場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。2枚以上ある場合、代わりに「{{jyouji.png|常時}}ライブの合計スコアを＋２する。」を得る。（この能力はセンターエリアに登場した場合のみ発動する。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': "μ's", 'zone': 'SUCCESS_LIVE'}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_STAGE {'min': 2}
  **Effect:** BOOST_SCORE (value=2)
  **Effect:** REPLACE_EFFECT (value=2) {'replaces': 'score_boost'}

**Ability 3:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

---

## PL!-pb1-005-R: 星空 凛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にカードがある場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!-pb1-005-P＋: 星空 凛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にカードがある場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!-pb1-006-R: 西木野真姫
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室から『μ's』のライブカードを1枚までデッキの一番上に置く。その後、相手のステージにウェイト状態のメンバーがいる場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** OPPONENT_HAS {}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!-pb1-006-P＋: 西木野真姫
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室から『μ's』のライブカードを1枚までデッキの一番上に置く。その後、相手のステージにウェイト状態のメンバーがいる場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** OPPONENT_HAS {}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!-pb1-007-R: 東條 希
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を3枚控え室に置く：自分のステージにほかの『lilywhite』のメンバーがいる場合、自分の控え室から『μ's』のライブカードを1枚手札に加える。この能力を起動するためのコストは、自分の成功ライブカード置き場にあるカード1枚につき、控え室に置く手札の数が1枚減る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=3
  **Conditions:** TURN_1 {}, GROUP_FILTER {'group': 'lilywhite', 'zone': 'DISCARD'}, GROUP_FILTER {'group': "μ's", 'zone': 'DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'lilywhite'}
  **Effect:** SWAP_CARDS (value=3) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ACTIVATED
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_live': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** REDUCE_COST (value=1)

---

## PL!-pb1-007-P＋: 東條 希
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を3枚控え室に置く：自分のステージにほかの『lilywhite』のメンバーがいる場合、自分の控え室から『μ's』のライブカードを1枚手札に加える。この能力を起動するためのコストは、自分の成功ライブカード置き場にあるカード1枚につき、控え室に置く手札の数が1枚減る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=3
  **Conditions:** TURN_1 {}, GROUP_FILTER {'group': 'lilywhite', 'zone': 'DISCARD'}, GROUP_FILTER {'group': "μ's", 'zone': 'DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'lilywhite'}
  **Effect:** SWAP_CARDS (value=3) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ACTIVATED
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_live': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** REDUCE_COST (value=1)

---

## PL!-pb1-008-R: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}メンバーを3人までウェイトにしてもよい：これによりウェイト状態にしたメンバー1人につき、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

### FAQ
**Q:** 『{{toujyou.png|登場}}メンバーを3人までウェイトにしてもよい：これによりウェイト状態にしたメンバー1人につき、カードを1枚引く。』について、
このカードの効果で相手プレイヤーのメンバーをウェイトにできますか？...
**A:** いいえ。できません。
能力のコストとしてメンバーカードをウェイト状態にする際には、必ず自身のステージのメンバーをウェイト状態にしなければなりません。...

---

## PL!-pb1-008-P＋: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}メンバーを3人までウェイトにしてもよい：これによりウェイト状態にしたメンバー1人につき、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

### FAQ
**Q:** 『{{toujyou.png|登場}}メンバーを3人までウェイトにしてもよい：これによりウェイト状態にしたメンバー1人につき、カードを1枚引く。』について、
このカードの効果で相手プレイヤーのメンバーをウェイトにできますか？...
**A:** いいえ。できません。
能力のコストとしてメンバーカードをウェイト状態にする際には、必ず自身のステージのメンバーをウェイト状態にしなければなりません。...

---

## PL!-pb1-009-R: 矢澤にこ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が1つ以下のメンバー1人をウェイトにする。
{{toujyou.png|登場}}このターン、自分と相手のステージにいるメンバーは、効果によってはアクティブにならない。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT

### FAQ
**Q:** 『{{toujyou.png|登場}}このターン、自分と相手のステージにいるメンバーは、効果によってはアクティブにならない。』について、この効果が発動したターンにアクティブフェイズを迎えました。そのアクティブフェイズでメンバーをアクティブにできますか？...
**A:** はい、できます。...

---

## PL!-pb1-009-P＋: 矢澤にこ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が1つ以下のメンバー1人をウェイトにする。
{{toujyou.png|登場}}このターン、自分と相手のステージにいるメンバーは、効果によってはアクティブにならない。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT

### FAQ
**Q:** 『{{toujyou.png|登場}}このターン、自分と相手のステージにいるメンバーは、効果によってはアクティブにならない。』について、この効果が発動したターンにアクティブフェイズを迎えました。そのアクティブフェイズでメンバーをアクティブにできますか？...
**A:** はい、できます。...

---

## PL!-pb1-010-R: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：ライブ終了時まで、自分のステージにいるほかのメンバーは{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!-pb1-010-P＋: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：ライブ終了時まで、自分のステージにいるほかのメンバーは{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!-pb1-011-R: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージに名前の異なる『BiBi』のメンバーが2人以上いる場合、相手のステージにいるコスト4以下のメンバー1人をウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'BiBi', 'min': 2, 'zone': 'OPPONENT_STAGE'}, OPPONENT_HAS {}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=2) → OPPONENT

---

## PL!-pb1-011-P＋: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージに名前の異なる『BiBi』のメンバーが2人以上いる場合、相手のステージにいるコスト4以下のメンバー1人をウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'BiBi', 'min': 2, 'zone': 'OPPONENT_STAGE'}, OPPONENT_HAS {}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** TAP_OPPONENT (value=2) → OPPONENT

---

## PL!-pb1-012-R: 南ことり
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいる『Printemps』のメンバーを1人までアクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT

---

## PL!-pb1-012-P＋: 南ことり
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいる『Printemps』のメンバーを1人までアクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT

---

## PL!-pb1-013-R: 園田海未
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の手札を、相手は見ないで1枚選び公開する。これにより公開されたカードがライブカードの場合、ライブ終了時まで、このメンバーは「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** REVEAL_CARDS (value=1)

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** REVEAL_CARDS (value=1) {'until': 'live_end'}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}:自分の手札を相手は見ないで１枚選び公開する。これにより公開されたカードがライブカードの場合、ライブ終了時までこのメンバーは「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について、公開するのは自分の手札ですか？相...
**A:** 自分の手札を公開します。...

---

## PL!-pb1-013-P＋: 園田海未
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}：自分の手札を、相手は見ないで1枚選び公開する。これにより公開されたカードがライブカードの場合、ライブ終了時まで、このメンバーは「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Conditions:** TURN_1 {}
  **Effect:** REVEAL_CARDS (value=1)

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** REVEAL_CARDS (value=1) {'until': 'live_end'}
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}{{icon_energy.png|E}}:自分の手札を相手は見ないで１枚選び公開する。これにより公開されたカードがライブカードの場合、ライブ終了時までこのメンバーは「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。』について、公開するのは自分の手札ですか？相...
**A:** 自分の手札を公開します。...

---

## PL!-pb1-014-R: 星空 凛
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分の成功ライブカード置き場に『lilywhite』のカードがある場合、手札にあるこのメンバーカードのコストは2減る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** GROUP_FILTER {'group': 'lilywhite', 'zone': 'SUCCESS_LIVE'}
  **Effect:** REDUCE_COST (value=1)

---

## PL!-pb1-014-P＋: 星空 凛
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分の成功ライブカード置き場に『lilywhite』のカードがある場合、手札にあるこのメンバーカードのコストは2減る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** GROUP_FILTER {'group': 'lilywhite', 'zone': 'SUCCESS_LIVE'}
  **Effect:** REDUCE_COST (value=1)

---

## PL!-pb1-015-R: 西木野真姫
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}{{center.png|センター}}『BiBi』のメンバー1人をウェイトにしてもよい：相手は、自身のステージにいるアクティブ状態のメンバー1人をウェイトにする。（この能力はセンターエリアにいる場合のみ発動する。）
{{jidou.png|自動}}{{turn1.png|ターン1回}}自分のカードの効果によって、相手のステージにいるアクティブ状態のコスト4以下のメンバーがウェイト状態になったとき、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 3:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}自分のカードの効果によって、相手のステージにいるアクティブ状態のコスト４以下のメンバーがウェイト状態になったとき、カードを１枚引く。』について、条件を満たした場合でも自動能力の効果を解決しないことはできますか？...
**A:** いいえ、必ず解決する必要があります。...

---

## PL!-pb1-015-P＋: 西木野真姫
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}{{center.png|センター}}『BiBi』のメンバー1人をウェイトにしてもよい：相手は、自身のステージにいるアクティブ状態のメンバー1人をウェイトにする。（この能力はセンターエリアにいる場合のみ発動する。）
{{jidou.png|自動}}{{turn1.png|ターン1回}}自分のカードの効果によって、相手のステージにいるアクティブ状態のコスト4以下のメンバーがウェイト状態になったとき、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** IS_CENTER {}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 3:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

### FAQ
**Q:** 『{{jidou.png|自動}}{{turn1.png|ターン1回}}自分のカードの効果によって、相手のステージにいるアクティブ状態のコスト４以下のメンバーがウェイト状態になったとき、カードを１枚引く。』について、条件を満たした場合でも自動能力の効果を解決しないことはできますか？...
**A:** いいえ、必ず解決する必要があります。...

---

## PL!-pb1-016-R: 東條 希
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中から『lilywhite』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=4)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'lilywhite'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'lilywhite'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!-pb1-016-P＋: 東條 希
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを4枚見る。その中から『lilywhite』のカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=4)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'lilywhite'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'lilywhite'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!-pb1-017-R: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：カードを1枚引く。その後、このメンバーが『Printemps』のメンバーからバトンタッチして登場していないかぎり、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Conditions:** GROUP_FILTER {'group': 'Printemps', 'zone': 'DISCARD'}

---

## PL!-pb1-017-P＋: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：カードを1枚引く。その後、このメンバーが『Printemps』のメンバーからバトンタッチして登場していないかぎり、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** DRAW (value=1) → PLAYER

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Conditions:** GROUP_FILTER {'group': 'Printemps', 'zone': 'DISCARD'}

---

## PL!-pb1-018-R: 矢澤にこ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からコスト2以下のメンバーカードを1枚、メンバーのいないエリアにウェイト状態で登場させる。（この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 2, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** ON_PLAY

### FAQ
**Q:** 『{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からコスト2以下のメンバーカードを1枚、メンバーのいないエリアにウェイト状態で登場させる。（この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できない。）』について、
この能力で登場したメンバーカードが何らかの効果で控え室に移動した場合、空いたエリアにメンバーカードを出すことはできますか？...
**A:** はい。できます。...

**Q:** 『{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からコスト2以下のメンバーカードを1枚、メンバーのいないエリアにウェイト状態で登場させる。（この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できない。）』について、この能力でお互いに{{toujyou.png|登場}}能力を持つメンバーカードを登場させました。どちらから能力を使用できますか？...
**A:** 通常フェイズを行っているプレイヤーから順番に{{toujyou.png|登場}}能力を使用します。...

**Q:** 『{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からコスト2以下のメンバーカードを1枚、メンバーのいないエリアにウェイト状態で登場させる。（この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できない。）』について、この能力を先行で使用しました。このターン、相手はこのカードの能力で登場させたメンバーカードをバトンタッチに使用することはできますか？...
**A:** いいえできません。この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できないため、バトンタッチも使用できません。...

**Q:** 『{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からコスト2以下のメンバーカードを1枚、メンバーのいないエリアにウェイト状態で登場させる。（この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できない。）』について、自分または相手の控え室にコスト2以下のメンバーカードがいない場合、どうなりますか？...
**A:** 控え室にコスト2以下のメンバーカードがいないプレイヤーはメンバーカードを登場させずに効果の処理を終了します。...

---

## PL!-pb1-018-P＋: 矢澤にこ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からコスト2以下のメンバーカードを1枚、メンバーのいないエリアにウェイト状態で登場させる。（この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 2, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** ON_PLAY

### FAQ
**Q:** 『{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からコスト2以下のメンバーカードを1枚、メンバーのいないエリアにウェイト状態で登場させる。（この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できない。）』について、
この能力で登場したメンバーカードが何らかの効果で控え室に移動した場合、空いたエリアにメンバーカードを出すことはできますか？...
**A:** はい。できます。...

**Q:** 『{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からコスト2以下のメンバーカードを1枚、メンバーのいないエリアにウェイト状態で登場させる。（この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できない。）』について、この能力でお互いに{{toujyou.png|登場}}能力を持つメンバーカードを登場させました。どちらから能力を使用できますか？...
**A:** 通常フェイズを行っているプレイヤーから順番に{{toujyou.png|登場}}能力を使用します。...

**Q:** 『{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からコスト2以下のメンバーカードを1枚、メンバーのいないエリアにウェイト状態で登場させる。（この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できない。）』について、この能力を先行で使用しました。このターン、相手はこのカードの能力で登場させたメンバーカードをバトンタッチに使用することはできますか？...
**A:** いいえできません。この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できないため、バトンタッチも使用できません。...

**Q:** 『{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からコスト2以下のメンバーカードを1枚、メンバーのいないエリアにウェイト状態で登場させる。（この効果で登場したメンバーのいるエリアには、このターンにメンバーは登場できない。）』について、自分または相手の控え室にコスト2以下のメンバーカードがいない場合、どうなりますか？...
**A:** 控え室にコスト2以下のメンバーカードがいないプレイヤーはメンバーカードを登場させずに効果の処理を終了します。...

---

## PL!-pb1-019-N: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!-pb1-024-N: 西木野真姫
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!-pb1-025-N: 東條 希
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

### FAQ
**Q:** 『{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。』などについて。
このメンバーカードが登場したターンにこの能力を使用しました。このターン中、このメンバーカードが置かれていたエリアにメンバーカードを登場させることはできますか？...
**A:** はい、できます。
起動能力のコストでこのメンバーカードがステージから控え室に置かれることにより、このエリアにはこのターンに登場したメンバーカードが置かれていない状態になるため、そのエリアにメンバーカードを登場させることができます。...

---

## PL!-pb1-028-L: WAO-WAO Powerful day!
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいる『Printemps』のメンバーをアクティブにする。これによりウェイト状態のメンバーが3人以上アクティブ状態になったとき、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにいる『Printemps』のメンバーをアクティブにする。これによりウェイト状態のメンバーが３人以上アクティブ状態になったとき、このカードのスコアを＋１する。』について、元々アクティブ状態のメンバーが３枚いる状態でこの効果を解決した際、スコアを＋１することはできますか？...
**A:** いいえ、できません。
この効果によって、ウェイト状態のメンバー3人以上をアクティブにする必要があります。...

**Q:** 『{{live_start.png|ライブ開始時}}自分のステージにいる『Printemps』のメンバーをアクティブにする。』について、メンバーを複数枚アクティブにするにすることはできますか？...
**A:** はい、できます。...

---

## PL!-pb1-029-L: 知らないLove＊教えてLove
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場のカードが0枚で、かつ自分のステージにいるメンバーが『lilywhite』のみの場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': 'lilywhite', 'zone': 'SUCCESS_LIVE'}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!-pb1-030-L: Cutie Panther
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}相手のステージにウェイト状態のメンバーがいる場合、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}{{heart_00.png|heart0}}減らす。
{{live_success.png|ライブ成功時}}自分のステージに名前の異なる『BiBi』のメンバーが2人以上いる場合、自分の控え室から『BiBi』のメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** OPPONENT_HAS {}
  **Effect:** REDUCE_HEART_REQ (value=2) → PLAYER
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_GROUP {'group': 'BiBi', 'min': 2, 'zone': 'DISCARD'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'BiBi'}

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!-pb1-031-L: 輝夜の城で踊りたい
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}手札を1枚控え室に置いてもよい：エールにより公開された自分のカードの中から、『μ's』のメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard', 'group': "μ's"}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SWAP_ZONE (value=1)

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!-pb1-032-L: SENTIMENTAL StepS
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}自分の成功ライブカード置き場に『μ's』のカードがある場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** GROUP_FILTER {'group': "μ's", 'zone': 'SUCCESS_LIVE'}
  **Effect:** DRAW (value=1) → PLAYER

### FAQ
**Q:** {{live_success.png|ライブ成功時}}とはいつのことですか？...
**A:** 両方のプレイヤーのパフォーマンスフェイズを行った後、ライブ勝敗判定フェイズで、ライブに勝利したプレイヤーを決定する前のタイミングです。...

---

## PL!-bp4-001-R: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーのコストの合計が相手より低い場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!-bp4-001-P: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーのコストの合計が相手より低い場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!-bp4-002-R＋: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のライブ中のライブカードに、{{live_start.png|ライブ開始時}}能力も{{live_success.png|ライブ成功時}}能力も持たないカードがあるかぎり、{{heart_06.png|heart06}}{{heart_06.png|heart06}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から『μ's』のライブカードを1枚手札に加える。この能力は、自分の成功ライブカード置き場にあるカードのスコアの合計が６以上の場合のみ起動できる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=2
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ACTIVATED

---

## PL!-bp4-002-P: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のライブ中のライブカードに、{{live_start.png|ライブ開始時}}能力も{{live_success.png|ライブ成功時}}能力も持たないカードがあるかぎり、{{heart_06.png|heart06}}{{heart_06.png|heart06}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から『μ's』のライブカードを1枚手札に加える。この能力は、自分の成功ライブカード置き場にあるカードのスコアの合計が６以上の場合のみ起動できる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=2
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ACTIVATED

---

## PL!-bp4-002-P＋: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のライブ中のライブカードに、{{live_start.png|ライブ開始時}}能力も{{live_success.png|ライブ成功時}}能力も持たないカードがあるかぎり、{{heart_06.png|heart06}}{{heart_06.png|heart06}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から『μ's』のライブカードを1枚手札に加える。この能力は、自分の成功ライブカード置き場にあるカードのスコアの合計が６以上の場合のみ起動できる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=2
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ACTIVATED

---

## PL!-bp4-002-SEC: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のライブ中のライブカードに、{{live_start.png|ライブ開始時}}能力も{{live_success.png|ライブ成功時}}能力も持たないカードがあるかぎり、{{heart_06.png|heart06}}{{heart_06.png|heart06}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を2枚控え室に置く：自分の控え室から『μ's』のライブカードを1枚手札に加える。この能力は、自分の成功ライブカード置き場にあるカードのスコアの合計が７以上の場合のみ起動できる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=2) → MEMBER_SELF

**Ability 2:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=2
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': "μ's"}
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

**Ability 3:**
  **Trigger:** ACTIVATED

---

## PL!-bp4-003-R: 南 ことり
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

---

## PL!-bp4-003-P: 南 ことり
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

---

## PL!-bp4-004-R: 園田海未
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にあるカードのスコアの合計が６以上の場合、エネルギーを2枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

---

## PL!-bp4-004-P: 園田海未
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にあるカードのスコアの合計が６以上の場合、エネルギーを2枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

---

## PL!-bp4-005-R＋: 星空 凛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からコスト2以下のメンバーカードを1枚手札に加える。
{{jyouji.png|常時}}{{center.png|センター}}ライブの合計スコアを＋１する。
{{live_start.png|ライブ開始時}}自分のステージに{{icon_blade.png|ブレード}}を5つ以上持つ『μ's』のメンバーがいない場合、このメンバーはセンターエリア以外にポジションチェンジする。(このメンバーを今いるエリア以外のエリアに移動させる。そのエリアにメンバーがいる場合、そのメンバーはこのメンバーがいたエリアに移動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 2, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'cost_max': 2}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BOOST_SCORE (value=1)

**Ability 3:**
  **Trigger:** ON_LIVE_START
  **Conditions:** NOT GROUP_FILTER {'group': "μ's", 'zone': 'CENTER_STAGE'}, IS_CENTER {}
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!-bp4-005-P: 星空 凛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からコスト2以下のメンバーカードを1枚手札に加える。
{{jyouji.png|常時}}{{center.png|センター}}ライブの合計スコアを＋１する。
{{live_start.png|ライブ開始時}}自分のステージに{{icon_blade.png|ブレード}}を5つ以上持つ『μ's』のメンバーがいない場合、このメンバーはセンターエリア以外にポジションチェンジする。(このメンバーを今いるエリア以外のエリアに移動させる。そのエリアにメンバーがいる場合、そのメンバーはこのメンバーがいたエリアに移動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 2, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'cost_max': 2}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BOOST_SCORE (value=1)

**Ability 3:**
  **Trigger:** ON_LIVE_START
  **Conditions:** NOT GROUP_FILTER {'group': "μ's", 'zone': 'CENTER_STAGE'}, IS_CENTER {}
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!-bp4-005-P＋: 星空凛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からコスト2以下のメンバーカードを1枚手札に加える。
{{jyouji.png|常時}}{{center.png|センター}}ライブの合計スコアを＋１する。
{{live_start.png|ライブ開始時}}自分のステージに{{icon_blade.png|ブレード}}を5つ以上持つ『μ's』のメンバーがいない場合、このメンバーはセンターエリア以外にポジションチェンジする。(このメンバーを今いるエリア以外のエリアに移動させる。そのエリアにメンバーがいる場合、そのメンバーはこのメンバーがいたエリアに移動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 2, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'cost_max': 2}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BOOST_SCORE (value=1)

**Ability 3:**
  **Trigger:** ON_LIVE_START
  **Conditions:** NOT GROUP_FILTER {'group': "μ's", 'zone': 'CENTER_STAGE'}, IS_CENTER {}
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!-bp4-005-SEC: 星空凛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室からコスト2以下のメンバーカードを1枚手札に加える。
{{jyouji.png|常時}}{{center.png|センター}}ライブの合計スコアを＋１する。
{{live_start.png|ライブ開始時}}自分のステージに{{icon_blade.png|ブレード}}を5つ以上持つ『μ's』のメンバーがいない場合、このメンバーはセンターエリア以外にポジションチェンジする。(このメンバーを今いるエリア以外のエリアに移動させる。そのエリアにメンバーがいる場合、そのメンバーはこのメンバーがいたエリアに移動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COST_CHECK {'value': 2, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'cost_max': 2}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BOOST_SCORE (value=1)

**Ability 3:**
  **Trigger:** ON_LIVE_START
  **Conditions:** NOT GROUP_FILTER {'group': "μ's", 'zone': 'CENTER_STAGE'}, IS_CENTER {}
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!-bp4-006-R: 西木野真姫
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にあるカードのスコアの合計が３以上の場合、自分のデッキの上からカードを5枚見る。その中から『μ's』のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=5)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': "μ's"}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': "μ's"}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!-bp4-006-P: 西木野真姫
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にあるカードのスコアの合計が３以上の場合、自分のデッキの上からカードを5枚見る。その中から『μ's』のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=5)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': "μ's"}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': "μ's"}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!-bp4-007-R: 東條 希
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にカードが1枚以上あり、かつスコアの合計が１以下の場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_SUCCESS_LIVE {'min': 1}, COUNT_STAGE {'count': 1, 'zone': 'SUCCESS_LIVE'}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!-bp4-007-P: 東條 希
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にカードが1枚以上あり、かつスコアの合計が１以下の場合、ライブ終了時まで、「{{jyouji.png|常時}}ライブの合計スコアを＋１する。」を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_SUCCESS_LIVE {'min': 1}, COUNT_STAGE {'count': 1, 'zone': 'SUCCESS_LIVE'}
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!-bp4-008-R: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分の成功ライブカード置き場にあるカードのスコアの合計が６以上であるかぎり、ステージにいるこのメンバーのコストを＋３する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** BOOST_SCORE (value=3)

---

## PL!-bp4-008-P: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分の成功ライブカード置き場にあるカードのスコアの合計が６以上であるかぎり、ステージにいるこのメンバーのコストを＋３する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** BOOST_SCORE (value=3)

---

## PL!-bp4-009-R: 矢澤にこ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}相手は、自身のステージにいるアクティブ状態のメンバー1人をウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!-bp4-009-P: 矢澤にこ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}相手は、自身のステージにいるアクティブ状態のメンバー1人をウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

### FAQ
**Q:** ウェイトするメンバーを決めるのは自分と相手のどちらですか？...
**A:** 対戦相手となります。...

---

## PL!-bp4-010-N: 高坂穂乃果
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!-bp4-011-N: 絢瀬絵里
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：ライブ終了時まで、自分のセンターエリアにいる『μ's』のメンバーは、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!-bp4-013-N: 園田海未
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札を1枚控え室に置いてもよい：ライブ終了時まで、自分のステージにいるこのメンバー以外のメンバー1人は、{{heart_01.png|heart01}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!-bp4-014-N: 星空 凛
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のライブ中のライブカードに、{{live_start.png|ライブ開始時}}能力も{{live_success.png|ライブ成功時}}能力も持たないカードがある場合、ライブ終了時まで、自分のステージにいるこのメンバー以外のメンバー1人は、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!-bp4-016-N: 東條 希
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にあるカードのスコアの合計が３以上の場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!-bp4-017-N: 小泉花陽
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：ライブ終了時まで、自分のセンターエリアにいる『μ's』のメンバーは、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!-bp4-018-N: 矢澤にこ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分の成功ライブカード置き場にあるカードのスコアの合計が相手より高いかぎり、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Conditions:** LIFE_LEAD {'type': 'score'}
  **Effect:** ADD_BLADES (value=1) → OPPONENT
  **Effect:** BOOST_SCORE (value=1)

---

## PL!-bp4-019-L: Angelic Angel
Type: ライブ

### Original Ability Text
```
{{jyouji.png|常時}}このカードが自分の成功ライブカード置き場にあり、かつ自分のステージに『μ's』のメンバーがいるかぎり、自分の成功ライブカード置き場にあるこのカードのスコアを＋５する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** BOOST_SCORE (value=5)

---

## PL!-bp4-020-L: Love wing bell
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーが『μ's』のみの場合、自分のステージにいるメンバー1人をポジションチェンジさせてもよい。
{{jyouji.png|常時}}このカードが自分の成功ライブカード置き場にあるかぎり、自分のセンターエリアにいる『μ's』のメンバーは{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': "μ's", 'zone': 'STAGE'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!-bp4-021-L: ?←HEARTBEAT
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にあるカードのスコアの合計が６以上の場合、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}減らす。スコアの合計が９以上の場合、さらにこのカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** REDUCE_HEART_REQ (value=1) → PLAYER
  **Effect:** BOOST_SCORE (value=1)

---

## PL!-bp4-022-L: No brand girls
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のセンターエリアに{{icon_blade.png|ブレード}}を9つ以上持つ『μ's』のメンバーがいる場合、このカードのスコアを＋２する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': "μ's", 'zone': 'CENTER_STAGE'}, IS_CENTER {}
  **Effect:** BOOST_SCORE (value=2)

---

## PL!-bp4-023-L: もぎゅっと"love"で接近中！
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}自分が余剰ハートに{{heart_01.png|heart01}}を1つ以上持つ場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!-bp4-024-L: 小夜啼鳥恋詩
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}ライブ終了時まで、自分のステージにいる『μ's』のメンバー1人は、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp4-001-R: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}自分のエネルギーが相手より少ない場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!N-bp4-001-P: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}自分のエネルギーが相手より少ない場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!N-bp4-002-R: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーのデッキの一番上のカードを見る。自分はそのカードを控え室に置いてもよい。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-bp4-002-P: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分か相手を選ぶ。自分は、そのプレイヤーのデッキの一番上のカードを見る。自分はそのカードを控え室に置いてもよい。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-bp4-003-R: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** LIFE_LEAD {'type': 'score'}
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!N-bp4-003-P: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}ライブの合計スコアが相手より高い場合、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** LIFE_LEAD {'type': 'score'}
  **Effect:** DRAW (value=1) → PLAYER

---

## PL!N-bp4-004-R＋: 朝香果林
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}カードを1枚引く。相手のステージにいるコスト9以下のメンバーを1人までウェイトにする。
{{live_start.png|ライブ開始時}}相手のステージにいるウェイト状態のメンバーの数まで、自分の控え室にある『虹ヶ咲』のメンバーカードを選ぶ。それらを好きな順番でデッキの上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COST_CHECK {'value': 9, 'comparison': 'LE'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** ORDER_DECK (value=1)

---

## PL!N-bp4-004-P: 朝香果林
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}カードを1枚引く。相手のステージにいるコスト9以下のメンバーを1人までウェイトにする。
{{live_start.png|ライブ開始時}}相手のステージにいるウェイト状態のメンバーの数まで、自分の控え室にある『虹ヶ咲』のメンバーカードを選ぶ。それらを好きな順番でデッキの上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COST_CHECK {'value': 9, 'comparison': 'LE'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** ORDER_DECK (value=1)

---

## PL!N-bp4-004-P＋: 朝香果林
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}カードを1枚引く。相手のステージにいるコスト9以下のメンバーを1人までウェイトにする。
{{live_start.png|ライブ開始時}}相手のステージにいるウェイト状態のメンバーの数まで、自分の控え室にある『虹ヶ咲』のメンバーカードを選ぶ。それらを好きな順番でデッキの上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COST_CHECK {'value': 9, 'comparison': 'LE'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** ORDER_DECK (value=1)

---

## PL!N-bp4-004-SEC: 朝香果林
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}カードを1枚引く。相手のステージにいるコスト9以下のメンバーを1人までウェイトにする。
{{live_start.png|ライブ開始時}}相手のステージにいるウェイト状態のメンバーの数まで、自分の控え室にある『虹ヶ咲』のメンバーカードを選ぶ。それらを好きな順番でデッキの上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COST_CHECK {'value': 9, 'comparison': 'LE'}
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT
  **Effect:** ORDER_DECK (value=1)

---

## PL!N-bp4-005-R: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：相手のステージにいるコスト4以下のメンバーを2人までウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** TAP_OPPONENT (value=2) → OPPONENT
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

---

## PL!N-bp4-005-P: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：相手のステージにいるコスト4以下のメンバーを2人までウェイトにする。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** TAP_OPPONENT (value=2) → OPPONENT
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

---

## PL!N-bp4-006-R: 近江彼方
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分の手札からコスト4以下の『虹ヶ咲』のメンバーカードを1枚ステージに登場させる。これにより登場したメンバーがブレードハートを持つ場合、このメンバーをウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0

---

## PL!N-bp4-006-P: 近江彼方
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：自分の手札からコスト4以下の『虹ヶ咲』のメンバーカードを1枚ステージに登場させる。これにより登場したメンバーがブレードハートを持つ場合、このメンバーをウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0

---

## PL!N-bp4-007-R＋: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からライブカードを1枚手札に加える。
{{jyouji.png|常時}}自分と相手のエネルギーの合計が15枚以上あるかぎり、{{heart_02.png|heart02}}{{heart_02.png|heart02}}を得る。
{{live_success.png|ライブ成功時}}自分と相手はそれぞれ、自身のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=2) → OPPONENT

**Ability 3:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!N-bp4-007-P: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からライブカードを1枚手札に加える。
{{jyouji.png|常時}}自分と相手のエネルギーの合計が15枚以上あるかぎり、{{heart_02.png|heart02}}{{heart_02.png|heart02}}を得る。
{{live_success.png|ライブ成功時}}自分と相手はそれぞれ、自身のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=2) → OPPONENT

**Ability 3:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!N-bp4-007-P＋: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からライブカードを1枚手札に加える。
{{jyouji.png|常時}}自分と相手のエネルギーの合計が15枚以上あるかぎり、{{heart_02.png|heart02}}{{heart_02.png|heart02}}を得る。
{{live_success.png|ライブ成功時}}自分と相手はそれぞれ、自身のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=2) → OPPONENT

**Ability 3:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!N-bp4-007-SEC: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分と相手はそれぞれ、自身の控え室からライブカードを1枚手札に加える。
{{jyouji.png|常時}}自分と相手のエネルギーの合計が15枚以上あるかぎり、{{heart_02.png|heart02}}{{heart_02.png|heart02}}を得る。
{{live_success.png|ライブ成功時}}自分と相手はそれぞれ、自身のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=2) → OPPONENT

**Ability 3:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!N-bp4-008-R: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：エネルギー1枚か『虹ヶ咲』のメンバー1人をアクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Conditions:** TURN_1 {}
  **Effect:** ENERGY_CHARGE (value=1)
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT {'target': 'energy'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp4-008-P: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}手札を1枚控え室に置く：エネルギー1枚か『虹ヶ咲』のメンバー1人をアクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Conditions:** TURN_1 {}
  **Effect:** ENERGY_CHARGE (value=1)
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT {'target': 'energy'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp4-009-R: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーのコストの合計が相手より低い場合、カードを2枚引き、自分の手札を1枚デッキの一番上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}

---

## PL!N-bp4-009-P: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージにいるメンバーのコストの合計が相手より低い場合、カードを2枚引き、自分の手札を1枚デッキの一番上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}

---

## PL!N-bp4-010-R＋: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にある『虹ヶ咲』のライブカードを1枚控え室に置いてもよい。そうした場合、自分の控え室にある『虹ヶ咲』のライブカードを1枚成功ライブカード置き場に置く。
{{live_start.png|ライブ開始時}}自分のライブ中の『虹ヶ咲』のライブカードを1枚選ぶ。それと同じカード名のカードが自分の成功ライブカード置き場にある場合、ライブ終了時まで、{{heart_04.png|heart04}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'SUCCESS_LIVE'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp4-010-P: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にある『虹ヶ咲』のライブカードを1枚控え室に置いてもよい。そうした場合、自分の控え室にある『虹ヶ咲』のライブカードを1枚成功ライブカード置き場に置く。
{{live_start.png|ライブ開始時}}自分のライブ中の『虹ヶ咲』のライブカードを1枚選ぶ。それと同じカード名のカードが自分の成功ライブカード置き場にある場合、ライブ終了時まで、{{heart_04.png|heart04}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'SUCCESS_LIVE'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp4-010-P＋: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にある『虹ヶ咲』のライブカードを1枚控え室に置いてもよい。そうした場合、自分の控え室にある『虹ヶ咲』のライブカードを1枚成功ライブカード置き場に置く。
{{live_start.png|ライブ開始時}}自分のライブ中の『虹ヶ咲』のライブカードを1枚選ぶ。それと同じカード名のカードが自分の成功ライブカード置き場にある場合、ライブ終了時まで、{{heart_04.png|heart04}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'SUCCESS_LIVE'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp4-010-SEC: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の成功ライブカード置き場にある『虹ヶ咲』のライブカードを1枚控え室に置いてもよい。そうした場合、自分の控え室にある『虹ヶ咲』のライブカードを1枚成功ライブカード置き場に置く。
{{live_start.png|ライブ開始時}}自分のライブ中の『虹ヶ咲』のライブカードを1枚選ぶ。それと同じカード名のカードが自分の成功ライブカード置き場にある場合、ライブ終了時まで、{{heart_04.png|heart04}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'SUCCESS_LIVE'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp4-011-R＋: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札のライブカードを1枚控え室に置いてもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
{{live_success.png|ライブ成功時}}自分のデッキの上からカードを5枚控え室に置く。その後、自分の控え室にカード名の異なる『虹ヶ咲』のライブカードが3枚以上ある場合、自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_GROUP {'group': '虹ヶ咲', 'min': 3, 'zone': 'DISCARD'}
  **Effect:** SWAP_CARDS (value=5) {'target': 'discard', 'from': 'deck'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}

---

## PL!N-bp4-011-P: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札のライブカードを1枚控え室に置いてもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
{{live_success.png|ライブ成功時}}自分のデッキの上からカードを5枚控え室に置く。その後、自分の控え室にカード名の異なる『虹ヶ咲』のライブカードが3枚以上ある場合、自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_GROUP {'group': '虹ヶ咲', 'min': 3, 'zone': 'DISCARD'}
  **Effect:** SWAP_CARDS (value=5) {'target': 'discard', 'from': 'deck'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}

### FAQ
**Q:** 好きなハートの色を選ぶとき、ALLハートを選ぶことはできますか？...
**A:** いいえ。できません。...

---

## PL!N-bp4-011-P＋: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札のライブカードを1枚控え室に置いてもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
{{live_success.png|ライブ成功時}}自分のデッキの上からカードを5枚控え室に置く。その後、自分の控え室にカード名の異なる『虹ヶ咲』のライブカードが3枚以上ある場合、自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_GROUP {'group': '虹ヶ咲', 'min': 3, 'zone': 'DISCARD'}
  **Effect:** SWAP_CARDS (value=5) {'target': 'discard', 'from': 'deck'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}

---

## PL!N-bp4-011-SEC: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}手札のライブカードを1枚控え室に置いてもよい：好きなハートの色を1つ指定する。ライブ終了時まで、そのハートを1つ得る。
{{live_success.png|ライブ成功時}}自分のデッキの上からカードを5枚控え室に置く。その後、自分の控え室にカード名の異なる『虹ヶ咲』のライブカードが3枚以上ある場合、自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** SET_BLADES (value=1)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_GROUP {'group': '虹ヶ咲', 'min': 3, 'zone': 'DISCARD'}
  **Effect:** SWAP_CARDS (value=5) {'target': 'discard', 'from': 'deck'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}

---

## PL!N-bp4-012-R: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}相手の成功ライブカード置き場にあるカードのスコアの合計が６以上であるかぎり、ライブの合計スコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** BOOST_SCORE (value=1)

---

## PL!N-bp4-012-P: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}相手の成功ライブカード置き場にあるカードのスコアの合計が６以上であるかぎり、ライブの合計スコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** BOOST_SCORE (value=1)

---

## PL!N-bp4-013-N: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp4-016-N: 朝香果林
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分のデッキの上からカードを2枚見る。その中から好きな枚数を好きな順番でデッキの上に置き、残りを控え室に置く。（ウェイト状態のメンバーが持つ{{icon_blade.png|ブレード}}は、エールで公開する枚数を増やさない。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** ORDER_DECK (value=1)
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_member': True}

---

## PL!N-bp4-017-N: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

---

## PL!N-bp4-018-N: 近江彼方
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}自分のメインフェイズの間、このメンバーがアクティブ状態からウェイト状態になったとき、カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

### FAQ
**Q:** 「[PL!-pb1-018-R]矢澤にこ」の登場時効果でこのカードを登場させた場合、自動能力の条件を満たし、効果を解決することができますか？...
**A:** いいえ。できません。...

---

## PL!N-bp4-020-N: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

---

## PL!N-bp4-021-N: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分の控え室にあるカード1枚をデッキの一番上に置いてもよい。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}

---

## PL!N-bp4-023-N: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}『虹ヶ咲」のメンバー1人をウェイトにしてもよい：カードを1枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** DRAW (value=1) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-bp4-025-L: VIVID WORLD
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}ライブ終了時まで、エールによって公開される自分のカードが持つ[桃ブレード]、[赤ブレード]、[黄ブレード]、[緑ブレード]、[紫ブレード]、{{icon_b_all.png|ALLブレード}}は、すべて[青ブレード]になる。
{{live_success.png|ライブ成功時}}エールにより公開された自分の『虹ヶ咲』のメンバーカードが持つハートの中に{{heart_01.png|heart01}}、{{heart_02.png|heart02}}、{{heart_03.png|heart03}}、{{heart_04.png|heart04}}、{{heart_05.png|heart05}}、{{heart_06.png|heart06}}がある場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** TRANSFORM_COLOR (value=1) {'target_color': '青ブレード'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** ライブ成功時効果によって公開されたブレードハートの色が変更されており、かつALLハートをエールによって得た場合、PL!N-bp03-030-Lのライブ成功時効果の条件を満たしますか？...
**A:** いいえ。満たしません。...

---

## PL!N-bp4-026-L: DIVE!
Type: ライブ

### Original Ability Text
```
{{jidou.png|自動}}自分のメインフェイズにこのカードが控え室から手札に加えられたとき、自分の手札からカード名が「DIVE!」のライブカード1枚を表向きでライブカード置き場に置いてもよい。そうした場合、次のライブカードセットフェイズで自分がライブカード置き場に置けるカード枚数の上限が1枚減る。
{{jidou.png|自動}}このカードが表向きでライブカード置き場に置かれたとき、ライブ終了時まで、自分のステージにいる『虹ヶ咲』のメンバー1人は、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_live': True}

**Ability 2:**
  **Trigger:** ON_LEAVES
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-bp4-027-L: EMOTION
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場にあるカード名が「EMOTION」のカード1枚につき、このカードのスコアを＋２し、成功させるための必要ハートを{{heart_00.png|heart0}}{{heart_00.png|heart0}}{{heart_00.png|heart0}}増やす。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'multiplier': True, 'per_live': True}
  **Effect:** BOOST_SCORE (value=2)

---

## PL!N-bp4-028-L: stars we chase
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の控え室にカード名の異なる『虹ヶ咲』のライブカードが4枚以上ある場合、このカードのスコアを＋１する。6枚以上ある場合、代わりにスコアを＋２する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_GROUP {'group': '虹ヶ咲', 'min': 4, 'zone': 'DISCARD'}, COUNT_STAGE {'min': 6}
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** BOOST_SCORE (value=2)
  **Effect:** REPLACE_EFFECT (value=2) {'replaces': 'score_boost'}

---

## PL!N-bp4-029-L: Rise Up High!
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}このゲームの1ターン目のライブフェイズの場合、このカードのスコアを＋１し、ライブ終了時まで、自分のステージにいる『虹ヶ咲』のメンバー1人は、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'STAGE'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!N-bp4-030-L: Daydream Mermaid
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}以下から1つを選ぶ。自分の成功ライブカード置き場に『虹ヶ咲』のカードがある場合、代わりに1つ以上を選ぶ。
・自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
・自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'SUCCESS_LIVE'}
  **Effect:** SELECT_MODE (value=1)

### FAQ
**Q:** ライブ成功時効果が発動した際、同じ効果を２回選ぶことができますか？...
**A:** いいえ。できません。...

---

## PL!N-bp4-031-L: NEO SKY, NEO MAP!
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージのエリアすべてに『虹ヶ咲』のメンバーがいて、かつそれらのコストの合計が20以上の場合、カードを3枚引き、自分の手札を3枚好きな順番でデッキの上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'HAND'}
  **Effect:** DRAW (value=3) → PLAYER
  **Effect:** ORDER_DECK (value=1) {'filter': 'live'}

---

## PL!SP-bp4-001-R: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバーが『Liella!』のみで、かつ自分のエネルギーが7枚以上ある場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'Liella!', 'min': 7, 'zone': 'STAGE'}, COUNT_ENERGY {'min': 7}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

---

## PL!SP-bp4-001-P: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のステージにいるメンバーが『Liella!』のみで、かつ自分のエネルギーが7枚以上ある場合、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'Liella!', 'min': 7, 'zone': 'STAGE'}, COUNT_ENERGY {'min': 7}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

---

## PL!SP-bp4-002-R: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分のデッキの上からカードを4枚見る。その中から必要ハートの合計が8以上の『Liella!』のライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** LOOK_DECK (value=4)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Liella!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp4-002-P: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをウェイトにしてもよい：自分のデッキの上からカードを4枚見る。その中から必要ハートの合計が8以上の『Liella!』のライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** TAP_SELF=0 (optional)
  **Effect:** LOOK_DECK (value=4)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked', 'group': 'Liella!'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!SP-bp4-003-R: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}【左サイド】【右サイド】カードを2枚引き、手札を2枚控え室に置く。（この能力は左サイドエリアか右サイドエリアに登場した場合のみ発動する。）
{{jyouji.png|常時}}{{center.png|センター}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

**Ability 3:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!SP-bp4-003-P: 嵐 千砂都
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}【左サイド】【右サイド】カードを2枚引き、手札を2枚控え室に置く。（この能力は左サイドエリアか右サイドエリアに登場した場合のみ発動する。）
{{jyouji.png|常時}}{{center.png|センター}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

**Ability 3:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!SP-bp4-004-R＋: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}このカードのプレイに際し、2人のメンバーとバトンタッチしてもよい。
{{toujyou.png|登場}}{{center.png|センター}}『Liella!』のメンバー2人からバトンタッチして登場している場合、カードを2枚引き、自分の控え室にあるコスト4以下の『Liella!』のメンバーカード1枚を自分のステージのメンバーのいないエリアに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** BATON_TOUCH_MOD (value=2)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}, GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** RECOVER_MEMBER (value=2) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}
  **Effect:** BATON_TOUCH_MOD (value=2)

### FAQ
**Q:** {{jyouji.png|常時}}このカードのプレイに際し、2人のメンバーとバトンタッチしてもよい。
---------------------
2人のメンバーとバトンタッチする際、2人の中にこのターン中に登場したメンバーを含んでいてもバトンタッチできますか？...
**A:** いいえ、2人とも前のターンから登場している必要があります。...

**Q:** 2人のメンバーとバトンタッチした際、このメンバーが登場できるエリアはどこになりますか？...
**A:** バトンタッチした2人のメンバーがいたエリアのうち、いずれかのエリアに登場します。登場するエリアはプレイヤーが任意に選べます。...

---

## PL!SP-bp4-004-P: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}このカードのプレイに際し、2人のメンバーとバトンタッチしてもよい。
{{toujyou.png|登場}}{{center.png|センター}}『Liella!』のメンバー2人からバトンタッチして登場している場合、カードを2枚引き、自分の控え室にあるコスト4以下の『Liella!』のメンバーカード1枚を自分のステージのメンバーのいないエリアに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** BATON_TOUCH_MOD (value=2)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}, GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** RECOVER_MEMBER (value=2) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}
  **Effect:** BATON_TOUCH_MOD (value=2)

---

## PL!SP-bp4-004-P＋: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}このカードのプレイに際し、2人のメンバーとバトンタッチしてもよい。
{{toujyou.png|登場}}{{center.png|センター}}『Liella!』のメンバー2人からバトンタッチして登場している場合、カードを2枚引き、自分の控え室にあるコスト4以下の『Liella!』のメンバーカード1枚を自分のステージのメンバーのいないエリアに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** BATON_TOUCH_MOD (value=2)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}, GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** RECOVER_MEMBER (value=2) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}
  **Effect:** BATON_TOUCH_MOD (value=2)

---

## PL!SP-bp4-004-SEC: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}このカードのプレイに際し、2人のメンバーとバトンタッチしてもよい。
{{toujyou.png|登場}}{{center.png|センター}}『Liella!』のメンバー2人からバトンタッチして登場している場合、カードを2枚引き、自分の控え室にあるコスト4以下の『Liella!』のメンバーカード1枚を自分のステージのメンバーのいないエリアに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** BATON_TOUCH_MOD (value=2)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}, GROUP_FILTER {'group': 'Liella!', 'zone': 'DISCARD'}, COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** RECOVER_MEMBER (value=2) → CARD_DISCARD {'auto_play': True, 'from': 'discard'}
  **Effect:** BATON_TOUCH_MOD (value=2)

---

## PL!SP-bp4-005-R＋: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}『Liella!』のメンバーからバトンタッチして登場しており、かつ自分のエネルギーが7枚以上ある場合、自分のエネルギーデッキから、エネルギーカードを2枚ウェイト状態で置く。
{{jyouji.png|常時}}自分のエネルギーが10枚以上あるかぎり、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'Liella!', 'min': 7, 'zone': 'DECK'}, COUNT_ENERGY {'min': 7}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_ENERGY {'min': 10}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!SP-bp4-005-P: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}『Liella!』のメンバーからバトンタッチして登場しており、かつ自分のエネルギーが7枚以上ある場合、自分のエネルギーデッキから、エネルギーカードを2枚ウェイト状態で置く。
{{jyouji.png|常時}}自分のエネルギーが10枚以上あるかぎり、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'Liella!', 'min': 7, 'zone': 'DECK'}, COUNT_ENERGY {'min': 7}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_ENERGY {'min': 10}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!SP-bp4-005-P＋: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}『Liella!』のメンバーからバトンタッチして登場しており、かつ自分のエネルギーが7枚以上ある場合、自分のエネルギーデッキから、エネルギーカードを2枚ウェイト状態で置く。
{{jyouji.png|常時}}自分のエネルギーが10枚以上あるかぎり、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'Liella!', 'min': 7, 'zone': 'DECK'}, COUNT_ENERGY {'min': 7}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_ENERGY {'min': 10}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!SP-bp4-005-SEC: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}『Liella!』のメンバーからバトンタッチして登場しており、かつ自分のエネルギーが7枚以上ある場合、自分のエネルギーデッキから、エネルギーカードを2枚ウェイト状態で置く。
{{jyouji.png|常時}}自分のエネルギーが10枚以上あるかぎり、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** COUNT_GROUP {'group': 'Liella!', 'min': 7, 'zone': 'DECK'}, COUNT_ENERGY {'min': 7}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Conditions:** COUNT_ENERGY {'min': 10}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!SP-bp4-006-R: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中に、名前が異なる『Liella!』のメンバーカードが3枚以上ある場合、エールにより公開された自分のカードの中から『Liella!』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_GROUP {'group': 'Liella!', 'min': 3, 'zone': 'HAND'}
  **Effect:** REVEAL_CARDS (value=3)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_ZONE (value=1)

---

## PL!SP-bp4-006-P: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中に、名前が異なる『Liella!』のメンバーカードが3枚以上ある場合、エールにより公開された自分のカードの中から『Liella!』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_GROUP {'group': 'Liella!', 'min': 3, 'zone': 'HAND'}
  **Effect:** REVEAL_CARDS (value=3)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': 'Liella!'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_ZONE (value=1)

---

## PL!SP-bp4-007-R: 米女メイ
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}このメンバーがエリアを移動したとき、自分の控え室から、スコア3以下の『Liella!』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'Liella!'}
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-bp4-007-P: 米女メイ
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}このメンバーがエリアを移動したとき、自分の控え室から、スコア3以下の『Liella!』のライブカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'Liella!'}
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-bp4-008-R＋: 若菜四季
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}【左サイド】カードを2枚引き、手札を1枚控え室に置く。
{{toujyou.png|登場}}【右サイド】エネルギーを2枚アクティブにする。
{{live_start.png|ライブ開始時}}このメンバーをポジションチェンジしてもよい。(このメンバーを今いるエリア以外のエリアに移動させる。そのエリアにメンバーがいる場合、そのメンバーはこのメンバーがいたエリアに移動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

**Ability 3:**
  **Trigger:** ON_LIVE_START
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-bp4-008-P: 若菜四季
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}【左サイド】カードを2枚引き、手札を1枚控え室に置く。
{{toujyou.png|登場}}【右サイド】エネルギーを2枚アクティブにする。
{{live_start.png|ライブ開始時}}このメンバーをポジションチェンジしてもよい。(このメンバーを今いるエリア以外のエリアに移動させる。そのエリアにメンバーがいる場合、そのメンバーはこのメンバーがいたエリアに移動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

**Ability 3:**
  **Trigger:** ON_LIVE_START
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-bp4-008-P＋: 若菜四季
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}【左サイド】カードを2枚引き、手札を1枚控え室に置く。
{{toujyou.png|登場}}【右サイド】エネルギーを2枚アクティブにする。
{{live_start.png|ライブ開始時}}このメンバーをポジションチェンジしてもよい。(このメンバーを今いるエリア以外のエリアに移動させる。そのエリアにメンバーがいる場合、そのメンバーはこのメンバーがいたエリアに移動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

**Ability 3:**
  **Trigger:** ON_LIVE_START
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-bp4-008-SEC: 若菜四季
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}【左サイド】カードを2枚引き、手札を1枚控え室に置く。
{{toujyou.png|登場}}【右サイド】エネルギーを2枚アクティブにする。
{{live_start.png|ライブ開始時}}このメンバーをポジションチェンジしてもよい。(このメンバーを今いるエリア以外のエリアに移動させる。そのエリアにメンバーがいる場合、そのメンバーはこのメンバーがいたエリアに移動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

**Ability 3:**
  **Trigger:** ON_LIVE_START
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-bp4-009-R: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージにいるメンバーのコストの合計が相手より低いかぎり、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → OPPONENT

---

## PL!SP-bp4-009-P: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージにいるメンバーのコストの合計が相手より低いかぎり、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → OPPONENT

---

## PL!SP-bp4-010-R: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}このメンバーをウェイトにする：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

---

## PL!SP-bp4-010-P: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{turn1.png|ターン1回}}{{icon_energy.png|E}}このメンバーをウェイトにする：自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0, ENERGY=1
  **Conditions:** TURN_1 {}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

---

## PL!SP-bp4-011-R＋: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動したとき、相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が3つ以下のメンバー1人をウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!SP-bp4-011-P: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動したとき、相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が3つ以下のメンバー1人をウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!SP-bp4-011-P＋: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動したとき、相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が3つ以下のメンバー1人をウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!SP-bp4-011-SEC: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}このメンバーが登場か、エリアを移動したとき、相手のステージにいる元々持つ{{icon_blade.png|ブレード}}の数が3つ以下のメンバー1人をウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT

---

## PL!SP-bp4-012-N: 澁谷かのん
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}支払ってもよい：ライブ終了時まで、{{heart_02.png|heart02}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=1 (optional)
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!SP-bp4-013-N: 唐 可可
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}このメンバーをポジションチェンジしてもよい。(このメンバーを今いるエリア以外のエリアに移動させる。そのエリアにメンバーがいる場合、そのメンバーはこのメンバーがいたエリアに移動させる。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-bp4-015-N: 平安名すみれ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

---

## PL!SP-bp4-016-N: 葉月 恋
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}カードの効果によって自分のエネルギー置き場にエネルギーカードが置かれるたび、ライブ終了時まで、{{heart_06.png|heart06}}を得る。(相手のカードの効果でも発動する。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LEAVES
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!SP-bp4-017-N: 桜小路きな子
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}【左サイド】このターン、このメンバーがエリアを移動している場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（この能力は左サイドエリアにいる場合のみ発動する。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** MOVE_MEMBER (value=1) {'until': 'live_end'}
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

---

## PL!SP-bp4-018-N: 米女メイ
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室から『Liella!』のカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand', 'group': 'Liella!'}

---

## PL!SP-bp4-019-N: 若菜四季
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** SACRIFICE_SELF=0
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'to': 'hand'}

---

## PL!SP-bp4-020-N: 鬼塚夏美
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}【右サイド】このターン、このメンバーがエリアを移動している場合、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。（この能力は右サイドエリアにいる場合のみ発動する。）
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** MOVE_MEMBER (value=1) {'until': 'live_end'}
  **Effect:** TRIGGER_REMOTE (value=1) {'from': 'stage'}

---

## PL!SP-bp4-021-N: ウィーン・マルガレーテ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のエネルギーが相手より多いかぎり、{{heart_06.png|heart06}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=1) → OPPONENT

---

## PL!SP-bp4-022-N: 鬼塚冬毬
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{icon_energy.png|E}}を2つまで支払ってもよい：ライブ終了時まで、支払った{{icon_energy.png|E}}につき、{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Costs:** ENERGY=2 (optional)
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'until': 'live_end'}

---

## PL!SP-bp4-023-L: Dazzling Game
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}ライブ終了時まで、自分のステージにいる、「澁谷かのん」「ウィーン・マルガレーテ」「鬼塚冬毬」のうちのメンバー1人と、これにより選んだメンバー以外の『Liella!』のメンバー1人は、{{icon_blade.png|ブレード}}を得る。
{{live_start.png|ライブ開始時}}ライブ終了時まで、エールによって公開される自分のカードが持つ[桃ブレード]、[赤ブレード]、[黄ブレード]、[緑ブレード]、[青ブレード]、{{icon_b_all.png|ALLブレード}}は、すべて[紫ブレード]になる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** ADD_BLADES (value=1) → MEMBER_NAMED {'target_name': '澁谷かのん', 'until': 'live_end'}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}
  **Effect:** TRANSFORM_COLOR (value=1) {'target_color': '紫ブレード'}

### FAQ
**Q:** ライブ成功時効果によって公開されたブレードハートの色が変更されており、かつALLハートをエールによって得た場合、PL!N-bp03-030-Lのライブ成功時効果の条件を満たしますか？...
**A:** いいえ。満たしません。...

**Q:** 「これにより選んだメンバー以外の『Liella!』のメンバー１人は、{{icon_blade.png|ブレード}}を得る。」について、選んだメンバー以外のメンバーを選ぶ必要がありますか？...
**A:** はい。あります。...

---

## PL!SP-bp4-024-L: ノンフィクション!!
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のセンターエリアにいる『Liella!』のメンバーのコストが、相手のセンターエリアにいるメンバーより高い場合、このカードのスコアを＋１する。
{{live_start.png|ライブ開始時}}自分のステージの左サイドエリアにいる『Liella!』のメンバーが{{heart_02.png|heart02}}を3つ以上持つ場合、そのメンバーは、ライブ終了時まで、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'OPPONENT_CENTER_STAGE'}, IS_CENTER {}
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'LEFT_STAGE'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=1) → MEMBER_SELF {'until': 'live_end'}

---

## PL!SP-bp4-025-L: Special Color
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}ライブ終了時まで、自分のステージのセンターエリアにいる『Liella!』のメンバーが元々持つ{{icon_blade.png|ブレード}}の数は3つになる。
{{live_success.png|ライブ成功時}}自分のステージのセンターエリアにいる『Liella!』のメンバーが、このターン中に移動している場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'CENTER_STAGE'}, IS_CENTER {}
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** BOOST_SCORE (value=1)

### FAQ
**Q:** {{live_start.png|ライブ開始時}}ライブ終了時まで、自分のステージのセンターエリアにいる『Liella!』のメンバーが元々持つ{{icon_blade.png|ブレード}}の数は3つになる。
---------------------
いずれかの効果でブレードを1つ得ているメンバーに対して、この能力を使いました。最終的なブレードの数はいくつになりますか？"
いずれかの効果でブレード...
**A:** 4つになります。元々持つブレードの数を変更した後、ブレードを得る効果が適用されるため、結果4つのブレードを持つことになります。...

---

## PL!SP-bp4-026-L: Wish Song
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中に名前が異なる『Liella!』のメンバーカードが5枚以上ある場合、このカードのスコアを＋１する。
{{live_success.png|ライブ成功時}}自分のエネルギーが11枚以上ある場合、カードを2枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** COUNT_GROUP {'group': 'Liella!', 'min': 5}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** BOOST_SCORE (value=1)

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Conditions:** COUNT_DISCARD {'count': 11, 'zone': 'DISCARD'}, COUNT_ENERGY {'min': 11}
  **Effect:** DRAW (value=11) → PLAYER
  **Effect:** ENERGY_CHARGE (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!SP-bp4-027-L: Chance Day, Chance Way!
Type: ライブ

### Original Ability Text
```
{{live_success.png|ライブ成功時}}自分のステージにいるメンバーが『Liella!』のみの場合、自分のステージにいるメンバーをフォーメーションチェンジしてもよい。(メンバーをそれぞれ好きなエリアに移動させる。この効果で1つのエリアに2人以上のメンバーを移動させることはできない。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_SUCCESS
  **Conditions:** GROUP_FILTER {'group': 'Liella!', 'zone': 'STAGE'}
  **Effect:** MOVE_MEMBER (value=1)
  **Effect:** MOVE_MEMBER (value=1)

---

## PL!SP-bp4-028-L: DAISUKI FULL POWER
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}アクティブ状態の自分のエネルギーがある場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BOOST_SCORE (value=1)

---

## LL-bp4-001-R＋: 絢瀬絵里&朝香果林&葉月 恋
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}自分のデッキの上からカードを5枚見る。その中から「絢瀬絵里」か「朝香果林」か「葉月恋」のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。その後、相手のステージにいる、これにより公開したカードのコスト以下で、かつ元々持つ{{icon_blade.png|ブレード}}の数が3つ以下のメンバーをすべてウェイトにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=5)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** TAP_OPPONENT (value=1) → OPPONENT {'all': True}

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Effect:** LOOK_DECK (value=5)

---

## PL!N-pb1-001-R: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のステージにこのメンバー以外のコスト11のメンバーがいる場合、自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
{{jyouji.png|常時}}自分のライブ中のライブカードが2枚以上あるかぎり、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** NOT GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!N-pb1-001-P＋: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のステージにこのメンバー以外のコスト11のメンバーがいる場合、自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
{{jyouji.png|常時}}自分のライブ中のライブカードが2枚以上あるかぎり、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Conditions:** NOT GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'DISCARD'}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

---

## PL!N-pb1-002-R: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギー置き場にあるエネルギー2枚をこのメンバーの下に置いてもよい。
{{jyouji.png|常時}}このメンバーの下にエネルギーカードが2枚以上置かれているかぎり、ライブの合計スコアを＋１する。
(メンバーがステージから離れたとき、下に置かれているエネルギーカードはエネルギーデッキに戻す。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** PLACE_UNDER (value=1)

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** PLACE_UNDER (value=1)

---

## PL!N-pb1-002-P＋: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のエネルギー置き場にあるエネルギー2枚をこのメンバーの下に置いてもよい。
{{jyouji.png|常時}}このメンバーの下にエネルギーカードが2枚以上置かれているかぎり、ライブの合計スコアを＋１する。
(メンバーがステージから離れたとき、下に置かれているエネルギーカードはエネルギーデッキに戻す。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** PLACE_UNDER (value=1)

**Ability 2:**
  **Trigger:** CONSTANT
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** PLACE_UNDER (value=1)

---

## PL!N-pb1-003-R: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}このカードを手札から控え室に置く：カードを1枚引き、ライブ終了時まで、自分のステージにいる『虹ヶ咲』のメンバー1人は{{icon_blade.png|ブレード}}を得る。この能力は、このカードが手札にある場合のみ起動できる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Effect:** DRAW (value=1) → PLAYER {'until': 'live_end'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ACTIVATED

### FAQ
**Q:** 自分のステージにいるメンバーが0人の場合でも、このカードの起動能力を使用することはできますか？...
**A:** はい。できます。...

---

## PL!N-pb1-003-P＋: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}{{icon_energy.png|E}}{{icon_energy.png|E}}このカードを手札から控え室に置く：カードを1枚引き、ライブ終了時まで、自分のステージにいる『虹ヶ咲』のメンバー1人は{{icon_blade.png|ブレード}}を得る。この能力は、このカードが手札にある場合のみ起動できる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** ENERGY=2
  **Effect:** DRAW (value=1) → PLAYER {'until': 'live_end'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

**Ability 2:**
  **Trigger:** ACTIVATED

### FAQ
**Q:** 自分のステージにいるメンバーが0人の場合でも、このカードの起動能力を使用することはできますか？...
**A:** はい。できます。...

---

## PL!N-pb1-004-R: 朝香果林
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}このターンにこのメンバーが移動していないかぎり、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
{{live_start.png|ライブ開始時}}自分のデッキの一番上のカードを公開する。公開したカードがコスト9以下のメンバーカードの場合、公開したカードを手札に加え、このメンバーはポジションチェンジする。それ以外の場合、公開したカードを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COST_CHECK {'value': 9, 'comparison': 'LE'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'cost_max': 9}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-004-P＋: 朝香果林
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}このターンにこのメンバーが移動していないかぎり、{{icon_blade.png|ブレード}}{{icon_blade.png|ブレード}}を得る。
{{live_start.png|ライブ開始時}}自分のデッキの一番上のカードを公開する。公開したカードがコスト9以下のメンバーカードの場合、公開したカードを手札に加え、このメンバーはポジションチェンジする。それ以外の場合、公開したカードを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF

**Ability 2:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COST_CHECK {'value': 9, 'comparison': 'LE'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** MOVE_TO_DECK (value=1) {'position': 'top'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'cost_max': 9}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-005-R: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}自分のステージにコスト10のメンバーが登場したとき、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

### FAQ
**Q:** このカードとバトンタッチしてコスト10のメンバーが登場した場合、このカードの自動能力をは発動できますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-005-P＋: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}自分のステージにコスト10のメンバーが登場したとき、カードを1枚引く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** TURN_1 {}
  **Effect:** DRAW (value=1) → PLAYER

### FAQ
**Q:** このカードとバトンタッチしてコスト10のメンバーが登場した場合、このカードの自動能力をは発動できますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-006-R: 近江彼方
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをウェイトにする：エネルギーを1枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELF {'target': 'energy'}

---

## PL!N-pb1-006-P＋: 近江彼方
Type: メンバー

### Original Ability Text
```
{{kidou.png|起動}}このメンバーをウェイトにする：エネルギーを1枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ACTIVATED
  **Costs:** TAP_SELF=0
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELF {'target': 'energy'}

---

## PL!N-pb1-007-R: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のライブ中のライブカードの必要ハートの中に{{heart_01.png|heart01}}、{{heart_02.png|heart02}}、{{heart_03.png|heart03}}、{{heart_04.png|heart04}}、{{heart_05.png|heart05}}、{{heart_06.png|heart06}}がそれぞれ1以上含まれるかぎり、{{icon_all.png|ハート}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=6) → MEMBER_SELF

### FAQ
**Q:** 自分のライブ中のライブカードが2枚あり、片方のライブカードの必要ハートには{{heart_01.png|heart01}}{{heart_02.png|heart02}}{{heart_03.png|heart03}}が、他方には{{heart_04.png|heart04}}{{heart_05.png|heart05}}{{heart_06.png|heart06}}が含まれています。
このと...
**A:** はい、得ます。...

---

## PL!N-pb1-007-P＋: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のライブ中のライブカードの必要ハートの中に{{heart_01.png|heart01}}、{{heart_02.png|heart02}}、{{heart_03.png|heart03}}、{{heart_04.png|heart04}}、{{heart_05.png|heart05}}、{{heart_06.png|heart06}}がそれぞれ1以上含まれるかぎり、{{icon_all.png|ハート}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_HEARTS (value=6) → MEMBER_SELF

### FAQ
**Q:** 自分のライブ中のライブカードが2枚あり、片方のライブカードの必要ハートには{{heart_01.png|heart01}}{{heart_02.png|heart02}}{{heart_03.png|heart03}}が、他方には{{heart_04.png|heart04}}{{heart_05.png|heart05}}{{heart_06.png|heart06}}が含まれています。
このと...
**A:** はい、得ます。...

---

## PL!N-pb1-008-R: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージにウェイト状態の『虹ヶ咲』のメンバーがいるかぎり、手札にあるこのメンバーカードのコストは2減る。
{{toujyou.png|登場}}自分のステージにいるメンバー1人か、エネルギーを2枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** REDUCE_COST (value=1)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

### FAQ
**Q:** 自分のステージにウェイト状態のメンバーが1人だけおり、このメンバーを登場させるためにそのウェイト状態のメンバーをバトンタッチで控え室に置こうとしています。
このとき、このメンバーカードのコストはいくつになりますか？...
**A:** 15コストとしてプレイできます。...

---

## PL!N-pb1-008-P＋: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}自分のステージにウェイト状態の『虹ヶ咲』のメンバーがいるかぎり、手札にあるこのメンバーカードのコストは2減る。
{{toujyou.png|登場}}自分のステージにいるメンバー1人か、エネルギーを2枚アクティブにする。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** REDUCE_COST (value=1)

**Ability 2:**
  **Trigger:** ON_PLAY
  **Effect:** ACTIVATE_MEMBER (value=2) → MEMBER_SELECT {'target': 'energy'}

### FAQ
**Q:** 自分のステージにウェイト状態のメンバーが1人だけおり、このメンバーを登場させるためにそのウェイト状態のメンバーをバトンタッチで控え室に置こうとしています。
このとき、このメンバーカードのコストはいくつになりますか？...
**A:** 15コストとしてプレイできます。...

---

## PL!N-pb1-009-R: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}このターン、ブレードハートを持たないメンバーカードが自分のライブカード置き場から控え室に置かれている場合、カードを1枚引き、ライブ終了時まで、{{heart_03.png|heart03}}{{heart_05.png|heart05}}{{heart_06.png|heart06}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** DRAW (value=1) → PLAYER {'until': 'live_end'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=3) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-009-P＋: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}このターン、ブレードハートを持たないメンバーカードが自分のライブカード置き場から控え室に置かれている場合、カードを1枚引き、ライブ終了時まで、{{heart_03.png|heart03}}{{heart_05.png|heart05}}{{heart_06.png|heart06}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** DRAW (value=1) → PLAYER {'until': 'live_end'}
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** ADD_HEARTS (value=3) → MEMBER_SELF {'until': 'live_end'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-010-R: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}以下から1つを選ぶ。
・エネルギーを1枚アクティブにする。
・自分の控え室にある『虹ヶ咲』のライブカードを2枚まで好きな順番でデッキの上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SELECT_MODE (value=1)

---

## PL!N-pb1-010-P＋: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}以下から1つを選ぶ。
・エネルギーを1枚アクティブにする。
・自分の控え室にある『虹ヶ咲』のライブカードを2枚まで好きな順番でデッキの上に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** SELECT_MODE (value=1)

---

## PL!N-pb1-011-R: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}このメンバーの下にあるエネルギーカード1枚につき、{{icon_blade.png|ブレード}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置く：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
(メンバーがステージから離れたとき、下に置かれているエネルギーカードはエネルギーデッキに戻す。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'per_energy': True}

**Ability 2:**
  **Trigger:** ACTIVATED
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** ENERGY_CHARGE (value=1)
  **Effect:** PLACE_UNDER (value=1)

---

## PL!N-pb1-011-P＋: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{jyouji.png|常時}}このメンバーの下にあるエネルギーカード1枚につき、{{icon_blade.png|ブレード}}を得る。
{{kidou.png|起動}}{{turn1.png|ターン1回}}自分のエネルギー置き場にあるエネルギー1枚をこのメンバーの下に置く：自分の控え室から『虹ヶ咲』のライブカードを1枚手札に加える。
(メンバーがステージから離れたとき、下に置かれているエネルギーカードはエネルギーデッキに戻す。)
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** CONSTANT
  **Effect:** ADD_BLADES (value=1) → MEMBER_SELF {'multiplier': True, 'per_energy': True}

**Ability 2:**
  **Trigger:** ACTIVATED
  **Conditions:** TURN_1 {}
  **Effect:** RECOVER_LIVE (value=1) → CARD_DISCARD {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** ENERGY_CHARGE (value=1)
  **Effect:** PLACE_UNDER (value=1)

---

## PL!N-pb1-012-R: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}自分のステージにこのメンバー以外のコスト11のメンバーが登場したとき、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中から、『虹ヶ咲』のメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** NOT TURN_1 {}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_ZONE (value=1)

### FAQ
**Q:** このカードとバトンタッチしてコスト11のメンバーが登場した場合、このカードの自動能力は発動できますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-012-P＋: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{jidou.png|自動}}{{turn1.png|ターン1回}}自分のステージにこのメンバー以外のコスト11のメンバーが登場したとき、自分のエネルギーデッキから、エネルギーカードを1枚ウェイト状態で置く。
{{live_success.png|ライブ成功時}}エールにより公開された自分のカードの中から、『虹ヶ咲』のメンバーカードを1枚手札に加える。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Conditions:** NOT TURN_1 {}
  **Effect:** ENERGY_CHARGE (value=1) {'from': 'deck'}

**Ability 2:**
  **Trigger:** ON_LIVE_SUCCESS
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'group': '虹ヶ咲'}
  **Effect:** CHEER_REVEAL (value=1)
  **Effect:** SWAP_ZONE (value=1)

### FAQ
**Q:** このカードとバトンタッチしてコスト11のメンバーが登場した場合、このカードの自動能力は発動できますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-013-R: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：手札からコスト4以下の「上原歩夢」のメンバーカードを1枚ステージに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}

### FAQ
**Q:** このカードの能力で「PL!N-sd1-013-SD上原歩夢」を登場させたとき、そのカードの登場能力は使用できますか？...
**A:** はい。できます。...

**Q:** このカードの能力で登場させたメンバーを、そのターンのうちにバトンタッチすることはできますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-013-P＋: 上原歩夢
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：手札からコスト4以下の「上原歩夢」のメンバーカードを1枚ステージに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}

### FAQ
**Q:** このカードの能力で「PL!N-sd1-013-SD上原歩夢」を登場させたとき、そのカードの登場能力は使用できますか？...
**A:** はい。できます。...

**Q:** このカードの能力で登場させたメンバーを、そのターンのうちにバトンタッチすることはできますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-014-R: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}「中須かすみ」からバトンタッチして登場した場合、カードを2枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-pb1-014-P＋: 中須かすみ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}「中須かすみ」からバトンタッチして登場した場合、カードを2枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-pb1-015-R: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：手札からコスト4以下の「桜坂しずく」のメンバーカードを1枚ステージに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}

### FAQ
**Q:** このカードの能力で登場させたメンバーを、そのターンのうちにバトンタッチすることはできますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-015-P＋: 桜坂しずく
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：手札からコスト4以下の「桜坂しずく」のメンバーカードを1枚ステージに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}

### FAQ
**Q:** このカードの能力で登場させたメンバーを、そのターンのうちにバトンタッチすることはできますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-016-R: 朝香果林
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを2枚見る。その中から「朝香果林」のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-016-P＋: 朝香果林
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを2枚見る。その中から「朝香果林」のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-017-R: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：手札からコスト4以下の「宮下愛」のメンバーカードを1枚ステージに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}

### FAQ
**Q:** このカードの能力で「PL!N-bp4-005-R、PL!N-bp4-005-P宮下愛」を登場させたとき、そのカードの登場能力は使用できますか？...
**A:** はい。できます。...

**Q:** このカードの能力で登場させたメンバーを、そのターンのうちにバトンタッチすることはできますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-017-P＋: 宮下 愛
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：手札からコスト4以下の「宮下愛」のメンバーカードを1枚ステージに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}

### FAQ
**Q:** このカードの能力で「PL!N-bp4-005-R、PL!N-bp4-005-P宮下愛」を登場させたとき、そのカードの登場能力は使用できますか？...
**A:** はい。できます。...

**Q:** このカードの能力で登場させたメンバーを、そのターンのうちにバトンタッチすることはできますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-018-R: 近江彼方
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを2枚見る。その中から「近江彼方」のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-018-P＋: 近江彼方
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを2枚見る。その中から「近江彼方」のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-019-R: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}「優木せつ菜」からバトンタッチして登場した場合、カードを2枚引き、手札を2枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-pb1-019-P＋: 優木せつ菜
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}「優木せつ菜」からバトンタッチして登場した場合、カードを2枚引き、手札を2枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-pb1-020-R: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}「エマ・ヴェルデ」からバトンタッチして登場した場合、カードを2枚引き、手札を2枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-pb1-020-P＋: エマ・ヴェルデ
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}「エマ・ヴェルデ」からバトンタッチして登場した場合、カードを2枚引き、手札を2枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=2
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-pb1-021-R: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを2枚見る。その中から「天王寺璃奈」のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-021-P＋: 天王寺璃奈
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを2枚見る。その中から「天王寺璃奈」のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-022-R: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}「三船栞子」からバトンタッチして登場した場合、カードを2枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-pb1-022-P＋: 三船栞子
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}「三船栞子」からバトンタッチして登場した場合、カードを2枚引き、手札を1枚控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1, DISCARD_HAND=1
  **Effect:** DRAW (value=2) → PLAYER
  **Effect:** SWAP_CARDS (value=2) {'target': 'discard', 'from': 'hand'}

---

## PL!N-pb1-023-R: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：手札からコスト4以下の「ミア・テイラー」のメンバーカードを1枚ステージに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}

### FAQ
**Q:** このカードの能力で「PL!N-PR-013-PRミア・テイラー」を登場させたとき、そのカードの登場能力は使用できますか？...
**A:** はい。できます。...

**Q:** このカードの能力で登場させたメンバーを、そのターンのうちにバトンタッチすることはできますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-023-P＋: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}{{icon_energy.png|E}}{{icon_energy.png|E}}支払ってもよい：手札からコスト4以下の「ミア・テイラー」のメンバーカードを1枚ステージに登場させる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** ENERGY=2 (optional)
  **Conditions:** COST_CHECK {'value': 4, 'comparison': 'LE'}
  **Effect:** RECOVER_MEMBER (value=1) → CARD_DISCARD {'auto_play': True, 'from': 'hand'}

### FAQ
**Q:** このカードの能力で「PL!N-PR-013-PRミア・テイラー」を登場させたとき、そのカードの登場能力は使用できますか？...
**A:** はい。できます。...

**Q:** このカードの能力で登場させたメンバーを、そのターンのうちにバトンタッチすることはできますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-024-R: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを2枚見る。その中から「鐘嵐珠」のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-024-P＋: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}自分のデッキの上からカードを2枚見る。その中から「鐘嵐珠」のメンバーカードを1枚公開して手札に加えてもよい。残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Effect:** LOOK_DECK (value=2)
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** REVEAL_CARDS (value=1)
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard'}

---

## PL!N-pb1-028-N: 朝香果林
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを2枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=2)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-pb1-034-N: 三船栞子
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{heart_03.png|heart03}}か{{heart_04.png|heart04}}か{{heart_05.png|heart05}}のうち1つを選ぶ。ライブ終了時まで、このメンバーが元々持つハートは選んだハートになる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}

---

## PL!N-pb1-035-N: ミア・テイラー
Type: メンバー

### Original Ability Text
```
{{toujyou.png|登場}}手札を1枚控え室に置いてもよい：自分のデッキの上からカードを2枚見る。その中から1枚を手札に加え、残りを控え室に置く。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_PLAY
  **Costs:** DISCARD_HAND=1 (optional), DISCARD_HAND=1 (optional)
  **Effect:** LOOK_DECK (value=2)
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'deck'}
  **Effect:** LOOK_AND_CHOOSE (value=1) {'source': 'looked'}
  **Effect:** ADD_TO_HAND (value=1) {'to': 'hand', 'from': 'discard'}
  **Effect:** SWAP_CARDS (value=1) {'target': 'discard', 'from': 'hand'}

---

## PL!N-pb1-036-N: 鐘 嵐珠
Type: メンバー

### Original Ability Text
```
{{live_start.png|ライブ開始時}}{{heart_01.png|heart01}}か{{heart_02.png|heart02}}か{{heart_06.png|heart06}}のうち1つを選ぶ。ライブ終了時まで、このメンバーが元々持つハートは選んだハートになる。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Effect:** BUFF_POWER (value=1) {'until': 'live_end', 'temporary': True}

---

## PL!N-pb1-037-L: Cara Tesoro
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}このターン、自分の『虹ヶ咲』のカードの効果によってウェイト状態の自分のエネルギーをアクティブにしていた場合、このカードのスコアを＋１する。さらに、自分の『虹ヶ咲』のカードの効果によって自分のステージにいるウェイト状態のメンバーもアクティブにしていた場合、代わりにスコアを＋２する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲'}, GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'STAGE'}
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT {'target': 'energy'}
  **Effect:** BOOST_SCORE (value=1)
  **Effect:** ACTIVATE_MEMBER (value=1) → MEMBER_SELECT
  **Effect:** BOOST_SCORE (value=2)
  **Effect:** REPLACE_EFFECT (value=2) {'replaces': 'score_boost'}

### FAQ
**Q:** 『虹ヶ咲』のカードの効果で自分のステージにいるウェイト状態のメンバーだけをアクティブにしていた場合、スコアは＋2されますか？...
**A:** いいえ。できません。...

---

## PL!N-pb1-038-L: PHOENIX
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場かライブ中のライブカードの中に、必要ハートに含まれる{{heart_01.png|heart01}}が4の『虹ヶ咲』のライブカードがある場合、このカードのスコアを＋１する。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'SUCCESS_LIVE'}, HAS_LIVE_CARD {}
  **Effect:** BOOST_SCORE (value=1)

---

## PL!N-pb1-039-L: Stellar Stream
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分の成功ライブカード置き場かライブ中のライブカードの中に、必要ハートに含まれる{{heart_01.png|heart01}}が3の『虹ヶ咲』のライブカードがある場合、ライブ終了時まで、自分のステージにいる{{heart_06.png|heart06}}を持つ『虹ヶ咲』のメンバー1人は{{heart_06.png|heart06}}{{heart_06.png|heart06}}{{heart_06.png|heart06}}{{heart_06.png|heart06}}を得る。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'SUCCESS_LIVE'}, GROUP_FILTER {'group': '虹ヶ咲', 'zone': 'SUCCESS_LIVE'}, HAS_LIVE_CARD {}
  **Effect:** ADD_HEARTS (value=6) → MEMBER_SELF {'until': 'live_end'}

---

## PL!N-pb1-042-L: Eternalize Love!!
Type: ライブ

### Original Ability Text
```
{{live_start.png|ライブ開始時}}自分のステージに同じ名前の『虹ヶ咲』のメンバーが2人以上いる場合、このカードを成功させるための必要ハートを{{heart_00.png|heart0}}{{heart_00.png|heart0}}{{heart_00.png|heart0}}減らす。
```

### Parsed Abilities
**Ability 1:**
  **Trigger:** ON_LIVE_START
  **Conditions:** COUNT_GROUP {'group': '虹ヶ咲', 'min': 2, 'zone': 'STAGE'}
  **Effect:** REDUCE_HEART_REQ (value=3) → PLAYER

### FAQ
**Q:** 自分のステージにいるメンバーが、「PL!N-pb1-016-R朝香果林」と「LL-bp4-001-R+絢瀬絵里&朝香果林&葉月恋」や「PL!N-pb1-021-R天王寺璃奈」と「LL-bp3-001-R+園田海未&津島善子&天王寺璃奈」のような状況でも、このカードのライブ開始時の効果の条件を満たしますか？...
**A:** はい。満たします。...

---
