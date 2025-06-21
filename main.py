#!/usr/bin/env python3
"""
MyBabbittQuote Application Entry Point

Launch the beautiful, simplified quote generator with Babbitt International styling.

File: main.py (REPLACE EXISTING)
"""

import os
import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

# Print startup info
print("🚀 Starting MyBabbittQuote...")
print(f"📁 Working directory: {os.getcwd()}")
print(f"🐍 Python version: {sys.version}")

try:
    # Import the updated main window
    from src.ui.views.main_window import MainWindow
    from src.ui.theme.babbitt_theme import BabbittTheme
    print("✅ Imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)


def main():
    """Launch the MyBabbittQuote application with beautiful styling."""
    try:
        print("🎨 Creating application...")
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("MyBabbittQuote")
        app.setApplicationVersion("1.0")
        app.setOrganizationName("Babbitt International")
        
        # Set application-wide style
        app.setStyleSheet(BabbittTheme.get_main_stylesheet())
        
        print("🏠 Creating main window...")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        print("✨ Application ready! Launching...")
        
        # Run the application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Application error: {e}")
        traceback.print_exc()
        
        # Show error dialog if possible
        try:
            if QApplication.instance():
                error_box = QMessageBox()
                error_box.setIcon(QMessageBox.Critical)
                error_box.setWindowTitle("MyBabbittQuote - Error")
                error_box.setText(f"Application failed to start: {str(e)}")
                error_box.setDetailedText(traceback.format_exc())
                error_box.exec()
        except:
            pass
        
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()