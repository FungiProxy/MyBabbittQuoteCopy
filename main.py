#!/usr/bin/env python3
"""
Babbitt Quote Generator - Main Application Entry Point
"""

import sys
import os
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt  # Add Qt import for High DPI attributes

# Print debug information
print("Starting Babbitt Quote Generator...")
print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")

try:
    # Import main window
    print("Importing MainWindow...")
    from src.ui.main_window import MainWindow
    print("MainWindow imported successfully")
except Exception as e:
    print(f"Error during initialization: {e}")
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)

def main():
    """Main application entry point."""
    try:
        print("Creating QApplication...")
        # Enable High DPI scaling
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        
        # Create application
        app = QApplication(sys.argv)
        app.setStyle("Fusion")  # Use Fusion style for a modern look
        
        print("Creating MainWindow...")
        # Create and show main window
        window = MainWindow()
        
        print("Setting up styles...")
        window.setup_styles()  # Apply custom styles
        
        print("Showing window...")
        window.show()
        
        print("Entering event loop...")
        # Run application
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error in main: {e}")
        traceback.print_exc()
        
        if QApplication.instance():
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Critical)
            error_box.setWindowTitle("Application Error")
            error_box.setText(f"An error occurred: {str(e)}")
            error_box.setDetailedText(traceback.format_exc())
            error_box.exec()
        
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
