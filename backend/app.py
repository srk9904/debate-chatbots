"""
Gemini Multi-Agent Debate Console - Flask Backend
Main application file handling routes and agent coordination
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
from dotenv import load_dotenv

# Import agents
from agents.pro_agent import ProAgent
from agents.con_agent import ConAgent
from agents.moderator_agent import ModeratorAgent

# Import session store
from memory.session_store import SessionStore

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize session store
session_store = SessionStore()

# Initialize agents
pro_agent = ProAgent()
con_agent = ConAgent()
moderator_agent = ModeratorAgent()

# Verify API key is loaded
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment variables!")
    print("Please create a .env file with your API key")

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Gemini Multi-Agent Debate Console API',
        'version': '1.0.0'
    })

@app.route('/debate', methods=['POST'])
def debate():
    """
    Main debate endpoint
    Accepts a question and returns responses from all three agents
    """
    try:
        # Parse request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        question = data.get('question', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Get conversation history for this session
        history = session_store.get_history(session_id)
        
        # Add user question to history
        session_store.add_message(session_id, 'user', question)
        
        print(f"\n{'='*60}")
        print(f"Session: {session_id}")
        print(f"Question: {question}")
        print(f"{'='*60}\n")
        
        # Call Pro Agent
        print("🟢 Calling Pro Agent...")
        pro_response = pro_agent.generate_response(question, history)
        session_store.add_message(session_id, 'pro', pro_response)
        print(f"✓ Pro Agent responded ({len(pro_response)} chars)\n")
        
        # Add delay to avoid rate limiting (free tier: 5 requests/minute)
        print("⏳ Waiting 5 seconds to respect rate limits...")
        time.sleep(5)
        
        # Call Con Agent
        print("🔴 Calling Con Agent...")
        con_response = con_agent.generate_response(question, history)
        session_store.add_message(session_id, 'con', con_response)
        print(f"✓ Con Agent responded ({len(con_response)} chars)\n")
        
        # Add delay to avoid rate limiting
        print("⏳ Waiting 5 seconds to respect rate limits...")
        time.sleep(5)
        
        # Call Moderator Agent (gets both Pro and Con responses)
        print("⚖️  Calling Moderator Agent...")
        moderator_response = moderator_agent.generate_response(
            question=question,
            pro_argument=pro_response,
            con_argument=con_response,
            history=history
        )
        session_store.add_message(session_id, 'moderator', moderator_response)
        print(f"✓ Moderator responded ({len(moderator_response)} chars)\n")
        
        print(f"{'='*60}")
        print("✅ Debate completed successfully")
        print(f"{'='*60}\n")
        
        # Return all responses
        return jsonify({
            'success': True,
            'pro': pro_response,
            'con': con_response,
            'moderator': moderator_response,
            'session_id': session_id
        })
    
    except Exception as e:
        print(f"\n❌ Error in debate endpoint: {str(e)}\n")
        
        # Check if it's a rate limit error
        if "rate limit" in str(e).lower() or "quota" in str(e).lower():
            return jsonify({
                'success': False,
                'error': 'Rate limit exceeded. Please wait a minute before trying again. Free tier limit: 5 requests per minute.'
            }), 429
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    """
    Get conversation history for a session
    """
    try:
        history = session_store.get_history(session_id)
        return jsonify({
            'success': True,
            'session_id': session_id,
            'history': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/clear/<session_id>', methods=['DELETE'])
def clear_history(session_id):
    """
    Clear conversation history for a session
    """
    try:
        session_store.clear_session(session_id)
        return jsonify({
            'success': True,
            'message': f'Session {session_id} cleared'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/sessions', methods=['GET'])
def list_sessions():
    """
    List all active sessions
    """
    try:
        sessions = session_store.list_sessions()
        return jsonify({
            'success': True,
            'sessions': sessions,
            'count': len(sessions)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Gemini Multi-Agent Debate Console")
    print("="*60)
    print(f"API Key Status: {'✓ Loaded' if GEMINI_API_KEY else '✗ Missing'}")
    print("\n⚠️  FREE TIER RATE LIMITS:")
    print("   - 5 requests per minute per model")
    print("   - Each debate uses 3 requests (Pro, Con, Moderator)")
    print("   - Automatic 5-second delays added between calls")
    print("   - Total debate time: ~15-20 seconds")
    print("\n💡 TIP: Upgrade your API plan for faster responses")
    print("="*60)
    print("Server starting on http://localhost:5000")
    print("="*60 + "\n")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )