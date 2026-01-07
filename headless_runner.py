import sys
import os
import random
import numpy as np
import argparse
import logging
import time

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.game_state import GameState, Phase
from game.data_loader import CardDataLoader

class Agent:
    def choose_action(self, state: GameState, player_id: int) -> int:
        raise NotImplementedError

class RandomAgent(Agent):
    def choose_action(self, state: GameState, player_id: int) -> int:
        from game.game_state import Phase
        legal_mask = state.get_legal_actions()
        legal_indices = np.where(legal_mask)[0]
        if len(legal_indices) == 0:
            return 0 
        
        # Heuristic: If we can do something other than Pass (0) in MAIN or LIVE_SET, do it!
        # For Mulligan: confirm mulligan (0) or skip
        active_indices = [i for i in legal_indices if i != 0 and i < 200]
        
        if state.phase in (Phase.MULLIGAN_P1, Phase.MULLIGAN_P2):
            # Randomly pick 0-3 cards to mulligan (181-240) then confirm (0)
            if random.random() < 0.3: # 30% chance to confirm
                return 0
            mulligan_indices = [i for i in legal_indices if 181 <= i <= 240]
            if mulligan_indices:
                return int(np.random.choice(mulligan_indices))
            return 0

        if active_indices and state.phase in (Phase.MAIN, Phase.LIVE_SET):
            return int(np.random.choice(active_indices))
            
        return int(np.random.choice(legal_indices))

def generate_random_decks(member_ids, live_ids):
    """Generate two random decks: 40 members + 10 lives in ONE main_deck each"""
    m_pool = list(member_ids)
    l_pool = list(live_ids)
    
    # Ensure pool is not empty
    if not m_pool: m_pool = [0]
    if not l_pool: l_pool = [0]
    
    # Mix members and lives in one deck
    deck1 = [random.choice(m_pool) for _ in range(40)] + [random.choice(l_pool) for _ in range(10)]
    deck2 = [random.choice(m_pool) for _ in range(40)] + [random.choice(l_pool) for _ in range(10)]
    
    random.shuffle(deck1)
    random.shuffle(deck2)
    
    return deck1, deck2

def initialize_game(use_real_data: bool = True, cards_path: str = "data/cards.json") -> GameState:
    """Initializes GameState with card data."""
    if use_real_data:
        try:
            loader = CardDataLoader(cards_path)
            m_db, l_db = loader.load()
            GameState.member_db = m_db
            GameState.live_db = l_db
        except Exception as e:
            print(f"Failed to load real data: {e}")
            GameState.member_db = {}
            GameState.live_db = {}
    else:
        # For testing, ensure dbs are empty or mocked if not loading real data
        GameState.member_db = {}
        GameState.live_db = {}
    return GameState()

def create_easy_cards():
    """Create custom easy cards for testing scoring"""
    from game.game_state import MemberCard, LiveCard
    import numpy as np
    
    # Easy Member: Cost 1, provides 1 of each heart + 1 blade
    m = MemberCard(
        card_id=888,
        name="Easy Member",
        cost=1,
        hearts=np.array([1, 1, 1, 1, 1, 1], dtype=np.int32),
        blade_hearts=np.array([0, 0, 0, 0, 0, 0], dtype=np.int32),
        blades=1,
        volume_icons=0,
        draw_icons=0
    )
    
    # Easy Live: Score 1, Requires 1 Any Heart
    l = LiveCard(
        card_id=999,
        name="Easy Live",
        score=1,
        required_hearts=np.array([0, 0, 0, 0, 0, 0, 1], dtype=np.int32),
        volume_icons=0,
        draw_icons=0
    )
    
    return m, l

def setup_game(args):
    # Initialize game state
    use_easy = (args.deck_type == 'easy')
    
    state = initialize_game(use_real_data=(not use_easy), cards_path=args.cards_path)
    
    # Set seed
    np.random.seed(args.seed)
    random.seed(args.seed)
    
    if use_easy:
        # INJECT EASY CARDS
        m, l = create_easy_cards()
        state.member_db[888] = m
        state.live_db[999] = l
        
        # Single main_deck with BOTH Members (40) and Lives (10), shuffled
        for p in state.players:
            m_list = [888] * 48
            l_list = [999] * 12
            p.main_deck = m_list + l_list
            random.shuffle(p.main_deck)
            p.energy_deck = [200] * 12
            p.hand = []
            p.energy_zone = []
            p.live_zone = []
            p.discard = []
            p.stage = np.array([-1, -1, -1], dtype=np.int32)
    else:
         # Normal Random Decks (Members + Lives mixed)
         deck1, deck2 = generate_random_decks(state.member_db.keys(), state.live_db.keys())
         state.players[0].main_deck = deck1
         state.players[0].energy_deck = [999] * 10
         
         state.players[1].main_deck = deck2
         state.players[1].energy_deck = [999] * 10
         
         # Clear hands/zones just in case
         for p in state.players:
             p.hand = []
             p.energy_zone = []

    # Initial Draw (5 cards from main_deck)
    for _ in range(5):
        if state.players[0].main_deck:
            state.players[0].hand.append(state.players[0].main_deck.pop())
        if state.players[1].main_deck:
            state.players[1].hand.append(state.players[1].main_deck.pop())
        
    # Setup Energy Decks (Rule 6.1.1.3: 12 cards)
    for p in state.players:
        p.energy_deck = [200] * 12
        p.energy_zone = []
        # Initial Energy (Rule 6.2.1.7: Move 3 cards to energy zone)
        for _ in range(3):
            if p.energy_deck:
                p.energy_zone.append(p.energy_deck.pop(0))
                
    return state

def run_game(args):
    # Setup Logging
    logging.basicConfig(
        filename=args.log_file,
        level=logging.INFO,
        format='%(message)s',
        filemode='w'
    )
    logger = logging.getLogger()
    
    # Setup Game
    logger.info(f"Setting up game with seed {args.seed}...")
    random.seed(args.seed)
    np.random.seed(args.seed)
    
    state = setup_game(args)
    
    agents = [RandomAgent(), RandomAgent()]
    
    logger.info("Game Start!")
    start_time = time.time()
    
    turn_count = 0
    while turn_count < args.max_turns:
        if state.game_over:
            break
            
        # Check win condition manually if not handled in step (safety)
        state.check_win_condition()
        if state.game_over:
            break

        active_pid = state.current_player
        
        # Log Summary
        logger.info("-" * 40)
        logger.info(f"Turn {state.turn_number} | Phase {state.phase.name} | Active: P{active_pid}")
        p0 = state.players[0]
        p1 = state.players[1]
        logger.info(f"Score: P0({len(p0.success_lives)}) - P1({len(p1.success_lives)})")
        logger.info(f"Hand: P0({len(p0.hand)}) - P1({len(p1.hand)})")
        logger.info(f"Energy: P0({p0.count_untapped_energy()}/{len(p0.energy_zone)}) - P1({p1.count_untapped_energy()}/{len(p1.energy_zone)})")
        
        # Agent Act
        action = agents[active_pid].choose_action(state, active_pid)
        logger.info(f"Action: P{active_pid} chooses {action}")
        
        # Step
        try:
            state = state.step(action)
        except Exception as e:
            logger.error(f"Error during step: {e}")
            import traceback
            logger.error(traceback.format_exc())
            break
            
        # Limit check
        if state.turn_number > args.max_turns:
             logger.info("Max turns reached.")
             break
             
        turn_count += 1
        
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info("=" * 40)
    logger.info("Game Over")
    logger.info(f"Winner: {state.winner}")
    logger.info(f"Final Score: P0({len(state.players[0].success_lives)}) - P1({len(state.players[1].success_lives)})")
    logger.info(f"Total Steps: {turn_count}")
    logger.info(f"Duration: {duration:.4f}s")
    
    print(f"Game finished in {duration:.4f}s. Winner: {state.winner}. Log: {args.log_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cards_path", default="data/cards.json", help="Path to cards.json")
    parser.add_argument("--deck_type", default="normal", choices=["normal", "easy"], help="Deck type: normal or easy")
    parser.add_argument("--max_turns", type=int, default=1000, help="Max steps/turns to run")
    parser.add_argument("--log_file", default="game_log.txt", help="Output log file")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    
    args = parser.parse_args()
    
    run_game(args)
