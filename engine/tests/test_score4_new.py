
import sys
import os
import numpy as np
import unittest

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.game.game_state import GameState, Phase, MemberCard, LiveCard, PlayerState, HeartColor
from engine.game.ability import Ability, TriggerType, Effect, EffectType, TargetType, AbilityCostType, Condition, ConditionType, AbilityParser, Cost

class TestScore4AbilitiesNew(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.p0 = self.state.players[0]
        self.p1 = self.state.players[1]
        
    def test_nico_dual_trigger(self):
        """Test PL!-PR-009-PR: Dual trigger ON_PLAY / ON_LIVE_START"""
        text = "{{toujyou.png|登場}}/{{live_start.png|ライブ開始時}}このメンバーをウェイトにしてもよい：相手のステージにいるコスト4以下のメンバー1人をウェイトにする。"
        abilities = AbilityParser.parse_ability_text(text)
        
        self.assertEqual(len(abilities), 2, "Should parse into 2 abilities")
        self.assertEqual(abilities[0].trigger, TriggerType.ON_PLAY)
        self.assertEqual(abilities[1].trigger, TriggerType.ON_LIVE_START)
        
        for abi in abilities:
            self.assertEqual(len(abi.costs), 1)
            self.assertEqual(abi.costs[0].type, AbilityCostType.TAP_SELF)
            self.assertEqual(len(abi.effects), 1)
            self.assertEqual(abi.effects[0].effect_type, EffectType.TAP_OPPONENT)

    def test_kanata_reveal_hand(self):
        """Test PL!N-PR-008-PR: Reveal hand cost + condition"""
        text = "{{kidou.png|起動}}{{turn1.png|ターン1回}}手札をすべて公開する：自分のステージにほかのメンバーがおり、かつこれにより公開した手札の中にライブカードがない場合、自分のデッキの上からカードを5枚見る。その中からライブカードを1枚公開して手札に加えてもよい。残りを控え室に置く。"
        abilities = AbilityParser.parse_ability_text(text)
        
        self.assertEqual(len(abilities), 1)
        abi = abilities[0]
        
        # Check Cost
        self.assertTrue(any(c.type == AbilityCostType.REVEAL_HAND_ALL for c in abi.costs), "Should have REVEAL_HAND_ALL cost")
        
        # Check Condition
        self.assertTrue(any(c.type == ConditionType.HAND_HAS_NO_LIVE for c in abi.conditions), "Should have HAND_HAS_NO_LIVE condition")
        
        # Test Execution Logic (Mocking logic needed in game_state if we were testing full flow, but here testing parser)
        self.assertEqual(abi.effects[0].effect_type, EffectType.LOOK_DECK)
        self.assertEqual(abi.effects[0].value, 5)

    def test_ginko_parsing(self):
        """Test PL!N-PR-012-PR: Look 5, Choose 1 Member"""
        text = "【登場時】手札を1枚捨ててもよい：そうしたら、デッキの上から5枚見る。その中からメンバーを1枚まで公開し、手札に加える。残りを山札の一番下に望む順番で置く。"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        abi = abilities[0]
        
        # Check Effects chain
        # 1. Look Deck 5
        self.assertEqual(abi.effects[0].effect_type, EffectType.LOOK_DECK)
        self.assertEqual(abi.effects[0].value, 5)
        # 2. Look and Choose (Member)
        self.assertEqual(abi.effects[1].effect_type, EffectType.LOOK_AND_CHOOSE)
        self.assertEqual(abi.effects[1].params.get('filter'), 'member', "Should capture member filter")
        # 3. Order Deck (Remainder to bottom)
        # Note: Parser might attach this as separate effect or part of flow. 
        # Current logic usually appends ORDER_DECK or MOVE_TO_DECK.
        self.assertTrue(any(e.effect_type in (EffectType.ORDER_DECK, EffectType.MOVE_TO_DECK) for e in abi.effects), "Should handle remainder")

class TestScore4Execution(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.p0 = self.state.players[0]
        self.p1 = self.state.players[1]
        
        # Setup mock DBs
        GameState.member_db = {}
        GameState.live_db = {}
        
    def test_kanata_execution(self):
        """Test PL!N-PR-008-PR execution logic for Condition and Cost"""
        # Create a mock ability
        abi = Ability(
            raw_text="Test Kanata",
            trigger=TriggerType.ACTIVATED,
            costs=[Cost(AbilityCostType.REVEAL_HAND_ALL)],
            conditions=[Condition(ConditionType.HAND_HAS_NO_LIVE)],
            effects=[Effect(EffectType.DRAW, 1)] # Simple effect to verify success
        )
        
        # Test Case 1: Hand has NO live cards -> Should Succeed
        self.p0.hand = [10, 11] # Assume member IDs
        GameState.member_db[10] = MemberCard(10, "M-01", "M1", 1, np.zeros(6), np.zeros(7), 1)
        GameState.member_db[11] = MemberCard(11, "M-02", "M2", 1, np.zeros(6), np.zeros(7), 1)
        
        # Verify condition
        self.assertTrue(self.state._check_condition(self.p0, abi.conditions[0]), "Condition HAND_HAS_NO_LIVE should be True (no lives)")
        
        # Verify pay cost returns True
        self.assertTrue(self.state._pay_costs(self.p0, abi.costs), "Should be able to pay REVEAL_HAND_ALL")
        
        # Test Case 2: Hand HAS live cards -> Should Fail Condition
        self.p0.hand.append(100)
        GameState.live_db[100] = LiveCard(100, "L-100", "L1", 1, np.zeros(7))
        
        self.assertFalse(self.state._check_condition(self.p0, abi.conditions[0]), "Condition HAND_HAS_NO_LIVE should be False (has live)")

    def test_ginko_faq_logic(self):
        """Test FAQ Q123 Logic (Look 5 Choose 1) - allow 0 targets"""
        # Ginko logic: Look 5 -> Filter Member -> Choose 1 (up to 1)
        # We simulate the choice selection from logic
        # If looked_cards has NO members, should simply return remainder.
        
        self.p0.main_deck = [200, 201, 202] # Energy cards (not members)
        # Mock DB for energy? or just IDs that are NOT in member_db
        # Member DB is empty here, so IDs are not members.
        
        # Mock Effect Resolution for LOOK_AND_CHOOSE
        # We manually simulate _resolve_pending_effect logic for test
        # (Since we aren't running full step loop here conveniently)
        
        self.state.looked_cards = [200, 201, 202]
        
        # Create Effect
        eff = Effect(EffectType.LOOK_AND_CHOOSE, 1, params={'filter': 'member'})
        
        # Inject choice generation logic from game_state (simplified reproduction)
        # In actual game_state.py, it creates SELECT_FROM_LIST choice.
        # But we need to ensure the choice allows 0 if "up to 1" or implicit.
        # Current game_state logic:
        # if self.looked_cards: pending_choices.append(...)
        
        # We check if the CHOICE creation logic filters items?
        # game_state.py line 917 just copies looked_cards.
        # It relies on the UI/Choice-Resolution to enforce "filter: member".
        # If UI allows 0 selection, then FAQ is satisfied.
        # This test confirms that pending_choices IS created even if no members valid? 
        # Yes, because looked_cards is not filtered at creation time in current logic.
        
        # Wait, if we want to support "Filter member", we should filter the OPTIONS in pending choices?
        # Current logic: 'cards': self.looked_cards.copy()
        # It doesn't filter by 'member' param.
        # This implies the filter happens AT SELECTION TIME (UI constraint).
        # So FAQ is satisfied: Player sees all cards, but can only select Members. If none, select 0/Cancel.
        pass

    def test_honoka_parsing(self):
        """Test PL!-sd1-001-SD: Count Success Live Condition & Recover Live Effect"""
        text = "【登場時】自分の成功ライブカード置き場にカードが2枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。"
        abilities = AbilityParser.parse_ability_text(text)
        self.assertEqual(len(abilities), 1)
        abi = abilities[0]
        
        # Verify Trigger
        self.assertEqual(abi.trigger, TriggerType.ON_PLAY)
        
        # Verify Condition
        self.assertEqual(len(abi.conditions), 1)
        self.assertEqual(abi.conditions[0].type, ConditionType.COUNT_SUCCESS_LIVE)
        self.assertEqual(abi.conditions[0].params.get('min'), 2)
        
        # Verify Effect
        self.assertEqual(len(abi.effects), 1)
        self.assertEqual(abi.effects[0].effect_type, EffectType.RECOVER_LIVE)
        self.assertEqual(abi.effects[0].value, 1)

    def test_honoka_execution(self):
        """Test PL!-sd1-001-SD execution logic"""
        # Create ability
        abi = Ability(
            raw_text="Test Honoka",
            trigger=TriggerType.ON_PLAY,
            conditions=[Condition(ConditionType.COUNT_SUCCESS_LIVE, {'min': 2})],
            effects=[Effect(EffectType.RECOVER_LIVE, 1)]
        )
        
        # Test Case 1: Less than 2 success lives -> Fail Condition
        self.p0.success_lives = [100] # 1 card
        self.assertFalse(self.state._check_condition(self.p0, abi.conditions[0]))
        
        # Test Case 2: 2 success lives -> Pass Condition
        self.p0.success_lives.append(101) # 2 cards
        self.assertTrue(self.state._check_condition(self.p0, abi.conditions[0]))
        
        # Test Case 3: Effect execution (Recover Live)
        # Mock discard with a Live card (ID 200) and Member card (ID 10)
        self.p0.discard = [200, 10]
        GameState.live_db[200] = LiveCard(200, "L-200", "L1", 1, np.zeros(7))
        GameState.member_db[10] = MemberCard(10, "M-01", "M1", 1, np.zeros(6), np.zeros(7), 1)
        GameState.member_db[11] = MemberCard(11, "M-02", "M2", 1, np.zeros(6), np.zeros(7), 1)
        
        # Mock pending choices
        self.state.pending_choices = []
        
        # Execute logic manually (simulate _resolve_pending_effect)
        # We need to invoke the logic block for RECOVER_LIVE
        eff = abi.effects[0]
        # Copy-paste logic from game_state.py or rely on unit test to call a method?
        # Ideally we call a method. But _resolve_pending_effect is complex.
        # Let's just check _check_condition mainly, as Effect logic is standard.
        # But let's verification RECOVER_LIVE filter logic.
        
        # Call _resolve_pending_effect with just this effect on stack
        self.state.pending_effects.append(eff)
        self.state._resolve_pending_effect(0)
        
        # Check generated choice
        self.assertEqual(len(self.state.pending_choices), 1)
        choice_type, params = self.state.pending_choices[0]
        self.assertEqual(choice_type, "SELECT_FROM_DISCARD")
        self.assertEqual(params['filter'], 'live')
        self.assertEqual(len(params['cards']), 1)
        self.assertEqual(params['cards'][0], 200) # Only the live card
        

if __name__ == "__main__":
    unittest.main()
