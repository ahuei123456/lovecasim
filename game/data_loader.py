"""
Data loader for Love Live Card Game.
Parses the cards.json file and converts it into GameState objects.
"""

import json
import numpy as np
from typing import Dict, Tuple

try:
    from game.game_state import MemberCard, LiveCard
    from game.ability import AbilityParser
except ImportError:
    from game_state import MemberCard, LiveCard
    from ability import AbilityParser

class CardDataLoader:
    def __init__(self, json_path: str):
        self.json_path = json_path
        
    def _resolve_img_path(self, data: dict) -> str:
        """Resolve local image path, falling back to URL or deriving from URL."""
        img_path = data.get('_img', '')
        if img_path:
            # Strip 'img/' prefix since Flask route /img/ adds it
            if img_path.startswith('img/'):
                return img_path[4:]  # Remove 'img/' prefix
            return img_path
        
        raw_url = data.get('img', '')
        if raw_url and 'cardlist/' in raw_url:
            # Example: .../cardlist/PLSD01/LL-E-001-SD.png
            try:
                parts = raw_url.split('cardlist/')[-1].split('/')
                if len(parts) >= 2:
                    product = parts[0]
                    filename = parts[1]
                    # Server route is /img/<path>, so return cards/PRODUCT/FILENAME
                    return f"cards/{product}/{filename}"
            except:
                pass
        return raw_url

    def load(self) -> Tuple[Dict[int, MemberCard], Dict[int, LiveCard], Dict[int, MemberCard]]:
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        members = {}
        lives = {}
        energy = {}
        
        # Consistent mapping for string IDs to ints
        # We need a stable hash or a saved mapping, but for this session we'll generate one
        # Ideally, we should sort keys to ensure deterministic ID assignment
        
        sorted_keys = sorted(data.keys())
        # Use a simple counter for IDs to keep them small for array indexing
        # 0-999: Members
        # 1000-1999: Lives
        # 2000+: Energy (handled separately or as generic)
        
        m_idx = 0
        l_idx = 1000
        e_idx = 2000
        
        for key in sorted_keys:
            card_data = data[key]
            ctype = card_data.get('type')
            
            if ctype == 'メンバー':
                m_card = self._parse_member(m_idx, card_data)
                members[m_idx] = m_card
                m_idx += 1
            elif ctype == 'ライブ':
                l_card = self._parse_live(l_idx, card_data)
                lives[l_idx] = l_card
                l_idx += 1
            elif ctype == 'エネルギー':
                # Use simple MemberCard struct for energy for now or just dict
                # Standard Energy Card ID is usually fixed, but we'll assign dynamic
                e_card = self._parse_member(e_idx, card_data) # Structure is similar enough
                energy[e_idx] = e_card
                e_idx += 1
                
        return members, lives, energy

    def _parse_hearts(self, heart_dict: dict) -> np.ndarray:
        """
        Parses heart dictionary: {"heart01": 1, "heart06": 2}
        Returns array of 6 ints.
        """
        hearts = np.zeros(6, dtype=np.int32)
        if not heart_dict:
            return hearts
            
        # Mapping: heart01 -> 0, heart02 -> 1, ... heart06 -> 5
        for k, v in heart_dict.items():
            if k.startswith('heart'):
                try:
                    idx = int(k.replace('heart', '')) - 1
                    if 0 <= idx < 6:
                        hearts[idx] = int(v)
                except ValueError:
                    pass
        return hearts
    
    def _parse_live_reqs(self, req_dict: dict) -> np.ndarray:
        """
        Parses live requirements. Like hearts but index 6 is 'any'.
        """
        reqs = np.zeros(7, dtype=np.int32)
        if not req_dict:
            return reqs
            
        # Standard colors
        base_hearts = self._parse_hearts(req_dict)
        reqs[:6] = base_hearts
        
        # 'star' or 'any' or 'common'
        for k, v in req_dict.items():
            if k in ['star', 'any', 'common']:
                reqs[6] = int(v)
                
        return reqs

    def _parse_blade_hearts(self, heart_dict: dict) -> np.ndarray:
        """
        Parses blade heart dictionary: {"b_heart06": 1}
        Returns array of 6 ints.
        """
        hearts = np.zeros(6, dtype=np.int32)
        if not heart_dict:
            return hearts
            
        # Mapping: b_heart01 -> 0, ... b_heart06 -> 5
        for k, v in heart_dict.items():
            if k.startswith('b_heart'):
                try:
                    idx = int(k.replace('b_heart', '')) - 1
                    if 0 <= idx < 6:
                        hearts[idx] = int(v)
                except ValueError:
                    pass
        return hearts

    def _parse_member(self, card_id: int, data: dict) -> MemberCard:
        # Cost
        cost = int(data.get('cost', 0))
        
        # Blades (AP)
        # JSON key 'blade': 3
        blades = int(data.get('blade', 0))
        
        # Hearts
        hearts = self._parse_hearts(data.get('base_heart', {}))
        
        # Abilities
        raw_ability = data.get('ability', '')
        abilities = AbilityParser.parse_ability_text(raw_ability)
        
        # Blade hearts (Hearts given during Yell)
        blade_hearts = self._parse_blade_hearts(data.get('blade_heart', {}))
        
        # Volume/Draw icons (from special_heart)
        spec = data.get('special_heart', {})
        volume = int(spec.get('score', 0))
        draw = int(spec.get('draw', 0))
        
        return MemberCard(
            card_id=card_id,
            name=data.get('name', 'Unknown'),
            cost=cost,
            hearts=hearts,
            blade_hearts=blade_hearts, 
            blades=blades,
            group=data.get('series', ''),
            unit=data.get('unit', ''),
            abilities=abilities, # Store ability objects
            img_path=self._resolve_img_path(data),
            ability_text=raw_ability,
            volume_icons=volume,
            draw_icons=draw
        )

    def _parse_live(self, card_id: int, data: dict) -> LiveCard:
        score = int(data.get('score', 0))
        reqs = self._parse_live_reqs(data.get('need_heart', {}))
        
        raw_ability = data.get('ability', '')
        abilities = AbilityParser.parse_ability_text(raw_ability)
        
        # Volume/Draw icons (from special_heart)
        spec = data.get('special_heart', {})
        volume = int(spec.get('score', 0))
        draw = int(spec.get('draw', 0))
        
        return LiveCard(
            card_id=card_id,
            name=data.get('name', 'Unknown'),
            score=score,
            required_hearts=reqs,
            abilities=abilities,
            group=data.get('series', ''),
            img_path=self._resolve_img_path(data),
            ability_text=raw_ability,
            volume_icons=volume,
            draw_icons=draw
        )
