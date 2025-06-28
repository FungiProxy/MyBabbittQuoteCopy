"""
Modern Form Components for MyBabbittQuote

Reusable form widgets with consistent styling and enhanced functionality
that can replace existing Qt widgets throughout the application.
"""

from PySide6.QtWidgets import (QPushButton, QLineEdit, QTextEdit, QComboBox, 
                               QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton,
                               QWidget, QVBoxLayout, QHBoxLayout, QLabel)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QIcon

# Import styling from centralized theme system
from ..theme import (
    COLORS, FONTS, SPACING, RADIUS,
    get_button_style, get_input_style
)


class ModernButton(QPushButton):
    """
    A modern button component with consistent styling and enhanced functionality.
    
    Usage:
        btn = ModernButton("Save", "primary")
        btn = ModernButton("Cancel", "secondary")
        btn = ModernButton("Delete", "danger")
    """
    
    def __init__(self, text="", button_type="primary", size="normal", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.size = size
        self.setup_style()
        self.setup_behavior()
    
    def setup_style(self):
        """Apply modern styling based on button type and size"""
        self.setStyleSheet(get_button_style(self.button_type))
        
        # Set size-specific properties
        if self.size == "small":
            self.setMinimumHeight(32)
            self.setFont(QFont(FONTS['family'], FONTS['sizes']['sm'], FONTS['weights']['medium']))
        elif self.size == "large":
            self.setMinimumHeight(48)
            self.setFont(QFont(FONTS['family'], FONTS['sizes']['lg'], FONTS['weights']['semibold']))
        else:  # normal
            self.setMinimumHeight(40)
            self.setFont(QFont(FONTS['family'], FONTS['sizes']['base'], FONTS['weights']['semibold']))
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def setup_behavior(self):
        """Setup button behavior and interactions"""
        # Add any additional behavior here
        pass
    
    def set_button_type(self, button_type):
        """Update button type and styling"""
        self.button_type = button_type
        self.setup_style()
    
    def set_size(self, size):
        """Update button size and styling"""
        self.size = size
        self.setup_style()
    
    def set_loading(self, loading=True):
        """Set loading state (future enhancement)"""
        if loading:
            self.setEnabled(False)
            self.setText("Loading...")
        else:
            self.setEnabled(True)
            # Restore original text (would need to store it)


class ModernLineEdit(QLineEdit):
    """
    A modern line edit component with enhanced styling and functionality.
    
    Usage:
        input = ModernLineEdit("Enter your name...")
        input = ModernLineEdit("Search...", "search")
    """
    
    def __init__(self, placeholder="", input_type="text", parent=None):
        super().__init__(parent)
        self.input_type = input_type
        self.setup_style()
        self.setup_behavior(placeholder)
    
    def setup_style(self):
        """Apply modern styling"""
        self.setStyleSheet(get_input_style())
        self.setMinimumHeight(44)
        self.setFont(QFont(FONTS['family'], FONTS['sizes']['base']))
    
    def setup_behavior(self, placeholder):
        """Setup input behavior"""
        self.setPlaceholderText(placeholder)
        
        # Add input type specific behavior
        if self.input_type == "search":
            # Add search icon or other search-specific features
            pass
        elif self.input_type == "email":
            # Add email validation
            pass
    
    def set_input_type(self, input_type):
        """Update input type and behavior"""
        self.input_type = input_type
        self.setup_behavior(self.placeholderText())
    
    def set_error(self, has_error=True, error_message=""):
        """Set error state with optional error message"""
        if has_error:
            self.setStyleSheet(f"""
                QLineEdit {{
                    border: 2px solid {COLORS['danger']};
                    border-radius: {RADIUS['md']}px;
                    padding: {SPACING['md']}px {SPACING['lg']}px;
                    background-color: {COLORS['bg_primary']};
                    font-size: {FONTS['sizes']['base']}px;
                    color: {COLORS['text_primary']};
                    font-family: {FONTS['family']};
                }}
                QLineEdit:focus {{
                    border-color: {COLORS['danger']};
                    outline: none;
                }}
            """)
        else:
            self.setStyleSheet(get_input_style())
    
    def clear_error(self):
        """Clear error state"""
        self.set_error(False)


class ModernTextEdit(QTextEdit):
    """
    A modern text edit component with enhanced styling.
    
    Usage:
        text_edit = ModernTextEdit("Enter description...")
    """
    
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setup_style()
        self.setup_behavior(placeholder)
    
    def setup_style(self):
        """Apply modern styling"""
        self.setStyleSheet(f"""
            QTextEdit {{
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['md']}px {SPACING['lg']}px;
                background-color: {COLORS['bg_primary']};
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_primary']};
                font-family: {FONTS['family']};
            }}
            QTextEdit:focus {{
                border-color: {COLORS['primary']};
                outline: none;
            }}
            QTextEdit:hover {{
                border-color: {COLORS['border_medium']};
            }}
        """)
        self.setMinimumHeight(120)
        self.setFont(QFont(FONTS['family'], FONTS['sizes']['base']))
    
    def setup_behavior(self, placeholder):
        """Setup text edit behavior"""
        # Note: QTextEdit doesn't have built-in placeholder, but we can implement it
        self.placeholder_text = placeholder
        if placeholder:
            self.setPlainText("")
            # Could implement custom placeholder behavior
    
    def set_error(self, has_error=True):
        """Set error state"""
        if has_error:
            self.setStyleSheet(f"""
                QTextEdit {{
                    border: 2px solid {COLORS['danger']};
                    border-radius: {RADIUS['md']}px;
                    padding: {SPACING['md']}px {SPACING['lg']}px;
                    background-color: {COLORS['bg_primary']};
                    font-size: {FONTS['sizes']['base']}px;
                    color: {COLORS['text_primary']};
                    font-family: {FONTS['family']};
                }}
                QTextEdit:focus {{
                    border-color: {COLORS['danger']};
                    outline: none;
                }}
            """)
        else:
            self.setup_style()
    
    def clear_error(self):
        """Clear error state"""
        self.set_error(False)


class ModernComboBox(QComboBox):
    """
    A modern combo box component with enhanced styling.
    
    Usage:
        combo = ModernComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
        self.setup_behavior()
    
    def setup_style(self):
        """Apply modern styling"""
        self.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['md']}px {SPACING['lg']}px;
                background-color: {COLORS['bg_primary']};
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_primary']};
                font-family: {FONTS['family']};
                min-height: 44px;
            }}
            QComboBox:focus {{
                border-color: {COLORS['primary']};
                outline: none;
            }}
            QComboBox:hover {{
                border-color: {COLORS['border_medium']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                width: 12px;
                height: 12px;
                background-color: {COLORS['text_muted']};
            }}
            QComboBox QAbstractItemView {{
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
                background-color: {COLORS['bg_primary']};
                selection-background-color: {COLORS['primary']};
                selection-color: white;
            }}
        """)
        self.setMinimumHeight(44)
        self.setFont(QFont(FONTS['family'], FONTS['sizes']['base']))
    
    def setup_behavior(self):
        """Setup combo box behavior"""
        # Add any additional behavior here
        pass
    
    def set_error(self, has_error=True):
        """Set error state"""
        if has_error:
            self.setStyleSheet(f"""
                QComboBox {{
                    border: 2px solid {COLORS['danger']};
                    border-radius: {RADIUS['md']}px;
                    padding: {SPACING['md']}px {SPACING['lg']}px;
                    background-color: {COLORS['bg_primary']};
                    font-size: {FONTS['sizes']['base']}px;
                    color: {COLORS['text_primary']};
                    font-family: {FONTS['family']};
                    min-height: 44px;
                }}
                QComboBox:focus {{
                    border-color: {COLORS['danger']};
                    outline: none;
                }}
                QComboBox::drop-down {{
                    border: none;
                    width: 30px;
                }}
                QComboBox::down-arrow {{
                    width: 12px;
                    height: 12px;
                    background-color: {COLORS['text_muted']};
                }}
            """)
        else:
            self.setup_style()
    
    def clear_error(self):
        """Clear error state"""
        self.set_error(False)


class ModernSpinBox(QSpinBox):
    """
    A modern spin box component with enhanced styling.
    
    Usage:
        spin = ModernSpinBox()
        spin.setRange(1, 100)
        spin.setValue(50)
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
        self.setup_behavior()
    
    def setup_style(self):
        """Apply modern styling"""
        self.setStyleSheet(f"""
            QSpinBox {{
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['md']}px;
                padding: {SPACING['md']}px {SPACING['lg']}px;
                background-color: {COLORS['bg_primary']};
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_primary']};
                font-family: {FONTS['family']};
                min-height: 44px;
            }}
            QSpinBox:focus {{
                border-color: {COLORS['primary']};
                outline: none;
            }}
            QSpinBox:hover {{
                border-color: {COLORS['border_medium']};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                border: none;
                background-color: {COLORS['gray_100']};
                border-radius: {RADIUS['sm']}px;
                margin: 2px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {COLORS['gray_200']};
            }}
            QSpinBox::up-arrow, QSpinBox::down-arrow {{
                width: 8px;
                height: 8px;
                background-color: {COLORS['text_muted']};
            }}
        """)
        self.setMinimumHeight(44)
        self.setFont(QFont(FONTS['family'], FONTS['sizes']['base']))
    
    def setup_behavior(self):
        """Setup spin box behavior"""
        # Add any additional behavior here
        pass


class ModernCheckBox(QCheckBox):
    """
    A modern check box component with enhanced styling.
    
    Usage:
        checkbox = ModernCheckBox("Accept terms and conditions")
    """
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setup_style()
    
    def setup_style(self):
        """Apply modern styling"""
        self.setStyleSheet(f"""
            QCheckBox {{
                spacing: {SPACING['md']}px;
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_primary']};
                font-family: {FONTS['family']};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['sm']}px;
                background-color: {COLORS['bg_primary']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {COLORS['primary']};
                border-color: {COLORS['primary']};
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }}
            QCheckBox::indicator:hover {{
                border-color: {COLORS['primary']};
            }}
        """)
        self.setFont(QFont(FONTS['family'], FONTS['sizes']['base']))
    
    def set_error(self, has_error=True):
        """Set error state"""
        if has_error:
            self.setStyleSheet(f"""
                QCheckBox {{
                    spacing: {SPACING['md']}px;
                    font-size: {FONTS['sizes']['base']}px;
                    color: {COLORS['danger']};
                    font-family: {FONTS['family']};
                }}
                QCheckBox::indicator {{
                    width: 18px;
                    height: 18px;
                    border: 2px solid {COLORS['danger']};
                    border-radius: {RADIUS['sm']}px;
                    background-color: {COLORS['bg_primary']};
                }}
                QCheckBox::indicator:checked {{
                    background-color: {COLORS['danger']};
                    border-color: {COLORS['danger']};
                }}
            """)
        else:
            self.setup_style()
    
    def clear_error(self):
        """Clear error state"""
        self.set_error(False)


class ModernRadioButton(QRadioButton):
    """
    A modern radio button component with enhanced styling.
    
    Usage:
        radio = ModernRadioButton("Option 1")
    """
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setup_style()
    
    def setup_style(self):
        """Apply modern styling"""
        self.setStyleSheet(f"""
            QRadioButton {{
                spacing: {SPACING['md']}px;
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_primary']};
                font-family: {FONTS['family']};
            }}
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {COLORS['border_light']};
                border-radius: 9px;
                background-color: {COLORS['bg_primary']};
            }}
            QRadioButton::indicator:checked {{
                background-color: {COLORS['primary']};
                border-color: {COLORS['primary']};
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNiIgaGVpZ2h0PSI2IiB2aWV3Qm94PSIwIDAgNiA2IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8Y2lyY2xlIGN4PSIzIiBjeT0iMyIgcj0iMiIgZmlsbD0id2hpdGUiLz4KPC9zdmc+Cg==);
            }}
            QRadioButton::indicator:hover {{
                border-color: {COLORS['primary']};
            }}
        """)
        self.setFont(QFont(FONTS['family'], FONTS['sizes']['base'])) 