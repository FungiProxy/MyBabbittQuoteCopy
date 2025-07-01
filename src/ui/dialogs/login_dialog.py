"""
Login dialog for user authentication.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QMessageBox, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QPixmap, QIcon
import os

from src.core.auth import AuthService


class LoginDialog(QDialog):
    """Modern login dialog with professional styling."""
    
    # Signals
    login_successful = Signal(object)  # Emits user object on successful login
    login_cancelled = Signal()
    
    def __init__(self, auth_service: AuthService, parent=None):
        """Initialize login dialog."""
        super().__init__(parent)
        self.auth_service = auth_service
        self.setup_ui()
        self.setup_connections()
        
        # Focus on username field
        QTimer.singleShot(100, self.username_edit.setFocus)
    
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("MyBabbittQuote - Login")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Logo/Branding section
        self.setup_branding(layout)
        
        # Login form
        self.setup_login_form(layout)
        
        # Buttons
        self.setup_buttons(layout)
        
        # Status bar
        self.setup_status_bar(layout)
        
        # Apply styling
        self.apply_styling()
    
    def setup_branding(self, layout):
        """Setup branding section."""
        # Company logo/name
        logo_label = QLabel("MyBabbittQuote")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFont(QFont("Arial", 24, QFont.Bold))
        logo_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(logo_label)
        
        # Subtitle
        subtitle_label = QLabel("Professional Quote Management System")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 10))
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        layout.addWidget(subtitle_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #bdc3c7;")
        layout.addWidget(separator)
    
    def setup_login_form(self, layout):
        """Setup login form fields."""
        # Username field
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Arial", 10, QFont.Bold))
        username_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(username_label)
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter your username")
        self.username_edit.setFont(QFont("Arial", 11))
        self.username_edit.setMinimumHeight(40)
        self.username_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px 12px;
                background-color: white;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(self.username_edit)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 10, QFont.Bold))
        password_label.setStyleSheet("color: #2c3e50; margin-top: 15px;")
        layout.addWidget(password_label)
        
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Enter your password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFont(QFont("Arial", 11))
        self.password_edit.setMinimumHeight(40)
        self.password_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px 12px;
                background-color: white;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(self.password_edit)
        
        # Remember me checkbox
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setFont(QFont("Arial", 9))
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #2c3e50;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border-color: #3498db;
            }
        """)
        layout.addWidget(self.remember_checkbox)
    
    def setup_buttons(self, layout):
        """Setup action buttons."""
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.login_button.setMinimumHeight(45)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        layout.addWidget(self.login_button)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(QFont("Arial", 11))
        self.cancel_button.setMinimumHeight(45)
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7b7d;
            }
        """)
        layout.addWidget(self.cancel_button)
    
    def setup_status_bar(self, layout):
        """Setup status bar for messages."""
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 9))
        self.status_label.setStyleSheet("color: #e74c3c; min-height: 20px;")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        # Add stretch to push everything up
        layout.addStretch()
    
    def setup_connections(self):
        """Setup signal connections."""
        self.login_button.clicked.connect(self.handle_login)
        self.cancel_button.clicked.connect(self.handle_cancel)
        
        # Enter key handling
        self.username_edit.returnPressed.connect(self.handle_login)
        self.password_edit.returnPressed.connect(self.handle_login)
    
    def apply_styling(self):
        """Apply overall dialog styling."""
        self.setStyleSheet("""
            QDialog {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 10px;
            }
        """)
    
    def handle_login(self):
        """Handle login attempt."""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        remember_me = self.remember_checkbox.isChecked()
        
        # Validation
        if not username:
            self.show_error("Please enter a username")
            self.username_edit.setFocus()
            return
        
        if not password:
            self.show_error("Please enter a password")
            self.password_edit.setFocus()
            return
        
        # Disable login button during authentication
        self.login_button.setEnabled(False)
        self.login_button.setText("Logging in...")
        self.clear_error()
        
        # Attempt login
        success, message = self.auth_service.login(
            username, password, remember_me
        )
        
        if success:
            user = self.auth_service.get_current_user()
            self.login_successful.emit(user)
            self.accept()
        else:
            self.show_error(message)
            self.password_edit.clear()
            self.password_edit.setFocus()
        
        # Re-enable login button
        self.login_button.setEnabled(True)
        self.login_button.setText("Login")
    
    def handle_cancel(self):
        """Handle cancel action."""
        self.login_cancelled.emit()
        self.reject()
    
    def show_error(self, message: str):
        """Show error message."""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: #e74c3c; min-height: 20px;")
    
    def clear_error(self):
        """Clear error message."""
        self.status_label.setText("")
    
    def closeEvent(self, event):
        """Handle dialog close event."""
        self.login_cancelled.emit()
        super().closeEvent(event) 