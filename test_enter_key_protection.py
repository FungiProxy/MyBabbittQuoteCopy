#!/usr/bin/env python3
"""
Test script to verify Enter key protection in ProductSelectionDialog
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog
from src.core.services.product_service import ProductService

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Key Protection Test")
        self.setGeometry(100, 100, 400, 200)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create button to open dialog
        open_dialog_btn = QPushButton("Open Product Selection Dialog")
        open_dialog_btn.clicked.connect(self.open_dialog)
        layout.addWidget(open_dialog_btn)
        
        # Add instructions
        from PySide6.QtWidgets import QLabel
        instructions = QLabel(
            "Instructions:\n"
            "1. Click the button above to open the Product Selection Dialog\n"
            "2. Select a product family (e.g., LS2000)\n"
            "3. Try pressing Enter in various input fields:\n"
            "   - Probe Length spinbox\n"
            "   - Quantity spinbox\n"
            "   - Bent Probe degree input (if available)\n"
            "   - Any other input fields\n"
            "4. The dialog should NOT close when pressing Enter in input fields\n"
            "5. Only pressing Enter outside of input fields should trigger 'Add to Quote'"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
    
    def open_dialog(self):
        """Open the ProductSelectionDialog for testing"""
        try:
            product_service = ProductService()
            dialog = ModernProductSelectionDialog(product_service, self)
            
            # Show the dialog
            result = dialog.exec()
            
            if result == dialog.DialogCode.Accepted:
                print("Dialog accepted - product added to quote")
            else:
                print("Dialog cancelled")
                
        except Exception as e:
            print(f"Error opening dialog: {e}")
            import traceback
            traceback.print_exc()

def main():
    app = QApplication(sys.argv)
    
    # Create and show test window
    window = TestWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 