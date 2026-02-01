"""
Con Agent - TURN-BASED VERSION
Directly challenges Pro's arguments, concise and clear
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.gemini_client import GeminiClient

class ConAgent:
    def __init__(self):
        self.client = GeminiClient()
        self.agent_name = "Con Agent"
    
    def generate_response(self, question, history=None):
        """Generate con argument that directly responds to Pro"""
        try:
            # Get the last Pro argument
            last_pro_arg = None
            if history:
                for msg in reversed(history):
                    if msg.get('role') == 'pro':
                        last_pro_arg = msg.get('content', '')
                        break
            
            if last_pro_arg:
                # Responding to Pro's argument
                prompt = f"""You are the CON side in a debate about: "{question}"

The PRO side just argued:
"{last_pro_arg[:300]}..."

YOUR TASK:
1. Point out specific flaws in their argument
2. Explain WHY their reasoning is wrong or incomplete  
3. Present 1-2 strong counterpoints
4. Keep it focused and concise (200-250 words)
5. Use clear, complete sentences - no bullet points
6. Make it conversational and engaging

Write a compelling counterargument:"""
            else:
                # Opening argument
                prompt = f"""You are the CON side arguing AGAINST: "{question}"

YOUR TASK:
1. Present 2-3 clear reasons opposing this position
2. Identify risks, downsides, or problems
3. Keep it concise (200-250 words)
4. Write in clear paragraphs
5. Be critical but constructive

Make a strong opening argument:"""
            
            print(f"\n🔴 Con Agent - Generating response...")
            
            response = self.client.generate(
                prompt=prompt,
                max_tokens=1500,  # INCREASED - was 800
                temperature=0.8
            )
            
            print(f"✅ Con: {len(response)} chars\n")
            
            return response
        
        except Exception as e:
            return f"Error: {str(e)}"