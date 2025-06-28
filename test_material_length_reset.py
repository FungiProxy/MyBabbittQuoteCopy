#!/usr/bin/env python3
"""
Test script to verify material length reset functionality
"""

import sys
import logging
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QDialog
from PySide6.QtCore import Qt

# Import our modern dialog
from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog
from src.core.services.product_service import ProductService
from src.core.database import SessionLocal
from src.core.config.material_defaults import get_material_default_length

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestMaterialLengthReset(QMainWindow):
    """Test window for material length reset functionality"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Material Length Reset")
        self.setGeometry(100, 100, 400, 200)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Add test button
        test_button = QPushButton("Test Material Length Reset")
        test_button.clicked.connect(self.test_material_reset)
        layout.addWidget(test_button)
        
        # Add status label
        self.status_label = QLabel("Click the button to test material length reset")
        layout.addWidget(self.status_label)
        
    def test_material_reset(self):
        """Test the material length reset functionality"""
        try:
            print("=== TESTING MATERIAL LENGTH RESET ===")
            
            # Test material default lengths
            test_materials = ["S", "H", "TS", "U", "T", "C", "CPVC"]
            print("\n--- Material Default Lengths ---")
            for material in test_materials:
                default_length = get_material_default_length(material)
                print(f"{material}: {default_length}\"")
            
            # Create database session and product service
            db = SessionLocal()
            product_service = ProductService(db)
            
            # Create and show the dialog
            dialog = ModernProductSelectionDialog(product_service, self)
            
            # Show the dialog
            result = dialog.exec()
            
            if result == QDialog.DialogCode.Accepted:
                self.status_label.setText("Dialog accepted - material length reset tested")
            else:
                self.status_label.setText("Dialog cancelled")
                
        except Exception as e:
            print(f"Error testing material reset: {e}")
            import traceback
            traceback.print_exc()
            self.status_label.setText(f"Error: {e}")

def main():
    """Main function to run the test"""
    app = QApplication(sys.argv)
    
    # Create and show the test window
    window = TestMaterialLengthReset()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 