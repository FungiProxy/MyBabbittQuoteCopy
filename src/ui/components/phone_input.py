"""
Custom phone number input widget with automatic formatting.

This module provides a QLineEdit subclass that automatically formats
phone numbers to (XXX) XXX-XXXX format as the user types.
"""

import re
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent

from src.utils.phone_formatter import format_phone_number, is_valid_phone_number


class PhoneNumberInput(QLineEdit):
    """
    Custom phone number input widget with automatic formatting.
    
    This widget automatically formats phone numbers to (XXX) XXX-XXXX format
    as the user types, and provides validation.
    """
    
    # Signal emitted when the phone number becomes valid/invalid
    phone_validity_changed = Signal(bool)
    
    def __init__(self, parent=None):
        """Initialize the phone number input widget."""
        super().__init__(parent)
        
        # Set placeholder text
        self.setPlaceholderText("(555) 123-4567")
        
        # Connect text changed signal
        self.textChanged.connect(self._on_text_changed)
        
        # Track cursor position for proper formatting
        self._last_cursor_pos = 0
        self._is_formatting = False
        
    def _on_text_changed(self, text: str):
        """Handle text changes and apply formatting."""
        if self._is_formatting:
            return
            
        # Store current cursor position
        cursor_pos = self.cursorPosition()
        
        # Format the phone number
        formatted = self._format_phone_number(text, cursor_pos)
        
        if formatted != text:
            self._is_formatting = True
            self.setText(formatted)
            self._is_formatting = False
            
            # Restore cursor position as close as possible
            new_cursor_pos = self._calculate_new_cursor_position(text, formatted, cursor_pos)
            self.setCursorPosition(new_cursor_pos)
        
        # Emit validity signal
        is_valid = is_valid_phone_number(formatted)
        self.phone_validity_changed.emit(is_valid)
    
    def _format_phone_number(self, text: str, cursor_pos: int) -> str:
        """
        Format phone number to (XXX) XXX-XXXX format.
        
        Args:
            text: Current text in the input
            cursor_pos: Current cursor position
            
        Returns:
            Formatted phone number
        """
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', text)
        
        # If we have more than 10 digits, truncate
        if len(digits_only) > 10:
            digits_only = digits_only[:10]
        
        # Format based on number of digits
        if len(digits_only) == 0:
            return ""
        elif len(digits_only) <= 3:
            return f"({digits_only}"
        elif len(digits_only) <= 6:
            return f"({digits_only[:3]}) {digits_only[3:]}"
        else:
            return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
    
    def _calculate_new_cursor_position(self, old_text: str, new_text: str, old_cursor_pos: int) -> int:
        """
        Calculate the new cursor position after formatting.
        
        Args:
            old_text: Text before formatting
            new_text: Text after formatting
            old_cursor_pos: Cursor position before formatting
            
        Returns:
            New cursor position
        """
        # Count digits before cursor in old text
        digits_before_cursor = 0
        for i in range(min(old_cursor_pos, len(old_text))):
            if old_text[i].isdigit():
                digits_before_cursor += 1
        
        # Find position in new text with same number of digits before it
        digits_counted = 0
        for i, char in enumerate(new_text):
            if char.isdigit():
                digits_counted += 1
                if digits_counted > digits_before_cursor:
                    return i
            elif digits_counted == digits_before_cursor:
                # If we've counted the right number of digits, position after the current char
                return i + 1
        
        # If we get here, position at the end
        return len(new_text)
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press events for special formatting behavior."""
        # Allow navigation keys, backspace, delete
        if event.key() in [Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Home, Qt.Key.Key_End,
                          Qt.Key.Key_Backspace, Qt.Key.Key_Delete]:
            super().keyPressEvent(event)
            return
        
        # Allow digits and some formatting characters
        if (event.key() >= Qt.Key.Key_0 and event.key() <= Qt.Key.Key_9) or \
           event.key() in [Qt.Key.Key_Space, Qt.Key.Key_Minus, Qt.Key.Key_ParenLeft, Qt.Key.Key_ParenRight]:
            super().keyPressEvent(event)
            return
        
        # Ignore other keys
        event.ignore()
    
    def setPhoneNumber(self, phone: str):
        """
        Set the phone number with proper formatting.
        
        Args:
            phone: Phone number to set
        """
        formatted = format_phone_number(phone)
        if formatted:
            self.setText(formatted)
        else:
            self.setText(phone)
    
    def getPhoneNumber(self) -> str:
        """
        Get the current phone number.
        
        Returns:
            Current phone number text
        """
        return self.text()
    
    def isValid(self) -> bool:
        """
        Check if the current phone number is valid.
        
        Returns:
            True if valid, False otherwise
        """
        return is_valid_phone_number(self.text())
    
    def getCleanPhoneNumber(self) -> str:
        """
        Get the phone number with only digits.
        
        Returns:
            Phone number with only digits, or empty string if invalid
        """
        from src.utils.phone_formatter import clean_phone_number
        cleaned = clean_phone_number(self.text())
        return cleaned if cleaned else "" 