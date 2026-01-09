import unittest
from game.ability import AbilityParser, Ability, TriggerType, EffectType, ConditionType, Condition

class TestComplexAbilityParser(unittest.TestCase):
    
    def test_meta_rule_clarification(self):
        # "(登場能力がコストを持つ場合、支払って発動させる。)"
        text = "(登場能力がコストを持つ場合、支払って発動させる。)"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        self.assertEqual(abilities[0].trigger, TriggerType.CONSTANT)
        self.assertEqual(abilities[0].effects[0].effect_type, EffectType.META_RULE)

    def test_select_mode(self):
        # "登場以下から1つを選ぶ。"
        text = "【登場時】以下から1つを選ぶ。" # Simulated standard format or just raw
        # Raw from unparsed: "- 登場以下から1つを選ぶ。" -> "登場以下から1つを選ぶ。"
        text = "登場以下から1つを選ぶ。"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        self.assertEqual(abilities[0].trigger, TriggerType.ON_PLAY)
        self.assertEqual(abilities[0].effects[0].effect_type, EffectType.SELECT_MODE)

    def test_deck_ordering_top(self):
        # "登場自分の控え室からカードを1枚までデッキの一番上に置く。"
        text = "登場自分の控え室からカードを1枚までデッキの一番上に置く。"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        self.assertEqual(abilities[0].effects[0].effect_type, EffectType.MOVE_TO_DECK)
        self.assertEqual(abilities[0].effects[0].params['position'], 'top')

    def test_deck_ordering_bottom(self):
        # "登場自分の控え室からライブカードを1枚までデッキの一番下に置く。"
        text = "登場自分の控え室からライブカードを1枚までデッキの一番下に置く。"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        self.assertEqual(abilities[0].effects[0].effect_type, EffectType.MOVE_TO_DECK)
        self.assertEqual(abilities[0].effects[0].params['position'], 'bottom')

    def test_tap_opponent_member(self):
        # "登場相手のステージにいる元々持つブレードの数が1つ以下のメンバー1人をウェイトにする。"
        text = "登場相手のステージにいる元々持つブレードの数が1つ以下のメンバー1人をウェイトにする。"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        self.assertEqual(abilities[0].effects[0].effect_type, EffectType.TAP_OPPONENT)
        
    def test_restriction_cannot_live(self):
        # "常時自分のステージにほかのメンバーがいない場合、自分はライブできない。"
        text = "常時自分のステージにほかのメンバーがいない場合、自分はライブできない。"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        self.assertEqual(abilities[0].trigger, TriggerType.CONSTANT)
        self.assertTrue(any(e.effect_type == EffectType.RESTRICTION for e in abilities[0].effects))
        self.assertEqual(abilities[0].effects[0].params['type'], 'live')

    def test_baton_touch_mod(self):
        # "常時このカードのプレイに際し、2人のメンバーとバトンタッチしてもよい。"
        text = "常時このカードのプレイに際し、2人のメンバーとバトンタッチしてもよい。"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        self.assertEqual(abilities[0].effects[0].effect_type, EffectType.BATON_TOUCH_MOD)
        self.assertEqual(abilities[0].effects[0].value, 2)

    def test_flavor_action(self):
        # "ライブ開始時相手に何が好き？と聞く。"
        text = "ライブ開始時相手に何が好き？と聞く。"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        self.assertEqual(abilities[0].trigger, TriggerType.ON_LIVE_START)
        self.assertEqual(abilities[0].effects[0].effect_type, EffectType.FLAVOR_ACTION)

    def test_set_score(self):
        # "ライブ成功時...このカードのスコアは４になる。"
        text = "ライブ成功時このカードのスコアは４になる。"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        self.assertEqual(abilities[0].effects[0].effect_type, EffectType.SET_SCORE)
        self.assertEqual(abilities[0].effects[0].value, 4)

    def test_swap_zone(self):
        # "登場...公開したカードを自分の成功ライブカード置き場に置く。"
        text = "登場公開したカードを自分の成功ライブカード置き場に置く。"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        self.assertEqual(abilities[0].effects[0].effect_type, EffectType.SWAP_ZONE)

if __name__ == '__main__':
    unittest.main()
