"""
Pro Agent - TURN-BASED VERSION
Responds directly to previous arguments, concise and clear
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.gemini_client import GeminiClient

class ProAgent:
    def __init__(self):
        self.client = GeminiClient()
        self.agent_name = "Pro Agent"
    
    def generate_response(self, question, history=None):
        """Generate pro argument that responds to context"""
        try:
            # Check if this is a response to Con agent
            last_con_arg = None
            if history:
                for msg in reversed(history):
                    if msg.get('role') == 'con':
                        last_con_arg = msg.get('content', '')
                        break
            
            if last_con_arg:
                # Responding to Con's argument
                prompt = f"""You are the PRO side in a debate about: "{question}"

The CON side just argued:
"{last_con_arg[:300]}..."

YOUR TASK:
1. Address their main objection directly (why they're wrong or missing the point)
2. Present 1-2 NEW strong points supporting your position
3. Keep it focused and concise (200-250 words)
4. Use clear, complete sentences
5. Make your argument flow naturally - don't use bullet points

Write a compelling response that builds on the debate:"""
            else:
                # Opening argument
                prompt = f"""You are the PRO side arguing FOR: "{question}"

YOUR TASK:
1. Present 2-3 clear, strong reasons supporting this position
2. Use concrete examples or evidence
3. Keep it concise (200-250 words)
4. Write in clear paragraphs with complete sentences
5. Be persuasive but not preachy

Make a strong opening argument:"""
            
            print(f"\n🟢 Pro Agent - Generating response...")
            
            response = self.client.generate(
                prompt=prompt,
                max_tokens=1500,  # INCREASED - was 800
                temperature=0.8
            )
            
            print(f"✅ Pro: {len(response)} chars\n")
            
            return response
        
        except Exception as e:
            return f"Error: {str(e)}"