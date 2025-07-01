"""
Test for Simple Settings Page
File: test_simple_settings.py

Tests the simplified settings page with Phase 7 features.
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PySide6.QtCore import Qt

# Import the simplified settings page
from src.ui.views.enhanced_settings_page import EnhancedSettingsPage


class TestMainWindow(QMainWindow):
    """Test main window to verify global font scaling."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Font Scaling Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Add test content
        title = QLabel("Font Scaling Test - This text should scale with the slider")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Add some test widgets
        test_label1 = QLabel("This is a test label that should scale")
        test_label1.setStyleSheet("margin: 10px;")
        layout.addWidget(test_label1)
        
        test_label2 = QLabel("Another test label for verification")
        test_label2.setStyleSheet("margin: 10px;")
        layout.addWidget(test_label2)
        
        test_button = QPushButton("Test Button - Should also scale")
        test_button.setStyleSheet("margin: 10px; padding: 10px;")
        layout.addWidget(test_button)
        
        # Add settings page
        self.settings_page = EnhancedSettingsPage()
        layout.addWidget(self.settings_page)
        
        # Add spacer
        layout.addStretch()


def main():
    """Main test function."""
    app = QApplication(sys.argv)
    
    # Create test window
    window = TestMainWindow()
    window.show()
    
    print("Font Scaling Test")
    print("=================")
    print("1. Move the font scale slider in the settings section")
    print("2. Observe that ALL text in the window scales, not just the settings page")
    print("3. The scaling should apply to the title, labels, button, and settings page")
    print("4. Try different scale values (50% to 200%)")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 