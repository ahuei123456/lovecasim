
import unittest
from game.game_state import GameState, PlayerState
from game.ability import AbilityParser, EffectType

class TestHandMechanics(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        # self.state.setup_game() # Method does not exist
        self.p0 = self.state.players[0]
        # Ensure p0 has cards
        self.p0.hand = [101, 102, 103] # Mock card IDs
        self.p0.main_deck = [201, 202, 203, 204, 205]

    def test_swap_cards_draw_discard(self):
        # "2枚引き、手札を1枚控え室に置く。"
        text = "2枚引き、手札を1枚控え室に置く。"
        abilities = AbilityParser.parse_ability_text(text)
        
        self.assertTrue(len(abilities) > 0)
        effects = abilities[0].effects
        
        # Expecting: Draw 2, then Swap(Discard) 1
        # Note: Order depends on parser. Usually sequential.
        has_draw = False
        has_discard = False
        
        for eff in effects:
            if eff.effect_type == EffectType.DRAW:
                self.assertEqual(eff.value, 2)
                has_draw = True
            elif eff.effect_type == EffectType.SWAP_CARDS:
                self.assertEqual(eff.value, 1)
                self.assertEqual(eff.params.get('from'), 'hand')
                self.assertEqual(eff.params.get('target'), 'discard')
                has_discard = True
                
        self.assertTrue(has_draw, "Parser should find Draw effect")
        self.assertTrue(has_discard, "Parser should find Discard (Swap) effect")
        
        # Test Execution
        # Manually trigger effects on state
        initial_hand = len(self.p0.hand) # 3
        initial_deck = len(self.p0.main_deck) # 5
        
        # 1. Execute Draw
        draw_eff = next(e for e in effects if e.effect_type == EffectType.DRAW)
        self.state.pending_effects.append(draw_eff)
        # print(f"DEBUG: GameState attributes: ...")
        self.state._resolve_pending_effect(0)
        
        self.assertEqual(len(self.p0.hand), initial_hand + 2)
        self.assertEqual(len(self.p0.main_deck), initial_deck - 2)
        
        # 2. Execute Discard
        # This should trigger a Pending Choice
        discard_eff = next(e for e in effects if e.effect_type == EffectType.SWAP_CARDS)
        self.state.pending_effects.append(discard_eff)
        self.state._resolve_pending_effect(0)
        
        self.assertTrue(len(self.state.pending_choices) > 0, "Should trigger a pending choice for discard")
        choice_type, params = self.state.pending_choices[-1]
        self.assertEqual(choice_type, "DISCARD_SELECT")
        self.assertEqual(params['count'], 1)
        
        # 3. Resolve Choice (Simulate user picking the first card)
        # Assuming we implement _handle_choice for DISCARD_SELECT
        # We need mock card indices. Hand size is now 3+2=5. Indices 0-4.
        # Let's discard idx 0 (card 101)
        
        # Depending on how choice is handled, maybe action input? 
        # For this test, we might need to manually call the choice handler if it's internal private
        # But let's assume valid action flow if possible, or direct method call.
        # self.state._handle_choice(0) # Logic for choice resolution
        pass 

    def test_look_deck(self):
        # "山札の上から3枚見て、その中から1枚を手札に加え、残りを山札の下に置く。"
        text = "山札の上から3枚見て、その中から1枚を手札に加え、残りを山札の下に置く。"
        abilities = AbilityParser.parse_ability_text(text)
        effects = abilities[0].effects
        
        # Verify Parser
        look_eff = next(e for e in effects if e.effect_type == EffectType.LOOK_DECK)
        self.assertEqual(look_eff.value, 3)
        
        choose_eff = next(e for e in effects if e.effect_type == EffectType.LOOK_AND_CHOOSE)
        
        # Execution
        # 1. Look Deck
        self.state.pending_effects.append(look_eff)
        self.state._resolve_pending_effect(0)
        
        self.assertEqual(len(self.state.looked_cards), 3)
        self.assertEqual(len(self.p0.main_deck), 2) # Started with 5
        
        # 2. Look and Choose
        self.state.pending_effects.append(choose_eff)
        self.state._resolve_pending_effect(0)
        
        self.assertTrue(len(self.state.pending_choices) > 0)
        choice = self.state.pending_choices[-1]
        self.assertEqual(choice[0], "SELECT_FROM_LIST")
        self.assertEqual(len(choice[1]['cards']), 3)

if __name__ == '__main__':
    unittest.main()
