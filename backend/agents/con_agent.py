
# ============================================
# FILE: backend/agents/con_agent.py
# ============================================

"""
Con Agent - Argues against the proposition
"""

import os
from utils.gemini_client import GeminiClient

class ConAgent:
    def __init__(self):
        self.client = GeminiClient()
        self.agent_name = "Con Agent"
    
    def generate_response(self, question, history=None):
        """Generate a con argument"""
        try:
            prompt = f"""You are a debate expert arguing AGAINST this proposition:

"{question}"

Provide a comprehensive argument with 2-3 strong counterpoints opposing this position.
Write 300-400 words across multiple paragraphs for clarity.
Be thorough, critical, and complete your thoughts."""
            
            print(f"\n{'='*60}")
            print(f"🔴 {self.agent_name}")
            print(f"Prompt length: {len(prompt)} chars")
            
            response = self.client.generate(
                prompt=prompt,
                max_tokens=3000,  # VERY HIGH LIMIT
                temperature=0.8
            )
            
            print(f"Response length: {len(response)} chars")
            print(f"First 150 chars: {response[:150]}...")
            print(f"{'='*60}\n")
            
            return response
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return f"Error: {str(e)}"
