"""
Session Store - Manages conversation history for debate sessions
Stores messages in memory for multi-turn conversations
"""

from datetime import datetime
from typing import List, Dict, Optional


class SessionStore:
    def __init__(self):
        """Initialize the session store with an empty storage dictionary"""
        self.sessions = {}
        print("✓ Session Store initialized")
    
    def get_history(self, session_id: str) -> List[Dict]:
        """
        Get conversation history for a specific session
        
        Args:
            session_id (str): Unique session identifier
        
        Returns:
            list: List of message dictionaries with role and content
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'created_at': datetime.now().isoformat(),
                'messages': []
            }
        
        return self.sessions[session_id]['messages']
    
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """
        Add a message to the session history
        
        Args:
            session_id (str): Unique session identifier
            role (str): Message role (user, pro, con, moderator)
            content (str): Message content
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'created_at': datetime.now().isoformat(),
                'messages': []
            }
        
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        
        self.sessions[session_id]['messages'].append(message)
    
    def clear_session(self, session_id: str) -> bool:
        """
        Clear all messages for a specific session
        
        Args:
            session_id (str): Unique session identifier
        
        Returns:
            bool: True if session was found and cleared, False otherwise
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def list_sessions(self) -> List[str]:
        """
        Get a list of all active session IDs
        
        Returns:
            list: List of session ID strings
        """
        return list(self.sessions.keys())
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """
        Get metadata about a specific session
        
        Args:
            session_id (str): Unique session identifier
        
        Returns:
            dict: Session metadata or None if not found
        """
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        return {
            'session_id': session_id,
            'created_at': session['created_at'],
            'message_count': len(session['messages']),
            'last_activity': session['messages'][-1]['timestamp'] if session['messages'] else session['created_at']
        }
    
    def get_message_count(self, session_id: str) -> int:
        """
        Get the number of messages in a session
        
        Args:
            session_id (str): Unique session identifier
        
        Returns:
            int: Number of messages in the session
        """
        if session_id not in self.sessions:
            return 0
        return len(self.sessions[session_id]['messages'])
    
    def __len__(self):
        """Return the number of active sessions"""
        return len(self.sessions)
    
    def __str__(self):
        """String representation of the session store"""
        return f"SessionStore(sessions={len(self.sessions)})"