#!/usr/bin/env python3
"""
Babbitt Quote Generator - Main Application Entry Point
"""

import logging
import os
import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

# Set global logging level to INFO
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Print debug information
print('Starting Babbitt Quote Generator...')
print(f'Current directory: {os.getcwd()}')
print(f'Python version: {sys.version}')

try:
    # Import main window and theme
    print('Importing MainWindowRedesign...')
    from src.ui.main_window_redesign import MainWindowRedesign
    from src.ui.theme.modern_professional_theme import apply_theme_to_application
    from src.ui.components.configuration_dialog_helper import ConfigurationDialogHelper

    print('MainWindowRedesign imported successfully')
except Exception as e:
    print(f'Error during initialization: {e}')
    traceback.print_exc()
    input('Press Enter to exit...')
    sys.exit(1)


def main():
    """Main application entry point."""
    try:
        print('Creating QApplication...')

        # Create application
        app = QApplication(sys.argv)
        
        # === THEME SELECTION ===
        THEME_NAME = 'modern_professional'  # Change to 'dark_professional' or 'corporate' as desired
        print(f'Applying theme: {THEME_NAME}...')
        apply_theme_to_application(THEME_NAME)
        
        print('Creating MainWindowRedesign...')
        # Create and show main window
        window = MainWindowRedesign()

        print('Showing window...')
        window.show()

        print('Entering event loop...')
        # Run application
        sys.exit(app.exec())
    except Exception as e:
        print(f'Error in main: {e}')
        traceback.print_exc()

        if QApplication.instance():
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Critical)
            error_box.setWindowTitle('Application Error')
            error_box.setText(f'An error occurred: {e!s}')
            error_box.setDetailedText(traceback.format_exc())
            error_box.exec()

        input('Press Enter to exit...')
        sys.exit(1)


if __name__ == "__main__":
    main()
