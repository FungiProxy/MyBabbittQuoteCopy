#!/usr/bin/env python3
"""
Simple test to verify the modern product selection dialog is working correctly
"""

import sys
import logging
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QDialog
from PySide6.QtCore import Qt

# Import our modern dialog
from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog
from src.core.services.product_service import ProductService
from src.core.database import SessionLocal

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestWindow(QMainWindow):
    """Test window for the modern product selection dialog"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Modern Product Selection Dialog")
        self.setGeometry(100, 100, 400, 200)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Add test button
        test_button = QPushButton("Open Modern Product Selection Dialog")
        test_button.clicked.connect(self.open_dialog)
        layout.addWidget(test_button)
        
        # Add status label
        self.status_label = QLabel("Click the button to test the dialog")
        layout.addWidget(self.status_label)
        
    def open_dialog(self):
        """Open the modern product selection dialog"""
        try:
            print("=== OPENING MODERN PRODUCT SELECTION DIALOG ===")
            
            # Create database session and product service
            db = SessionLocal()
            product_service = ProductService(db)
            
            # Create and show the dialog
            dialog = ModernProductSelectionDialog(product_service, self)
            
            # Show the dialog
            result = dialog.exec()
            
            if result == QDialog.DialogCode.Accepted:
                self.status_label.setText("Dialog accepted - product added to quote")
            else:
                self.status_label.setText("Dialog cancelled")
                
        except Exception as e:
            print(f"Error opening dialog: {e}")
            import traceback
            traceback.print_exc()
            self.status_label.setText(f"Error: {e}")

def main():
    """Main function to run the test"""
    app = QApplication(sys.argv)
    
    # Create and show the test window
    window = TestWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 