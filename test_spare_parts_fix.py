#!/usr/bin/env python3
"""
Test script to verify the spare parts functionality fixes.
This script tests that spare parts can be selected and added to quotes properly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer
from src.core.database import SessionLocal
from src.core.services.product_service import ProductService
from src.ui.product_selection_dialog_modern import ModernProductSelectionDialog

def test_spare_parts_functionality():
    """Test the spare parts functionality."""
    app = QApplication(sys.argv)
    
    # Initialize services
    db = SessionLocal()
    product_service = ProductService(db=db)
    
    # Create the dialog
    dialog = ModernProductSelectionDialog(product_service=product_service)
    
    # Connect the product_added signal to a test handler
    def on_product_added(config_data):
        print(f"✅ Item added to quote:")
        print(f"   Type: {'Spare Part' if config_data.get('is_spare_part') else 'Product'}")
        print(f"   Name: {config_data.get('description', 'N/A')}")
        print(f"   Part Number: {config_data.get('model_number', 'N/A')}")
        print(f"   Price: ${config_data.get('total_price', 0):.2f}")
    
    dialog.product_added.connect(on_product_added)
    
    # Show the dialog
    print("🚀 Opening product selection dialog...")
    print("📋 Instructions for testing spare parts:")
    print("   1. Look for '🔧 Spare Parts' in the left panel")
    print("   2. Click on '🔧 Spare Parts' to enter spare parts mode")
    print("   3. Select a spare part from the list")
    print("   4. Verify that:")
    print("      - The part number appears in the top right")
    print("      - The price updates in the total display")
    print("      - The 'Add to Quote' button becomes enabled")
    print("   5. Click 'Add to Quote' to add the spare part")
    print("   6. Choose whether to add more items or finish")
    print()
    
    result = dialog.exec()
    
    if result == dialog.DialogCode.Accepted:
        print("✅ Dialog closed normally")
    else:
        print("❌ Dialog was cancelled")
    
    db.close()
    return result

if __name__ == "__main__":
    test_spare_parts_functionality() 