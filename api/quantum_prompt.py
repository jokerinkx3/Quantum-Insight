class QuantumPromptGenerator:
    @staticmethod
    def get_quantum_prompt() -> str:
        return """
Please analyze the above text and provide a quantum state analysis in the following format:

Quantum State Analysis:
💎 [Absolute statements - highest certainty]
❄️ [Cold statements - very high certainty]
🌊 [Cool statements - high certainty]
🌡️ [Tepid statements - moderate certainty]
☀️ [Warm statements - low certainty]
🔥 [Hot statements - very low certainty]
⚡ [Plasma statements - highly uncertain/speculative]

Entanglements:
🔄 (strength/5) [source statement] → [target statement]

Rules:
1. Each statement should be preceded by the appropriate emoji
2. Entanglements should show relationships between statements
3. Rate entanglement strength from 1-5
""".strip()

prompt_generator = QuantumPromptGenerator()
