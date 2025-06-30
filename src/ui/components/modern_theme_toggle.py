"""
Modern Theme Toggle Component

This module provides a modern theme toggle component that allows users
to switch between light and dark themes with smooth animations.
"""

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QIcon, QPixmap

from src.ui.theme import COLORS, FONTS, SPACING, RADIUS
from src.ui.theme.theme_manager import theme_manager


class ModernThemeToggle(QWidget):
    """
    Modern theme toggle component with smooth animations.
    
    Features:
    - Beautiful toggle button design
    - Smooth animations when switching themes
    - Automatic theme state detection
    - Hover and focus effects
    - Accessibility support
    """
    
    theme_toggled = Signal(str)  # Emitted when theme is toggled
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_modern_styling()
        self.connect_signals()
        
        # Update initial state
        self.update_theme_indicator()
    
    def setup_ui(self):
        """Setup the UI components."""
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(SPACING['sm'], SPACING['sm'], SPACING['sm'], SPACING['sm'])
        self.main_layout.setSpacing(SPACING['sm'])
        
        # Theme label
        self.theme_label = QLabel("Theme:")
        self.theme_label.setStyleSheet(f"""
            QLabel {{
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_secondary']};
                font-family: {FONTS['family']};
            }}
        """)
        self.main_layout.addWidget(self.theme_label)
        
        # Toggle button
        self.toggle_button = QPushButton()
        self.toggle_button.setFixedSize(60, 32)
        self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_button.clicked.connect(self.toggle_theme)
        self.main_layout.addWidget(self.toggle_button)
        
        # Current theme label
        self.current_theme_label = QLabel()
        self.current_theme_label.setStyleSheet(f"""
            QLabel {{
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_primary']};
                font-family: {FONTS['family']};
                font-weight: {FONTS['weights']['medium']};
            }}
        """)
        self.main_layout.addWidget(self.current_theme_label)
        
        self.main_layout.addStretch()
    
    def apply_modern_styling(self):
        """Apply modern styling to the toggle button."""
        self.toggle_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['gray_200']};
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['full']}px;
                padding: 2px;
                position: relative;
            }}
            QPushButton:hover {{
                background-color: {COLORS['gray_300']};
                border-color: {COLORS['border_medium']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['gray_400']};
            }}
        """)
        
        # Create toggle indicator
        self.create_toggle_indicator()
    
    def create_toggle_indicator(self):
        """Create the toggle indicator (sun/moon icon)."""
        # Create a simple circular indicator
        self.indicator = QWidget(self.toggle_button)
        self.indicator.setFixedSize(24, 24)
        self.indicator.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['primary']};
                border-radius: {RADIUS['full']}px;
                border: 2px solid white;
            }}
        """)
        
        # Position indicator
        self.update_indicator_position()
    
    def update_indicator_position(self):
        """Update the position of the toggle indicator."""
        if theme_manager.get_current_theme() == "light":
            # Position for light mode (left side)
            self.indicator.move(2, 2)
        else:
            # Position for dark mode (right side)
            self.indicator.move(32, 2)
    
    def connect_signals(self):
        """Connect theme manager signals."""
        theme_manager.theme_changed.connect(self.on_theme_changed)
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        current_theme = theme_manager.get_current_theme()
        new_theme = "dark" if current_theme == "light" else "light"
        
        # Animate the toggle
        self.animate_toggle(new_theme)
        
        # Switch theme
        theme_manager.switch_theme(new_theme, animate=True)
        
        # Emit signal
        self.theme_toggled.emit(new_theme)
    
    def animate_toggle(self, new_theme: str):
        """Animate the toggle indicator."""
        # Create animation for indicator movement
        animation = QPropertyAnimation(self.indicator, b"pos")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        if new_theme == "dark":
            # Move to right (dark mode)
            animation.setStartValue(self.indicator.pos())
            animation.setEndValue(self.toggle_button.mapToParent(self.toggle_button.rect().topRight()) - self.indicator.rect().topRight() + self.indicator.pos())
        else:
            # Move to left (light mode)
            animation.setStartValue(self.indicator.pos())
            animation.setEndValue(self.toggle_button.mapToParent(self.toggle_button.rect().topLeft()) + self.indicator.pos())
        
        # Update indicator position after animation
        animation.finished.connect(self.update_indicator_position)
        animation.start()
    
    def on_theme_changed(self, theme_name: str):
        """Handle theme changes from the theme manager."""
        self.update_theme_indicator()
    
    def update_theme_indicator(self):
        """Update the theme indicator and labels."""
        current_theme = theme_manager.get_current_theme()
        
        # Update current theme label
        theme_names = {"light": "Light", "dark": "Dark"}
        self.current_theme_label.setText(theme_names.get(current_theme, current_theme.title()))
        
        # Update toggle button styling based on theme
        if current_theme == "dark":
            self.toggle_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['gray_700']};
                    border: 2px solid {COLORS['border_light']};
                    border-radius: {RADIUS['full']}px;
                    padding: 2px;
                    position: relative;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['gray_600']};
                    border-color: {COLORS['border_medium']};
                }}
                QPushButton:pressed {{
                    background-color: {COLORS['gray_500']};
                }}
            """)
        else:
            self.toggle_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['gray_200']};
                    border: 2px solid {COLORS['border_light']};
                    border-radius: {RADIUS['full']}px;
                    padding: 2px;
                    position: relative;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['gray_300']};
                    border-color: {COLORS['border_medium']};
                }}
                QPushButton:pressed {{
                    background-color: {COLORS['gray_400']};
                }}
            """)
        
        # Update indicator position
        self.update_indicator_position()


class ModernThemeSelector(QWidget):
    """
    Modern theme selector with dropdown-style theme selection.
    
    Features:
    - Dropdown-style theme selection
    - Theme previews
    - Smooth animations
    - Multiple theme support
    """
    
    theme_selected = Signal(str)  # Emitted when a theme is selected
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_modern_styling()
        self.connect_signals()
        
        # Update initial state
        self.update_theme_display()
    
    def setup_ui(self):
        """Setup the UI components."""
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(SPACING['sm'], SPACING['sm'], SPACING['sm'], SPACING['sm'])
        self.main_layout.setSpacing(SPACING['sm'])
        
        # Theme label
        self.theme_label = QLabel("Theme:")
        self.theme_label.setStyleSheet(f"""
            QLabel {{
                font-size: {FONTS['sizes']['base']}px;
                color: {COLORS['text_secondary']};
                font-family: {FONTS['family']};
            }}
        """)
        self.main_layout.addWidget(self.theme_label)
        
        # Theme buttons
        self.create_theme_buttons()
        
        self.main_layout.addStretch()
    
    def create_theme_buttons(self):
        """Create theme selection buttons."""
        self.theme_buttons = {}
        
        for theme_name, display_name in theme_manager.get_available_themes().items():
            button = QPushButton(display_name)
            button.setFixedSize(80, 32)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda checked, tn=theme_name: self.select_theme(tn))
            
            # Store button reference
            self.theme_buttons[theme_name] = button
            
            # Add to our layout
            self.main_layout.addWidget(button)
    
    def apply_modern_styling(self):
        """Apply modern styling to theme buttons."""
        for theme_name, button in self.theme_buttons.items():
            if theme_name == theme_manager.get_current_theme():
                # Active theme styling
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {COLORS['primary']};
                        color: white;
                        border: none;
                        border-radius: {RADIUS['md']}px;
                        font-size: {FONTS['sizes']['base']}px;
                        font-weight: {FONTS['weights']['semibold']};
                        font-family: {FONTS['family']};
                    }}
                    QPushButton:hover {{
                        background-color: {COLORS['primary_hover']};
                    }}
                    QPushButton:pressed {{
                        background-color: {COLORS['primary_pressed']};
                    }}
                """)
            else:
                # Inactive theme styling
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {COLORS['secondary']};
                        color: {COLORS['text_secondary']};
                        border: 2px solid {COLORS['border_light']};
                        border-radius: {RADIUS['md']}px;
                        font-size: {FONTS['sizes']['base']}px;
                        font-weight: {FONTS['weights']['medium']};
                        font-family: {FONTS['family']};
                    }}
                    QPushButton:hover {{
                        background-color: {COLORS['secondary_hover']};
                        border-color: {COLORS['border_medium']};
                    }}
                    QPushButton:pressed {{
                        background-color: {COLORS['secondary_pressed']};
                    }}
                """)
    
    def connect_signals(self):
        """Connect theme manager signals."""
        theme_manager.theme_changed.connect(self.on_theme_changed)
    
    def select_theme(self, theme_name: str):
        """Select a theme."""
        if theme_name != theme_manager.get_current_theme():
            theme_manager.switch_theme(theme_name, animate=True)
            self.theme_selected.emit(theme_name)
    
    def on_theme_changed(self, theme_name: str):
        """Handle theme changes from the theme manager."""
        self.update_theme_display()
    
    def update_theme_display(self):
        """Update the theme display."""
        self.apply_modern_styling() 