#!/usr/bin/env python3
"""
Test script to verify the add to quote alert functionality.
This script tests the new alert box that asks users if they want to add more items or finish.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer
from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog

def test_add_to_quote_alert():
    """Test the add to quote alert functionality."""
    app = QApplication(sys.argv)
    
    # Initialize services
    db = SessionLocal()
    product_service = ProductService(db=db)
    
    # Create the dialog
    dialog = ModernProductSelectionDialog(product_service=product_service)
    
    # Connect the product_added signal to a test handler
    def on_product_added(config_data):
        print(f"✅ Product added to quote: {config_data.get('product', 'Unknown')}")
        print(f"   Description: {config_data.get('description', 'N/A')}")
        print(f"   Quantity: {config_data.get('quantity', 0)}")
        print(f"   Total Price: ${config_data.get('total_price', 0):.2f}")
    
    dialog.product_added.connect(on_product_added)
    
    # Show the dialog
    print("🚀 Opening product selection dialog...")
    print("📋 Instructions:")
    print("   1. Select a product from the left panel")
    print("   2. Configure the product options")
    print("   3. Click 'Add to Quote' button")
    print("   4. You should see an alert box asking if you want to add more items")
    print("   5. Choose 'Yes' to reset the dialog or 'No' to close it")
    print("   6. The product should be added to the quote regardless of your choice")
    print()
    
    result = dialog.exec()
    
    if result == dialog.DialogCode.Accepted:
        print("✅ Dialog closed normally")
    else:
        print("❌ Dialog was cancelled")
    
    db.close()
    return result

if __name__ == "__main__":
    test_add_to_quote_alert() 