import re
from typing import List, Dict

class QuantumStateExtractor:
    TEMPERATURE_MAPPING = {
        '💎': 'ABSOLUTE',
        '❄️': 'COLD',
        '🌊': 'COOL',
        '🌡️': 'TEPID',
        '☀️': 'WARM',
        '🔥': 'HOT',
        '⚡': 'PLASMA'
    }

    def extract_states(self, text: str) -> List[Dict]:
        """Extract quantum states from the text."""
        states = []
        lines = text.split('\n')
        
        for line in lines:
            for emoji, temp in self.TEMPERATURE_MAPPING.items():
                if emoji in line:
                    state = {
                        'emoji': emoji,
                        'temperature': temp,
                        'statement': line.replace(emoji, '').strip()
                    }
                    states.append(state)
                    break
        
        return states

    def extract_entanglements(self, text: str) -> List[Dict]:
        """Extract entanglements from the text."""
        entanglements = []
        lines = text.split('\n')
        
        for line in lines:
            if '🔄' in line:
                # Parse entanglement pattern: 🔄 (strength/5) source → target
                match = re.search(r'🔄\s*\((\d+)/5\)\s*(.*?)\s*→\s*(.*)', line)
                if match:
                    entanglement = {
                        'type': 'quantum_entanglement',
                        'strength': int(match.group(1)),
                        'source': match.group(2).strip(),
                        'target': match.group(3).strip()
                    }
                    entanglements.append(entanglement)
        
        return entanglements

extractor = QuantumStateExtractor()
