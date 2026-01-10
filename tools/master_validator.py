"""
Master Ability Verification & Dashboard Tool (v2)

Combines:
1. Coverage Analysis (Frequency of effects/triggers)
2. Parsing Verification (Text -> Code mapping)
3. Inverse Parsing (Code -> Description) - ENHANCED
4. Heuristic Semantic Validation (Gaps & Mismatches) - ENHANCED
5. Behavioral Results Integration
6. FAQ Integration

Outputs a comprehensive report: docs/master_ability_report.md
"""
import json
import sys
import os
import re
from collections import Counter, defaultdict
from typing import List, Dict, Any

# Ensure we can import from game/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.ability import AbilityParser, Ability, TriggerType, EffectType, ConditionType, AbilityCostType, TargetType

# --- DESCRIPTIONS (Merged from existing tools) ---

EFFECT_DESCRIPTIONS = {
    EffectType.DRAW: "Draw {value} card(s)",
    EffectType.LOOK_DECK: "Look at top {value} card(s) of deck",
    EffectType.ADD_BLADES: "Gain {value} Blade(s)",
    EffectType.ADD_HEARTS: "Gain {value} Heart(s)",
    EffectType.REDUCE_COST: "Reduce cost by {value}",
    EffectType.BOOST_SCORE: "Boost score by {value}",
    EffectType.RECOVER_LIVE: "Recover {value} Live card(s) from discard",
    EffectType.RECOVER_MEMBER: "Recover {value} Member card(s) from discard",
    EffectType.BUFF_POWER: "Buff power/blade by {value}",
    EffectType.IMMUNITY: "Gain immunity",
    EffectType.MOVE_MEMBER: "Move member zone",
    EffectType.SWAP_CARDS: "Discard/Swap {value} card(s)",
    EffectType.SEARCH_DECK: "Search deck",
    EffectType.ENERGY_CHARGE: "Energy Charge {value}",
    EffectType.META_RULE: "[Rule modifier]",
    EffectType.SELECT_MODE: "Choose one effect",
    EffectType.MOVE_TO_DECK: "Move {value} card(s) to deck",
    EffectType.TAP_OPPONENT: "Tap {value} opponent's member(s)",
    EffectType.PLACE_UNDER: "Place card under member",
    EffectType.RESTRICTION: "Apply restriction",
    EffectType.SET_SCORE: "Set score to {value}",
    EffectType.REVEAL_CARDS: "Reveal {value} card(s)",
    EffectType.LOOK_AND_CHOOSE: "Choose {value} card(s) from looked deck",
    EffectType.ACTIVATE_MEMBER: "Activate {value} member(s)",
    EffectType.ADD_TO_HAND: "Add {value} card(s) to hand",
    EffectType.TRIGGER_REMOTE: "Trigger ability from other zone",
}

TRIGGER_DESCRIPTIONS = {
    TriggerType.ON_PLAY: "[On Play]",
    TriggerType.ON_LIVE_START: "[Live Start]",
    TriggerType.ON_LIVE_SUCCESS: "[Live Success]",
    TriggerType.TURN_START: "[Turn Start]",
    TriggerType.TURN_END: "[Turn End]",
    TriggerType.CONSTANT: "[Constant]",
    TriggerType.ACTIVATED: "[Activated]",
    TriggerType.ON_LEAVES: "[When Leaves]",
}

# --- LOGIC CLASSES ---

class MasterValidator:
    def __init__(self, cards_path: str):
        self.cards_path = cards_path
        with open(cards_path, encoding='utf-8') as f:
            self.cards = json.load(f)
        
        self.stats = {
            'total_cards': len(self.cards),
            'with_abilities': 0,
            'parsed_ok': 0,
            'parse_failed': 0,
            'with_faq': 0,
            'semantic_gaps': 0,
            'heuristic_issues': 0
        }
        
        self.effect_counts = Counter()
        self.trigger_counts = Counter()
        self.gap_counts = Counter()
        self.issue_counts = Counter()
        self.reports_by_card = {}
        self.passed_cards = set()

        # Load behavioral results
        if os.path.exists('tests/behavioral_results.json'):
            with open('tests/behavioral_results.json', encoding='utf-8') as f:
                res = json.load(f)
                self.passed_cards = set(res.get('passed_cards', []))

        # Complexity Tiers
        self.card_scores = self._load_tiers('docs/card_complexity_tiers.md')
        self.tier_stats = defaultdict(lambda: {'total': 0, 'passed': 0})

    def _load_tiers(self, path: str) -> Dict[str, int]:
        scores = {}
        if not os.path.exists(path): return scores
        with open(path, encoding='utf-8') as f:
            for line in f:
                # Match ID and score in markdown table row
                match = re.search(r'\|\s*([^\|\s]+?)\s*\|\s*(\d+)\s*\|', line)
                if match:
                    scores[match.group(1).strip()] = int(match.group(2))
        return scores

    def _calculate_score(self, text: str, abilities: List[Ability]) -> int:
        score = 0
        if not text: return 0
        
        # Base components
        for ab in abilities:
            score += 10 # Each ability block
            score += len(ab.effects) * 8
            score += len(ab.conditions) * 6
            score += len(ab.costs) * 5
            if ab.is_once_per_turn: score += 5
            if ab.modal_options: score += 15 # Select Mode
            
        # Keyword complexity
        keywords = {
            '選ぶ|選んだ': 12,      # Choice
            '見る': 8,              # Look
            '代わりに': 20,         # Replacement
            '枚につき|人につき': 15, # Multiplier
            '相手': 10,             # Opponent interaction
            '控え室': 5,            # Discard interaction
            'エネルギー': 5,        # Energy interaction
            'デッキ|山札': 5,       # Deck interaction
            'シャッフル': 10,       # Randomness
            'ならない|できない': 15, # Logic restrictions
            '。その後、': 10,       # Sequential effects
        }
        for pattern, points in keywords.items():
            if re.search(pattern, text):
                score += points
                
        return score

    def reconstruct_ability(self, ability: Ability) -> str:
        parts = []
        parts.append(TRIGGER_DESCRIPTIONS.get(ability.trigger, f"[{ability.trigger.name}]"))
        
        for cost in ability.costs:
            parts.append(f"(Cost: {cost.type.name} {cost.value})")
        
        for cond in ability.conditions:
            neg = "NOT " if cond.is_negated else ""
            parts.append(f"{neg}{cond.type.name}")
            
        for eff in ability.effects:
            template = EFFECT_DESCRIPTIONS.get(eff.effect_type, eff.effect_type.name)
            context = eff.params.copy()
            context['value'] = eff.value
            try:
                desc = template.format(**context)
            except KeyError:
                desc = template
            parts.append(f"→ {desc}")
            
        return " ".join(parts)

    def find_semantic_gaps(self, text: str, reconstructed: str) -> List[str]:
        gaps = []
        checks = [
            ('引く|ドロー', 'Draw', 'drawing'),
            ('控え室', 'discard', 'discard interaction'),
            ('ハート', 'Heart', 'hearts'),
            ('ブレード', 'Blade', 'blades'),
            ('エネルギー|チャージ', 'Energy', 'energy'),
            ('デッキ|山札', 'deck', 'deck interaction'),
            ('相手', 'opponent', 'opponent interaction'),
            ('スコア', 'score', 'score interaction'),
            ('ライブ', 'live', 'live interaction'),
            ('公開', 'Reveal', 'reveal'),
            ('選ぶ|選択', 'Choose|Pick', 'choice'),
        ]
        for pattern, concept_en, label in checks:
            if re.search(pattern, text) and not re.search(concept_en, reconstructed, re.IGNORECASE):
                gaps.append(f"Missing '{label}'")
        return gaps

    def validate_heuristics(self, card, abilities) -> List[str]:
        text = card.get('ability', '')
        issues = []
        
        all_effects = [e.effect_type for a in abilities for e in a.effects]
        
        if '引く' in text and EffectType.DRAW not in all_effects:
            issues.append("MISSING_DRAW")
        if 'スコア' in text and EffectType.BOOST_SCORE not in all_effects and EffectType.META_RULE not in all_effects:
            issues.append("MISSING_SCORE")
        if 'ハート' in text and '得る' in text and EffectType.ADD_HEARTS not in all_effects:
            issues.append("MISSING_HEARTS")
        if 'ブレード' in text and '得る' in text and EffectType.ADD_BLADES not in all_effects:
            issues.append("MISSING_BLADES")
            
        return issues

    def run(self):
        for card_no, card in self.cards.items():
            text = card.get('ability', '')
            faq = card.get('faq', [])
            
            if not text: continue
            
            self.stats['with_abilities'] += 1
            if faq: self.stats['with_faq'] += 1
            
            try:
                abilities = AbilityParser.parse_ability_text(text)
                self.stats['parsed_ok'] += 1
                
                # Tier stats (Prefer manual score if exists, else automated)
                score = self.card_scores.get(card_no)
                if score is None:
                    score = self._calculate_score(text, abilities)
                
                tier = "S" if score >= 35 else "A" if score >= 20 else "B" if score >= 10 else "C" if score >= 5 else "D"
                self.tier_stats[tier]['total'] += 1
                if card_no in self.passed_cards:
                    self.tier_stats[tier]['passed'] += 1

                reconstructions = [self.reconstruct_ability(ab) for ab in abilities]
                full_recon = " | ".join(reconstructions)
                
                # Update counts
                for ab in abilities:
                    self.trigger_counts[ab.trigger.name] += 1
                    for eff in ab.effects:
                        self.effect_counts[eff.effect_type.name] += 1
                
                # Analysis
                gaps = self.find_semantic_gaps(text, full_recon)
                issues = self.validate_heuristics(card, abilities)
                
                if gaps:
                    self.stats['semantic_gaps'] += 1
                    for g in gaps: self.gap_counts[g] += 1
                if issues:
                    self.stats['heuristic_issues'] += 1
                    for iss in issues: self.issue_counts[iss] += 1
                
                self.reports_by_card[card_no] = {
                    'name': card.get('name', 'Unknown'),
                    'text': text,
                    'recon': full_recon,
                    'gaps': gaps,
                    'issues': issues,
                    'faq': faq,
                    'score': score
                }
                
            except Exception as e:
                self.stats['parse_failed'] += 1
                self.reports_by_card[card_no] = {'name': card.get('name', 'Unknown'), 'text': text, 'error': str(e), 'faq': faq}

    def write_report(self, output_path: str):
        with open(output_path, 'w', encoding='utf-8-sig') as f:
            f.write("# Master Ability Verification Dashboard\n\n")
            
            # Summary
            f.write("## 1. System Summary\n\n")
            f.write(f"| Metric | Count | Status |\n")
            f.write(f"|--------|-------|--------|\n")
            f.write(f"| Total Cards | {self.stats['total_cards']} | - |\n")
            f.write(f"| Cards with Abilities | {self.stats['with_abilities']} | - |\n")
            f.write(f"| Successful Parse | {self.stats['parsed_ok']} | ✅ |\n")
            f.write(f"| Behaviorally Verified | {len(self.passed_cards)} | ✅ |\n")
            f.write(f"| Semantic Gaps found | {self.stats['semantic_gaps']} | ⚠️ |\n")
            f.write(f"| Heuristic Issues found | {self.stats['heuristic_issues']} | ❌ |\n")
            f.write(f"| Cards with FAQ | {self.stats['with_faq']} | - |\n\n")

            # Complexity Tier Verification
            f.write("## 2. Verification by Complexity Tier\n\n")
            f.write("| Tier | Score Range | Total Cards | Verified | % |\n")
            f.write("|------|-------------|-------------|----------|---|\n")
            tier_meta = {
                'S': '≥ 35 (Final Boss)',
                'A': '≥ 20 (Complex)',
                'B': '≥ 10 (Advanced)',
                'C': '≥ 5 (Standard)',
                'D': '< 5 (Minimal)'
            }
            for t in ['S', 'A', 'B', 'C', 'D']:
                ts = self.tier_stats[t]
                perc = (ts['passed'] / ts['total'] * 100) if ts['total'] > 0 else 0
                emoji = "🏆" if perc == 100 else "💪" if perc > 50 else "🚧"
                f.write(f"| {t} | {tier_meta[t]} | {ts['total']} | {ts['passed']} | {perc:.1f}% {emoji} |\n")
            f.write("\n")
            
            # Effect Coverage
            f.write("## 3. Effect Coverage\n\n")
            f.write("| Effect Type | Count |\n")
            f.write("|-------------|-------|\n")
            for et, count in self.effect_counts.most_common(15):
                f.write(f"| {et} | {count} |\n")
            f.write("\n")
            
            # Detailed Analysis
            f.write("## 3. Analysis Breakdown\n\n")
            f.write("### Semantic Gaps (Keyword Mismatch)\n")
            for gap, count in self.gap_counts.most_common():
                f.write(f"- {gap}: {count} cards\n")
            f.write("\n### Heuristic Issues (Logic Gaps)\n")
            for iss, count in self.issue_counts.most_common():
                f.write(f"- {iss}: {count} cards\n")
            f.write("\n")
            
            # Samples with Gaps/Issues
            f.write("## 4. Problematic Cards (Sample)\n\n")
            count = 0
            for card_no, r in self.reports_by_card.items():
                if (r.get('gaps') or r.get('issues')) and count < 100:
                    status = "✅ (Verified) " if card_no in self.passed_cards else ""
                    f.write(f"### {card_no}: {r['name']} {status}\n")
                    f.write(f"**Text:**\n```\n{r['text']}\n```\n")
                    f.write(f"**Parsed:** {r['recon']}\n")
                    if r['gaps']: f.write(f"⚠️ **Gaps:** {', '.join(r['gaps'])}\n")
                    if r['issues']: f.write(f"❌ **Issues:** {', '.join(r['issues'])}\n")
                    score = r.get('score', 0)
                    tier = "S" if score >= 35 else "A" if score >= 20 else "B" if score >= 10 else "C" if score >= 5 else "D"
                    f.write(f"📈 **Tier:** {tier} (Score: {score})\n")
                    if r['faq']: f.write(f"📚 **FAQ:** {len(r['faq'])} entries\n")
                    f.write("\n---\n\n")
                    count += 1

if __name__ == '__main__':
    validator = MasterValidator('data/cards.json')
    validator.run()
    validator.write_report('docs/master_ability_report.md')
    print("Master report updated at docs/master_ability_report.md")
