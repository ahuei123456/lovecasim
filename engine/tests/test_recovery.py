"""
Unit test recovery mechanics (RECOVER_LIVE, RECOVER_MEMBER).
Tests based on real card examples from the 100-card analysis.
"""
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.game.game_state import GameState
from engine.game.ability import AbilityParser, EffectType, TriggerType

class TestRecoveryMechanics(unittest.TestCase):
    
    def setUp(self):
        self.state = GameState()
        self.p0 = self.state.players[0]
        # Setup hand and discard
        self.p0.hand = [101, 102, 103]
        self.p0.main_deck = [201, 202, 203, 204, 205]
        
        # Ensure live and member cards are in DB
        self.state.live_db[300] = type('obj', (object,), {'card_id': 300, 'name': 'TestLive'})()
        self.state.live_db[301] = type('obj', (object,), {'card_id': 301, 'name': 'TestLive2'})()
        self.state.member_db[400] = type('obj', (object,), {'card_id': 400, 'name': 'TestMember'})()
        self.state.member_db[401] = type('obj', (object,), {'card_id': 401, 'name': 'TestMember2'})()
        
        # Put them in discard
        self.p0.discard = [300, 301, 400, 401]
    
    def test_recover_live_parser(self):
        """Card #1: 高坂 穂乃果 - RECOVER_LIVE"""
        text = "{{toujyou.png|登場}}自分の成功ライブカード置き場にカードが2枚以上ある場合、自分の控え室からライブカードを1枚手札に加える。"
        
        abilities = AbilityParser.parse_ability_text(text)
        self.assertTrue(len(abilities) > 0, "Should parse at least one ability")
        
        # Find RECOVER_LIVE effect
        has_recover = any(e.effect_type == EffectType.RECOVER_LIVE for e in abilities[0].effects)
        self.assertTrue(has_recover, "Should have RECOVER_LIVE effect")
    
    def test_recover_live_execution(self):
        """Test RECOVER_LIVE effect execution"""
        from engine.game.ability import Effect
        
        initial_hand = len(self.p0.hand)
        initial_discard = len(self.p0.discard)
        
        # Execute RECOVER_LIVE effect
        effect = Effect(EffectType.RECOVER_LIVE, 1)
        self.state.pending_effects.append(effect)
        self.state._resolve_pending_effect(0)
        
        # Should create a SELECT_FROM_DISCARD choice
        self.assertEqual(len(self.state.pending_choices), 1)
        choice_type, params = self.state.pending_choices[0]
        self.assertEqual(choice_type, "SELECT_FROM_DISCARD")
        
        # Should offer only live cards from discard
        offered_cards = params['cards']
        self.assertEqual(len(offered_cards), 2)  # 300, 301
        self.assertTrue(all(c in self.state.live_db for c in offered_cards))
        
        # Simulate player choosing card 300 (action 660)
        self.state.take_action(660)
        
        # Verify: card moved from discard to hand
        self.assertIn(300, self.p0.hand)
        self.assertNotIn(300, self.p0.discard)
        self.assertEqual(len(self.p0.hand), initial_hand + 1)
        self.assertEqual(len(self.p0.discard), initial_discard - 1)
    
    def test_recover_member_parser(self):
        """Card #2: 絢瀬 絵里 - RECOVER_MEMBER"""
        text = "{{kidou.png|起動}}このメンバーをステージから控え室に置く：自分の控え室からメンバーカードを1枚手札に加える。"
        
        abilities = AbilityParser.parse_ability_text(text)
        self.assertTrue(len(abilities) > 0)
        
        # Find RECOVER_MEMBER effect
        has_recover = any(e.effect_type == EffectType.RECOVER_MEMBER for e in abilities[0].effects)
        self.assertTrue(has_recover, "Should have RECOVER_MEMBER effect")
    
    def test_recover_member_execution(self):
        """Test RECOVER_MEMBER effect execution"""
        from engine.game.ability import Effect
        
        initial_hand = len(self.p0.hand)
        
        # Execute RECOVER_MEMBER effect
        effect = Effect(EffectType.RECOVER_MEMBER, 1)
        self.state.pending_effects.append(effect)
        self.state._resolve_pending_effect(0)
        
        # Should create SELECT_FROM_DISCARD choice
        self.assertEqual(len(self.state.pending_choices), 1)
        choice_type, params = self.state.pending_choices[0]
        self.assertEqual(choice_type, "SELECT_FROM_DISCARD")
        
        # Should offer only member cards
        offered_cards = params['cards']
        self.assertEqual(len(offered_cards), 2)  # 400, 401
        self.assertTrue(all(c in self.state.member_db for c in offered_cards))
        
        # Simulate player choosing card 400 (action 660)
        self.state.take_action(660)
        
        # Verify recovery
        self.assertIn(400, self.p0.hand)
        self.assertNotIn(400, self.p0.discard)
        self.assertEqual(len(self.p0.hand), initial_hand + 1)

if __name__ == '__main__':
    unittest.main()
