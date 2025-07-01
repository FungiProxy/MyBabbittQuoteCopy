"""
Authentication manager for the main application.
"""

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QObject, Signal
from typing import Optional

from src.core.auth import AuthService
from src.core.auth.user_manager import User
from src.ui.dialogs.login_dialog import LoginDialog
from src.ui.dialogs.user_management_dialog import UserManagementDialog


class AuthManager(QObject):
    """Manages authentication flow and user sessions."""
    
    # Signals
    user_logged_in = Signal(object)  # Emits user object
    user_logged_out = Signal()
    authentication_required = Signal()
    
    def __init__(self, app: QApplication):
        """Initialize authentication manager."""
        super().__init__()
        self.app = app
        self.auth_service = AuthService()
        self.current_user: Optional[User] = None
        
        # Check if user is already logged in
        if self.auth_service.is_logged_in():
            self.current_user = self.auth_service.get_current_user()
            self.user_logged_in.emit(self.current_user)
    
    def show_login_dialog(self) -> bool:
        """
        Show login dialog and handle authentication.
        
        Returns:
            bool: True if login successful, False otherwise
        """
        login_dialog = LoginDialog(self.auth_service)
        
        # Connect signals
        login_dialog.login_successful.connect(self.on_login_successful)
        login_dialog.login_cancelled.connect(self.on_login_cancelled)
        
        # Show dialog
        result = login_dialog.exec()
        
        return result == LoginDialog.Accepted
    
    def on_login_successful(self, user: User):
        """Handle successful login."""
        self.current_user = user
        self.user_logged_in.emit(user)
        
        # Show welcome message
        QMessageBox.information(
            None, "Welcome", 
            f"Welcome back, {user.full_name}!\nRole: {user.role.title()}"
        )
    
    def on_login_cancelled(self):
        """Handle login cancellation."""
        self.user_logged_out.emit()
    
    def logout(self):
        """Log out current user."""
        if self.current_user:
            self.auth_service.logout()
            self.current_user = None
            self.user_logged_out.emit()
            
            QMessageBox.information(
                None, "Logged Out", 
                "You have been successfully logged out."
            )
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self.auth_service.is_logged_in()
    
    def get_current_user(self) -> Optional[User]:
        """Get current user."""
        return self.current_user
    
    def get_user_role(self) -> Optional[str]:
        """Get current user role."""
        return self.current_user.role if self.current_user else None
    
    def has_permission(self, permission: str) -> bool:
        """Check if current user has permission."""
        return self.auth_service.has_permission(permission)
    
    def show_user_management(self):
        """Show user management dialog (admin only)."""
        if not self.has_permission('manage_users'):
            QMessageBox.warning(
                None, "Access Denied", 
                "You don't have permission to manage users."
            )
            return
        
        dialog = UserManagementDialog(self.auth_service)
        dialog.exec()
    
    def change_password(self):
        """Show password change dialog."""
        if not self.current_user:
            QMessageBox.warning(
                None, "Error", 
                "No user is currently logged in."
            )
            return
        
        # TODO: Implement password change dialog
        QMessageBox.information(
            None, "Info", 
            "Password change functionality will be implemented soon."
        )
    
    def require_auth(self, permission: str = None):
        """
        Decorator to require authentication for functions.
        
        Usage:
            @auth_manager.require_auth('create_quotes')
            def create_quote():
                pass
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not self.is_logged_in():
                    self.authentication_required.emit()
                    return None
                
                if permission and not self.has_permission(permission):
                    QMessageBox.warning(
                        None, "Access Denied", 
                        f"You don't have permission to perform this action."
                    )
                    return None
                
                return func(*args, **kwargs)
            return wrapper
        return decorator 