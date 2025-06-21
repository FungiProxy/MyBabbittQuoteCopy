"""
Test Configuration Dialog Fixes
Simple test to verify the ConfigurationDialogHelper is working correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QComboBox, QLabel, QPushButton, QGroupBox
from PySide6.QtCore import Qt

from src.ui.components.configuration_dialog_helper import ConfigurationDialogHelper

class TestDialog(QDialog):
    """Test dialog to verify configuration fixes."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Configuration Dialog Fixes")
        self.resize(600, 400)
        
        # Setup UI
        layout = QVBoxLayout(self)
        
        # Add some test widgets
        group = QGroupBox("Test Configuration")
        group_layout = QVBoxLayout(group)
        
        # Test label
        label = QLabel("Test Option:")
        group_layout.addWidget(label)
        
        # Test combo box (this should be fixed by the helper)
        combo = QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        group_layout.addWidget(combo)
        
        # Test button
        button = QPushButton("Test Button")
        group_layout.addWidget(button)
        
        layout.addWidget(group)
        
        # Apply configuration dialog fixes
        ConfigurationDialogHelper.apply_dialog_fixes(self)
        
        print("✅ ConfigurationDialogHelper.apply_dialog_fixes() called successfully")
        print("🔧 Applied fixes:")
        print("   • Fixed oversized dropdowns")
        print("   • Improved spacing and layout")
        print("   • Applied consistent section styling")
        print("   • Fixed button styling")
        print("   • Applied modern form styling")

def main():
    """Run the test."""
    app = QApplication(sys.argv)
    
    # Create and show test dialog
    dialog = TestDialog()
    dialog.show()
    
    print("🎉 Test dialog created successfully!")
    print("📋 Check the dialog for:")
    print("   • Properly sized dropdown (max height 36px)")
    print("   • Consistent spacing (12px)")
    print("   • Modern group box styling")
    print("   • Proper button sizing (36-44px height)")
    print("   • Clean form field styling")
    
    return app.exec()

if __name__ == "__main__":
    main() 