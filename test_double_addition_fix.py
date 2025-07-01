#!/usr/bin/env python3
"""
Test script to verify that products are not added twice to quotes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt
from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog
from src.core.services.product_service import ProductService

class TestDoubleAdditionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Double Addition Test")
        self.setGeometry(100, 100, 500, 300)
        
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
        instructions = QLabel(
            "Instructions:\n"
            "1. Click the button above to open the Product Selection Dialog\n"
            "2. Select a product family (e.g., LS2000)\n"
            "3. Configure the product as needed\n"
            "4. Click 'Add to Quote' or press Enter\n"
            "5. Check the console output - you should see only ONE call to _on_add_to_quote\n"
            "6. The product should be added to the quote only once\n"
            "\n"
            "Expected behavior:\n"
            "- Only one '_on_add_to_quote called' message in console\n"
            "- Only one '_on_product_configured called' message in console\n"
            "- Product added to quote only once"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Track additions
        self.additions_count = 0
    
    def open_dialog(self):
        """Open the ProductSelectionDialog for testing"""
        try:
            product_service = ProductService()
            dialog = ModernProductSelectionDialog(product_service, self)
            
            # Connect to the signal
            dialog.product_added.connect(self._on_product_added)
            
            # Show the dialog
            result = dialog.exec()
            
            if result == dialog.DialogCode.Accepted:
                print(f"Dialog accepted - product added {self.additions_count} time(s)")
            else:
                print("Dialog cancelled")
                
        except Exception as e:
            print(f"Error opening dialog: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_product_added(self, config_data):
        """Handle product addition - this should only be called once"""
        self.additions_count += 1
        print(f"Product added to quote (call #{self.additions_count}): {config_data.get('product', 'Unknown')}")

def main():
    app = QApplication(sys.argv)
    
    # Create and show test window
    window = TestDoubleAdditionWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 