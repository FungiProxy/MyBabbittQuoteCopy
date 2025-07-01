"""
Session management for user authentication.
"""

import json
import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from .user_manager import User


class SessionManager:
    """Manages user sessions and authentication state."""
    
    def __init__(self, session_file: str = "data/session.json"):
        """Initialize session manager."""
        self.session_file = session_file
        self.current_user: Optional[User] = None
        self.session_data: Dict[str, Any] = {}
        self._load_session()
    
    def _load_session(self):
        """Load session data from file."""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    self.session_data = json.load(f)
        except Exception as e:
            print(f"Error loading session: {e}")
            self.session_data = {}
    
    def _save_session(self):
        """Save session data to file."""
        try:
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            with open(self.session_file, 'w') as f:
                json.dump(self.session_data, f, indent=2)
        except Exception as e:
            print(f"Error saving session: {e}")
    
    def login(self, user: User, remember_me: bool = False):
        """Log in a user and create a session."""
        self.current_user = user
        
        # Update session data
        self.session_data.update({
            'user_id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'role': user.role,
            'login_time': datetime.now().isoformat(),
            'remember_me': remember_me
        })
        
        self._save_session()
    
    def logout(self):
        """Log out the current user."""
        self.current_user = None
        self.session_data = {}
        
        # Remove session file
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
        except Exception as e:
            print(f"Error removing session file: {e}")
    
    def is_logged_in(self) -> bool:
        """Check if a user is currently logged in."""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[User]:
        """Get the currently logged in user."""
        return self.current_user
    
    def get_user_role(self) -> Optional[str]:
        """Get the role of the currently logged in user."""
        return self.current_user.role if self.current_user else None
    
    def has_permission(self, permission: str) -> bool:
        """Check if the current user has a specific permission."""
        if not self.current_user:
            return False
        
        # Simple role-based permissions
        role_permissions = {
            'admin': ['all'],
            'manager': ['view_quotes', 'create_quotes', 'edit_quotes', 'view_reports'],
            'user': ['view_quotes', 'create_quotes'],
            'viewer': ['view_quotes']
        }
        
        user_permissions = role_permissions.get(self.current_user.role, [])
        return 'all' in user_permissions or permission in user_permissions
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get current session information."""
        if not self.current_user:
            return {}
        
        return {
            'user_id': self.current_user.id,
            'username': self.current_user.username,
            'full_name': self.current_user.full_name,
            'role': self.current_user.role,
            'login_time': self.session_data.get('login_time'),
            'remember_me': self.session_data.get('remember_me', False)
        }
    
    def update_user_info(self, user: User):
        """Update session with new user information."""
        if self.current_user and self.current_user.id == user.id:
            self.current_user = user
            self.session_data.update({
                'username': user.username,
                'full_name': user.full_name,
                'role': user.role
            })
            self._save_session() 