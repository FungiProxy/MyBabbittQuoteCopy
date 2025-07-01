"""
Main authentication service that coordinates user management and sessions.
"""

from typing import Optional, Tuple
from .user_manager import UserManager, User
from .session_manager import SessionManager


class AuthService:
    """Main authentication service."""
    
    def __init__(self):
        """Initialize authentication service."""
        self.user_manager = UserManager()
        self.session_manager = SessionManager()
        
        # Create default admin user if no users exist
        self.user_manager.create_default_admin()
    
    def login(self, username: str, password: str, 
              remember_me: bool = False, ip_address: str = None) -> Tuple[bool, str]:
        """
        Authenticate user and create session.
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Authenticate user
        user = self.user_manager.authenticate_user(username, password, ip_address)
        
        if not user:
            return False, "Invalid username or password"
        
        if not user.is_active:
            return False, "Account is deactivated"
        
        # Create session
        self.session_manager.login(user, remember_me)
        
        return True, f"Welcome, {user.full_name}!"
    
    def logout(self):
        """Log out current user."""
        self.session_manager.logout()
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self.session_manager.is_logged_in()
    
    def get_current_user(self) -> Optional[User]:
        """Get current user."""
        return self.session_manager.get_current_user()
    
    def get_user_role(self) -> Optional[str]:
        """Get current user role."""
        return self.session_manager.get_user_role()
    
    def has_permission(self, permission: str) -> bool:
        """Check if current user has permission."""
        return self.session_manager.has_permission(permission)
    
    def change_password(self, current_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change current user's password.
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        user = self.get_current_user()
        if not user:
            return False, "No user logged in"
        
        if len(new_password) < 6:
            return False, "Password must be at least 6 characters long"
        
        success = self.user_manager.change_password(user.id, current_password, new_password)
        
        if success:
            return True, "Password changed successfully"
        else:
            return False, "Current password is incorrect"
    
    def create_user(self, username: str, email: str, full_name: str, 
                   password: str, role: str = "user") -> tuple[bool, str]:
        """
        Create a new user account.
        
        Returns:
            tuple[bool, str]: (success, message)
        """
        # Check if current user has permission
        if not self.has_permission('manage_users'):
            return False, "Insufficient permissions"
        
        success, message = self.user_manager.create_user(username, email, full_name, password, role)
        return success, message
    
    def get_session_info(self):
        """Get current session information."""
        return self.session_manager.get_session_info()
    
    def require_auth(self, permission: str = None):
        """
        Decorator to require authentication for functions.
        
        Usage:
            @auth_service.require_auth('create_quotes')
            def create_quote():
                pass
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not self.is_logged_in():
                    raise PermissionError("Authentication required")
                
                if permission and not self.has_permission(permission):
                    raise PermissionError(f"Permission '{permission}' required")
                
                return func(*args, **kwargs)
            return wrapper
        return decorator 