#!/usr/bin/env python3
"""
Test script to verify that connection codes work properly in the UI.
This will open the product selection dialog and test connection options.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog

def test_ui_connection_codes():
    """Test connection codes in the UI."""
    app = QApplication(sys.argv)
    
    # Initialize services
    db = SessionLocal()
    product_service = ProductService(db=db)
    
    # Create the dialog
    dialog = ModernProductSelectionDialog(product_service=product_service)
    
    print("=== TESTING CONNECTION CODES IN UI ===")
    print("Instructions:")
    print("1. Select a product family (e.g., LS2000)")
    print("2. In the Connections section, select 'Flange' as Connection Type")
    print("3. Set Flange Size to '2' and Flange Rating to '150#'")
    print("4. Check that the part number updates to include '2\"150#'")
    print("5. Change Connection Type to 'Tri-clamp'")
    print("6. Select a tri-clamp size (e.g., '2\" Tri-clamp Process Connection')")
    print("7. Check that the part number updates to include 'TC2\"'")
    print("8. Close the dialog when done testing")
    
    # Show the dialog
    dialog.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_ui_connection_codes() 