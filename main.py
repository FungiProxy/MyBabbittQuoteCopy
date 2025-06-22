#!/usr/bin/env python3
"""
MyBabbittQuote Application Entry Point - Working Version
"""

import os
import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

print("🚀 Starting MyBabbittQuote...")
print(f"📁 Working directory: {os.getcwd()}")
print(f"🐍 Python version: {sys.version}")

try:
    from src.ui.main_window import MainWindow
    from src.ui.theme.babbitt_industrial_theme import BabbittIndustrialTheme
    print("✅ Imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)

def main():
    """Launch the application with proper styling."""
    try:
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("MyBabbittQuote")
        app.setOrganizationName("Babbitt International")
        
        # Apply the new industrial theme
        BabbittIndustrialTheme.apply_theme(app)
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        print("✨ Industrial theme applied!")
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()