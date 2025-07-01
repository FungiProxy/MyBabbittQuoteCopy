"""
User management dialog for administrators.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QMessageBox, QFrame, QHeaderView, QAbstractItemView,
    QFormLayout, QGroupBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QColor, QKeyEvent
from typing import List, Optional

from src.core.auth import AuthService
from src.core.auth.user_manager import User
from src.ui.components.phone_input import PhoneNumberInput


class UserManagementDialog(QDialog):
    """Dialog for managing user accounts."""
    
    def __init__(self, auth_service: AuthService, parent=None):
        """Initialize user management dialog."""
        super().__init__(parent)
        self.auth_service = auth_service
        self.users: List[User] = []
        self.setup_ui()
        self.setup_connections()
        self.load_users()
    
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("User Management")
        self.setMinimumSize(800, 900)  # Height matches main window
        self.resize(800, 900)          # Height matches main window
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("User Management")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # User table
        self.setup_user_table(layout)
        
        # Action buttons
        self.setup_action_buttons(layout)
        
        # Add/Edit user form
        self.setup_user_form(layout)
        
        # Apply styling
        self.apply_styling()
    
    def setup_user_table(self, layout):
        """Setup user table."""
        # Table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(7)
        self.user_table.setHorizontalHeaderLabels([
            "ID", "Username", "Full Name", "Email", "Role", "Work Phone", "Status"
        ])
        
        # Table styling
        self.user_table.setAlternatingRowColors(True)
        self.user_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.user_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.user_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Header styling
        header = self.user_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.user_table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                gridline-color: #ecf0f1;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.user_table)
    
    def setup_action_buttons(self, layout):
        """Setup action buttons."""
        button_layout = QHBoxLayout()
        
        # Add user button
        self.add_user_button = QPushButton("Add User")
        self.add_user_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.add_user_button.setMinimumHeight(35)
        self.add_user_button.setCursor(Qt.PointingHandCursor)
        self.add_user_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        button_layout.addWidget(self.add_user_button)
        
        # Edit user button
        self.edit_user_button = QPushButton("Edit User")
        self.edit_user_button.setFont(QFont("Arial", 10))
        self.edit_user_button.setMinimumHeight(35)
        self.edit_user_button.setCursor(Qt.PointingHandCursor)
        self.edit_user_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:pressed {
                background-color: #d35400;
            }
        """)
        button_layout.addWidget(self.edit_user_button)
        
        # Delete user button
        self.delete_user_button = QPushButton("Delete User")
        self.delete_user_button.setFont(QFont("Arial", 10))
        self.delete_user_button.setMinimumHeight(35)
        self.delete_user_button.setCursor(Qt.PointingHandCursor)
        self.delete_user_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        button_layout.addWidget(self.delete_user_button)
        
        button_layout.addStretch()
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.setFont(QFont("Arial", 10))
        self.close_button.setMinimumHeight(35)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7b7d;
            }
        """)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
    
    def setup_user_form(self, layout):
        """Setup user form for adding/editing users."""
        # Form group
        form_group = QGroupBox("Add/Edit User")
        form_group.setFont(QFont("Arial", 11, QFont.Bold))
        form_group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
        """)
        
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(15)
        
        # Username field
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter username")
        self.username_edit.setFont(QFont("Arial", 10))
        self.username_edit.setMinimumHeight(30)
        self.username_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                padding: 5px 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow("Username:", self.username_edit)
        
        # Email field
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Enter email address")
        self.email_edit.setFont(QFont("Arial", 10))
        self.email_edit.setMinimumHeight(30)
        self.email_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                padding: 5px 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow("Email:", self.email_edit)
        
        # Full name field
        self.fullname_edit = QLineEdit()
        self.fullname_edit.setPlaceholderText("Enter full name")
        self.fullname_edit.setFont(QFont("Arial", 10))
        self.fullname_edit.setMinimumHeight(30)
        self.fullname_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                padding: 5px 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow("Full Name:", self.fullname_edit)
        
        # Role combo box
        self.role_combo = QComboBox()
        self.role_combo.addItems(["user", "manager", "admin"])
        self.role_combo.setFont(QFont("Arial", 10))
        self.role_combo.setMinimumHeight(30)
        self.role_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                padding: 5px 8px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #2c3e50;
                margin-right: 5px;
            }
        """)
        form_layout.addRow("Role:", self.role_combo)
        
        # Work Phone field
        self.work_phone_edit = PhoneNumberInput()
        self.work_phone_edit.setPlaceholderText("Enter work phone number")
        self.work_phone_edit.setFont(QFont("Arial", 10))
        self.work_phone_edit.setMinimumHeight(30)
        self.work_phone_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                padding: 5px 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow("Work Phone:", self.work_phone_edit)
        
        # Password field with show/hide button
        password_layout = QHBoxLayout()
        password_layout.setSpacing(5)
        
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Enter password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFont(QFont("Arial", 10))
        self.password_edit.setMinimumHeight(30)
        self.password_edit.setMaximumWidth(260)  # Shorten width for button space
        self.password_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                padding: 5px 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        password_layout.addWidget(self.password_edit)
        
        # Show/hide password button (controls both password fields)
        self.show_password_button = QPushButton()
        self.show_password_button.setToolTip("Show/Hide Passwords")
        self.show_password_button.setFixedSize(36, 30)  # Make button square and slightly smaller
        self.show_password_button.setCursor(Qt.PointingHandCursor)
        self.show_password_button.setStyleSheet("""
            QPushButton {
                background-color: #ecf0f1;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                font-size: 18px;  /* Larger for better eye icon */
                font-weight: bold;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #d5dbdb;
                border-color: #95a5a6;
            }
            QPushButton:pressed {
                background-color: #bdc3c7;
            }
        """)
        # Set eye icon (using Unicode eye symbol)
        self.show_password_button.setText("👁")
        password_layout.addWidget(self.show_password_button)
        
        form_layout.addRow("Password:", password_layout)
        
        # Confirm Password field (no button, controlled by the one above)
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setPlaceholderText("Confirm password")
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setFont(QFont("Arial", 10))
        self.confirm_password_edit.setMinimumHeight(30)
        self.confirm_password_edit.setMaximumWidth(260)  # Shorten width for alignment
        self.confirm_password_edit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                padding: 5px 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        form_layout.addRow("Confirm Password:", self.confirm_password_edit)
        
        # Active checkbox
        self.active_checkbox = QCheckBox("Active")
        self.active_checkbox.setChecked(True)
        self.active_checkbox.setFont(QFont("Arial", 10))
        self.active_checkbox.setStyleSheet("""
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
                background-color: #27ae60;
                border-color: #27ae60;
            }
        """)
        form_layout.addRow("Status:", self.active_checkbox)
        
        # Form buttons
        form_button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.save_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.save_button.setMinimumHeight(35)
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        form_button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFont(QFont("Arial", 10))
        self.cancel_button.setMinimumHeight(35)
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7b7d;
            }
        """)
        form_button_layout.addWidget(self.cancel_button)
        
        form_button_layout.addStretch()
        form_layout.addRow("", form_button_layout)
        
        layout.addWidget(form_group)
        
        # Initially hide form
        form_group.setVisible(False)
        self.form_group = form_group
    
    def setup_connections(self):
        """Setup signal connections."""
        self.add_user_button.clicked.connect(self.add_user)
        self.edit_user_button.clicked.connect(self.edit_user)
        self.delete_user_button.clicked.connect(self.delete_user)
        self.close_button.clicked.connect(self.accept)
        
        self.save_button.clicked.connect(self.save_user)
        self.cancel_button.clicked.connect(self.cancel_edit)
        
        self.user_table.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Password show/hide connection (controls both password fields)
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
    
    def apply_styling(self):
        """Apply overall dialog styling."""
        self.setStyleSheet("""
            QDialog {
                background-color: #ecf0f1;
            }
        """)
    
    def load_users(self):
        """Load users from database and display in the table."""
        self.users = self.auth_service.user_manager.list_users()
        self.user_table.setRowCount(0)
        for user in self.users:
            row = self.user_table.rowCount()
            self.user_table.insertRow(row)
            self.user_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.user_table.setItem(row, 1, QTableWidgetItem(user.username))
            self.user_table.setItem(row, 2, QTableWidgetItem(user.full_name))
            self.user_table.setItem(row, 3, QTableWidgetItem(user.email))
            self.user_table.setItem(row, 4, QTableWidgetItem(user.role))
            self.user_table.setItem(row, 5, QTableWidgetItem(user.work_phone or ""))
            status = "Active" if user.is_active else "Inactive"
            self.user_table.setItem(row, 6, QTableWidgetItem(status))
        self.user_table.resizeColumnsToContents()
        self.user_table.clearSelection()
        self.form_group.setVisible(False)

    def add_user(self):
        """Show form to add a new user."""
        self.clear_form()
        self.form_group.setVisible(True)
        self.username_edit.setEnabled(True)
        self.password_edit.setEnabled(True)
        self.confirm_password_edit.setEnabled(True)
        self.save_button.setText("Create")
        self.username_edit.setFocus()
        self._editing_user_id = None

    def edit_user(self):
        """Edit selected user."""
        current_row = self.user_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a user to edit.")
            return
        user = self.users[current_row]
        self._editing_user_id = user.id
        self.username_edit.setText(user.username)
        self.username_edit.setEnabled(False)
        self.email_edit.setText(user.email)
        self.fullname_edit.setText(user.full_name)
        self.role_combo.setCurrentText(user.role)
        self.active_checkbox.setChecked(user.is_active)
        self.work_phone_edit.setPhoneNumber(user.work_phone or "")
        self.password_edit.clear()
        self.confirm_password_edit.clear()
        self.password_edit.setEnabled(True)
        self.confirm_password_edit.setEnabled(True)
        self.save_button.setText("Update")
        self.form_group.setVisible(True)

    def delete_user(self):
        """Delete selected user."""
        current_row = self.user_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a user to delete.")
            return
        user = self.users[current_row]
        if user.username == "admin":
            QMessageBox.warning(self, "Error", "Cannot delete the default admin user.")
            return
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to delete user '{user.username}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.auth_service.user_manager.delete_user(user.id):
                QMessageBox.information(self, "Success", f"User '{user.username}' deleted.")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete user.")
            self.load_users()

    def save_user(self):
        """Save user data (create or update)."""
        username = self.username_edit.text().strip()
        email = self.email_edit.text().strip()
        full_name = self.fullname_edit.text().strip()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()
        role = self.role_combo.currentText()
        is_active = self.active_checkbox.isChecked()
        work_phone = self.work_phone_edit.getPhoneNumber().strip()
        
        # Validation
        if not username or not email or not full_name:
            QMessageBox.warning(self, "Validation Error", "Please fill in all required fields.")
            return
        
        if self._editing_user_id is None:
            # Creating new user
            if not password:
                QMessageBox.warning(self, "Validation Error", "Please enter a password.")
                return
            
            if not confirm_password:
                QMessageBox.warning(self, "Validation Error", "Please confirm your password.")
                return
            
            if password != confirm_password:
                QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
                return
            
            success, message = self.auth_service.create_user(
                username, email, full_name, password, role, work_phone
            )
            if success:
                QMessageBox.information(self, "Success", f"User '{username}' created successfully!")
                self.cancel_edit()
                self.load_users()
            else:
                QMessageBox.warning(self, "Error", message)
        else:
            # Editing existing user
            if password:
                if not confirm_password:
                    QMessageBox.warning(self, "Validation Error", "Please confirm your password.")
                    return
                
                if password != confirm_password:
                    QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
                    return
                
                # For admin user management, we'll set a new password directly
                # This bypasses the current password requirement for admin convenience
                user = self.auth_service.user_manager.get_user_by_id(self._editing_user_id)
                if user:
                    # Use a special admin method to set password without current password
                    pw_success, pw_message = self.auth_service.user_manager.set_password_admin(user.id, password)
                    if not pw_success:
                        QMessageBox.warning(self, "Error", pw_message)
                        return
            
            success = self.auth_service.user_manager.update_user(
                self._editing_user_id, email, full_name, role, is_active, work_phone
            )
            if success:
                QMessageBox.information(self, "Success", f"User '{username}' updated successfully!")
                self.cancel_edit()
                self.load_users()
            else:
                QMessageBox.warning(self, "Error", "Failed to update user.")

    def cancel_edit(self):
        """Cancel editing and hide form."""
        self.clear_form()
        self.form_group.setVisible(False)
        self._editing_user_id = None

    def clear_form(self):
        """Clear all form fields."""
        self.username_edit.clear()
        self.email_edit.clear()
        self.fullname_edit.clear()
        self.password_edit.clear()
        self.confirm_password_edit.clear()
        self.role_combo.setCurrentIndex(0)
        self.active_checkbox.setChecked(True)
        self.work_phone_edit.clear()
        self._editing_user_id = None

    def on_selection_changed(self):
        """Handle table selection change."""
        has_selection = self.user_table.currentRow() >= 0
        self.edit_user_button.setEnabled(has_selection)
        self.delete_user_button.setEnabled(has_selection)

    def toggle_password_visibility(self):
        """Toggle both password fields visibility."""
        if self.password_edit.echoMode() == QLineEdit.Password:
            # Show passwords
            self.password_edit.setEchoMode(QLineEdit.Normal)
            self.confirm_password_edit.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText("🙈")
        else:
            # Hide passwords
            self.password_edit.setEchoMode(QLineEdit.Password)
            self.confirm_password_edit.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText("👁")

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events."""
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            # Prevent Enter/Return from doing anything
            event.accept()
            return
        super().keyPressEvent(event) 