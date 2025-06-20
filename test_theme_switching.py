#!/usr/bin/env python3
"""
Test script for theme switching functionality.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel

from src.ui.theme.theme_manager import ThemeManager
from src.core.services.settings_service import SettingsService


class ThemeTestWindow(QMainWindow):
    """Simple test window to demonstrate theme switching."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Theme Switching Test')
        self.resize(600, 400)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel('Theme Switching Test')
        title.setObjectName('pageTitle')
        layout.addWidget(title)
        
        # Description
        desc = QLabel('Click the buttons below to switch between themes:')
        layout.addWidget(desc)
        
        # Theme buttons
        for theme_name in ThemeManager.get_available_themes():
            btn = QPushButton(f'Switch to {theme_name}')
            btn.setProperty('class', 'primary')
            btn.clicked.connect(lambda checked, name=theme_name: self.switch_theme(name))
            layout.addWidget(btn)
        
        # Status label
        self.status_label = QLabel('Current theme: Babbitt Theme')
        layout.addWidget(self.status_label)
        
        # Settings service
        self.settings_service = SettingsService()
    
    def switch_theme(self, theme_name):
        """Switch to the specified theme."""
        try:
            ThemeManager.apply_theme(theme_name)
            self.settings_service.set_theme(theme_name)
            self.settings_service.sync()
            self.status_label.setText(f'Current theme: {theme_name}')
            print(f'Successfully switched to {theme_name}')
        except Exception as e:
            print(f'Failed to switch to {theme_name}: {e}')


def main():
    """Main test function."""
    app = QApplication(sys.argv)
    
    # Apply initial theme
    settings = SettingsService()
    initial_theme = settings.get_theme('Babbitt Theme')
    ThemeManager.apply_theme(initial_theme, app)
    
    # Create and show test window
    window = ThemeTestWindow()
    window.show()
    
    print(f'Test window created with initial theme: {initial_theme}')
    print('Available themes:', ThemeManager.get_available_themes())
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main() 