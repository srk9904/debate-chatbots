
# ============================================
# FILE: backend/agents/moderator_agent.py
# ============================================

"""
Moderator Agent - Synthesizes both arguments
"""

import os
from utils.gemini_client import GeminiClient

class ModeratorAgent:
    def __init__(self):
        self.client = GeminiClient()
        self.agent_name = "Moderator Agent"
    
    def generate_response(self, question, pro_argument, con_argument, history=None):
        """Generate a moderated synthesis"""
        try:
            prompt = f"""You are a neutral debate moderator.

DEBATE TOPIC: "{question}"

PRO ARGUMENT:
{pro_argument}

CON ARGUMENT:
{con_argument}

Provide a balanced synthesis that:
1. Summarizes key points from both sides
2. Identifies areas of agreement and disagreement
3. Offers a nuanced conclusion

Write 350-450 words across multiple paragraphs. Be thorough and complete your analysis."""
            
            print(f"\n{'='*60}")
            print(f"⚖️  {self.agent_name}")
            print(f"Prompt length: {len(prompt)} chars")
            
            response = self.client.generate(
                prompt=prompt,
                max_tokens=3000,  # VERY HIGH LIMIT
                temperature=0.7
            )
            
            print(f"Response length: {len(response)} chars")
            print(f"First 150 chars: {response[:150]}...")
            print(f"{'='*60}\n")
            
            return response
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return f"Error: {str(e)}"