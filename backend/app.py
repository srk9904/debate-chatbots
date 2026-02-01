"""
Gemini Multi-Agent Debate Console - SINGLE API CALL VERSION
Generates all three agent responses in one call to save rate limits
IMPROVED: Better readability with bullet points for long responses
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import re
from dotenv import load_dotenv

from utils.gemini_client import GeminiClient
from memory.session_store import SessionStore

load_dotenv()

app = Flask(__name__)
CORS(app)

session_store = SessionStore()
gemini_client = GeminiClient()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'message': 'Gemini Multi-Agent Debate Console - Single API Call Edition',
        'version': '3.1.0'
    })

def generate_all_responses(question, round_num, history):
    """
    Generate all three agent responses in a single API call
    Returns: {'pro': '...', 'con': '...', 'moderator': '...'}
    """
    
    # Get previous arguments for context
    last_pro_arg = None
    last_con_arg = None
    
    if history:
        for msg in reversed(history):
            if msg.get('role') == 'con' and not last_con_arg:
                last_con_arg = msg.get('content', '')
            if msg.get('role') == 'pro' and not last_pro_arg:
                last_pro_arg = msg.get('content', '')
            if last_pro_arg and last_con_arg:
                break
    
    # Build the unified prompt
    if round_num == 1:
        # Opening round
        prompt = f"""You are managing a debate with three AI agents on the topic: "{question}"

Generate responses for all three agents in this EXACT format:

===PRO_AGENT===
[Pro's response arguing FOR the proposition]

===CON_AGENT===
[Con's response arguing AGAINST the proposition]

===MODERATOR===
[Moderator's balanced synthesis]

INSTRUCTIONS FOR EACH AGENT:

PRO AGENT:
- Make 2-3 distinct, strong points SUPPORTING the proposition
- Keep TOTAL response under 250 words
- If your response exceeds 200 words, use bullet points (•) with brief explanations
- If under 200 words, use clear paragraphs
- Each point should be concise but complete
- Use concrete examples briefly

CON AGENT:
- Make 2-3 distinct, strong points OPPOSING the proposition
- Keep TOTAL response under 250 words
- If your response exceeds 200 words, use bullet points (•) with brief explanations
- If under 200 words, use clear paragraphs
- Each point should be concise but complete
- Identify key flaws and risks briefly

MODERATOR:
- Summarize the key clash between Pro and Con
- Keep TOTAL response under 200 words
- If your response exceeds 150 words, use bullet points (•) for clarity
- If under 150 words, use clear paragraphs
- Note strongest point from each side
- Identify the core tension

Now generate all three responses:"""

    else:
        # Continuation round
        context = f"""
PREVIOUS EXCHANGE:

PRO previously argued:
{last_pro_arg[:400] if last_pro_arg else 'N/A'}...

CON previously argued:
{last_con_arg[:400] if last_con_arg else 'N/A'}...
"""
        
        prompt = f"""You are managing Round {round_num} of a debate on: "{question}"

{context}

Generate responses for all three agents in this EXACT format:

===PRO_AGENT===
[Pro's response]

===CON_AGENT===
[Con's response]

===MODERATOR===
[Moderator's synthesis]

INSTRUCTIONS:

PRO AGENT:
- Address the main objection Con raised
- Make 1-2 NEW points supporting your position
- Keep TOTAL response under 250 words
- If response exceeds 200 words, use bullet points (•)
- If under 200 words, use paragraphs
- Be concise but complete

CON AGENT:
- Address what Pro just argued
- Point out specific flaws
- Make 1-2 NEW counter-points
- Keep TOTAL response under 250 words
- If response exceeds 200 words, use bullet points (•)
- If under 200 words, use paragraphs
- Be concise but complete

MODERATOR:
- Summarize the key clash in THIS round
- Note how debate has evolved
- Keep TOTAL response under 200 words
- If response exceeds 150 words, use bullet points (•)
- If under 150 words, use paragraphs
- Be balanced and fair

Now generate all three responses:"""
    
    print(f"\n{'='*60}")
    print(f"🎯 Generating all agents for Round {round_num}...")
    print(f"{'='*60}\n")
    
    # Single API call for all three
    response = gemini_client.generate(
        prompt=prompt,
        max_tokens=3000,  # Reduced since we want shorter responses
        temperature=0.8
    )
    
    print(f"✅ Received combined response: {len(response)} chars\n")
    
    # Parse the response
    try:
        # Extract each agent's response using markers
        pro_match = re.search(r'===PRO_AGENT===\s*(.*?)\s*===CON_AGENT===', response, re.DOTALL)
        con_match = re.search(r'===CON_AGENT===\s*(.*?)\s*===MODERATOR===', response, re.DOTALL)
        mod_match = re.search(r'===MODERATOR===\s*(.*?)$', response, re.DOTALL)
        
        pro_response = pro_match.group(1).strip() if pro_match else "Error: Could not parse Pro response"
        con_response = con_match.group(1).strip() if con_match else "Error: Could not parse Con response"
        moderator_response = mod_match.group(1).strip() if mod_match else "Error: Could not parse Moderator response"
        
        print(f"📊 Parsed responses:")
        print(f"   Pro: {len(pro_response)} chars")
        print(f"   Con: {len(con_response)} chars")
        print(f"   Mod: {len(moderator_response)} chars\n")
        
        return {
            'pro': pro_response,
            'con': con_response,
            'moderator': moderator_response
        }
    
    except Exception as e:
        print(f"❌ Error parsing response: {e}")
        return {
            'pro': f"Error parsing response: {e}",
            'con': f"Error parsing response: {e}",
            'moderator': f"Error parsing response: {e}"
        }

@app.route('/debate/start', methods=['POST'])
def start_debate():
    """
    Start a new debate - generates all Round 1 responses at once
    """
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        session_id = data.get('session_id', 'default')
        total_rounds = data.get('rounds', 3)
        
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Clear previous session
        session_store.clear_session(session_id)
        session_store.add_message(session_id, 'user', question)
        
        print(f"\n{'='*60}")
        print(f"🎭 NEW DEBATE STARTED")
        print(f"Question: {question}")
        print(f"Total Rounds: {total_rounds}")
        print(f"{'='*60}\n")
        
        # Generate all Round 1 responses in one call
        responses = generate_all_responses(question, 1, [])
        
        # Store all responses
        session_store.add_message(session_id, 'pro', responses['pro'])
        session_store.add_message(session_id, 'con', responses['con'])
        session_store.add_message(session_id, 'moderator', responses['moderator'])
        
        return jsonify({
            'success': True,
            'round': 1,
            'total_rounds': total_rounds,
            'responses': responses,
            'session_id': session_id
        })
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/debate/next-round', methods=['POST'])
def next_round():
    """
    Generate next round - all three responses at once
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        current_round = data.get('current_round', 1)
        total_rounds = data.get('total_rounds', 3)
        
        next_round_num = current_round + 1
        
        if next_round_num > total_rounds:
            return jsonify({
                'success': True,
                'debate_complete': True,
                'message': 'Debate completed'
            })
        
        history = session_store.get_history(session_id)
        question = history[0]['content'] if history else "No question"
        
        print(f"\n{'='*60}")
        print(f"🔄 Generating Round {next_round_num}")
        print(f"{'='*60}\n")
        
        # Generate all responses for this round
        responses = generate_all_responses(question, next_round_num, history)
        
        # Store all responses
        session_store.add_message(session_id, 'pro', responses['pro'])
        session_store.add_message(session_id, 'con', responses['con'])
        session_store.add_message(session_id, 'moderator', responses['moderator'])
        
        return jsonify({
            'success': True,
            'round': next_round_num,
            'total_rounds': total_rounds,
            'responses': responses,
            'debate_complete': next_round_num >= total_rounds,
            'session_id': session_id
        })
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/debate/add-comment', methods=['POST'])
def add_comment():
    """User adds a comment during the debate"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        comment = data.get('comment', '').strip()
        
        if comment:
            session_store.add_message(session_id, 'user', comment)
        
        return jsonify({
            'success': True,
            'message': 'Comment added to debate history'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    history = session_store.get_history(session_id)
    return jsonify({'success': True, 'session_id': session_id, 'history': history})

@app.route('/clear/<session_id>', methods=['DELETE'])
def clear_history(session_id):
    session_store.clear_session(session_id)
    return jsonify({'success': True, 'message': f'Session {session_id} cleared'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎭 Gemini Multi-Agent Debate Console v3.1")
    print("="*60)
    print(f"API Key: {'✓ Loaded' if GEMINI_API_KEY else '✗ Missing'}")
    print("\n✨ NEW FEATURES:")
    print("   • Single API call per round (3x fewer requests!)")
    print("   • Smart formatting: bullets for long responses")
    print("   • Better readability and concise arguments")
    print("   • Agents respond directly to each other")
    print("="*60)
    print("Server: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)