#!/usr/bin/env python3
"""
Test script for theme switching functionality.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel

from src.ui.theme.theme_manager import ThemeManager
from src.core.services.settings_service import SettingsService


class ThemeTestWindow(QMainWindow):
    """Simple test window to verify theme switching."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Theme Switching Test")
        self.resize(400, 300)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Title
        title = QLabel("Theme Switching Test")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Theme buttons
        available_themes = ThemeManager.get_available_themes()
        for theme_name in available_themes:
            btn = QPushButton(f"Apply {theme_name}")
            btn.clicked.connect(lambda checked, name=theme_name: self.apply_theme(name))
            layout.addWidget(btn)
        
        # Status label
        self.status_label = QLabel("Select a theme to test")
        self.status_label.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.status_label)
        
        # Apply default theme
        settings = SettingsService()
        default_theme = settings.get_theme('Modern Babbitt')
        ThemeManager.apply_theme(default_theme, QApplication.instance())
        self.status_label.setText(f"Current theme: {default_theme}")
    
    def apply_theme(self, theme_name):
        """Apply the selected theme."""
        try:
            ThemeManager.apply_theme(theme_name, QApplication.instance())
            self.status_label.setText(f"Applied theme: {theme_name}")
            
            # Save the theme setting
            settings = SettingsService()
            settings.set_theme(theme_name)
            settings.sync()
            
        except Exception as e:
            self.status_label.setText(f"Error applying theme: {e}")


def main():
    """Main test function."""
    app = QApplication(sys.argv)
    
    # Create test window
    window = ThemeTestWindow()
    window.show()
    
    print("Theme switching test window opened.")
    print("Available themes:", ThemeManager.get_available_themes())
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 