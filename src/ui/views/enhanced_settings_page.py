"""
Simple Settings Page for MyBabbittQuote
File: src/ui/views/enhanced_settings_page.py

Clean, simple settings page with just the essential Phase 7 features.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
)

# Import Phase 7 features
from src.ui.components import (
    ModernThemeToggle,
    ResponsiveManager,
    theme_manager,
    Breakpoint
)

from src.ui.theme import COLORS, FONTS, SPACING, RADIUS


class EnhancedSettingsPage(QWidget):
    """
    Simple settings page with essential Phase 7 features.
    
    Features:
    - Theme switching (light/dark mode)
    - Responsive design status
    - Clean, minimal interface
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Set up the simple settings UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Page title
        title_label = QLabel("Settings")
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: {FONTS['sizes']['3xl']}px;
                font-weight: {FONTS['weights']['bold']};
                color: {COLORS['text_primary']};
                margin-bottom: {SPACING['lg']}px;
            }}
        """)
        main_layout.addWidget(title_label)
        
        # Theme Settings Group
        theme_group = QGroupBox("Appearance")
        theme_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: {FONTS['weights']['semibold']};
                border: 2px solid {COLORS['border_light']};
                border-radius: {RADIUS['lg']}px;
                margin-top: {SPACING['md']}px;
                padding-top: {SPACING['md']}px;
                background-color: {COLORS['bg_primary']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: {SPACING['md']}px;
                padding: 0 {SPACING['sm']}px 0 {SPACING['sm']}px;
                color: {COLORS['text_primary']};
            }}
        """)
        theme_layout = QVBoxLayout(theme_group)
        theme_layout.setContentsMargins(20, 20, 20, 20)
        theme_layout.setSpacing(20)
        
        # Theme toggle
        theme_label = QLabel("Theme Mode:")
        theme_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: {FONTS['weights']['medium']};")
        theme_layout.addWidget(theme_label)
        
        self.theme_toggle = ModernThemeToggle()
        theme_layout.addWidget(self.theme_toggle)
        
        # Responsive design status
        self.responsive_status_label = QLabel("Responsive Design: Active")
        self.responsive_status_label.setStyleSheet(f"color: #28a745; font-weight: {FONTS['weights']['semibold']};")
        theme_layout.addWidget(self.responsive_status_label)
        
        main_layout.addWidget(theme_group)
        
        # Add spacer to push content to top
        main_layout.addStretch()
        
        # Apply styling to the main widget
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_primary']};
                color: {COLORS['text_primary']};
            }}
        """)
    
    def _connect_signals(self):
        """Connect all signal handlers."""
        # Initialize responsive manager
        self.responsive_manager = ResponsiveManager()
        self.responsive_manager.breakpoint_changed.connect(self._on_breakpoint_changed)
        
        # Connect theme toggle
        self.theme_toggle.theme_toggled.connect(self._on_theme_toggled)
    
    def _on_theme_toggled(self, theme_name):
        """Handle theme toggle from Phase 7."""
        print(f"Theme toggled to: {theme_name}")
    
    def _on_breakpoint_changed(self, breakpoint):
        """Handle responsive breakpoint changes."""
        self.responsive_status_label.setText(f"Responsive Design: {breakpoint.name} ({breakpoint.value}px)") 