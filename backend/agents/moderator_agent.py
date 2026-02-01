"""
Moderator Agent - TURN-BASED VERSION  
Synthesizes each round's exchange
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.gemini_client import GeminiClient

class ModeratorAgent:
    def __init__(self):
        self.client = GeminiClient()
        self.agent_name = "Moderator Agent"
    
    def generate_response(self, question, pro_argument, con_argument, history=None):
        """Generate concise synthesis of the current round"""
        try:
            # Determine round number
            round_num = 1
            if history:
                moderator_count = sum(1 for msg in history if msg.get('role') == 'moderator')
                round_num = moderator_count + 1
            
            prompt = f"""You are a neutral moderator in Round {round_num} of a debate about: "{question}"

THIS ROUND'S EXCHANGE:

PRO said:
{pro_argument[:400]}...

CON said:
{con_argument[:400]}...

YOUR TASK:
1. Briefly summarize the key clash in THIS round (what they disagreed about)
2. Note any good points from each side
3. Identify the core tension or trade-off
4. Keep it concise (150-200 words)
5. Write in clear paragraphs
6. Be balanced and fair

Provide a brief, insightful synthesis of this round:"""
            
            print(f"\n⚖️  Moderator - Round {round_num} synthesis...")
            
            response = self.client.generate(
                prompt=prompt,
                max_tokens=1200,  # INCREASED - was 600
                temperature=0.7
            )
            
            print(f"✅ Moderator: {len(response)} chars\n")
            
            return response
        
        except Exception as e:
            return f"Error: {str(e)}"