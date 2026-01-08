# Detailed Rule Implementation Report (v1.04)

Analysis of `game_state.py` distinguishing active logic from indexed references.

| Rule | Status | Type/Reason | Line # | Description snippet |
| :--- | :--- | :--- | :--- | :--- |
| 1.1 | ⚠️ Index Only | General Concept / Game Structure | Appendix | ゲーム人数 |
| 1.1.1 | ⚠️ Index Only | General Concept / Game Structure | Appendix | このゲームは原則2 名のプレイヤーにより対戦を |
| 1.2 | ✅ Logic | Implemented in Game Engine | [Line 263](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L263) | ゲームの勝敗 |
| 1.2.1 | ✅ Logic | Implemented in Game Engine | [Line 348](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L348) | いずれかのプレイヤーが勝利した、または敗北した |
| 1.2.1.1 | ✅ Logic | Implemented in Game Engine | [Line 348](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L348) | いずれかのプレイヤーの成功ライブカード置 |
| 1.2.1.2 | ⚠️ Index Only | General Concept / Game Structure | Appendix | 両方のプレイヤーが同時に3 枚以上になっ |
| 1.2.2 | ⚠️ Index Only | General Concept / Game Structure | Appendix | すべてのプレイヤーが同時に敗北する場合、その |
| 1.2.3 | ⚠️ Index Only | General Concept / Game Structure | Appendix | すべてのプレイヤーは、ゲーム中の任意の時点で |
| 1.2.3.1 | ⚠️ Index Only | General Concept / Game Structure | Appendix | 投了を行う行為は、いかなるカードの影響も |
| 1.2.4 | ⚠️ Index Only | General Concept / Game Structure | Appendix | なんらかのカードにより、いずれかのプレイヤーが |
| 1.3 | ✅ Logic | Implemented in Game Engine | [Line 20](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L20) | ゲームの大原則 |
| 1.3.1 | ✅ Logic | Implemented in Game Engine | [Line 21](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L21) | カードに書かれているテキストの内容が総合ルー |
| 1.3.2 | ✅ Logic | Implemented in Game Engine | [Line 22](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L22) | なんらかの理由によりプレイヤーが実行不可能なこ |
| 1.3.2.1 | ⚠️ Index Only | General Concept / Game Structure | Appendix | すでにある状態にあるものを改めてその状 |
| 1.3.2.2 | ⚠️ Index Only | General Concept / Game Structure | Appendix | ある行動を実行する際の単位数や回数が0 |
| 1.3.2.3 | ⚠️ Index Only | General Concept / Game Structure | Appendix | ある行動を要求する効果が複数発生し、そ |
| 1.3.2.4 | ⚠️ Index Only | General Concept / Game Structure | Appendix | プレイヤーやカードが持つ数値情報は、特に |
| 1.3.3 | ✅ Logic | Implemented in Game Engine | [Line 23](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L23) | あるカードの効果によりプレイヤーがなんらかの行 |
| 1.3.4 | ✅ Logic | Implemented in Game Engine | [Line 24](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L24) | 複数のプレイヤーが同時になんらかの選択を行う |
| 1.3.4.1 | ⚠️ Index Only | General Concept / Game Structure | Appendix | ある効果が複数のプレイヤーに適用され、 |
| 1.3.4.2 | ⚠️ Index Only | General Concept / Game Structure | Appendix | 非公開領域のカードを同時に選択する場 |
| 1.3.5 | ✅ Logic | Implemented in Game Engine | [Line 25](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L25) | なんらかの数を選ぶ場合、0 以上の整数を選ぶ必 |
| 1.3.5.1 | ⚠️ Index Only | General Concept / Game Structure | Appendix | カードやルールにより‘～まで’のように上限 |
| 2.1 | ✅ Logic | Implemented in Game Engine | [Line 92](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L92) | ハートアイコン |
| 2.1.1 | ⚠️ Index Only | Visual / Asset Spec | Appendix | ハートアイコンは |
| 2.1.2 | ⚠️ Index Only | Visual / Asset Spec | Appendix | 同色のハートアイコンが複数重なって表記されてい |
| 2.1.3 | ⚠️ Index Only | Visual / Asset Spec | Appendix | ブレードハート（2.7）のハートアイコンはブレード |
| 2.2 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カードタイプ |
| 2.2.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | カードの種類を表す情報です。 |
| 2.2.2 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カードタイプは、‘ライブ’‘メンバー’‘エネルギー’の |
| 2.2.2.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カードタイプがライブであるカードは、ゲーム |
| 2.2.2.1.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | スコア（2.10）や必要ハート（2.11）を持つ |
| 2.2.2.2 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カードタイプがメンバーであるカードは、ライ |
| 2.2.2.2.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | コスト（2.6）やハート（2.9）を持つカード |
| 2.2.2.3 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カードタイプがエネルギーであるカードは、メ |
| 2.2.2.3.1 | ⚠️ Index Only | Visual / Asset Spec | Appendix | カード左下に‘エネルギーカード’と表記 |
| 2.3 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カード名 |
| 2.3.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | このカードの持つ固有名称です。 |
| 2.3.2 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カード名は他の能力や効果で参照することがありま |
| 2.3.2.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カード名に＆を含むメンバーカードは、＆で |
| 2.3.2.2 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | テキスト中、「」（かぎ括弧）で囲まれた名称 |
| 2.4 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | グループ名 |
| 2.4.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | カードが属するアイドルグループの名称です。 |
| 2.4.2 | ⚠️ Index Only | Visual / Asset Spec | Appendix | グループ名はロゴで表記され、そのロゴに対応した |
| 2.4.2.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カード名に＆を含むメンバーカードは、＆で |
| 2.4.2.2 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | メンバー名称とグループ名称の対応は、巻 |
| 2.4.3 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | グループ名は他の能力や効果で参照することがあ |
| 2.4.3.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | テキスト中、『』（二重かぎ括弧）で囲まれた |
| 2.4.4 | ⚠️ Index Only | Visual / Asset Spec | Appendix | ロゴとグループ名称の対応は、巻末の付録を参照 |
| 2.5 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | ユニット名 |
| 2.5.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | カードが属するユニットの名称です。 |
| 2.5.2 | ⚠️ Index Only | Visual / Asset Spec | Appendix | ユニット名はロゴで表記され、そのロゴに対応した |
| 2.5.3 | ⚠️ Index Only | Visual / Asset Spec | Appendix | ユニット名とロゴの対応は、巻末の付録を参照して |
| 2.6 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | コスト |
| 2.6.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | メンバーカードをプレイするためのコスト（9.6.2.3.1） |
| 2.7 | ✅ Logic | Implemented in Game Engine | [Line 94](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L94) | ブレードハート |
| 2.7.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | エール（8.3.11）により実行する処理の内容を示すア |
| 2.7.2 | ⚠️ Index Only | Visual / Asset Spec | Appendix | アイコンとそれに対応する処理の内容に関しては、 |
| 2.8 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | ブレード |
| 2.8.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | メンバーがエール（8.3.11）による処理で公開する |
| 2.8.2 | ⚠️ Index Only | Visual / Asset Spec | Appendix | ブレードの数値はブレードアイコン |
| 2.9 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | ハート |
| 2.9.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | ライブ成功判定（8.3.14）を行う際にプレイヤーが得 |
| 2.9.2 | ⚠️ Index Only | Visual / Asset Spec | Appendix | ハートはハートアイコン（2.1）で示されます。 |
| 2.9.3 | ⚠️ Index Only | Visual / Asset Spec | Appendix | メンバーのハート表記では、複数のハートアイコン |
| 2.10 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | スコア |
| 2.10.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | ライブが成功した場合にこのライブカードにより得 |
| 2.11 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | 必要ハート |
| 2.11.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | ライブを成功させるために必要とするハートの数で |
| 2.11.2 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | 必要ハートは、ハート音符（右 |
| 2.11.2.1 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | 各ハート音符は、縦に |
| 2.11.2.2 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | ハート音符が複数ある場合、その全てを同 |
| 2.11.3 | ⚠️ Index Only | Visual / Asset Spec | Appendix | 与えられた数と種類のハートアイコンは、以下の |
| 2.12 | ✅ Logic | Implemented in Game Engine | [Line 92](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L92) | カードテキスト |
| 2.12.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | このカードが持つ固有の能力を示す情報です。 |
| 2.12.2 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カードテキスト（2.12）で『』（二重かぎ括弧）で指定 |
| 2.12.3 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カードテキストで「」（かぎ括弧）で指定した名称を |
| 2.12.4 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カードテキストの中に、（）（丸括弧）で囲まれた、能 |
| 2.13 | ⚠️ Index Only | Definition / Descriptive | Appendix | イラスト |
| 2.13.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | カードの内容をイメージしたイラストです。 |
| 2.13.2 | ⚠️ Index Only | Definition / Descriptive | Appendix | イラストは、ゲーム上は特に意味を持ちません。 |
| 2.14 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | 付帯条項 |
| 2.14.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | カードナンバー、イラストレーター表記、カードの著 |
| 2.14.2 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カードナンバーはデッキ構築の際に参照します。 |
| 2.14.3 | ⚠️ Index Only | Data Structure / Asset Definition | Appendix | カードナンバー以外の付帯条項は、ゲーム上は特 |
| 3.1 | ⚠️ Index Only | See Index for Details | Appendix | オーナーとマスター |
| 3.1.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | オーナーとは、カードの物理的な所有者を指しま |
| 3.1.2 | ⚠️ Index Only | Definition / Descriptive | Appendix | マスターとは、カードや能力や効果などを現在使用 |
| 3.1.2.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | 常時能力のマスターとは、その能力を有する |
| 3.1.2.2 | ⚠️ Index Only | Definition / Descriptive | Appendix | 起動能力のマスターとは、それをプレイした |
| 3.1.2.3 | ⚠️ Index Only | Definition / Descriptive | Appendix | 自動能力のマスターとは、その能力を有する |
| 3.1.2.4 | ⚠️ Index Only | Definition / Descriptive | Appendix | 効果のマスターとは、その効果を発生した能 |
| 3.1.2.4.1 | ⚠️ Index Only | See Index for Details | Appendix | ある効果により特にプレイヤーが指定 |
| 4.1 | ✅ Logic | Implemented in Game Engine | [Line 140](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L140) | 領域の基本 |
| 4.1.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 領域は、特に指定がない限り、各プレイヤーがそれ |
| 4.1.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 領域によっては、そこに置かれているカードの内容 |
| 4.1.2.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 公開領域にカードが置かれる場合、その |
| 4.1.2.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 領域が公開であるか非公開であるかにかか |
| 4.1.2.3 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 非公開領域においては、その領域のカード |
| 4.1.3 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 領域によっては、そこに置かれるカードの順番が管 |
| 4.1.3.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 順番を管理する領域のカードの順番は、 |
| 4.1.4 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | カードがメンバーエリアからメンバーエリアあるいは |
| 4.1.4.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | あるカードによる効果内で、その効果が移動 |
| 4.1.5 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 複数のカードがある領域に同時に置かれる場合、 |
| 4.1.5.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 公開領域から非公開領域に複数のカードが |
| 4.1.6 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | あるカードが持つテキストや能力や効果において、 |
| 4.1.7 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | あるカードがメンバーエリアやライブカード置き場以 |
| 4.2 | ✅ Logic | Implemented in Game Engine | [Line 136](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L136) | 領域の可視状態 |
| 4.2.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 領域内にあるカードは、公開状態か非公開状態か |
| 4.2.2 | ⚠️ Index Only | Definition / Descriptive | Appendix | 公開状態とは、カードの内容や情報をすべてのプレ |
| 4.2.3 | ⚠️ Index Only | Definition / Descriptive | Appendix | 非公開状態とは、一部または全部のプレイヤーが |
| 4.3 | ✅ Logic | Implemented in Game Engine | [Line 137](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L137) | カードの配置状態 |
| 4.3.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 一部の領域において、カードの配置状態が指定さ |
| 4.3.2 | ⚠️ Index Only | Physical Component Spec | Appendix | 向きを表す状態は、‘アクティブ状態’、‘ウェイト状 |
| 4.3.2.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | アクティブ状態のカードは、そのカードのマス |
| 4.3.2.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | ウェイト状態のカードは、そのカードのマス |
| 4.3.2.3 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 配置状態が指定される領域にカードが置か |
| 4.3.3 | ⚠️ Index Only | Physical Component Spec | Appendix | 表示面を表す状態は、‘表向き’か‘裏向き’のいず |
| 4.3.3.1 | ⚠️ Index Only | Physical Component Spec | Appendix | 表向き状態のカードは、カードの情報が書か |
| 4.3.3.2 | ⚠️ Index Only | Physical Component Spec | Appendix | 裏向き状態のカードは、カードの情報が書か |
| 4.4 | ✅ Logic | Implemented in Game Engine | [Line 135](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L135) | ステージ |
| 4.4.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | プレイヤーのメンバーエリアを統合した領域です。 |
| 4.4.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | プレイヤーはステージ内に自身のメンバーエリア |
| 4.5 | ✅ Logic | Implemented in Game Engine | [Line 848](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L848) | メンバーエリア |
| 4.5.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | プレイしたメンバーカードを置く領域です。 |
| 4.5.1.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | テキスト等で単に‘エリア’と書かれている場 |
| 4.5.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | プレイヤーはメンバーエリアを3 つ持ちます。 |
| 4.5.2.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 各メンバーエリアは、それぞれ‘左サイドエリ |
| 4.5.2.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 同一プレイヤーに属する、左サイドエリアは |
| 4.5.2.3 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 同一プレイヤーに属する、左サイドエリアと |
| 4.5.3 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | メンバーエリアはすべてのプレイヤーに対して公開 |
| 4.5.4 | ✅ Logic | Implemented in Game Engine | [Line 861](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L861) | メンバーエリアのメンバーカードは向きを示す配置 |
| 4.5.5 | ✅ Logic | Implemented in Game Engine | [Line 848](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L848) | メンバーエリアのメンバーカードの下に、エネル |
| 4.5.5.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | メンバーエリアのメンバーカードの下に重ね |
| 4.5.5.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | メンバーエリアのメンバーカードの下に重ね |
| 4.5.5.3 | ✅ Logic | Implemented in Game Engine | [Line 848](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L848) | メンバーエリアのメンバーが他のメンバーエ |
| 4.5.5.4 | ✅ Logic | Implemented in Game Engine | [Line 1222](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1222) | メンバーエリアのメンバーがメンバーエリア |
| 4.5.6 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | テキスト等で、特に領域を指定せずに‘メンバー’を |
| 4.6 | ✅ Logic | Implemented in Game Engine | [Line 139](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L139) | ライブカード置き場 |
| 4.6.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | プレイヤーが実行するライブカードを置く領域です。 |
| 4.6.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | ライブカード置き場はすべてのプレイヤーに対して |
| 4.7 | ✅ Logic | Implemented in Game Engine | [Line 138](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L138) | エネルギー置き場 |
| 4.7.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | エネルギーカードを置く領域です。 |
| 4.7.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | エネルギー置き場はすべてのプレイヤーに対して |
| 4.7.3 | ⚠️ Index Only | Physical Component Spec | Appendix | エネルギー置き場のカードは向きを示す配置状態 |
| 4.7.4 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | テキスト等で単に‘エネルギー’を参照する場合、そ |
| 4.8 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | メインデッキ置き場 |
| 4.8.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | ゲーム開始時に自分のメインデッキを置く領域で |
| 4.8.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | メインデッキ置き場はすべてのプレイヤーに対して |
| 4.8.3 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | メインデッキ置き場のカードを他の領域に複数枚移 |
| 4.8.4 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | テキスト等で単に‘デッキ’を参照する場合、それは |
| 4.9 | ✅ Logic | Implemented in Game Engine | [Line 141](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L141) | エネルギーデッキ置き場 |
| 4.9.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | ゲーム開始時に自分のエネルギーデッキを置く領 |
| 4.9.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | エネルギーデッキ置き場はすべてのプレイヤーに |
| 4.9.3 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | エネルギーデッキ置き場のカードを他の領域に複 |
| 4.9.4 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | テキスト等で単に‘エネルギーデッキ’を参照する場 |
| 4.10 | ✅ Logic | Implemented in Game Engine | [Line 140](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L140) | 成功ライブカード置き場 |
| 4.10.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | ゲーム中に成功したライブのライブカードを置く領 |
| 4.10.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 成功ライブカード置き場はすべてのプレイヤーに |
| 4.11 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 手札 |
| 4.11.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 各プレイヤーが未使用のカードを相手に見せずに |
| 4.11.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 手札は非公開領域ですが、自分の手札のカード |
| 4.11.3 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | ‘手札にあるカードを（数値）枚’は、カードテキスト |
| 4.12 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 控え室 |
| 4.12.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 各プレイヤーの使用済みのカードが置かれる領域 |
| 4.12.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 控え室は公開領域で、カードの順番は管理されま |
| 4.13 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 除外領域 |
| 4.13.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | ゲームから取り除かれたカードを置く領域です。 |
| 4.13.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 除外領域は原則として公開領域で、この領域の |
| 4.14 | ✅ Logic | Implemented in Game Engine | [Line 262](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L262) | 解決領域 |
| 4.14.1 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | ゲームの進行中に、能力やカードが一時的に置か |
| 4.14.2 | ⚠️ Index Only | Zone Definition (Implicit in State) | Appendix | 解決領域は公開領域で、カードの順番が管理され |
| 5.1 | ⚠️ Index Only | See Index for Details | Appendix | 概要 |
| 5.1.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | 特定行動とは、このゲームを行う際に特別な意味を |
| 5.2 | ⚠️ Index Only | See Index for Details | Appendix | アクティブにする/ウェイトにする |
| 5.2.1 | ⚠️ Index Only | See Index for Details | Appendix | カードを‘アクティブにする’または‘ウェイトにする’ |
| 5.3 | ⚠️ Index Only | See Index for Details | Appendix | 表にする/裏にする |
| 5.3.1 | ⚠️ Index Only | See Index for Details | Appendix | カードを‘表にする’または‘裏にする’指示がある |
| 5.4 | ⚠️ Index Only | See Index for Details | Appendix | 置く |
| 5.4.1 | ⚠️ Index Only | See Index for Details | Appendix | カードを指定領域に‘置く’指示がある場合、その |
| 5.5 | ⚠️ Index Only | See Index for Details | Appendix | シャッフルする |
| 5.5.1 | ⚠️ Index Only | See Index for Details | Appendix | 指定されたカード群を‘シャッフルする’指示がある |
| 5.5.1.1 | ⚠️ Index Only | See Index for Details | Appendix | カード群として単に領域名が指定された場 |
| 5.5.1.2 | ⚠️ Index Only | See Index for Details | Appendix | カード群のカードが0 枚または1 枚の状態 |
| 5.6 | ✅ Logic | Implemented in Game Engine | [Line 1194](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1194) | 引く |
| 5.6.1 | ⚠️ Index Only | See Index for Details | Appendix | カードを‘1 枚引く’指示がある場合、指定プレイ |
| 5.6.2 | ⚠️ Index Only | See Index for Details | Appendix | カードを‘（数値）枚引く’指示がある場合、指定プレ |
| 5.6.3 | ⚠️ Index Only | See Index for Details | Appendix | カードを‘（数値）枚まで引く’指示がある場合、指定 |
| 5.6.3.1 | ⚠️ Index Only | See Index for Details | Appendix | （数値）が0 以下である場合は、この指示を |
| 5.6.3.2 | ⚠️ Index Only | See Index for Details | Appendix | 指定プレイヤーはこの指示を終了することが |
| 5.6.3.3 | ⚠️ Index Only | See Index for Details | Appendix | 指定プレイヤーはカードを1 枚引きます。 |
| 5.6.3.4 | ⚠️ Index Only | See Index for Details | Appendix | この指示により5.6.3.3 を実行した回数が（数 |
| 5.7 | ✅ Logic | Implemented in Game Engine | [Line 764](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L764) | 上から見る |
| 5.7.1 | ⚠️ Index Only | See Index for Details | Appendix | ‘メインデッキ置き場を上から（数値）枚見る’指示が |
| 5.7.2 | ⚠️ Index Only | See Index for Details | Appendix | ‘メインデッキ置き場を上から（数値）枚まで見る’指 |
| 5.7.2.1 | ⚠️ Index Only | See Index for Details | Appendix | （数値）が0 以下である場合は、この指示を |
| 5.7.2.2 | ⚠️ Index Only | See Index for Details | Appendix | 枚数として1 を指定します。 |
| 5.7.2.3 | ⚠️ Index Only | See Index for Details | Appendix | 指定プレイヤーはこの指示を終了することが |
| 5.7.2.4 | ⚠️ Index Only | See Index for Details | Appendix | 指定プレイヤーは、メインデッキ置き場の一 |
| 5.7.2.5 | ⚠️ Index Only | See Index for Details | Appendix | この指示により5.7.2.4 を実行した回数が（数 |
| 5.8 | ✅ Logic | Implemented in Game Engine | [Line 768](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L768) | 入れ替える |
| 5.8.1 | ⚠️ Index Only | See Index for Details | Appendix | あるカードと別なカードを‘入れ替える’指示がある |
| 5.8.2 | ⚠️ Index Only | See Index for Details | Appendix | 何らかの理由で、入れ替える指示の実行時にいず |
| 5.9.1 | ⚠️ Index Only | See Index for Details | Appendix | あるプレイヤーが’ |
| 5.9.1.1 | ⚠️ Index Only | See Index for Details | Appendix | ‘ |
| 5.10 | ⚠️ Index Only | See Index for Details | Appendix | （エネルギーをメンバーの）下に置く |
| 5.10.1 | ⚠️ Index Only | See Index for Details | Appendix | あるエネルギーカードをあるメンバーの‘下に置く’ |
| 6.1 | ⚠️ Index Only | See Index for Details | Appendix | デッキの準備 |
| 6.1.1 | ⚠️ Index Only | See Index for Details | Appendix | 各プレイヤーは、ゲームの開始前に自身のカードに |
| 6.1.1.1 | ⚠️ Index Only | See Index for Details | Appendix | メインデッキは、メンバーカード48 枚ちょうど |
| 6.1.1.2 | ⚠️ Index Only | See Index for Details | Appendix | メインデッキには、カードナンバーが同一で |
| 6.1.1.3 | ⚠️ Index Only | See Index for Details | Appendix | エネルギーデッキは、エネルギーカード12 |
| 6.1.2 | ⚠️ Index Only | See Index for Details | Appendix | デッキの構築条件に関する常時能力は、上記の |
| 6.2 | ✅ Logic | Implemented in Game Engine | [Line 1161](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1161) | ゲーム前の手順 |
| 6.2.1 | ✅ Logic | Implemented in Game Engine | [Line 1161](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1161) | ゲームの開始前に、各プレイヤーは以下の手順を |
| 6.2.1.1 | ⚠️ Index Only | See Index for Details | Appendix | このゲームで使用する自身のデッキを提示 |
| 6.2.1.2 | ⚠️ Index Only | See Index for Details | Appendix | 各プレイヤーは自身のメインデッキを自身の |
| 6.2.1.3 | ⚠️ Index Only | See Index for Details | Appendix | 各プレイヤーは自身のエネルギーデッキを |
| 6.2.1.4 | ⚠️ Index Only | See Index for Details | Appendix | 各プレイヤーは無作為にどちらのプレイヤー |
| 6.2.1.5 | ⚠️ Index Only | See Index for Details | Appendix | 各プレイヤーは自身のメインデッキ置き場の |
| 6.2.1.6 | ✅ Logic | Implemented in Game Engine | [Line 1161](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1161) | 先攻プレイヤーから順に、各プレイヤーは自 |
| 6.2.1.7 | ✅ Logic | Implemented in Game Engine | [Line 1766](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1766) | 各プレイヤーは自身のエネルギーデッキ置 |
| 7.1 | ⚠️ Index Only | See Index for Details | Appendix | 概要 |
| 7.1.1 | ⚠️ Index Only | See Index for Details | Appendix | ゲームは‘ターン’と呼ばれる手順を繰り返すことで |
| 7.1.2 | ⚠️ Index Only | See Index for Details | Appendix | 各ターンは、‘先攻通常フェイズ’、‘後攻通常フェイ |
| 7.2 | ⚠️ Index Only | See Index for Details | Appendix | アクティブプレイヤー |
| 7.2.1 | ⚠️ Index Only | See Index for Details | Appendix | ゲーム中のフェイズにおいて、手番プレイヤーを指 |
| 7.2.1.1 | ⚠️ Index Only | See Index for Details | Appendix | 手番プレイヤーを指定するフェイズ中は、手 |
| 7.2.1.2 | ⚠️ Index Only | See Index for Details | Appendix | 手番プレイヤーを指定しないフェイズ中は、 |
| 7.2.2 | ⚠️ Index Only | See Index for Details | Appendix | アクティブプレイヤーでないもう一方のプレイヤーは |
| 7.3 | ⚠️ Index Only | See Index for Details | Appendix | 通常フェイズ |
| 7.3.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | 通常フェイズとは、いずれかのプレイヤーが一連の |
| 7.3.2 | ⚠️ Index Only | See Index for Details | Appendix | 各通常フェイズでは手番プレイヤーを1 人指定し、 |
| 7.3.2.1 | ⚠️ Index Only | See Index for Details | Appendix | 通常フェイズには、先攻プレイヤーが手番プ |
| 7.3.3 | ⚠️ Index Only | See Index for Details | Appendix | 通常フェイズでは、‘アクティブフェイズ’（7.4）、‘エ |
| 7.4 | ✅ Logic | Implemented in Game Engine | [Line 1139](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1139) | アクティブフェイズ |
| 7.4.1 | ⚠️ Index Only | See Index for Details | Appendix | 手番プレイヤーは、自身のエネルギー置き場とメン |
| 7.4.2 | ⚠️ Index Only | See Index for Details | Appendix | ‘ターンの始めに’および‘アクティブフェイズの始め |
| 7.4.3 | ⚠️ Index Only | See Index for Details | Appendix | チェックタイミングが発生します。このチェックタイミ |
| 7.5 | ✅ Logic | Implemented in Game Engine | [Line 1147](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1147) | エネルギーフェイズ |
| 7.5.1 | ⚠️ Index Only | See Index for Details | Appendix | ‘エネルギーフェイズの始めに’の誘発条件が発生 |
| 7.5.2 | ⚠️ Index Only | See Index for Details | Appendix | 手番プレイヤーは、自身のエネルギーデッキの一 |
| 7.5.3 | ⚠️ Index Only | See Index for Details | Appendix | チェックタイミングが発生します。このチェックタイミ |
| 7.6 | ✅ Logic | Implemented in Game Engine | [Line 1155](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1155) | ドローフェイズ |
| 7.6.1 | ⚠️ Index Only | See Index for Details | Appendix | ‘ドローフェイズの始めに’の誘発条件が発生し、 |
| 7.6.2 | ⚠️ Index Only | See Index for Details | Appendix | 手番プレイヤーはカードを1 枚引きます。 |
| 7.6.3 | ⚠️ Index Only | See Index for Details | Appendix | チェックタイミングが発生します。このチェックタイミ |
| 7.7 | ⚠️ Index Only | See Index for Details | Appendix | メインフェイズ |
| 7.7.1 | ⚠️ Index Only | See Index for Details | Appendix | ‘メインフェイズの始めに’の誘発条件が発生し、 |
| 7.7.2 | ⚠️ Index Only | See Index for Details | Appendix | 手番プレイヤーにプレイタイミング（9.5.2）が与えら |
| 7.7.2.1 | ⚠️ Index Only | See Index for Details | Appendix | 自分のカードが持つ起動能力を1 つ選び、 |
| 7.7.2.2 | ⚠️ Index Only | See Index for Details | Appendix | 自分の手札のメンバーカードを1 枚選び、そ |
| 7.7.3 | ⚠️ Index Only | See Index for Details | Appendix | メインフェイズが終了します。 |
| 7.8 | ⚠️ Index Only | See Index for Details | Appendix | ライブフェイズ |
| 7.8.1 | ⚠️ Index Only | See Index for Details | Appendix | 両プレイヤーはライブフェイズを実行します。詳しく |
| 8.1 | ⚠️ Index Only | See Index for Details | Appendix | 概要 |
| 8.1.1 | ⚠️ Index Only | See Index for Details | Appendix | ライブフェイズでは、両プレイヤーが手札のライブ |
| 8.1.2 | ⚠️ Index Only | See Index for Details | Appendix | ライブフェイズでは、‘ライブカードセットフェイズ’ |
| 8.2 | ⚠️ Index Only | See Index for Details | Appendix | ライブカードセットフェイズ |
| 8.2.1 | ⚠️ Index Only | See Index for Details | Appendix | ‘ライブフェイズの始めに’および‘ライブカードセット |
| 8.2.2 | ⚠️ Index Only | See Index for Details | Appendix | 先攻プレイヤーは、自身の手札のカードを3 枚まで |
| 8.2.3 | ⚠️ Index Only | See Index for Details | Appendix | チェックタイミングが発生します。 |
| 8.2.4 | ⚠️ Index Only | See Index for Details | Appendix | 後攻プレイヤーは、自身の手札のカードを3 枚まで |
| 8.2.5 | ⚠️ Index Only | See Index for Details | Appendix | チェックタイミングが発生します。このチェックタイミ |
| 8.3 | ✅ Logic | Implemented in Game Engine | [Line 163](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L163) | パフォーマンスフェイズ |
| 8.3.1 | ✅ Logic | Implemented in Game Engine | [Line 163](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L163) | パフォーマンスフェイズとは、いずれかのプレイ |
| 8.3.2 | ⚠️ Index Only | See Index for Details | Appendix | 各パフォーマンスフェイズでは手番プレイヤーを1 |
| 8.3.2.1 | ⚠️ Index Only | See Index for Details | Appendix | パフォーマンスフェイズには、先攻プレイ |
| 8.3.3 | ⚠️ Index Only | See Index for Details | Appendix | 手番プレイヤーの自動能力の‘パフォーマンスフェ |
| 8.3.4 | ✅ Logic | Implemented in Game Engine | [Line 165](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L165) | 手番プレイヤーは自身のライブカード置き場のカー |
| 8.3.4.1 | ✅ Logic | Implemented in Game Engine | [Line 165](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L165) | 手番プレイヤーが‘ライブできない’状態であ |
| 8.3.5 | ⚠️ Index Only | See Index for Details | Appendix | チェックタイミングが発生します。 |
| 8.3.6 | ⚠️ Index Only | See Index for Details | Appendix | この時点で手番プレイヤーのライブカード置き場に |
| 8.3.7 | ⚠️ Index Only | See Index for Details | Appendix | 手番プレイヤーのライブカード置き場にライブカード |
| 8.3.8 | ⚠️ Index Only | See Index for Details | Appendix | ‘ライブ開始時’の事象が発生します（11.4）。 |
| 8.3.9 | ⚠️ Index Only | See Index for Details | Appendix | チェックタイミングが発生します。 |
| 8.3.10 | ⚠️ Index Only | See Index for Details | Appendix | 手番プレイヤーは、自身のアクティブ状態なメン |
| 8.3.11 | ✅ Logic | Implemented in Game Engine | [Line 1353](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1353) | 手番プレイヤーは、自身のメインデッキの一番上 |
| 8.3.12 | ✅ Logic | Implemented in Game Engine | [Line 1355](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1355) | 手番プレイヤーは解決領域に置かれているすべ |
| 8.3.13 | ✅ Logic | Implemented in Game Engine | [Line 1372](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1372) | チェックタイミングが発生します。 |
| 8.3.14 | ✅ Logic | Implemented in Game Engine | [Line 1379](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1379) | 手番プレイヤーは自身のすべてのメンバーのハー |
| 8.3.15 | ✅ Logic | Implemented in Game Engine | [Line 163](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L163) | 手番プレイヤーはライブカード置き場の各ライブ |
| 8.3.15.1 | ✅ Logic | Implemented in Game Engine | [Line 1394](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1394) | 現在のライブ所有ハートにより、そのライブ |
| 8.3.15.1.1 | ⚠️ Index Only | See Index for Details | Appendix | その際、各 |
| 8.3.15.1.2 | ⚠️ Index Only | See Index for Details | Appendix | これによりそのライブカードの必要 |
| 8.3.16 | ✅ Logic | Implemented in Game Engine | [Line 1400](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1400) | 前述の手順によりいずれかのライブカードの必要 |
| 8.3.17 | ✅ Logic | Implemented in Game Engine | [Line 1414](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1414) | チェックタイミングが発生します。このチェックタイミ |
| 8.4 | ✅ Logic | Implemented in Game Engine | [Line 1355](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1355) | ライブ勝敗判定フェイズ |
| 8.4.1 | ✅ Logic | Implemented in Game Engine | [Line 1541](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1541) | ‘ライブ判定フェイズの始めに’の誘発条件が発生 |
| 8.4.2 | ✅ Logic | Implemented in Game Engine | [Line 1355](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1355) | ライブカード置き場にカードがあるプレイヤーは、自 |
| 8.4.2.1 | ⚠️ Index Only | See Index for Details | Appendix | その際、各プレイヤーは自身のエールの |
| 8.4.3 | ⚠️ Index Only | See Index for Details | Appendix | ライブの合計スコアを比較する場合、それは以下の |
| 8.4.3.1 | ⚠️ Index Only | See Index for Details | Appendix | 両方のプレイヤーのどちらのライブカード置 |
| 8.4.3.2 | ⚠️ Index Only | See Index for Details | Appendix | 一方のプレイヤーのライブカード置き場に |
| 8.4.3.3 | ⚠️ Index Only | See Index for Details | Appendix | 両方のプレイヤーのライブカード置き場に |
| 8.4.4 | ✅ Logic | Implemented in Game Engine | [Line 1510](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1510) | ライブカード置き場にカードがあるプレイヤーは、ラ |
| 8.4.5 | ⚠️ Index Only | See Index for Details | Appendix | チェックタイミングが発生します。 |
| 8.4.6 | ✅ Logic | Implemented in Game Engine | [Line 1496](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1496) | 合計スコアを比較し、ライブに勝利したプレイヤーを |
| 8.4.6.1 | ✅ Logic | Implemented in Game Engine | [Line 1504](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1504) | 両方のプレイヤーのどちらのライブカード置 |
| 8.4.6.2 | ✅ Logic | Implemented in Game Engine | [Line 1507](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1507) | いずれかのプレイヤーのライブカード置き場 |
| 8.4.7 | ✅ Logic | Implemented in Game Engine | [Line 1523](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1523) | ライブに勝利したプレイヤーは、自身のライブカード |
| 8.4.7.1 | ⚠️ Index Only | See Index for Details | Appendix | 両方のプレイヤーが勝利している場合 |
| 8.4.8 | ✅ Logic | Implemented in Game Engine | [Line 1533](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1533) | 各プレイヤーは、自身のライブ置き場に残っている |
| 8.4.9 | ⚠️ Index Only | See Index for Details | Appendix | チェックタイミングが発生します。 |
| 8.4.10 | ⚠️ Index Only | See Index for Details | Appendix | ‘ターンの終わりに’で示されている誘発条件のう |
| 8.4.11 | ✅ Logic | Implemented in Game Engine | [Line 1548](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1548) | チェックタイミングが発生します。このチェックタイミ |
| 8.4.12 | ⚠️ Index Only | See Index for Details | Appendix | この時点で、8.4.11 のチェックタイミングで自動能 |
| 8.4.13 | ✅ Logic | Implemented in Game Engine | [Line 1541](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1541) | 8.4.7 において、一方のプレイヤーのみが成功ライ |
| 8.4.14 | ✅ Logic | Implemented in Game Engine | [Line 1556](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1556) | このターンを終了します。 |
| 9.1 | ⚠️ Index Only | See Index for Details | Appendix | 能力の種別 |
| 9.1.1 | ⚠️ Index Only | See Index for Details | Appendix | 能力は、起動能力、自動能力、常時能力の3 種類 |
| 9.1.1.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | 起動能力とは、プレイタイミングが与えられ |
| 9.1.1.1.1 | ⚠️ Index Only | See Index for Details | Appendix | 起動能力は、カード上では‘ |
| 9.1.1.2 | ⚠️ Index Only | Definition / Descriptive | Appendix | 自動能力とは、その能力に示された事象が |
| 9.1.1.2.1 | ⚠️ Index Only | See Index for Details | Appendix | 自動能力は、カード上では‘ |
| 9.1.1.3 | ⚠️ Index Only | Definition / Descriptive | Appendix | 常時能力とは、その能力が有効な期間、常 |
| 9.1.1.3.1 | ⚠️ Index Only | See Index for Details | Appendix | 常時能力は、カード上では‘ |
| 9.2 | ⚠️ Index Only | See Index for Details | Appendix | 効果の種別 |
| 9.2.1 | ⚠️ Index Only | See Index for Details | Appendix | 効果は‘単発効果’‘継続効果’‘置換効果’の3 種 |
| 9.2.1.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | ‘単発効果’とは、解決中にその指示を実行 |
| 9.2.1.2 | ⚠️ Index Only | Definition / Descriptive | Appendix | ‘継続効果’とは、一定の期限の間（期間が |
| 9.2.1.3 | ⚠️ Index Only | Definition / Descriptive | Appendix | ‘置換効果’とは、ゲーム中にある事象が発 |
| 9.2.1.3.1 | ⚠️ Index Only | See Index for Details | Appendix | 能力に‘（行動A）する時、かわりに（行 |
| 9.2.1.3.2 | ⚠️ Index Only | See Index for Details | Appendix | 能力に‘（行動A）する時、かわりに[選 |
| 9.3 | ⚠️ Index Only | See Index for Details | Appendix | 有効な能力と無効な能力 |
| 9.3.1 | ⚠️ Index Only | See Index for Details | Appendix | 何らかの効果により、特定の効果が‘有効’であっ |
| 9.3.2 | ⚠️ Index Only | See Index for Details | Appendix | 何らかの効果の一部あるいは全部が特定の条件 |
| 9.3.3 | ⚠️ Index Only | See Index for Details | Appendix | 何らかの効果の一部あるいは全部が特定の条件 |
| 9.3.4 | ⚠️ Index Only | See Index for Details | Appendix | 能力は原則として以下の条件で有効になります。 |
| 9.3.4.1 | ⚠️ Index Only | See Index for Details | Appendix | 特定の領域や特定の状況でのプレイまたは |
| 9.3.4.1.1 | ⚠️ Index Only | See Index for Details | Appendix | あるカードのプレイ時やそのカードを特 |
| 9.3.4.2 | ⚠️ Index Only | See Index for Details | Appendix | カードタイプがメンバーであるカードの能力 |
| 9.3.4.3 | ⚠️ Index Only | See Index for Details | Appendix | カードタイプがライブであるカードの能力は、 |
| 9.4 | ✅ Logic | Implemented in Game Engine | [Line 979](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L979) | コストと支払い |
| 9.4.1 | ⚠️ Index Only | See Index for Details | Appendix | 起動能力や自動能力の先頭に、‘：’（コロン）の手 |
| 9.4.2 | ✅ Logic | Implemented in Game Engine | [Line 980](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L980) | ‘コストを支払う’とは’コストで示された行動を実行 |
| 9.4.2.1 | ⚠️ Index Only | See Index for Details | Appendix | コストに複数の行動がある場合、テキストの |
| 9.4.2.2 | ✅ Logic | Implemented in Game Engine | [Line 980](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L980) | コストのうち一部または全部を支払うことが |
| 9.4.3 | ⚠️ Index Only | See Index for Details | Appendix | コストのうち |
| 9.5 | ✅ Logic | Implemented in Game Engine | [Line 358](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L358) | チェックタイミングとプレイタイミング |
| 9.5.1 | ✅ Logic | Implemented in Game Engine | [Line 502](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L502) | チェックタイミングとは、ゲーム中で発生したルール |
| 9.5.1.1 | ⚠️ Index Only | See Index for Details | Appendix | チェックタイミングにおいては、まずルール処 |
| 9.5.2 | ⚠️ Index Only | Definition / Descriptive | Appendix | プレイタイミングとは、指定されたプレイヤーが能動 |
| 9.5.3 | ✅ Logic | Implemented in Game Engine | [Line 560](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L560) | チェックタイミングが発生した場合、ゲームは以下 |
| 9.5.3.1 | ⚠️ Index Only | See Index for Details | Appendix | 現在処理を行うべきルール処理すべてを同 |
| 9.5.3.2 | ✅ Logic | Implemented in Game Engine | [Line 620](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L620) | プレイヤーがマスターであるいずれかの自 |
| 9.5.3.3 | ✅ Logic | Implemented in Game Engine | [Line 643](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L643) | 非アクティブプレイヤーがマスターであるい |
| 9.5.3.4 | ⚠️ Index Only | See Index for Details | Appendix | チェックタイミングを終了します。 |
| 9.5.4 | ✅ Logic | Implemented in Game Engine | [Line 358](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L358) | いずれかのプレイヤーにプレイタイミングが発生し |
| 9.5.4.1 | ✅ Logic | Implemented in Game Engine | [Line 507](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L507) | チェックタイミングが発生します。チェックタイ |
| 9.5.4.2 | ⚠️ Index Only | See Index for Details | Appendix | プレイタイミングが実際にそのプレイヤーに |
| 9.5.4.3 | ⚠️ Index Only | See Index for Details | Appendix | プレイタイミングを与えられたプレイヤーが |
| 9.6 | ✅ Logic | Implemented in Game Engine | [Line 431](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L431) | プレイと解決 |
| 9.6.1 | ⚠️ Index Only | See Index for Details | Appendix | 起動能力や自動能力や手札のカードは、プレイす |
| 9.6.2 | ✅ Logic | Implemented in Game Engine | [Line 431](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L431) | カードや能力をプレイする場合は、以下の手順に従 |
| 9.6.2.1 | ✅ Logic | Implemented in Game Engine | [Line 431](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L431) | プレイする能力や手札のカードを指定しま |
| 9.6.2.1.1 | ✅ Logic | Implemented in Game Engine | [Line 1211](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1211) | プレイするのがカードである場合、それ |
| 9.6.2.1.2 | ✅ Logic | Implemented in Game Engine | [Line 431](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L431) | の処理を行います。 |
| 9.6.2.1.2.1 | ✅ Logic | Implemented in Game Engine | [Line 431](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L431) | その際、このターンにステージで |
| 9.6.2.1.3 | ⚠️ Index Only | See Index for Details | Appendix | プレイするのが能力である場合、その |
| 9.6.2.2 | ✅ Logic | Implemented in Game Engine | [Line 466](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L466) | カードや能力に何らかの選択が必要である |
| 9.6.2.3 | ⚠️ Index Only | See Index for Details | Appendix | プレイするためのコストがある場合、そのコ |
| 9.6.2.3.1 | ⚠️ Index Only | See Index for Details | Appendix | プレイするのがメンバーのカードである |
| 9.6.2.3.2 | ⚠️ Index Only | See Index for Details | Appendix | メンバーをプレイする際、支払うべき |
| 9.6.2.3.2.1 | ⚠️ Index Only | See Index for Details | Appendix | これによりコストを減らす処理を |
| 9.6.2.4 | ⚠️ Index Only | See Index for Details | Appendix | カードや能力の解決を行います。 |
| 9.6.2.4.1 | ⚠️ Index Only | See Index for Details | Appendix | プレイしたのがメンバーである場合、そ |
| 9.6.2.4.2 | ⚠️ Index Only | See Index for Details | Appendix | プレイしたのが起動能力や自動能力で |
| 9.6.2.4.2.1 | ⚠️ Index Only | See Index for Details | Appendix | 能力の解決によってメンバーカー |
| 9.6.3 | ⚠️ Index Only | See Index for Details | Appendix | カードや能力に’～選び’や’～選ぶ’と書かれてい |
| 9.6.3.1 | ⚠️ Index Only | See Index for Details | Appendix | 選ぶ数が指定されている場合、それが可能 |
| 9.6.3.1.1 | ⚠️ Index Only | See Index for Details | Appendix | 選ぶ数が’～まで選び’や’～まで選 |
| 9.6.3.1.2 | ⚠️ Index Only | See Index for Details | Appendix | 選ぶ数が指定されている場合に、指定 |
| 9.6.3.1.3 | ⚠️ Index Only | See Index for Details | Appendix | 選ぶ数が指定されている場合に、目標 |
| 9.6.3.1.4 | ⚠️ Index Only | See Index for Details | Appendix | 選ぶものが公開されていない非公開領 |
| 9.7 | ✅ Logic | Implemented in Game Engine | [Line 286](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L286) | 自動能力の処理 |
| 9.7.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | 自動能力とは、特定の誘発条件が発生したときに、 |
| 9.7.2 | ⚠️ Index Only | See Index for Details | Appendix | なんらかの自動能力の誘発条件が満たされた場 |
| 9.7.2.1 | ⚠️ Index Only | See Index for Details | Appendix | 自動能力の誘発条件が複数回満たされた |
| 9.7.3 | ✅ Logic | Implemented in Game Engine | [Line 667](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L667) | チェックタイミングが発生した段階で、自動能力のプ |
| 9.7.3.1 | ✅ Logic | Implemented in Game Engine | [Line 667](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L667) | 待機状態の自動能力のプレイは強制で、プ |
| 9.7.3.1.1 | ✅ Logic | Implemented in Game Engine | [Line 667](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L667) | 自動能力が任意でコストを支払うことに |
| 9.7.3.2 | ⚠️ Index Only | See Index for Details | Appendix | 選んだ待機状態の自動能力をプレイできな |
| 9.7.3.2.1 | ⚠️ Index Only | See Index for Details | Appendix | 自動能力が任意でコストを支払うことに |
| 9.7.4 | ⚠️ Index Only | See Index for Details | Appendix | あるカードが領域を移動することを誘発条件とする |
| 9.7.4.1 | ⚠️ Index Only | See Index for Details | Appendix | 領域移動誘発による自動能力が、その能力 |
| 9.7.4.1.1 | ⚠️ Index Only | See Index for Details | Appendix | カードが公開領域から非公開領域、あ |
| 9.7.4.1.2 | ⚠️ Index Only | See Index for Details | Appendix | カードがステージからそれ以外の領域 |
| 9.7.4.1.3 | ⚠️ Index Only | See Index for Details | Appendix | 上記に示された以外の、公開領域から |
| 9.7.4.2 | ⚠️ Index Only | See Index for Details | Appendix | あるカードが領域移動誘発能力を持ち、そ |
| 9.7.5 | ⚠️ Index Only | See Index for Details | Appendix | なんらかの効果により、以降の特定の時点で誘発 |
| 9.7.5.1 | ⚠️ Index Only | See Index for Details | Appendix | 時限誘発は、特に期限が示されていないか |
| 9.7.6 | ⚠️ Index Only | See Index for Details | Appendix | 自動能力が、特定の事項が発生したことではなく、 |
| 9.7.6.1 | ⚠️ Index Only | See Index for Details | Appendix | 状態誘発は、その状態が発生したときに1 |
| 9.7.7 | ⚠️ Index Only | See Index for Details | Appendix | 待機状態の自動能力のプレイ時に、その自動能力 |
| 9.8 | ⚠️ Index Only | See Index for Details | Appendix | 単発効果の処理 |
| 9.8.1 | ⚠️ Index Only | See Index for Details | Appendix | 単発効果を実行するよう求められた場合、そこに指 |
| 9.9 | ✅ Logic | Implemented in Game Engine | [Line 171](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L171) | 継続効果の処理 |
| 9.9.1 | ✅ Logic | Implemented in Game Engine | [Line 212](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L212) | なんらかの継続効果が存在する状態でカードの情 |
| 9.9.1.1 | ⚠️ Index Only | Visual / Asset Spec | Appendix | カード自身に表記されている情報が、常に基 |
| 9.9.1.2 | ⚠️ Index Only | See Index for Details | Appendix | 次に、能力を与える/失わせる/有効にする/ |
| 9.9.1.3 | ⚠️ Index Only | See Index for Details | Appendix | 次に、継続効果のうち情報の数値を変更す |
| 9.9.1.4 | ✅ Logic | Implemented in Game Engine | [Line 212](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L212) | 次に、継続効果のうち情報の数値を特定の |
| 9.9.1.4.1 | ⚠️ Index Only | See Index for Details | Appendix | ハートやブレードの個数を特定の数に |
| 9.9.1.5 | ✅ Logic | Implemented in Game Engine | [Line 216](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L216) | 次に、継続効果のうち情報の数値を変更す |
| 9.9.1.5.1 | ⚠️ Index Only | See Index for Details | Appendix | ハートやブレードの個数を加減算する |
| 9.9.1.6 | ⚠️ Index Only | See Index for Details | Appendix | 以上の9.9.1.2X-9.9.1.4 で適用順の前後が決 |
| 9.9.1.7 | ⚠️ Index Only | See Index for Details | Appendix | 以上の9.9.1.2X-9.9.1.6 で適用順の前後が決 |
| 9.9.1.7.1 | ⚠️ Index Only | See Index for Details | Appendix | 継続効果の発生源が常時能力である |
| 9.9.1.7.2 | ⚠️ Index Only | See Index for Details | Appendix | それ以外の能力の場合は、それがプレ |
| 9.9.2 | ⚠️ Index Only | See Index for Details | Appendix | 常時能力以外で発生している継続効果は、その能 |
| 9.9.3 | ⚠️ Index Only | See Index for Details | Appendix | 特定の領域におけるカードの情報を変更する継続 |
| 9.9.3.1 | ⚠️ Index Only | See Index for Details | Appendix | 特定の情報を持つカードが領域に入ることを |
| 9.10 | ⚠️ Index Only | See Index for Details | Appendix | 置換効果の処理 |
| 9.10.1 | ⚠️ Index Only | See Index for Details | Appendix | 置換効果が発生している場合、その置換効果の |
| 9.10.1.1 | ⚠️ Index Only | See Index for Details | Appendix | これにより、置換された元の事象はまったく |
| 9.10.2 | ⚠️ Index Only | See Index for Details | Appendix | 同一の事象に対し複数の置換効果が発生してい |
| 9.10.2.1 | ⚠️ Index Only | See Index for Details | Appendix | 影響を受ける事象がカードや能力である場 |
| 9.10.2.2 | ⚠️ Index Only | See Index for Details | Appendix | 影響を受ける事象がゲーム中の行動であ |
| 9.10.2.3 | ⚠️ Index Only | See Index for Details | Appendix | 同一の事象に対しては、各置換効果は最 |
| 9.10.3 | ⚠️ Index Only | See Index for Details | Appendix | 置換効果が選択型置換効果（’～する時、かわり |
| 9.11 | ⚠️ Index Only | See Index for Details | Appendix | 最終情報 |
| 9.11.1 | ⚠️ Index Only | See Index for Details | Appendix | ある効果が特定のカードの情報や状態を参照して |
| 9.12 | ⚠️ Index Only | See Index for Details | Appendix | 発生源 |
| 9.12.1 | ⚠️ Index Only | See Index for Details | Appendix | 能力や効果により、ある効果の発生源を求めるこ |
| 9.12.2 | ⚠️ Index Only | Definition / Descriptive | Appendix | 能力の発生源とは、その能力を持つカード、また |
| 10.1 | ⚠️ Index Only | See Index for Details | Appendix | ルール処理の基本 |
| 10.1.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | ルール処理とは、ゲームにおいて特定の事象が |
| 10.1.2 | ⚠️ Index Only | See Index for Details | Appendix | ルール処理は、リフレッシュ（10.2）を除き、チェック |
| 10.1.3 | ⚠️ Index Only | See Index for Details | Appendix | ルール処理が複数同時に実行を求められる場 |
| 10.2 | ✅ Logic | Implemented in Game Engine | [Line 573](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L573) | リフレッシュ |
| 10.2.1 | ⚠️ Index Only | See Index for Details | Appendix | リフレッシュはチェックタイミングにかぎらず、ゲー |
| 10.2.2 | ⚠️ Index Only | See Index for Details | Appendix | 以下のいずれかの条件を満たすとき、リフレッシュ |
| 10.2.2.1 | ⚠️ Index Only | See Index for Details | Appendix | いずれかのプレイヤーのメインデッキ置き |
| 10.2.2.2 | ⚠️ Index Only | See Index for Details | Appendix | メインデッキ置き場を上から見る指示があ |
| 10.2.3 | ⚠️ Index Only | See Index for Details | Appendix | リフレッシュを行うプレイヤーは、自身の控え室の |
| 10.2.4 | ⚠️ Index Only | See Index for Details | Appendix | 両方のプレイヤーが同時にリフレッシュを行う条件 |
| 10.3 | ✅ Logic | Implemented in Game Engine | [Line 610](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L610) | 勝利処理 |
| 10.3.1 | ⚠️ Index Only | See Index for Details | Appendix | いずれかのプレイヤーの勝利ライブカード置き場 |
| 10.4 | ⚠️ Index Only | See Index for Details | Appendix | 重複メンバー処理 |
| 10.4.1 | ⚠️ Index Only | See Index for Details | Appendix | いずれかのプレイヤーの1 つのメンバーエリアに |
| 10.5 | ✅ Logic | Implemented in Game Engine | [Line 581](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L581) | 不正カード処理 |
| 10.5.1 | ✅ Logic | Implemented in Game Engine | [Line 581](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L581) | いずれかのプレイヤーのライブカード置き場にライ |
| 10.5.2 | ⚠️ Index Only | See Index for Details | Appendix | いずれかのエネルギー置き場にエネルギーでない |
| 10.5.3 | ✅ Logic | Implemented in Game Engine | [Line 593](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L593) | いずれかのメンバーエリアに、上に重なっているメ |
| 10.5.4 | ⚠️ Index Only | See Index for Details | Appendix | 上記のいずれかの処理において、控え室に置く |
| 10.6 | ✅ Logic | Implemented in Game Engine | [Line 601](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L601) | 不正解決領域処理 |
| 10.6.1 | ✅ Logic | Implemented in Game Engine | [Line 601](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L601) | 解決領域に現在プレイ中または解決中であるまた |
| 11.1 | ✅ Logic | Implemented in Game Engine | [Line 789](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L789) | 概要 |
| 11.1.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | キーワードとは、特定の処理を行う能力を簡略表 |
| 11.1.2 | ⚠️ Index Only | Keyword Definition | Appendix | 自動能力を意味するキーワード能力において、 |
| 11.1.3 | ⚠️ Index Only | Keyword Definition | Appendix | 能力の中には’ |
| 11.2 | ✅ Logic | Implemented in Game Engine | [Line 168](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L168) | ターン1 回 |
| 11.2.2 | ⚠️ Index Only | Keyword Definition | Appendix | キーワード |
| 11.2.3 | ⚠️ Index Only | Keyword Definition | Appendix | ’ |
| 11.3 | ✅ Logic | Implemented in Game Engine | [Line 1237](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1237) | 登場 |
| 11.3.2 | ⚠️ Index Only | Keyword Definition | Appendix | ‘ |
| 11.4 | ✅ Logic | Implemented in Game Engine | [Line 1318](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L1318) | ライブ開始時 |
| 11.4.2 | ⚠️ Index Only | Keyword Definition | Appendix | ‘ |
| 11.4.2.1 | ⚠️ Index Only | Keyword Definition | Appendix | パフォーマンスフェイズ中、手番プレイヤー |
| 11.5 | ⚠️ Index Only | Keyword Definition | Appendix | ライブ成功時 |
| 11.5.2 | ⚠️ Index Only | Keyword Definition | Appendix | ‘ |
| 11.6 | ⚠️ Index Only | Keyword Definition | Appendix | センター |
| 11.6.2 | ⚠️ Index Only | Keyword Definition | Appendix | キーワード |
| 11.6.3 | ⚠️ Index Only | Keyword Definition | Appendix | キーワード |
| 11.6.4 | ⚠️ Index Only | Keyword Definition | Appendix | キーワード |
| 11.7 | ⚠️ Index Only | Keyword Definition | Appendix | 左サイド |
| 11.7.2 | ⚠️ Index Only | Keyword Definition | Appendix | キーワード |
| 11.7.3 | ⚠️ Index Only | Keyword Definition | Appendix | キーワード |
| 11.7.4 | ⚠️ Index Only | Keyword Definition | Appendix | キーワード |
| 11.8 | ⚠️ Index Only | Keyword Definition | Appendix | 右サイド |
| 11.8.2 | ⚠️ Index Only | Keyword Definition | Appendix | キーワード |
| 11.8.3 | ⚠️ Index Only | Keyword Definition | Appendix | キーワード |
| 11.8.4 | ⚠️ Index Only | Keyword Definition | Appendix | キーワード |
| 11.9 | ✅ Logic | Implemented in Game Engine | [Line 751](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L751) | ポジションチェンジ |
| 11.9.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | ポジションチェンジするとは、そのメンバーを今い |
| 11.9.2 | ✅ Logic | Implemented in Game Engine | [Line 847](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L847) | メンバーを移動させた先のエリアにすでにメンバー |
| 11.10 | ✅ Logic | Implemented in Game Engine | [Line 789](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L789) | フォーメーションチェンジ |
| 11.10.1 | ⚠️ Index Only | Definition / Descriptive | Appendix | フォーメーションチェンジするとは、ステージにい |
| 11.10.2 | ⚠️ Index Only | Keyword Definition | Appendix | この効果で1 つのエリアに2 人以上のメンバー |
| 12.1 | ✅ Logic | Implemented in Game Engine | [Line 293](file:///c:/Users/trios/.gemini/antigravity/scratch/loveca-copy/game/game_state.py#L293) | 永久循環 |
| 12.1.1 | ⚠️ Index Only | See Index for Details | Appendix | 何らかの処理を行う際に、ある行動を永久に実行 |
| 12.1.1.1 | ⚠️ Index Only | See Index for Details | Appendix | アクティブプレイヤー（7.2）は、その循環行 |
| 12.1.1.2 | ⚠️ Index Only | See Index for Details | Appendix | アクティブプレイヤーが何らかの行動を行 |
| 12.1.1.3 | ⚠️ Index Only | See Index for Details | Appendix | 何らかの理由により、どちらのプレイヤーに |
